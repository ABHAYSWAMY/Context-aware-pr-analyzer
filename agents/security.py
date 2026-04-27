from .llm import call_llm

async def security_agent(diff, context):
    prompt = f"""
You are a backend code reviewer.

Analyze the following pull request changes for SECURITY issues.

Focus on:
- Hardcoded secrets
- Unsafe input handling
- Injection risks
- Authentication/authorization issues

DIFF:
{diff}

CONTEXT:
{context}

Respond in concise bullet points.
"""
    return await call_llm(prompt)