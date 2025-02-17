import pandas as pd
from sqlalchemy import create_engine, text
import streamlit as st
from urllib.parse import quote

def upload_csv_to_db(file_path, table_name, db_host, db_name, db_user, db_password, db_port):
    try:
        # URL-encode the password to handle special characters like '@'
        db_password = quote(db_password)

        # Create SQLAlchemy engine to connect to MySQL server (not specifying a database)
        engine = create_engine(f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}")

        # Connect to MySQL server
        with engine.connect() as conn:
            # Check if the database exists
            result = conn.execute(text("SHOW DATABASES LIKE :db_name"), {"db_name": db_name})
            if not result.fetchone():
                # Create the database if it doesn't exist
                conn.execute(text(f"CREATE DATABASE {db_name}"))
          
            # Switch to the specified database
            conn.execute(text(f"USE {db_name}"))

        # Create a new engine to interact with the specified database
        engine = create_engine(f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

        # Define column types for the SQL table
        column_types = {
            'book_id': 'VARCHAR(255)',
            'search_key': 'VARCHAR(255)',
            'book_title': 'VARCHAR(255)',
            'book_subtitle': 'TEXT',
            'book_authors': 'TEXT',
            'book_description': 'TEXT',
            'industryIdentifiers': 'TEXT',
            'text_readingModes': 'BOOLEAN',
            'image_readingModes': 'BOOLEAN',
            'pageCount': 'INT',
            'categories': 'TEXT',
            'language': 'VARCHAR(255)',
            'imageLinks': 'TEXT',
            'ratingsCount': 'INT',
            'averageRating': 'DECIMAL(10,2)',
            'country': 'VARCHAR(255)',
            'saleability': 'VARCHAR(255)',
            'isEbook': 'BOOLEAN',
            'amount_listPrice': 'DECIMAL(10,2)',
            'currencyCode_listPrice': 'VARCHAR(255)',
            'amount_retailPrice': 'DECIMAL(10,2)',
            'currencyCode_retailPrice': 'VARCHAR(255)',
            'buyLink': 'TEXT',
            'year': 'TEXT',
            'publisher': 'TEXT'
        }

        # Create a SQL statement to create the table with specified data types
        create_table_statement = f"CREATE TABLE IF NOT EXISTS {table_name} ("
        create_table_statement += ", ".join([f"{col} {col_type}" for col, col_type in column_types.items()])
        create_table_statement += ")"

        # Execute the create table statement
        with engine.connect() as conn:
            conn.execute(text(create_table_statement))

        # Read the CSV file
        df = pd.read_csv(file_path)

        # Upload the CSV data to the table (append mode to avoid table overwriting)
        df.to_sql(table_name, con=engine, if_exists='append', index=False)
        print(f"Successfully uploaded data to {table_name} table.")

    except Exception as e:
        print(f"Error uploading data: {e}")

if __name__ == "__main__":
    # Get database credentials from Streamlit Secrets
    db_host = st.secrets["bookscape_db_config"]["server"]
    db_name = st.secrets["bookscape_db_config"]["database"]
    db_user = st.secrets["bookscape_db_config"]["username"]
    db_password = st.secrets["bookscape_db_config"]["password"]
    db_port = st.secrets["bookscape_db_config"]["port"]

    # Get file path from user input (or potentially from another source)
    file_path = st.secrets["bookscape_csv_path"]["input_file"]

    # Set the table name directly
    table_name = "book_search"

    # Upload data to the database
    upload_csv_to_db(file_path, table_name, db_host, db_name, db_user, db_password, db_port)
