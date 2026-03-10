from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import await_fallback

from app.database.dao.cve import get_cve
from app.database.session import get_db

router = APIRouter()

@router.get("/generate/{cve_id}")
async def generate(cve_id, db: AsyncSession = Depends(get_db)):
    cve = await get_cve(cve_id, db)

    msg = (
        "Create a .md report for the given data \n"
        "Use the internet to find more about this cve.\n"
        "Also add the CVE timeline from discovery to patch. \n"
        "Find the list of affected products. \n"
        "Find any related exploits or malware using this CVE. \n" \
        "Find the files or components affected. \n"
        "Keep all reference in the last section. \n"
        "Just give the .md report, no prompts. \n"
        "Do not add any internal reference from your side."
        "Do not add :contentReference"
    )

    return {"CVE": cve[0], "Instructions": msg}
