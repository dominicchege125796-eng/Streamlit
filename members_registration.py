import streamlit as st
import mysql.connector
import pandas as pd


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sample"
    )

def run_query(query, data=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, data)
    conn.commit()
    conn.close()


def registration_form():
    st.header("Welcome to Members Registration")
    st.subheader("Add New Member")

    names = st.text_input("Names", placeholder="Enter your Names")
    admno = st.number_input("Admission Number", value=0)
    course = st.selectbox("Course", ["Computer Science", "Journalism","Electrical Engineering", "Fashion","Tourism","Catering"])
    role = st.text_input("Role", placeholder="Enter your roles")

    if st.button("Add Member", type="primary"):
        if names: 
            sql = "INSERT INTO group_members (names, admno, course, role) VALUES (%s, %s, %s, %s)"
            val = (names, admno, course, role)
            try:
                run_query(sql, val)
                st.success(f"Successfully added {names}!")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter your names.")


def crud_matrix():
    st.header("Main Page")
    
    
    st.info("Member Database")
    try:
        with st.expander("View Table"):
            conn = get_connection()
            df = pd.read_sql("SELECT * FROM group_members", conn)
            st.dataframe(df, use_container_width=True)
        conn.close()
    except Exception as e:
        st.error(f"Error loading table: {e}")

    
    with st.expander("Update Member Details"):
        u_adm = st.number_input("Target Admission Number", value=0, key="upd_adm")
        u_name = st.text_input("New Name")
        u_course = st.selectbox("New Course", ["Computer Science", "Journalism", "Electrical Engineering", "Fashion", "Tourism", "Catering"])
        u_role = st.text_input("New Role")
        
        if st.button("Save Changes"):
            sql = "UPDATE group_members SET names=%s, course=%s, role=%s WHERE admno=%s"
            run_query(sql, (u_name, u_course, u_role, u_adm))
            st.success("Record updated!")

   
    with st.expander("Delete Member"):
        adm_del = st.number_input("Enter Adm No to Delete", value=0)
        if st.button("Delete Record", type="primary"):
            run_query("DELETE FROM group_members WHERE admno = %s", (adm_del,))
            st.success(f"Record {adm_del} deleted.")

st.sidebar.header("Navigations")
pg_home = st.Page(registration_form, title="Home Page", icon="🏠")
pg_crud = st.Page(crud_matrix, title="Main Page", icon="⚙️")

pg = st.navigation([pg_home, pg_crud])
pg.run()
