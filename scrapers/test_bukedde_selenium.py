from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://www.bukedde.co.ug/amawulire/BUK_159637_022026/poliisi-eyongedde-amaanyi-mu-bikwekweto-byayo"
driver.get(url)

time.sleep(5)  # wait for JS to load

paragraphs = driver.find_elements(By.TAG_NAME, "p")

for p in paragraphs[:10]:
    print(p.text)

driver.quit()
