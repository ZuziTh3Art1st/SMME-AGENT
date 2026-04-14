import sqlite3
import os

def creation_database():
    sql_file_path_tino = 'The_Main_Database.sql'

    if not os.path.exists(sql_file_path_tino):
        return

    conn_buz = sqlite3.connect('the_farm_agent.db')
    db_line = conn_buz.cursor()

    try:
        with open(sql_file_path_tino, 'r') as sql_file:
            sql_script = sql_file.read()

        db_line.executescript(sql_script)
        conn_buz.commit()

    except Exception as e:
        print(f"ERROR while running SQL script: {e}")
        conn_buz.rollback()

    finally:
        conn_buz.close()

if __name__ == "__main__":
    creation_database()