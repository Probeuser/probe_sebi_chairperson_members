from functions import get_data_count, check_new_data, send_mail
from functions.data_scraping_log_function import updateDataScrapeLog
from log import log
import traceback
import sys
import pandas as pd
from bs4 import BeautifulSoup
from config import sebi_config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.sebi_config import no_data_avaliable,no_data_scraped,source_name,source_status,table_name



url = "https://www.sebi.gov.in/sebiweb/home/HomeAction.do?doListing=yes&sid=2&ssid=9&smid=2"


def extract_data_website(cursor):
    try:

        sebi_config.browser.get(url)
        sebi_config.browser.maximize_window()
        enforcement  = WebDriverWait(sebi_config.browser, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="menu3"]'))
            )
        enforcement.click()
        orders = WebDriverWait(sebi_config.browser, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="member-wrapper"]/section/div/ul/li[1]/a'))
            )
        orders.click()

        type_sebi= WebDriverWait(sebi_config.browser, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="member-wrapper"]/section/div/ul/li[2]/a'))
            )
        # type_sebi_text = type_sebi.get_attribute('innerText')
        type_sebi_text = "chairperson_members"
        print(type_sebi_text)
        type_sebi.click()

        total_records_text = sebi_config.browser.find_element(By.CSS_SELECTOR, ".pagination_inner p").text
        total_records = int(total_records_text.split()[-2])

       
        total_pages = (total_records + 24) // 25

        data = []

        for i in range(1, total_pages + 1):
            
            # time.sleep(5)
            page_xpath = f"//*[@class='pagination_outer']/ul/li/a[text()='{i}']"
            page_link = WebDriverWait(sebi_config.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, page_xpath))
            )
            page_link.click()

            table = WebDriverWait(sebi_config.browser, 10).until(
                EC.presence_of_element_located((By.ID, 'sample_1'))
            )

            
            page_source = sebi_config.browser.page_source

            
            soup = BeautifulSoup(page_source, 'html.parser')

           
            table = soup.find('table', {'id': 'sample_1'})

            
            for row in table.find_all('tr')[1:]:
                columns = row.find_all('td')
                date = columns[0].get_text(strip=True)
                title = columns[1].find('a').get_text(strip=True)
                link = columns[1].find('a')['href']
                data.append({'Date': date, 'Title': title, 'Link': link, 'type': type_sebi_text})

        
        df = pd.DataFrame(data)

        excel_file_name = f'sebi_data_all_pages_{type_sebi_text}{sebi_config.current_date}.xlsx'
        excel_file_path = rf"C:\Users\devadmin\sebi_final_script\chairperson_members\data\first_set_excel_sheet_files\{excel_file_name}"
        df.to_excel(excel_file_path, index=False)
        print(f"Data from all pages saved to sebi_data_all_pages_{type_sebi_text}.xlsx")
        check_new_data.check_new_data(excel_file_path, cursor,type_sebi_text)
        
        sebi_config.browser.quit()


    except Exception as e:
        script_status = "Failure"
        failure_reason = "script error"
        comments= ""
        updateDataScrapeLog(source_name,script_status,no_data_avaliable,no_data_scraped,get_data_count.get_data_count(),failure_reason,comments,source_status) 
        traceback.print_exc()
        send_mail.send_email("SEBI chairperson_members order script error", e)
        sys.exit("script error")