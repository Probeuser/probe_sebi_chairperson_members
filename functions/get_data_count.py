from config import sebi_config
def get_data_count():
    mydb = sebi_config.db_connection()
    db_cursor = mydb.cursor()
    with mydb.cursor() as db_cursor:
        db_cursor.execute("SELECT COUNT(*) FROM sebi_orders where type_of_order='chairperson_members';")
        total_record_count = db_cursor.fetchone()[0]   
        mydb.commit()
    return total_record_count