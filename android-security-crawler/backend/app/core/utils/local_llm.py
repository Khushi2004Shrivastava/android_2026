import os
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.inspection import inspect
from ollama import AsyncClient # Switched to Async

from app.database.dao.cve import get_cve

def orm_to_string(obj) -> str:
    mapper = inspect(obj)
    return ", ".join(
        f"{attr.key}={getattr(obj, attr.key)!r}"
        for attr in mapper.mapper.column_attrs
    )

# Point to local Ollama
# client = AsyncClient(host="http://localhost:11434")
client = AsyncClient(
    host="https://ollama.com",
    headers={'Authorization': 'Bearer 61b52d38f1e947838fd58c0dd356e661.mFnxBI0lGjJxXeqQY_Kt_L8-'},
)


async def save_report(cve_id, db: AsyncSession):
    msg = (
        "Create a .md report for the given data. \n"
        "Use the internet to find more about this cve.\n"
        "Also add the CVE timeline from discovery to patch. \n"
        "Find the list of affected products. \n"
        "Find any related exploits or malware using this CVE. \n"
        "Find the files or components affected. \n"
        "Search and find the patch commit and link to it. \n"
        "Keep all reference in the last section. \n"
        "Just give the .md report, no prompts. \n"
        "Do not add any internal reference from your side. \n"
        "Do not add :contentReference. \n"
        f"CVE ID {cve_id}. \n"
        "Do not add ```markdown ```"
    )

    cve = await get_cve(cve_id, db)
    if not cve:
        return

    # Ensure local directory exists
    os.makedirs("generated_reports", exist_ok=True)
    file_path = f"generated_reports/{cve_id}.md"

    messages = [{"role": "user", "content": f"{orm_to_string(cve[0])}\n{msg}"}]
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            # Using async for-loop for local streaming
            async for part in await client.chat(
                model='cogito-2.1:671b', 
                messages=messages, 
                stream=True
            ):
                chunk = part["message"]['content']
                if chunk:
                    f.write(chunk)
                    f.flush()
    except Exception as e:
        print(f"Error during report generation: {e}")
        return

    return file_path
