import asyncio

async def run_agents(diff, context, security_agent, performance_agent, quality_agent):
    results = await asyncio.gather(
        security_agent(diff, context),
        performance_agent(diff, context),
        quality_agent(diff, context),
    )
    return results