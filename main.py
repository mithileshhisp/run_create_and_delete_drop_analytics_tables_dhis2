import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# PostgreSQL Configuration
# ============================================================

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


# ============================================================
# Connect to PostgreSQL
# ============================================================
###
#SHOW max_locks_per_transaction; -- 64
#SHOW max_locks_per_transaction;
#SHOW max_connections;
###ALTER SYSTEM SET max_locks_per_transaction = 256;
try:
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    conn.autocommit = False
    cursor = conn.cursor()

    print("Connected to PostgreSQL")

    print()


    # ========================================================
    # Find all analytics tables
    # ========================================================

    cursor.execute("""
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public'
          AND tablename LIKE 'analytics_%'
        ORDER BY tablename;
    """)

    tables = cursor.fetchall()

    if not tables:
        print("No analytics tables found.")
        cursor.close()
        conn.close()
        exit()


    print(f"Found {len(tables)} analytics tables:")
    print()

    for table in tables:
        print(f"  - {table[0]}")

    print()


    # ========================================================
    # Confirmation
    # ========================================================

    '''
    confirmation = input(
        "Do you want to TRUNCATE all these tables? (yes/no): "
    )
    '''

    confirmation = input(
        "Do you want to DROP all these tables? (yes/no): "
    )
    if confirmation.lower() != "yes":
        print("Operation cancelled.")
        cursor.close()
        conn.close()
        exit()


    # ========================================================
    # TRUNCATE/ DROP analytics tables
    # ========================================================

    for table in tables:

        table_name = table[0]

        #print(f"Truncating: {table_name}")
        print(f"Dropping Table: {table_name}")

        '''
        cursor.execute(
            f'TRUNCATE TABLE public."{table_name}" CASCADE;'
            #f'TRUNCATE TABLE public."{table_name}";'
        )
        '''

        cursor.execute(
            f'DROP TABLE IF EXISTS public."{table_name}" CASCADE;'
            #f'DROP TABLE public."{table_name}";'
        )

        print()
        print("========================================")
        #print("All analytics tables have been truncated")
        print(f"Dropped Table: {table_name}")
        print("========================================")


    # ========================================================
    # Commit
    # ========================================================

    conn.commit()

    print()
    print("========================================")
    #print("All analytics tables have been truncated")
    print("All analytics tables have been dropped")
    print("========================================")


except Exception as e:

    print()
    print("ERROR:")
    print(e)

    if 'conn' in locals():
        conn.rollback()

finally:

    if 'cursor' in locals():
        cursor.close()

    if 'conn' in locals():
        conn.close()

    print()
    print("Database connection closed.")