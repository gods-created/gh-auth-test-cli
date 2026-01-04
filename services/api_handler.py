from aiohttp.web_exceptions import HTTPException
from aiohttp.client_exceptions import ClientError
from aiohttp.http_exceptions import HttpProcessingError
from pydantic import BaseModel, ValidationError, field_validator
from loguru import logger
from bs4 import BeautifulSoup as bs

class Validator(BaseModel):
    url: str

    @field_validator('url')
    @classmethod
    def url_validate(cls, url: str):
        if not url.startswith('https://'):
            raise ValueError('URL is not valid')
        
        if not 'github.com/login?return_to' in url:
            raise ValueError('Incorrect GITHUB LOGIN url')
        return url

async def api_handler(url: str, **options) -> bool:
    try:
        try:
         Validator(url=url)
        
        except ValidationError as e:
            raise Exception(str(e))
        
        try:
            client_session = options.get('client_session')
            semaphore = options.get('semaphore')

            if not client_session or not semaphore:
                raise Exception('Not all needs parameters for func executing')

            async with semaphore:
                async with client_session.get(url=url) as request:
                    request.raise_for_status()
                    html_doc = await request.text()

                soup = bs(html_doc, 'html.parser')
                auth_form = soup.find_all('div', attrs={'class': 'authentication'})
                if not auth_form:
                    raise Exception('Authentication form didn\'t find')
                
                return True

        except HTTPException as e:
            raise Exception(f'HTTP Error: {str(e)}')
        
        except ClientError as e:
            raise Exception(f'Client Error: {str(e)}')
        
        except HttpProcessingError as e:
            raise Exception(f'HTTP Processing Error: {str(e)}')
    
    except Exception as e:
        logger.error(str(e))

    return False
