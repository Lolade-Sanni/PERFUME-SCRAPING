import requests

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


# SETTING UP OPTIONS
options = Options()
options.add_argument("--disable-extensions")
options.add_argument("--headless=new")
options.add_experimental_option("detach", True)
n = 1

# SETTING UP CHROMEDRIVER
try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(10)
except requests.exceptions.ConnectionError:
    print("YOU SEEM TO BE OFFLINE")
    quit()

for n in range(22):
    login_url = f"https://dazzlescloset.bumpa.shop/?page={n+1}"
    driver.get(login_url)
    try:
        close_btn = driver.find_element(By.CLASS_NAME,"close-modal")
        close_btn.click()
    except NoSuchElementException:
        ...

    product_cards = driver.find_elements(By.CLASS_NAME, "product-data")
    product_cards = [(product_card.find_element(By.CLASS_NAME,"product-name" ).text, product_card.find_element(By.CLASS_NAME,"product-price" )
                      .text) for product_card in product_cards]
    for product_card in product_cards:
        name = product_card[0]
        price = product_card[1].replace(",", "").replace("₦","")
        with open("perfume.csv", "+a", encoding="UTF-16") as file:
            file.write(f"{name},{price}\n",)
    print(f"PAGES SCRAPPED {n+1}/22")

print("SUCCESSFULLY RAN TO COMPLETION")