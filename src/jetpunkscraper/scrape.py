import numpy as np
import pandas as pd
import json
from datetime import date

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from bs4 import BeautifulSoup
import getpass

import typer
from typing_extensions import Annotated

def retrieve_scores(
        username: Annotated[str, typer.Argument(help="Your JetPunk username or email address")],
        out_file: Annotated[str, typer.Option(help="Output CSV file path")] = "scores.csv",
        browser: Annotated[str, typer.Option(help="Browser to use: either Firefox or Chrome")] = "Firefox",
    ):
    """Log in to Jetpunk and scrape user scores from the daily-stats page."""
    
    # # Launch browser (headless optional)
    if browser.lower() == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
    elif browser.lower() == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
    else:
        raise ValueError("Browser must be either 'Firefox' or 'Chrome'.")

    password = getpass.getpass(prompt="Enter your JetPunk password: ")

    max_attempts = 5
    att_no = 0
    while att_no < max_attempts:
        try:
            # Go to main page
            driver.get("https://www.jetpunk.com/")
            login_button = driver.find_element(By.CSS_SELECTOR, ".login-link")
            login_button.click()
            
            driver.find_element(By.CSS_SELECTOR, ".txt-email").send_keys(username)
            driver.find_element(By.CSS_SELECTOR, ".txt-password").send_keys(password)
            driver.find_element(By.CSS_SELECTOR, ".txt-password").send_keys(Keys.RETURN)

            driver.get("https://www.jetpunk.com/daily-trivia/your-stats")
            html = driver.page_source
            driver.quit()
            soup = BeautifulSoup(html, 'html.parser')

            scripts = soup.find_all('script')
            unformat_data = list([scr for scr in scripts if 'chartData' in scr.text][0].children)[0]
            break

        except (UnboundLocalError, IndexError, NoSuchElementException, ElementNotInteractableException) as e:
            att_no += 1
            print(f"Attempt {att_no} failed: {e}")

    format_data = unformat_data.split('=')[1].strip().rstrip(';').replace("true", '"True"') \
    .replace("false", '"False"') \
    .replace("null", '"None"')

    data = json.loads(format_data)['data']['chartData']

    dates = [date.fromisoformat(datum[0]) for datum in data]
    scores = np.array([np.nan if datum[1] == 'None' else int(datum[1]) for datum in data])

    df = pd.DataFrame({'date': dates, 'score': scores})
    df.to_csv(out_file, index=False)

    driver.quit()
