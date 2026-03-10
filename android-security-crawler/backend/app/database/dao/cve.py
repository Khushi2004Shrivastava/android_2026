from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CVE


async def get_cve(cve_id, db: AsyncSession):
    stm = select(CVE).where(CVE.id == cve_id)
    result = await db.execute(stm)

    result = result.scalars().all()

    return result