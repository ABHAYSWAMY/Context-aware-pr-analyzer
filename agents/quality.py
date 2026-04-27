from .llm import call_llm

async def quality_agent(diff, context):
    prompt = f"""
You are a backend code reviewer.

Analyze the following pull request changes for CODE QUALITY issues.

Focus on:
- Readability
- Naming conventions
- Code structure
- Maintainability

DIFF:
{diff}

CONTEXT:
{context}

Respond in concise bullet points.
"""
    return await call_llm(prompt)