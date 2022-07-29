import logging
import multiprocessing
import random
import time
import discord as discord
from discord.ext import commands, tasks
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from multiprocessing import Process

import bot_secrets

dunks_ayer = []
dunk_nuevas = []


nike_page='https://www.nike.com/es/w?q=dunk&vst=dunk'
options = webdriver.ChromeOptions()
options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
token = bot_secrets.bot_token
bot = discord.Client()



@tasks.loop(seconds=10)
async def lista_dunks():
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.get(nike_page)
        # Aceptar cookies
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="gen-nav-commerce-header-v2"]/div[1]/div/div[2]/div/div[2]/div[2]/button'))).click()

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
        for link in dunks_hoy:          #TODO CREAR UNA POOL DE PROCESOS Y QUE CADA PROCESO COMPRUEBE EL STOCK DE LOS PARES QUE PUEDA
            await comprueba_stock(driver,channel,link)
    except Exception as e:
        logging.warning(f"Excepción con código: {e}")


async def comprueba_stock(driver, channel, link):
    #driver.get(link)
    driver.get("https://www.nike.com/es/launch/t/dunk-low-golden-moss")
    tallas = driver.find_elements(By.NAME, "skuAndSize")
    disponibles = []
    if tallas:      # Dos tipos de listings, con nombre skuAndSize y con propiedad size-available
        for talla in tallas:
            if not talla.get_attribute("disabled"):
                atributo = talla.get_attribute("id")
                disponibles.append(driver.find_element(By.XPATH,f"//*[@for='{atributo}']").text)

    else:
        tallas = driver.find_elements(By.XPATH, "//*[@data-qa='size-available']")
        for talla in tallas:
            disponibles.append(talla.text)

    if disponibles:
        await channel.send(link + "\n" + "\n".join(disponibles))
    else:
        await channel.send(link + "\nSin stock")



async def work(item, count):
    name = multiprocessing.current_process().name
    logging.info(f'{name} started: {item}')
    for x in range(count):
        logging.info(f'{name}: {item} = {x}')
        time.sleep(1)
    logging.info(f'{name} finished')
    return item + ' is finished'

async def proc_result(result):
    logging.info(f'result = {result}')


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