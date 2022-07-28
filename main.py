import logging
import time

import discord as discord
from discord.ext import commands, tasks
import schedule
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os

dunks_ayer = []
dunk_nuevas = []


nike_page='https://www.nike.com/es/w?q=dunk&vst=dunk'
options = webdriver.ChromeOptions()
options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
token = os.getenv('TOKEN')
bot = discord.Client()



@tasks.loop(seconds=10)
async def lista_dunks():
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(nike_page)
    try:    # Aceptar cookies
        driver.implicitly_wait(10)
        driver.find_element(By.XPATH, '//*[@id="gen-nav-commerce-header-v2"]/div[1]/div/div[2]/div/div[2]/div[2]/button').click()

    except NoSuchElementException:
        print("No hubo cookies que aceptar")

    finally:
        scroll_bottom(driver)
        dunks = driver.find_elements(By.CLASS_NAME, 'product-card__img-link-overlay')
        dunks_hoy = [dunk.get_attribute('href') for dunk in dunks if 'high' not in dunk.get_attribute('href')]
        dunks_nuevas = list(filter(lambda dunk: dunk not in dunks_ayer, dunks_hoy))
        global dunks_ayer
        dunks_ayer = dunks_hoy
        print(dunks_nuevas)
        channel = bot.get_channel(1002216168163115172)
        for link in dunks_nuevas:
            await channel.send(link)
            time.sleep(1)


@bot.event
async def on_ready():
    lista_dunks.start()


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


bot.run(token)
lista_dunks.start()
