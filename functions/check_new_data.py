from functions import get_data_count, send_mail, find_new_data
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



# log_list = [None] * 8



def get_number_of_new_data_in_excel(excel_file_path):

    try:
        df = pd.read_excel(excel_file_path)
        num_rows, num_columns = df.shape
        print(f"Number of rows: {num_rows}")
        print(f"Number of columns: {num_columns}")
        return num_rows
    except Exception as e:
            script_status = "Failure"
            failure_reason = "script error"
            comments= ""
            updateDataScrapeLog(source_name,script_status,no_data_avaliable,no_data_scraped,get_data_count.get_data_count(),failure_reason,comments,source_status) 
            traceback.print_exc()
            send_mail.send_email("SEBI chairperson_members order script error", e)
            sys.exit("script error")

def check_new_data(excel_file_path, cursor, type_sebi_text):
    try:
        # mydb = sebi_config.db_connection()
        # db_cursor = mydb.cursor()
        number_new_data = get_number_of_new_data_in_excel(excel_file_path)
        print(number_new_data,"number of total record in the website")
        # with mydb.cursor() as db_cursor:
        #     db_cursor.execute("SELECT COUNT(*) FROM sebi_orders where type_of_order='chairperson_members';")
        #     row_count = db_cursor.fetchone()[0]   
        #     mydb.commit()
        row_count = get_data_count.get_data_count()
        number_old_data = row_count

        no_data_avaliable = number_new_data - number_old_data

        print(no_data_avaliable,"number of new data")

        print(f"Number of data in database '{table_name}': {row_count}")

        if number_new_data == number_old_data:
            script_status = "Success"
            failure_reason = " "
            comments= ""
            updateDataScrapeLog(source_name,script_status,no_data_avaliable,no_data_scraped,row_count,failure_reason,comments,source_status) 
            sys.exit("There is no new data found")
        else:
            find_new_data.find_new_data(excel_file_path, table_name, type_sebi_text)
    
    except Exception as e:
            script_status = "Failure"
            failure_reason = "script error"
            comments= ""
            updateDataScrapeLog(source_name,script_status,no_data_avaliable,no_data_scraped,row_count,failure_reason,comments,source_status) 
            traceback.print_exc()
            send_mail.send_email("SEBI chairperson_members order script error", e)
            sys.exit("script error")
