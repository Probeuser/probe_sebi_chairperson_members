from functions import get_data_count, send_mail, move_files_to_specific_folder, get_non_pdf_download
from functions.data_scraping_log_function import updateDataScrapeLog
from log import log
import traceback
import sys
import time
import pandas as pd
from datetime import datetime
import re
from bs4 import BeautifulSoup
from config import sebi_config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.sebi_config import no_data_avaliable,no_data_scraped,source_name,source_status,table_name


def download_pdf_files(df, type_sebi_text):
    global log_list

    excel_with_final_name = f'file_name_excel_sheet_{type_sebi_text}{sebi_config.current_date}.xlsx'
    file_name_excel_path = fr"C:\Users\devadmin\sebi_final_script\chairperson_members\data\file_name_excel_sheets\{excel_with_final_name}"

    try:
        for index, row in df.iterrows():
            link = row['Link']

            browser = webdriver.Chrome(options=sebi_config.chrome_options)

            try:
                browser.get(link)
                browser.maximize_window()
                time.sleep(5)
                iframe_tag = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//iframe"))
                )

                src_value = iframe_tag.get_attribute("src")
                file_name = src_value.split("/")[-1]


                browser.switch_to.frame(iframe_tag)
                time.sleep(5)
                download_button = browser.find_element(By.XPATH, '//*[@id="download"]')
                time.sleep(5)
                download_button.click()
                time.sleep(10)
                print(f"File {file_name} downloaded.")

                df.at[index, 'pdf_file_name'] = file_name
                df.to_excel(file_name_excel_path, index=False)
                
            except Exception as e:
                date = row['Date']
                title = row['Title']
                pattern = r'(?i)in the matter of (.*)'
                date = datetime.strptime(date, '%b %d, %Y')
                formatted_date = date.strftime('%b %d, %Y').replace(",", "").lower()
                formatted_date_with_underscores = formatted_date.replace(" ", "_").lower()

                match = re.search(pattern, title)
                if match:
                    extracted_string = match.group(1).strip().replace(' ', '_').lower()
                    modified_string = extracted_string[:-1] if extracted_string.endswith('.') else extracted_string
                else:
                    modified_string = title.lower().replace(' ', '_')[:-1] if title.lower().endswith('.') else title.lower().replace(' ', '_')

                cleaned_string = re.sub(r'[^a-zA-Z0-9\s]', '', modified_string)[:30]
                cleaned_string += f"_{formatted_date_with_underscores}"
                name = cleaned_string
                print(name, "name of the file")
                non_pdf_file_name = get_non_pdf_download.get_non_pdf_download(link,browser,name,index)
                print(non_pdf_file_name,"non pdf file name")
                df.at[index, 'pdf_file_name'] = non_pdf_file_name
                df.to_excel(file_name_excel_path, index=False)
                print(f"Failed to download file {index + 1}. {str(e)}")
                traceback.print_exc()
                continue

            finally:
                browser.quit()


    except Exception as e:
        print(df)
        script_status = "Failure"
        failure_reason = "script error"
        comments= ""
        updateDataScrapeLog(source_name,script_status,no_data_avaliable,no_data_scraped,get_data_count.get_data_count(),failure_reason,comments,source_status) 
        traceback.print_exc()
        send_mail.send_email("SEBI chairperson_members order script error", e)
        sys.exit("script error")

    move_files_to_specific_folder.move_files_to_specific_folder(file_name_excel_path, type_sebi_text)