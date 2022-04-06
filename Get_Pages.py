import urllib.request , urllib.error, urllib.parse
from telnetlib import EC

from selenium import webdriver
import io
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import pathlib
import time


options = webdriver.ChromeOptions()
options.add_argument("--enable-javascript")
# options.add_argument("--headless")
# options.add_argument("--disable-gpu")


url = 'https://www.tripadvisor.co.uk/Restaurants-g187191-Rouen_Seine_Maritime_Haute_Normandie_Normandy.html'
driver = webdriver.Chrome("driver/chromedriver.exe", options=options)
driver.get(url)
output = 'Pages'


restraunt_num = 0
page = 1
resume = True
while resume:
    try:
        WebDriverWait(driver, 20).until(
            ec.visibility_of_element_located((By.XPATH, './/a[contains(@class, "_15_ydu6b")]')))
    except TimeoutException:
        print('Cannot locate producers table')
        continue

    time.sleep(20)
    restraunts = driver.find_elements_by_class_name('_15_ydu6b')
    for restraunt in restraunts:

        restraunt_num += 1
        if pathlib.Path('{}/{}.html'.format(output, str(restraunt_num))).exists():
            print('File {} already exists, continue'.format(restraunt_num))
            continue

        ActionChains(driver).key_down(Keys.CONTROL).click(restraunt).key_up(Keys.CONTROL).perform()
        try:
            driver.switch_to.window(driver.window_handles[1])
        except IndexError:
            print('Index error on vine {}'.format(restraunt_num))
            continue

        # driver.switch_to.window(driver.window_handles[1])

        try:
            WebDriverWait(driver, 20).until(
                ec.visibility_of_element_located((By.XPATH, './/div[contains(@class, "_3acGlZjD")]')))
        except TimeoutException:
            print('Cannot locate vine card')
            continue
        time.sleep(0.1)

        with io.open(output + '/' + str(restraunt_num) + ".html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
            f.close()
        print('Saved vine {}'.format(str(restraunt_num)))
        time.sleep(0.5)

        # restraunt_num += 1
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    try:
        time.sleep(5)
        current_button = driver.find_elements_by_xpath(
            './/a[contains(@class, "nav next rndBtn ui_button primary taLnk")]'.format(page)).pop()
        # driver.execute_script("arguments[0].scrollIntoView();", current_button)
        # driver.implicitly_wait(2)
        ActionChains(driver).click(current_button).perform()
        print('Next page button clicked')
    except IndexError:
        resume = False

print('Done')
driver.quit()
