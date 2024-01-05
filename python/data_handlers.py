import pandas as pd
import time
from connections import get_sql_connection
import sqlalchemy as sal

""" 
A Collection Of Functions Which Allow Data To Be Manipulated From One Form Into Another. The Names Give A Clear
Indication Of What They Do.
"""


def calc_time(start, end, dec=2, level=2):
    q_time = end - start
    m_seconds = str(q_time).split(".")[1]
    intervals = (
        ('weeks', 604800),  # 60 * 60 * 24 * 7
        ('days', 86400),  # 60 * 60 * 24
        ('hours', 3600),  # 60 * 60
        ('minutes', 60),
        ('seconds', 1),
    )
    result = []

    for name, count in intervals:
        value = q_time // count
        if value:
            q_time -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append(f"{value}"
                          )
    result.append(f"{m_seconds}"[0:dec - 1])

    return "".join(result[:level])


def csv_to_df(csv_loc: str):
    print("Reading CSV file...")
    start = time.time()
    this_df = pd.read_csv(csv_loc)
    final = calc_time(start, time.time())
    print(f"Time To Complete Reading CSV: {final} Seconds")
    return this_df


def pull_query_to_df(query, conn_eng):
    print("Downloading Data From SQL Table...")
    start = time.time()
    this_df = pd.read_sql(query, conn_eng, index_col=None, coerce_float=True, params=None, parse_dates=None)
    final = calc_time(start, time.time())
    print(f"Time To Complete Download: {final} Seconds")
    return this_df


def csv_to_sql(csv_loc, tablename, conn_string):
    conn_eng = sal.create_engine(conn_string, echo=False)
    print("Reading CSV data...")
    start = time.time()
    this_df = pd.read_csv(csv_loc)
    final = calc_time(start, time.time())
    print(f"Reading Completed In {final} Seconds")
    start = time.time()
    print("Uploading Data To SQL Table...")
    try:
        this_df.to_sql(tablename, con=conn_eng)
    except ValueError:
        print(f"Table: {tablename} Already Exists.")
        return False
    finally:
        final = calc_time(start, time.time())
        print(f"Time To Complete: {final} Seconds")
    return True


def sql_to_df(conn_string, query):
    conn_eng = get_sql_connection(conn_string)
    return pull_query_to_df(query, conn_eng)


def df_to_csv(DF, csv_loc):
    print("Saving To CSV...")
    start = time.time()
    this_df = DF.to_csv(csv_loc, index=False)
    final = calc_time(start, time.time())
    print(f"CSV Successfully Saved In: {final} Seconds")
    return True


def df_to_sql(DF, tablename, conn_string, if_exists="fail"):
    conn_eng = sal.create_engine(conn_string, echo=False)
    print(f"Uploading DataFrame To SQL DATABASE {conn_string}")
    try:
        start = time.time()
        DF.to_sql(name=tablename, con=conn_eng, index=False, if_exists=if_exists)
        final = calc_time(start, time.time())
        print(f"DataFrame Successfully Uploaded In: {final} Seconds")
    except ValueError:
        print("That Table Already Exists.")
        return False
    return True


def sql_to_csv(conn_string, query, csv_loc):
    start = time.time()
    this_df = sql_to_df(conn_string, query)
    final = calc_time(start, time.time())
    print(f"Time To Complete Upload: {final} Seconds")
    df_to_csv(this_df, csv_loc)
    return this_df


def pull_data(conn_string, query, csv_loc):
    this_df = None

    try:
        print("Trying To Pull Data From CSV File.")
        this_df = csv_to_df(csv_loc)
    except FileNotFoundError:
        print("FILE NOT FOUND!")
        this_df = sql_to_df(conn_string, query)
        try:
            print("Trying To Save A CSV BACKUP")
            this_df.to_csv(csv_loc, index=False, index_label=None)
        except:
            print("Something Went Wrong Saving Data To File.")
        finally:
            return this_df
    finally:
        if this_df is None:
            print("ERROR Something Went Wrong Getting The Data")
            return pd.DataFrame({"ok": [False]})
        else:
            print("Successfully Gathered Data!")
        return this_df


def query_db(conn_string, query, tablename):
    success = False
    conn_eng = get_sql_connection(conn_string)
    this_df = pull_query_to_df(query, conn_eng)
    save_loc = f"../{tablename}"
    try:
        df_to_csv(this_df, save_loc)
        print(f"Successfully Created CSV FILE for TABLE: {tablename}")
        success = True
    except:
        print(f"Something Went Wrong Saving TABLE: {tablename} -> To File.")
    finally:
        pass
    return success, save_loc


def get_all_travel_tide_tables(table_names, old_connection_string, new_connection_string):
    for table in table_names:
        q = f"SELECT * FROM {table}"
        start = time.time()
        ok, csv_loc = query_db(old_connection_string, q, table)
        final = calc_time(start, time.time())
        print(f"Time To Complete Download: {final} Seconds")
        if ok:
            start = time.time()
            transferred = csv_to_sql(csv_loc, table, new_connection_string)
            final = calc_time(start, time.time())

            if transferred:
                print(f"Successfully Created Table {table}")
                print(f"Time To Complete Transfer: {final} Seconds")
            else:
                print(f"The Transferring Of Table: {table} from {old_connection_string} to {new_connection_string} failed.")
                print("Check to see if the first word in the string is postgresql instead of postgres")
    return True






