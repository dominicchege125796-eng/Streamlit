import streamlit as st
import mysql.connector
import pandas as pd

# connects to the database
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="Library01"
    )

st.header("Library Management System")

# 2. Register new books to the library
st.subheader("Add a New Book")
with st.form(key="New_form", clear_on_submit=True):
    title = st.text_input("Book Title")
    book_id = st.text_input("Book Id")
    author = st.text_input("Author")
    date = st.date_input("Purchase Date")
    
    submit_button = st.form_submit_button("Add To Library")

# 3. inserting to the table
if submit_button:
    if title and author: 
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Ensure these variables match your input names above
            query = "INSERT INTO book_s (Book_Title, Book_id, Author_name, Date) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (title, book_id, author, date))
            
            conn.commit() 
            st.success(f"Added {title} successfully!")
            
            cursor.close()
            conn.close()
        except Exception as e:
            st.error(f"Error inserting data: {e}")
    else:
        st.warning("Please fill in the Title and Author.")

# 4. VIEW LOGIC
st.divider()
if st.button("View Books Available"):
    try:
        conn = get_db_connection()
        query = "SELECT * FROM book_s" 
        df = pd.read_sql(query, conn)
        st.dataframe(df, use_container_width=True)
        conn.close()
    except Exception as e:
        st.error(f"Error loading data: {e}")
