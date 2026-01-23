import streamlit as st
name = st.text_input("Enter your Names", "Type here")
Gender = st.radio("Choose gender" , ['Male', 'Female', 'Others`'])
age = st.slider("Choose your Age ", min_value = 10, max_value = 30)
st.write("Fill in your marks ")
maths = st.number_input("Maths", value=0.0)
os = st.number_input("Operating Systems", value=0.0)
oa = st.number_input("Computer Organization and Architecture", value=0.0)
ins = st.number_input("Information Systems", value=0.0)

average = (maths + os + oa + ins) / 4
if 80 <= average <= 100:
    message = "Distinction"
elif 60 <= average < 80:
    message = "Proficient"
elif 40 <= average < 60:
    message = "Pass"
elif average < 40:
    message = "Fail"
else :
     message = "Invalid"
    
if st.button("Calculate"):
    st.write("Your Name : " + name )
    st.write( "Gender : " + Gender)
    st.write(f"Age : {age}" )
    st.write(f"Average : {average}" )
    st.write(f"Grade : {message} " )
