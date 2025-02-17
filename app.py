import pandas as pd
import streamlit as st
import requests
import plotly.express as px
from sqlalchemy import create_engine, text
from urllib.parse import quote
from PIL import Image
import time
# Centralized function to get database configuration
def get_db_config():
    return {
        "host": st.secrets["bookscape_db_config"]["server"],
        "user": st.secrets["bookscape_db_config"]["username"],
        "password": st.secrets["bookscape_db_config"]["password"],
        "port": st.secrets["bookscape_db_config"]["port"],
        "database": st.secrets["bookscape_db_config"]["database"]
    }

# Centralized function to establish a database connection using SQLAlchemy
def create_connection():
    db_config = get_db_config()
    db_password = quote(db_config["password"])
    engine = create_engine(
        f"mysql+mysqlconnector://{db_config['user']}:{db_password}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    )
    return engine.connect()

# Function to fetch book data from the API
def fetch_books_data(query, api_key, start_index=0, max_results=40):
    API_URL = "https://www.googleapis.com/books/v1/volumes"
    response = requests.get(
        API_URL,
        params={
            "key": api_key,
            "q": query,
            "startIndex": start_index,
            "maxResults": max_results,
        },
    )
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching data. Status code: {response.status_code}")
        return None

# Function to process and extract book details
def extract_book_details(data, search_query):
    books = []
    for item in data.get("items", []):
        book_info = {
            "book_id": item["id"],
            "search_key": search_query,
            "book_title": item["volumeInfo"].get("title", "N/A"),
            "book_subtitle": item["volumeInfo"].get("subtitle", "N/A"),
            "book_authors": ", ".join(item["volumeInfo"].get("authors", ["N/A"])),
            "book_description": item["volumeInfo"].get("description", "N/A"),
            "industryIdentifiers": "; ".join([f"{ident['type']}: {ident['identifier']}" for ident in item["volumeInfo"].get("industryIdentifiers", [])]),
            "text_readingModes": item["volumeInfo"].get("readingModes", {}).get("text", False),
            "image_readingModes": item["volumeInfo"].get("readingModes", {}).get("image", False),
            "pageCount": item["volumeInfo"].get("pageCount", 0),
            "categories": ", ".join(item["volumeInfo"].get("categories", ["N/A"])),
            "language": item["volumeInfo"].get("language", "N/A"),
            "imageLinks": "; ".join([f"{k}: {v}" for k, v in item["volumeInfo"].get("imageLinks", {}).items()]),
            "ratingsCount": item["volumeInfo"].get("ratingsCount", 0),
            "averageRating": item["volumeInfo"].get("averageRating", 0.0),
            "country": item["saleInfo"].get("country", "N/A"),
            "saleability": item["saleInfo"].get("saleability", "N/A"),
            "isEbook": item["saleInfo"].get("isEbook", False),
            "amount_listPrice": item["saleInfo"].get("listPrice", {}).get("amount", 0.0),
            "currencyCode_listPrice": item["saleInfo"].get("listPrice", {}).get("currencyCode", "N/A"),
            "amount_retailPrice": item["saleInfo"].get("retailPrice", {}).get("amount", 0.0),
            "currencyCode_retailPrice": item["saleInfo"].get("retailPrice", {}).get("currencyCode", "N/A"),
            "buyLink": item["saleInfo"].get("buyLink", "N/A"),
            "year": item["volumeInfo"].get("publishedDate", "N/A").split("-")[0],
            "publisher": item["volumeInfo"].get("publisher", "N/A"),
        }
        books.append(book_info)
    return books

# Function to upload data to the database
def upload_to_db(df):
    try:
        db_config = get_db_config()
        db_password = quote(db_config["password"])
        engine = create_engine(
            f"mysql+mysqlconnector://{db_config['user']}:{db_password}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
        )
        
        with engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS extracted_books"))
        
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

        create_table_statement = "CREATE TABLE IF NOT EXISTS extracted_books ("
        create_table_statement += ", ".join([f"{col} {col_type}" for col, col_type in column_types.items()])
        create_table_statement += ")"

        with engine.connect() as conn:
            conn.execute(text(create_table_statement))

        df.to_sql('extracted_books', con=engine, if_exists='append', index=False)
        st.success("Data uploaded to the database successfully!")
    except Exception as e:
        st.error(f"Error uploading data to database: {e}")

# Function to execute an SQL query and return the results as a DataFrame
def execute_query(sql_query):
    conn = create_connection()
    return pd.read_sql_query(sql_query, conn)

# Function to display a graph based on the DataFrame
def display_graph(df, question):
    st.write("### 📈 Data Visualizations")
    if df.empty:
        st.write("No data available for visualization.")
        return

    if "ebook" in question.lower() or "physical" in question.lower():
        fig = px.pie(df, names=df.columns[0], values=df.columns[1], title="eBooks vs Physical Books Distribution")
    elif "publisher" in question.lower() and "most books" in question.lower():
        fig = px.bar(df, x=df.columns[0], y=df.columns[1], title="Publisher with the Most Books Published")
    elif "average rating" in question.lower() and "publisher" in question.lower():
        fig = px.bar(df, x=df.columns[0], y=df.columns[1], title="Publisher with the Highest Average Rating")
    elif "most expensive" in question.lower():
        fig = px.bar(df, x=df.columns[0], y=df.columns[1], title="Top 5 Most Expensive Books")
    elif "published after" in question.lower():
        fig = px.scatter(df, x=df.columns[2], y=df.columns[1], title="Books Published After 2010 with at Least 500 Pages")
    elif "discount" in question.lower():
        fig = px.bar(df, x=df.columns[0], y=df.columns[2], title="Books with Discounts Greater than 20%")
    elif "average page count" in question.lower():
        fig = px.box(df, x=df.columns[0], y=df.columns[1], title="Average Page Count for eBooks vs Physical Books")
    elif "authors" in question.lower() and "most books" in question.lower():
        fig = px.bar(df, x=df.columns[0], y=df.columns[1], title="Top 3 Authors with the Most Books")
    elif "publishers" in question.lower() and "more than 10 books" in question.lower():
        fig = px.bar(df, x=df.columns[0], y=df.columns[1], title="Publishers with More than 10 Books")
    elif "average page count" in question.lower() and "category" in question.lower():
        fig = px.bar(df, x=df.columns[0], y=df.columns[1], title="Average Page Count for Each Category")
    elif "ratings count greater than average" in question.lower():
        fig = px.bar(df, x=df.columns[0], y=df.columns[1], title="Books with Ratings Count Greater Than the Average")
    elif "specific keyword" in question.lower() and "title" in question.lower():
        fig = px.bar(df, x=df.columns[0], title="Books with a Specific Keyword in the Title")
    elif "highest average book price" in question.lower():
        fig = px.line(df, x=df.columns[0], y=df.columns[1], title="Year with the Highest Average Book Price")
    elif "consecutive years" in question.lower():
        fig = px.bar(df, x=df.columns[0], y=df.columns[1], title="Authors Who Published in Consecutive Years")
    elif "same year different publishers" in question.lower():
        fig = px.bar(df, x=df.columns[1], y=df.columns[2], color=df.columns[0], title="Authors Publishing in the Same Year Under Different Publishers")
    elif "average retail price" in question.lower() and "ebook" in question.lower():
        fig = px.bar(df, x=["eBooks", "Physical Books"], y=df.iloc[0], title="Average Retail Price of eBooks vs Physical Books")
    elif "outliers" in question.lower():
        fig = px.scatter(df, x=df.columns[1], y=df.columns[2], title="Books with Outlier Ratings")
    elif "highest average rating" in question.lower() and "publisher" in question.lower():
        fig = px.bar(df, x=df.columns[0], y=df.columns[1], title="Publisher with the Highest Average Rating (More than 10 Books)")
    else:
        fig = px.bar(df, x=df.columns[0], y=df.columns[1], title="General Analysis")

    st.plotly_chart(fig)

# Function to load SQL scripts from a file
def load_sql_script(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Mapping categories and questions to their corresponding SQL script paths
def get_question_to_script_map():
    # Attempt to get the SQL script path from Streamlit secrets or use a default script path
    try:
        default_script_path = st.secrets["bookscape_sql"]["scripts"]
        print("Using SQL script path from Streamlit secrets.")
    except Exception:
        default_script_path = "sql_query/"
        print("Using default SQL script path as Streamlit secrets are not set.")
    return {
        "Book Availability": {
            "Check Availability of eBooks vs Physical Books": f"{default_script_path}1.sql",
        },
        "Publishers": {
            "Find the Publisher with the Most Books Published": f"{default_script_path}2.sql",
            "Identify the Publisher with the Highest Average Rating": f"{default_script_path}3.sql",
            "Publisher with Highest Average Rating (More than 10 Books)": f"{default_script_path}20.sql",
        },
        "Book Prices and Discounts": {
            "Get the Top 5 Most Expensive Books by Retail Price": f"{default_script_path}4.sql",
            "List Books with Discounts Greater than 20%": f"{default_script_path}6.sql",
            "Year with the Highest Average Book Price": f"{default_script_path}15.sql",
            "Average Retail Price of eBooks and Physical Books": f"{default_script_path}18.sql",
        },
        "Book Details and Ratings": {
            "Find Books Published After 2010 with at Least 500 Pages": f"{default_script_path}5.sql",
            "Books with Ratings Count Greater Than the Average": f"{default_script_path}12.sql",
            "Books with Average Rating 2 Standard Deviations Away": f"{default_script_path}19.sql",
        },
        "Authors": {
            "Find the Top 3 Authors with the Most Books": f"{default_script_path}8.sql",
            "Count Authors Who Published 3 Consecutive Years": f"{default_script_path}16.sql",
            "Authors Who Published in the Same Year but Different Publishers": f"{default_script_path}17.sql",
        },
        "Categories and Page Count": {
            "Find the Average Page Count for eBooks vs Physical Books": f"{default_script_path}7.sql",
            "Find the Average Page Count for Each Category": f"{default_script_path}10.sql",
        },
        "Miscellaneous": {
            "Retrieve Books with More than 3 Authors": f"{default_script_path}11.sql",
            "Books with a Specific Keyword in the Title": f"{default_script_path}14.sql",
            "Books with the Same Author Published in the Same Year": f"{default_script_path}13.sql",
            "List Publishers with More than 10 Books": f"{default_script_path}9.sql",
        },
    }

# Function to render the extraction screen
def extraction_screen():
    st.button("Home", on_click=lambda: st.session_state.update({'current_screen': 'home', 'explore_clicked': False}))
    st.markdown("<h1 style='text-align: center; color: #4CAF50; font-size: 42px;'>Book Data Extraction & Download</h1>", unsafe_allow_html=True)
    
    query = st.text_input("Enter the search query", "")
    
    if st.button("Search Books"):
        
        if query:
            all_books = []
            start_index = 0
            max_results = 40
            total_records = 0
            api_key = st.secrets["bookscape_api"]["key"]
            API_URL = "https://www.googleapis.com/books/v1/volumes"
            
            # Make the API request
            try:
                response = requests.get(API_URL, params={"key": api_key, "q": query})
                st.write(f"HTTP Status Code: {response.status_code}")
                response.raise_for_status()
                data_function = response.json()
                total_items = data_function.get("totalItems", 0)
                print(f"Total records available: {total_items}")
                
                if total_items == 0:
                    st.write("No books found for the given query.")  # Display when no books are found
                
                # Fetch records if there are results
                while total_records < min(total_items, 1000):
                    print(f"Fetching records {start_index + 1} to {start_index + max_results}...")
                    data = fetch_books_data(query, api_key, start_index=start_index, max_results=max_results)
                    
                    if data and "items" in data:
                        books = extract_book_details(data, query)
                        all_books.extend(books)
                        total_records += len(books)
                        start_index += max_results
                    else:
                        print("No more data to fetch or error in API response.")
                        break

                if all_books:
                    st.write("### 📊 Data Overview")
                    df = pd.DataFrame(all_books)
                    st.dataframe(df)
                    upload_to_db(df)  # Upload to database
                    
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download CSV", 
                        data=csv, 
                        file_name=f"{query}_books.csv", 
                        mime="text/csv",
                        use_container_width=True
                    )
            except requests.exceptions.HTTPError as http_err:
                st.error(f"HTTP Status Code: {response.status_code}")  # Show only status code
            except Exception as err:
                st.error("An error occurred.")
        else:
            st.write("Please enter a search query.")


# Function to render the insights screen
def insights_screen():
    st.markdown("<h1 style='text-align: center; color: #4CAF50; font-size: 42px; '>BookScape Visual Explorer</h1>", unsafe_allow_html=True)
    st.button("Home", on_click=lambda: st.session_state.update({'current_screen': 'home', 'explore_clicked': False}))
    
    question_to_script_map = get_question_to_script_map()
    selected_category = st.selectbox("Select a Category", list(question_to_script_map.keys()))
    st.write("### Select a Question from the Category")

    selected_question = None
    with st.expander(f"{selected_category} Questions", expanded=True):
        questions_in_category = question_to_script_map[selected_category]
        selected_question = st.selectbox("Choose a question", list(questions_in_category.keys()))

    with st.expander("View SQL Query"):
        script_file = questions_in_category[selected_question]
        sql_script = load_sql_script(script_file)
        st.code(sql_script, language='sql')
        

    if selected_question:
        try:
            st.write("### 📊 Data Overview")
            df = execute_query(sql_script)
            st.table(df.style.set_properties(**{'text-align': 'left'}))
            display_graph(df, selected_question)
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Function to render the home screen

def home_screen():
    st.markdown(
        """
        <div style="text-align: center;">
            <h1 style="color: #4CAF50;">Online Bookscape Explorer</h1>
        </div>
        """, unsafe_allow_html=True
    )    
    image = Image.open("bookscape.png")
    image = image.resize((704, 500))
    st.image(image)
    st.markdown(
    """
    <div style="text-align: center; color: #000000; width: 704px; margin: 0 auto;">  
        <p style="text-align: justify;"> 
        The Online Bookscape Explorer is a comprehensive tool that bridges the gap between data fetching, database management, and interactive visualization. It leverages the Google Books API to fetch book data, processes it into a clean and structured format, and stores it in a database for further analysis. The project also includes an interactive Streamlit-based web application that allows users to explore the data, visualize insights, and download results. This project is ideal for book enthusiasts, researchers, and data analysts who want to explore and analyze book data in a user-friendly and efficient manner.</p>
    </div>
    """, unsafe_allow_html=True)

    if "explore_clicked" not in st.session_state:
        st.session_state.explore_clicked = False

    if not st.session_state.explore_clicked:
        if st.button("Try to Explore Now", use_container_width=True):
            st.session_state.explore_clicked = True
            with st.spinner('Exploring data...'):
                time.sleep(2)  
            st.session_state['current_screen'] = 'home' 
            st.rerun()
    else:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Insights", use_container_width=True):
                with st.spinner('Loading insights...'):
                    time.sleep(2) 
                st.session_state['current_screen'] = 'insights'  
                st.rerun()
        with col2:
            if st.button("Extraction", use_container_width=True):
                with st.spinner('Loading Extraction...'):
                    time.sleep(2) 
                st.session_state['current_screen'] = 'extraction' 
                st.rerun()

# Initialize session state
if 'current_screen' not in st.session_state:
    st.session_state['current_screen'] = 'home'

# Render the appropriate screen based on session state
if st.session_state['current_screen'] == 'home':
    home_screen()
elif st.session_state['current_screen'] == 'insights':
    insights_screen()
elif st.session_state['current_screen'] == 'extraction':
    extraction_screen()

