# Online BookScape Explorer 📊

Welcome to the **Online BookScape Explorer** project! This interactive web application is designed to help users explore, analyze, and visualize book data in an intuitive way. The application integrates with the Google Books API to fetch and process book data, storing it in a structured database for efficient analysis. Through an interactive Streamlit-based interface, users can seamlessly navigate the data, uncover insights, and download results for further exploration. Whether you're a book enthusiast, researcher, or data analyst, this tool provides a powerful and user-friendly platform for book data analysis.

---

## Live Application 🌐

Experience the application live at: [Online BookScape Explorer](https://onlinebookscapeexplorer.streamlit.app/)

**Try it now!** No installation required—explore book data in real-time with our interactive features.

---

## Project Goals 🎯

### Insights
1. **Data Fetching**: Fetch book data using the **Google Books API** based on user queries (up to 1000 records).
2. **Data Cleaning**: Clean the fetched data by handling missing values, duplicates, and inconsistencies.
3. **Database Integration**: Upload cleaned data to a **MySQL database** with specified data types.
4. **Data Analysis**: Use SQL queries to analyze the data and provide insights through the Streamlit application.

### Extraction
1. **User-Driven Data Fetching**: Allow users to input queries and fetch up to 1000 book records.
2. **Data Display**: Display raw data in a DataFrame on the Streamlit webpage.
3. **Data Download**: Provide an option to download the fetched data as a CSV file.

---

## Project Overview 🚀

This project includes several key components for processing and visualizing book data:

### Data Acquisition 📥

The book data is sourced using the Google Books API. To use this application, you need to generate a separate API key from the [Google Cloud Console](https://console.cloud.google.com/).

---

## Book Data Extraction and Structure 📊

The book data is extracted and structured into a MySQL database with the following key columns:

### Database Schema

| Column Name               | Data Type   | Description                                                                 |
|---------------------------|-------------|-----------------------------------------------------------------------------|
| `book_id`                 | VARCHAR     | A unique identifier for each book record.                                  |
| `search_key`              | VARCHAR     | The keyword or term used to search for the book via the API.               |
| `book_title`              | VARCHAR     | The title of the book.                                                     |
| `book_subtitle`           | TEXT        | A secondary or extended title for the book, if available.                 |
| `book_authors`            | TEXT        | The author(s) of the book.                                                 |
| `book_description`        | TEXT        | A brief summary or overview of the book's content.                        |
| `industryIdentifiers`     | TEXT        | Identifiers like ISBN (International Standard Book Number).                |
| `text_readingModes`       | BOOLEAN     | Indicates whether the book is available in a readable text format.         |
| `image_readingModes`      | BOOLEAN     | Indicates whether the book is available in an image-based reading mode.    |
| `pageCount`               | INT         | The total number of pages in the book.                                     |
| `categories`              | TEXT        | The genres or categories the book belongs to.                             |
| `language`                | VARCHAR     | The language code of the book.                                             |
| `imageLinks`              | TEXT        | URLs or links to the book's cover image or other related images.           |
| `ratingsCount`            | INT         | The total number of user ratings the book has received.                   |
| `averageRating`           | DECIMAL     | The average rating of the book based on user reviews.                     |
| `country`                 | VARCHAR     | The country code where the book is available or published.                |
| `saleability`             | VARCHAR     | Describes the availability of the book for sale.                          |
| `isEbook`                 | BOOLEAN     | Indicates whether the book is available as an eBook.                      |
| `amount_listPrice`        | DECIMAL     | The list price of the book in its native currency.                        |
| `currencyCode_listPrice`  | VARCHAR     | The currency code for the list price.                                     |
| `amount_retailPrice`      | DECIMAL     | The retail or discounted price of the book.                               |
| `currencyCode_retailPrice`| VARCHAR     | The currency code for the retail price.                                   |
| `buyLink`                 | TEXT        | A URL to purchase or access the book online.                              |
| `year`                    | TEXT        | The year of publication or release.                                       |
| `publisher`               | TEXT        | The publisher of the book.                                                |

---

### Data Cleaning and Transformation 🔧

- **Handling Missing Values**:
  - Numeric columns (e.g., `pageCount`, `ratingsCount`): Fill missing values with `0`.
  - Text columns (e.g., `book_description`, `categories`): Fill missing values with `"Not Available"`.
  - Boolean columns (e.g., `isEbook`, `text_readingModes`): Fill missing values with `False`.
- **Data Type Conversion**:
  - Convert `pageCount` to `INT`.
  - Convert `averageRating` to `DECIMAL`.
  - Convert `year` to `TEXT` (to handle non-numeric values like "2023-2024").

---

### Database Integration 🗄️

- **MySQL Database**: Set up a MySQL database to store and manage structured book data efficiently.
- **Data Ingestion**: Populated the database with cleaned and processed data for seamless exploration and analysis.

---

### Data Exploration and Analysis 🔍

- Developed a **Jupyter Notebook** to perform exploratory data analysis (EDA), including visualizations and summary statistics.
- Formulated and executed **20+ SQL queries** to answer key business questions.

---

### Web Application Development 🌐

- Built an interactive **Streamlit** application.
- Integrated the app with the MySQL database and included interactive **Plotly Express visualizations**.
- Enabled users to explore data with customizable filters.

---

## Key Features 🔑

- **Data Acquisition**: Fetch book data dynamically using the Google Books API.
- **Interactive Exploration**: Use the web-based interface to filter, search, and analyze book data effortlessly.
- **Data Visualization**: Gain insights through interactive charts and visual reports.
- **Creating Own Dataset**: Download the maximum number of records per query for further research and offline use.

---

## Example SQL Queries 📋

Here are some of the key SQL queries used to gain insights:

- Check Availability of eBooks vs Physical Books.
- Find the Publisher with the Most Books Published.
- Identify the Publisher with the Highest Average Rating.
- Get the Top 5 Most Expensive Books by Retail Price.
- Find Books Published After 2010 with at Least 500 Pages.
- List Books with Discounts Greater than 20%.

---

## Getting Started ⚙️

### Quick Start 🚀

Visit our [live application](https://onlinebookscapeexplorer.streamlit.app/) to start exploring the data immediately!

---

### Local Development Setup

#### Set up the Environment 🛠️

**Install Anaconda**: Download and install [Anaconda](https://www.anaconda.com/products/distribution).

**Install MySQL Community Server**: Download and install [MySQL](https://dev.mysql.com/downloads/mysql/).

---

#### Creating a New Conda Environment and Installing Dependencies 📦

1. **Create a new Conda environment using the `bookscape.yml` file**:
    ```bash
    conda env create -f bookscape.yml
    ```
2. **Activate the newly created environment**:
    ```bash
    conda activate bookscape
    ```

---

#### Configure Streamlit Secrets 🔑

Create a `.streamlit/secrets.toml` file in your project directory and add your database credentials:
```toml
[bookscape_api]
key = "your_API_key"
[bookscape_db_config]
server = "your_mysql_host"
database = "your_db_name"
username = "your_mysql_username"
password = "your_mysql_password"
port = "3306"
[bookscape_csv_path]
input_file = "your_csv_file_path"
[bookscape_sql]
scripts = "your_mysql_query_file_path"

```

### Prepare Data 💾
1. **Create a MySQL Database** and import the books data into it.
2. **Explore Data**: Open the provided Jupyter notebook for an interactive exploration.

### Run the Streamlit Application 🎬
- Navigate to your project directory in the terminal.
- Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

### Deploy to Streamlit Cloud ☁️
Follow the [Streamlit Cloud deployment instructions](https://docs.streamlit.io/streamlit-cloud) to easily share and deploy your application.

---

## Technologies Used 🛠️

- **Python**: For data manipulation, analysis, and visualization.
- **MySQL**: Relational database for storing and managing book data.
- **Plotly Express**: High-level library for creating interactive charts and graphs.
- **Streamlit**: Framework for building and deploying data-driven web apps.
- **Streamlit Secrets**: Secure storage and management of sensitive credentials.
- **Jupyter Notebook**: Interactive environment for data exploration and analysis.
- **Google Books API**: For fetching book data.
- **Anaconda**: Python and R distribution for data science.

---

## Contributing 🤝

Contributions are welcome! Feel free to fork this repository, make improvements, and submit a pull request.

---

## Disclaimer ⚠️

This project is for educational and demonstrative purposes. The provided code and data may not be suitable for production environments.

**Note**: This is a basic framework. You can customize and expand it further by adding more features, visualizations, and functionalities to meet your specific needs. For production environments, make sure to prioritize robust security practices, such as using environment variables or secrets management services.

---

Happy Exploring! 🎉
