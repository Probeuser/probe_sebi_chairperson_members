import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from config import sebi_config
from datetime import datetime
import pandas as pd
from config.sebi_config import source_name,source_status
from functions.data_scraping_log_function import updateDataScrapeLog
today = datetime.today()
today_formatted_date = today.strftime("%Y%m%d")
print(today_formatted_date)
# convert 2023-11-01 14:11:48 into  2023-11-01 format
formatted_today = str(today).split(" ")[0]
date_scraped = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def writeintodb(final_excel_sheets_path) :
    print(final_excel_sheets_path)
    # initializing cursor for db
    mydb = sebi_config.db_connection()
    db_cursor = mydb.cursor()
    date_scraped = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    insert_query = """
        INSERT INTO sebi_orders
        (date_of_order, title_of_order, type_of_order, link_to_order, pdf_file_path,pdf_file_name,updated_date,date_scraped) 
        VALUES (%s, %s, %s, %s, %s, %s, %s,%s)
    """

    excel_path = rf"{final_excel_sheets_path}"

    # excel_path = fr"C:\Users\devadmin\sebi_final_script\chairperson_members\data\first_set_excel_sheet_files\sebi_data_all_pages_chairpersonmembers2024-03-07.xlsx"
    new_df = pd.read_excel(excel_path)
    print(new_df)
        
    # Insert DataFrame rows into the table
    for index, row in new_df.iterrows():
        date_of_order = row[0]
        title_of_order = row[1]
        type_of_order = row[3]
        link_to_order = row[2]
        pdf_file_path = row[5]
        pdf_file_name = row[4]
        updated_date = "null"

        data_to_insert = (date_of_order, title_of_order, type_of_order, link_to_order, pdf_file_path,pdf_file_name,updated_date,date_scraped)
        print(insert_query,data_to_insert)
        db_cursor.execute(insert_query, data_to_insert)
        mydb.commit()
        

    print("Data inserted successfully into MySQL table")
    with mydb.cursor() as db_cursor:
        db_cursor.execute("SELECT COUNT(*) FROM sebi_orders where type_of_order='chairperson_members'")
        total_record_count = db_cursor.fetchone()[0]   
        mydb.commit()
    script_status = "Success"
    data_available= str(len(new_df))
    data_scraped = str(len(new_df))
    failure_reason = " "
    comments= ""
    updateDataScrapeLog(source_name,script_status,data_available,data_scraped,total_record_count,failure_reason,comments,source_status) 

