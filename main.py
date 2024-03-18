from functions import extract_data_website, get_data_count, send_mail
from functions.data_scraping_log_function import updateDataScrapeLog
from log import log
import traceback
import sys
from config import sebi_config
from config.sebi_config import no_data_avaliable,no_data_scraped,source_name,source_status,table_name



def main():
   
    try:

        if sebi_config.source_status == "Active":
            extract_data_website.extract_data_website(sebi_config.cursor)
            print("started")
        elif sebi_config.source_status == "Hibernated":
            script_status = "not run"
            failure_reason = ""
            comments= ""
            updateDataScrapeLog(source_name,script_status,no_data_avaliable,no_data_scraped,get_data_count.get_data_count,failure_reason,comments,source_status) 
            traceback.print_exc()
        elif sebi_config.source_status == "Inactive":
            script_status = "not run"
            failure_reason = ""
            comments= ""
            updateDataScrapeLog(source_name,script_status,no_data_avaliable,no_data_scraped,get_data_count.get_data_count,failure_reason,comments,source_status) 
            traceback.print_exc()

    except Exception as e:
        script_status = "Failure"
        failure_reason = "script error"
        comments= ""
        updateDataScrapeLog(source_name,script_status,no_data_avaliable,no_data_scraped,'None',failure_reason,comments,source_status) 
        traceback.print_exc()
        send_mail.send_email("SEBI chairperson_members order script error", e)
        sys.exit("script error")



# Entry point of the script
if __name__ == "__main__":
    main()
