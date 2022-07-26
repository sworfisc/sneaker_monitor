import logging

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def lista_dunks(url, driver):
    try: # Aceptar cookies
        driver.implicitly_wait(10)
        driver.find_element(By.XPATH, '//*[@id="gen-nav-commerce-header-v2"]/div[1]/div/div[2]/div/div[2]/div[2]/button').click()

    except NoSuchElementException:
        logging.info("No hubo cookies que aceptar")

    finally:
        all_dunks = driver.find_elements(By.CLASS_NAME, 'product-card__img-link-overlay')
        for dunk in all_dunks:
            print(dunk.get_attribute('href'))


if __name__ == "__main__":
    url = 'https://www.nike.com/es/w?q=dunk&vst=dunk'
    options = webdriver.ChromeOptions()
    options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
    # s=Service(r"C:\Users\javie\chromedriver_win32\chromedriver.exe")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)

    lista_dunks(url, driver)

    driver.quit()