import os
import sys
import shutil
import traceback
import pandas as pd
from functions.data_scraping_log_function import updateDataScrapeLog
from log import log
from config import sebi_config
from sqlalchemy import create_engine 
from functions import get_data_count, send_mail, download_pdf_files
from config.sebi_config import no_data_avaliable,no_data_scraped,source_name,source_status,table_name

def find_new_data(excel_file_path, db_table_name, type_sebi_text):
    try:
        database_uri = f'mysql://{sebi_config.user}:{sebi_config.password}@{sebi_config.host}/{sebi_config.database}'
        engine = create_engine(database_uri)

        excel_data_df = pd.read_excel(excel_file_path)

        select_query = f"SELECT link_to_order FROM {db_table_name} WHERE type_of_order = 'chairperson_members';"
        database_table_df = pd.read_sql(select_query, con=engine)

        missing_rows = []

        for index, row in excel_data_df.iterrows():
            if row['Link'] not in database_table_df['link_to_order'].values:
                missing_rows.append(row)

        print("Rows from Excel Data not in Database Table:")
        print(missing_rows)
        new_excel_file_path = rf"C:\Users\devadmin\sebi_final_script\chairperson_members\data\incremental_excel_sheets\Missing_Data_{type_sebi_text}_{sebi_config.current_date}.xlsx"
        missing_data_df = pd.DataFrame(missing_rows)
        missing_data_df.to_excel(new_excel_file_path, index=False)
        download_pdf_files.download_pdf_files(missing_data_df, type_sebi_text)  
        print(f"Missing rows saved to {new_excel_file_path}")

    except Exception as e:
        script_status = "Failure"
        failure_reason = "script error"
        comments= ""
        updateDataScrapeLog(source_name,script_status,no_data_avaliable,no_data_scraped,get_data_count.get_data_count(),failure_reason,comments,source_status) 
        traceback.print_exc()
        send_mail.send_email("SEBI chairperson_members order script error", e)
        sys.exit("script error")

