from .llm import call_llm

async def performance_agent(diff, context):
    prompt = f"""
You are a backend code reviewer.

Analyze the following pull request changes for PERFORMANCE issues.

Focus on:
- Inefficient loops
- Redundant computations
- Unnecessary database calls
- Poor algorithm complexity

DIFF:
{diff}

CONTEXT:
{context}

Respond in concise bullet points.
"""
    return await call_llm(prompt)