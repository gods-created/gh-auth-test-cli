from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By 
from selenium.common.exceptions import WebDriverException
from loguru import logger

def second_step(url: str, login: str, password: str, response_url: str) -> bool:
    try:
        driver = webdriver.Chrome()
        wait = WebDriverWait(driver, timeout=5)
        driver.get(url)

        login_field = driver.find_element(By.ID, 'login_field')
        password_field = driver.find_element(By.ID, 'password')
        login_field.send_keys(login)
        password_field.send_keys(password)

        submit_button = driver.find_element(By.CLASS_NAME, 'js-sign-in-button')
        driver.execute_script('arguments[0].click()', submit_button)

        wait.until(
            EC.url_to_be(response_url)
        )

        driver.quit()
        
        return True

    except WebDriverException as e:
        logger.error(f'WebDriver Error: {str(e)}')

    except Exception as e:
        logger.error(f'Second step fatal Error: {str(e)}')

    return False
