import os
import requests
import pandas as pd
import streamlit as st

API_URL = "https://www.googleapis.com/books/v1/volumes"

def get_api_key():
    try:
        return st.secrets["bookscape_api"]["key"]
    except KeyError as e:
        print("Error retrieving API key. Ensure the API key is set in Streamlit secrets.")
        raise e

def fetch_books_data(query, api_key, start_index=0, max_results=40):
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
        print(f"Error fetching data. Status code: {response.status_code}")
        return None

def extract_book_details(data, search_query):
    books = []
    for item in data.get("items", []):
        industry_identifiers = item["volumeInfo"].get("industryIdentifiers", [])
        industry_identifiers_str = "; ".join(
            [f"{ident['type']}: {ident['identifier']}" for ident in industry_identifiers]
        )
        image_links = item["volumeInfo"].get("imageLinks", {})
        image_links_str = "; ".join([f"{k}: {v}" for k, v in image_links.items()])
        
        book_info = {
            "book_id": item["id"],
            "search_key": search_query,
            "book_title": item["volumeInfo"].get("title", "N/A"),
            "book_subtitle": item["volumeInfo"].get("subtitle", "N/A"),
            "book_authors": ", ".join(item["volumeInfo"].get("authors", ["N/A"])),
            "book_description": item["volumeInfo"].get("description", "N/A"),
            "industryIdentifiers": industry_identifiers_str,
            "text_readingModes": item["volumeInfo"].get("readingModes", {}).get("text", False),
            "image_readingModes": item["volumeInfo"].get("readingModes", {}).get("image", False),
            "pageCount": item["volumeInfo"].get("pageCount", 0),
            "categories": ", ".join(item["volumeInfo"].get("categories", ["N/A"])),
            "language": item["volumeInfo"].get("language", "N/A"),
            "imageLinks": image_links_str,
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

def main():
    api_key = get_api_key()
    all_books = []
    total_records = 0
    max_limit = 1000
    
    os.makedirs("dataset", exist_ok=True)
    file_path = os.path.join("dataset", "books_data.csv")
    
    while total_records < max_limit:
        input_query = input(f"Enter book search query (collected {total_records}/{max_limit} records): ")
        start_index = 0
        max_results = 40
        
        response = requests.get(API_URL, params={"key": api_key, "q": input_query})
        data_function = response.json()
        total_items = data_function.get("totalItems", 0)
        print(f"Total records available for '{input_query}': {total_items}")
        
        while total_records < max_limit and start_index < total_items:
            print(f"Fetching records {start_index + 1} to {start_index + max_results}...")
            data = fetch_books_data(input_query, api_key, start_index=start_index, max_results=max_results)
            
            if data and "items" in data:
                books = extract_book_details(data, input_query)
                remaining_limit = max_limit - total_records
                books = books[:remaining_limit]
                all_books.extend(books)
                total_records += len(books)
                start_index += max_results
            else:
                print("No more data to fetch or error in API response.")
                break
        
        if total_records >= max_limit:
            break
    
    df = pd.DataFrame(all_books)
    
    df.to_csv(file_path, index=False)
    
    print(f"Data saved to {file_path}")
    
if __name__ == "__main__":
    main()
