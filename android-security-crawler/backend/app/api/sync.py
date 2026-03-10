import pathlib

from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.utils.local_llm import save_report
from app.database.session import get_db

REPORT_DIR = pathlib.Path("generated_reports")
REPORT_DIR.mkdir(exist_ok=True)

router = APIRouter(prefix="/llm", tags=["llm"])

@router.get("/generate/{cve_id}")
async def query(cve_id, db: AsyncSession = Depends(get_db)):
    return await save_report(cve_id, db)


# @router.get("/generate/all"):
# async def gen_all(db: AsyncSession = Depends(get_db)):
#     pass