import csv

def read_entries():
    with open('work_log.csv') as worklog_csv:
        csv_reader = csv.reader(worklog_csv, delimiter=';', dialect='excel')
        all_rows = list(csv_reader)[1:] # Assuming there's a header row

        
        for row in all_rows: 
            yield {
                'workorder': row[0],
                'activity': row[1],
                'description': row[2],
                'hours': float(row[3])
            }