from .first_step import first_step
from .second_step import second_step
from loguru import logger

async def run_test(
    url: str,
    response_url: str,
    login: str,
    password: str,
    times: int
) -> bool:
    first_step_response = await first_step(url, times)
    if not first_step_response:
        return False
    
    second_step_response = second_step(url, login, password, response_url)
    if not second_step_response:
        return False
    
    logger.success('GITHUB Auth action fulfilled success')
    
    return True