from config import sebi_config

def updateDataScrapeLog(source_name,script_status,data_available,data_scraped,total_record_count,failure_reason,comments,source_status):
    mydb = sebi_config.db_connection()
    cursor = mydb.cursor()
    print(source_name,script_status,data_available,data_scraped,total_record_count,failure_reason,comments,source_status)
    insert_qry = "INSERT INTO sebi_log (source_name,script_status,data_available,data_scraped,total_record_count,failure_reason,comments,source_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    try :
       cursor.execute(insert_qry,[source_name,script_status,data_available,data_scraped,total_record_count,failure_reason,comments,source_status])
       mydb.commit()
    except Exception as e :
        print("exception inside fn",str(e))        
      