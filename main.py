import logging
import time
import schedule
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

dunks_ayer = []

url='https://www.nike.com/es/w?q=dunk&vst=dunk'


def lista_dunks(url):
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)
    try:    # Aceptar cookies
        driver.implicitly_wait(10)
        driver.find_element(By.XPATH, '//*[@id="gen-nav-commerce-header-v2"]/div[1]/div/div[2]/div/div[2]/div[2]/button').click()

    except NoSuchElementException:
        print("No hubo cookies que aceptar")

    finally:
        scroll_bottom(driver)
        dunks = driver.find_elements(By.CLASS_NAME, 'product-card__img-link-overlay')
        dunks_hoy = [dunk.get_attribute('href') for dunk in dunks]
        dunks_nuevas = list(filter(lambda dunk: dunk not in dunks_ayer and, dunks_hoy))
        global dunks_ayer
        dunks_ayer = dunks_hoy
        print(dunks_nuevas)


schedule.every(1).minutes.do(lista_dunks, url)


def scroll_bottom(driver):
    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


while True:
    options = webdriver.ChromeOptions()
    options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
    # s=Service(r"C:\Users\javie\chromedriver_win32\chromedriver.exe")

    schedule.run_pending()
    time.sleep(1)