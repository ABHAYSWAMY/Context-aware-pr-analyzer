from fastapi import FastAPI

from utils.github import fetch_pr_files, fetch_file_content
from utils.chunking import chunk_text
from utils.embeddings import embed_texts
from utils.retrieval import build_index, retrieve

from agents.security import security_agent
from agents.performance import performance_agent
from agents.quality import quality_agent
from agents.runner import run_agents

app = FastAPI()


@app.get("/review")
async def review(pr_url: str):

    files = fetch_pr_files(pr_url)

    all_chunks = []

    for f in files:
        content = fetch_file_content(f)

        if not content:
            continue

        chunks = [c for c in chunk_text(content) if c.strip()]
        all_chunks.extend(chunks)

    embeddings = embed_texts(all_chunks)
    build_index(all_chunks, embeddings)

    output = "## 🔍 PR Review\n\n"

    for f in files[:2]:  # limit for demo
        if "patch" not in f:
            continue

        diff = f["patch"][:1200]

        query_embedding = embed_texts([diff])[0]
        context_chunks = retrieve(query_embedding)
        context = "\n\n".join(context_chunks[:2])[:1200]

        sec, perf, qual = await run_agents(
            diff,
            context,
            security_agent,
            performance_agent,
            quality_agent
        )

        output += f"""
### 📁 {f['filename']}

🔐 Security:
{sec}

⚡ Performance:
{perf}

🧹 Quality:
{qual}

---
"""

    return {"review": output}