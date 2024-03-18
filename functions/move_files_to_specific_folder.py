import os
import sys
import shutil
import traceback
import pandas as pd
from functions.data_scraping_log_function import updateDataScrapeLog
from log import log
from config import sebi_config
from functions import get_data_count, send_mail
from functions.writeIntodb import writeintodb
from config.sebi_config import no_data_avaliable,no_data_scraped,source_name,source_status,table_name

def move_files_to_specific_folder(file_name_excel_path, type_sebi_text):
    try:

        # main_folder_path = r"C:\Users\devadmin\sebi_final_script\chairperson_members\pdfdownload\chairperson_members"
        main_folder_path = r"C:\inetpub\wwwroot\Sebi_apiproject\pdfdownload\chairperson_members"
        excel_data = pd.read_excel(file_name_excel_path)

        df = pd.DataFrame(excel_data)

        years = set()

        months = set()

        final_rows = set()


        def save_to_excel():
            new_df = pd.DataFrame(final_rows)
            final_excel_sheets_name = f'final_excel_sheet{type_sebi_text}{sebi_config.current_date}.xlsx'
            final_excel_sheets_path = fr"C:\Users\devadmin\sebi_final_script\chairperson_members\data\final_excel_sheets\{final_excel_sheets_name}"
            new_df.to_excel(final_excel_sheets_path, index=False)
            # insert_excel_sheet_data_to_mysql.insert_excel_data_to_mysql(final_excel_sheets_path, sebi_config.cursor)
            writeintodb(final_excel_sheets_path)



        def move_files(selected_month_rows, year_folder_path, month, year):
            for row in selected_month_rows:
                file = row[4] 
                month_folder_path = os.path.join(year_folder_path, month) 
                print(month_folder_path) # Moved outside the loop
                if not os.path.exists(month_folder_path):  # Check if the month directory exists
                    os.makedirs(month_folder_path)
                else:
                    print(month, "it is already exists")


                old_file_path = os.path.join(sebi_config.download_folder,str(file))
                print(old_file_path,"old file path")
                new_file_path = os.path.join(month_folder_path,str(file))
                print(new_file_path,"new file path")
                shutil.move(old_file_path, new_file_path)
                _,_,relative_path = new_file_path.partition('Sebi_apiproject')
                relative_path = relative_path.replace('\\','/')
                print(relative_path,"relative path")
                final_rows.add(row + (relative_path,))



        def create_year_folders(selected_year_rows,year,months):
            year_folder_path = os.path.join(main_folder_path,year)
            if not os.path.exists(year_folder_path):
                os.makedirs(year_folder_path)
            else:
                print(year,"the folder is already exists")
            for month in months:
                selected_month_rows = set()   
                for row in selected_year_rows:
                    if month in row[0]:
                        selected_month_rows.add(row)
                        # print(row)
                # print(selected_month_rows)
                move_files(selected_month_rows,year_folder_path,month,year)



        def select_year_wise(months,years):
            for year in years:
                selected_year_rows = set()
                for index, row in df.iterrows():
                    if year in row['Date']:
                        selected_year_rows.add(tuple(row))
                print(year)
                # print(selected_year_rows)
                create_year_folders(selected_year_rows,year,months)
            save_to_excel()



        for index, row in df.iterrows():
            month_year = row['Date'] 
            parts = month_year.split(", ")
            year = parts[-1]
            years.add(year)
            month = parts[0].split()[0]  
            months.add(month)
        select_year_wise(months,years)

        print(months,"months in ewxcel sheets")
        print(years,"years in the excel sheets")

    except Exception as e:
        script_status = "Failure"
        failure_reason = "script error"
        comments= ""
        updateDataScrapeLog(source_name,script_status,no_data_avaliable,no_data_scraped,get_data_count.get_data_count(),failure_reason,comments,source_status) 
        traceback.print_exc()
        send_mail.send_email("SEBI chairperson_members order script error", e)
        sys.exit("script error")
