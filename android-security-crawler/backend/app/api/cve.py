from io import BytesIO

import markdown
from app.models.config_node import ConfigNode
from app.models.cpe_match import CPEMatch
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, Float, cast, exists, or_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from starlette.responses import StreamingResponse, HTMLResponse
# from weasyprint import HTML

from app.core.utils.local_llm import save_report
from app.models import CVE, CVSSMetric
from app.database.session import get_db
from app.models.android import Android

from pathlib import Path
from typing import List

REPORT_DIR = Path("generated_reports")
REPORT_DIR.mkdir(exist_ok=True)

router = APIRouter(prefix="/cve", tags=["llm"])

@router.get("/{cve_id}")
async def fetch_cve_by_id(cve_id, db: AsyncSession = Depends(get_db)):
    stm = select(CVE).where(CVE.id == cve_id)
    result = await db.execute(stm)
    cve = result.scalar_one_or_none()
    if not cve:
        raise HTTPException(status_code=404)

    return {"data":cve}

@router.get("/")
async def get_cve(keyword: str = "", 
                  startDate: date = "2019-01-01",
                  endDate: date = date.today(), 
                  minScore: float = 0.0, 
                  maxScore: float = 10,
                  vendors: List[str] = Query(default=[], alias="vendors[]"),
                  severity: List[str] = Query(default=[], alias="severity[]"),
                  db: AsyncSession = Depends(get_db)):
    base_score = cast(
        CVSSMetric.cvss_json["cvssData"]["baseScore"].astext,
        Float
    )
    stm = select(CVE.id.label('id'), CVE.cve_raw['descriptions'][0]['value'], 
                 CVE.published, CVE.last_modified, CVSSMetric.cvss_json['cvssData']['baseScore'], 
                 CVSSMetric.cvss_json['cvssData']['baseSeverity'].label('base_severity')
                ).join(
                     Android, CVE.id == Android.id
                ).join(
                    CVSSMetric, CVE.id == CVSSMetric.cve_id
                ).join(
                    ConfigNode, CVE.id == ConfigNode.cve_id 
                ).join(
                    CPEMatch, ConfigNode.id == CPEMatch.node_id
                ).filter(
                    CVE.id.ilike(f"%{keyword}%"),
                    CVE.published <= endDate, CVE.published >= startDate,  
                    base_score >= minScore, 
                    base_score <= maxScore,
                    # or_(
                    #     *(severity.ilike(f"%{sev}%") for sev in severity)
                    # )
                    or_(
                        *(
                            CVSSMetric.cvss_json['cvssData']
                                .op('->>')('baseSeverity')
                                .ilike(f"%{sev}%")   # ← note: usually %...% for substring match
                            for sev in severity
                        )
                    )
                    # CPEMatch.criteria.ilike(f"%{keyword}%")
                ).distinct(CVE.id).where(
                or_(
                    *(CPEMatch.criteria.ilike(f"%{kw}%") for kw in vendors)
                )
                )
    
    result = await db.execute(stm)

    result = result.fetchall()

    final_response = []

    for item in result:
        data = {
            'id': item[0],
            'description': item[1],
            'published': item[2].date() if item[2] else None,
            'lastModified': item[3].date() if item[3] else None,
            'score': item[4],
            'severity': item[5]
        }
        final_response.append(data)

    return final_response

@router.get("/report/{cve_id}.md")
async def get_cve(cve_id, db: AsyncSession = Depends(get_db)):
    path = REPORT_DIR / f"{cve_id}.md"
    if not path.exists():
        path = await save_report(cve_id, db)

    with open(path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    html_content = markdown.markdown(md_content, extensions=['extra', 'fenced_code', 'tables'])
    # pdf_bytes = HTML(string=html_content).write_pdf()

    html_body = f"""
        <!DOCTYPE html>
        <html>
          <head>
            <title>{cve_id}</title>
          </head>
          <body>
            {html_content}
          </body>
        </html>
        """

    return HTMLResponse(html_body)