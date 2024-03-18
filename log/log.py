from config import sebi_config

def insert_log_into_table(log_cursor, log_list):
    query = """
        INSERT INTO sebi_log (source_name, script_status, data_available, data_scraped, total_record_count, failure_reason, comments, source_status)
        VALUES (%(source_name)s, %(script_status)s, %(data_available)s, %(data_scraped)s, %(total_record_count)s, %(failure_reason)s, %(comments)s, %(source_status)s)
    """
    values = {
        'source_name': sebi_config.source_name,
        'script_status': log_list[1] if log_list[1] else None,
        'data_available': log_list[2] if log_list[2] else None,
        'data_scraped': log_list[3] if log_list[3] else None,
        'total_record_count': log_list[4] if log_list[4] else None,
        'failure_reason': log_list[5] if log_list[5] else None,
        'comments': log_list[6] if log_list[6] else None,
        'source_status': sebi_config.source_status
    
    }

    log_cursor.execute(query, values)
   

        # 'source_name': sebi_config.source_name,
        # 'script_status': log_list[0] if log_list[0] else None,
        # 'data_available': log_list[1] if log_list[1] else None,
        # 'data_scraped': log_list[2] if log_list[2] else None,
        # 'total_record_count': log_list[3] if log_list[3] else None,
        # 'failure_reason': log_list[4] if log_list[4] else None,
        # 'comments': log_list[5] if log_list[5] else None,
        # 'source_status': sebi_config.source_status