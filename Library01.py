import streamlit as st
import mysql.connector
import pandas as pd

# 1. DATABASE CONNECTION FUNCTION
def get_db_connection():
    return mysql.connector.connect(
        host="library-db-dominicchege125796-9e8b.h.aivencloud.com",
        user="avnadmin",
        port=20013, # Port must be an integer
        password="AVNS_5ETFXGZl1A3VlHfHenm",
        database="defaultdb"
    )

# 2. INITIAL DATABASE SETUP (CREATES TABLE IF IT DOESN'T EXIST)
def initialize_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Using the exact schema from your request
        create_table_query = """
        CREATE TABLE IF NOT EXISTS book_s (
            Book_Title VARCHAR(50),
            Book_id INT PRIMARY KEY NOT NULL,
            Author_Name VARCHAR(255) NOT NULL,
            Date DATE
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        st.error(f"Database Initialization Error: {e}")

# Run setup
initialize_db()

# 3. STYLING (Updated with Table Styling)
st.markdown(
    """
    <style>
    /* Main App Background (Sky Blue) */
    .stApp {
        background-color:#87CEEB; 
        color : white;
    }
    /* Text Color (Changed from red to black for high visibility) */
    .stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp label {
        color: #000000 !important; /* Changed from red to black */
        font-family : Arial;
    }

    /* --- TABLE SPECIFIC STYLING --- */
    /* Target the container that holds the dataframe */
    [data-testid="stDataFrame"] {
        border-radius: 10px; /* Rounded corners */
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); /* Subtle shadow */
        overflow: hidden; /* Ensures shadow/corners look good */
    }

    /* Style the table header background */
    .css-1e6zmbn { /* This class targets the dataframe header row */
        background-color: #2A4B7C; /* Use your galaxy blue color for contrast */
        color: white; /* White text for header */
        font-weight: bold;
    }
    
    /* Style the table rows (optional: alternate colors) */
    .css-1r6dn7w, .css-1dp5yyj { /* Target data rows */
        background-color: #FFFFFF; /* White rows */
        color: #000000; /* Black text for data */
    }
    
    /* Change button colors to match the theme */
    .stButton>button {
        background-color: #2A4B7C; /* Galaxy blue buttons */
        color: white;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.header("Library Management System")

# 4. FORM TO ADD BOOKS
st.subheader("Add a New Book")
with st.form(key="New_form", clear_on_submit=True):
    title = st.text_input("Book Title")
    b_id = st.number_input("Book Id (Number)", step=1) # Using number_input because your SQL is INT
    author = st.text_input("Author Name")
    purchase_date = st.date_input("Purchase Date")
    
    submit_button = st.form_submit_button("Add To Library")

# 5. INSERT LOGIC
if submit_button:
    if title and author: 
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Column names match your CREATE TABLE script exactly
            query = "INSERT INTO book_s (Book_Title, Book_id, Author_Name, Date) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (title, b_id, author, purchase_date))
            
            conn.commit() 
            st.success(f"Added '{title}' successfully!")
            
            cursor.close()
            conn.close()
        except Exception as e:
            st.error(f"Error inserting data: {e}")
    else:
        st.warning("Please fill in the Title and Author.")

# 6. VIEW LOGIC
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

