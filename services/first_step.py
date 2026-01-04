from asyncio import create_task, gather, wait_for, Semaphore
from aiohttp import ClientSession
from loguru import logger
from .api_handler import api_handler

async def first_step(url: str, times: int = 5) -> bool:
    try:
        async with ClientSession() as client_session:
            semaphore = Semaphore(value=times)
            tasks = [
                create_task(
                    api_handler(url, client_session=client_session, semaphore=semaphore)
                ) for _ in range(times)
            ]
            results = await wait_for(
                fut=gather(*tasks),
                timeout=60
            )

        if any(results):
            return True 
        
    except Exception as e:
        logger.error(f'First step fatal Error: {str(e)}')
    
    return False
