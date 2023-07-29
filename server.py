
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from flask import Flask, render_template,request
from google.oauth2.service_account import Credentials
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from urllib.parse import urlparse
import pandas as pd
import time
import os
app = Flask(__name__)


def extract_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    domain = domain.replace('www.', '')  # Remove 'www.' if present
    return domain


def createsheet(all_urls, domain):
    answer = True
    try:

        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/jeremygrant79/jeremy/credentials.json', scope)
        client = gspread.authorize(credentials)
        folder_id = '1eGG7jF2GBa63E4jNuM1RSwVtpNikJRzl'
        spreadsheet = client.create(domain,folder_id=folder_id)
        spreadsheet_id = spreadsheet.id
        worksheet = client.open_by_key(spreadsheet_id).sheet1
        for i, item in enumerate(all_urls):
            worksheet.update_cell(i+2, 1, item)
        # worksheet.insert_rows(data, row=1)
        print('Spreadsheet URL:', spreadsheet.url)
        print('google sheet add sucessfully')
        return True
    except Exception as e:
        return e

try:
    @app.route('/', methods=['GET', 'POST'])
    def getinks():
        options = Options()
        options.add_argument("--headless")
        options.add_argument("content-Type=application/x-www-form-urlencoded; charset=UTF-8")
        options.add_argument("user_agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
        options.add_argument("accept-language=en-US,en;q=0.9")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        answer = True


        driver = webdriver.Chrome(options=options)
        if request.method == 'POST' and request.form and request.form.get("search"):
            url = request.form.get("search")
            driver.get(url)
            link_elements = driver.find_elements(By.TAG_NAME, "a")
            links = [link.get_attribute("href") for link in link_elements]
            try:
                answer = createsheet(links, extract_domain(url))
            except Exception as e:
                answer = e
        return render_template('index.html',answer=answer)

except:
    pass

time.sleep(5)