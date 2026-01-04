from click import group, option
from dotenv import load_dotenv
from os import getenv
from typing import Optional
from asyncio import run
from services import run_test

load_dotenv()

@group()
def cli():
    pass

@cli.command(name='run_test')
@option('--url', default=getenv('URL'))
@option('--response_url', default=getenv('RESPONSE_URL'))
@option('--login', default=getenv('LOGIN'))
@option('--password', default=getenv('PASSWORD'))
@option('--times', default=getenv('TIMES', '5'))
def run_test_command(
    url: str, response_url: str, login: str, password: str, times: str = '5'
) -> Optional[str]:
    options = (url, response_url, login, password, int(times), )
    if not all(options):
        return 'Required fields: url, response_url, login, password!'
    
    run(run_test(*options))
    return None

if __name__ == '__main__':
    # python command.py run_test
    cli()