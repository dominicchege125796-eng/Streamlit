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


def run_query(query, data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, data)
    conn.commit()
    conn.close()

st.header("Welcome to Members Registration form")
st.subheader("Form")

names = st.text_input("Names", placeholder="Enter your Names")
admno = st.number_input("Admission Number", value=0)
course = st.selectbox("Course", ["Computer Science", "Journalism","Electrical Engineering", "Fashion","Tourism","Catering"])
role = st.text_input("Role", placeholder="Enter your roles")

st.info("Add new Member")
if st.button("Add Member"):
    if names: 
        sql = "INSERT INTO members (names, admno, course, role) VALUES (%s, %s, %s, %s)"
        val = (names, admno, course, role)
        
        try:
            run_query(sql, val)

            st.success(f"Successfully added {names} (Adm: {admno}) to the database!")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter your names.")

st.info("View the Table")
if st.button("View The Table"):
    try:
        conn = get_connection()
        query = "SELECT * FROM members"
        df = pd.read_sql(query, conn)
        st.dataframe(df)
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

st.sidebar.info("Options")
if st.sidebar.checkbox("Delete"):
    st.info("Delete a Member")


    adm = st.number_input("Enter Admission Number to Delete", value=125000)

    if st.button("Delete Record", type="primary"): 
         if adm:
       
              sql = "DELETE FROM members WHERE admno = %s"
              val = (adm,) 
         try:
             run_query(sql, val)
             st.success(f"Record with Admission Number {adm} has been removed.")
         except Exception as e:
                st.error(f"Error: {e}")
    

if st.sidebar.checkbox("Update Record"):
    st.subheader("Update Member")
    
    u_adm = st.number_input("Target Admission Number", value=0, key="update_adm_input")
    u_name = st.text_input("New Name")
    u_course = st.selectbox("New Course", ["Computer Science", "Journalism", "Electrical Engineering", "Fashion", "Tourism", "Catering"], key="update_course_select")
    u_role = st.text_input("New Role")
    
    
    if st.button("Save Changes"):
        if u_name: 
            sql = "UPDATE members SET names=%s, course=%s, role=%s WHERE admno=%s"
            val = (u_name, u_course, u_role, u_adm)
            
            try:
                run_query(sql, val)
                st.success(f"Record for Admission No {u_adm} updated successfully!")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please provide a name to update.")