# 🔐 Multi-Factor Authentication using ML + Streamlit

import streamlit as st
import random
import pandas as pd

from sklearn.linear_model import LogisticRegression

data = pd.DataFrame({
    "time": [0,0,1,1,0,1,0,1],
    "location": [0,1,0,1,0,1,1,0],
    "device": [0,0,1,1,0,1,0,1],
    "result": [1,1,0,0,1,0,1,0] 
})

X = data[["time","location","device"]]
y = data["result"]

model = LogisticRegression()
model.fit(X, y)

USER_PASSWORD = "admin123"

st.title("🔐 Multi-Factor Authentication System")
st.write("Password + OTP + ML-based verification")


password = st.text_input("Enter Password", type="password")

if st.button("Login"):
    if password != USER_PASSWORD:
        st.error("Wrong Password ❌")
    else:
        st.success("Password Verified ✅")

       
        otp = random.randint(1000, 9999)
        st.session_state["otp"] = otp
        st.info(f"Your OTP is: {otp}")
if "otp" in st.session_state:
    user_otp = st.text_input("Enter OTP")

    if st.button("Verify OTP"):
        if str(user_otp) == str(st.session_state["otp"]):
            st.success("OTP Verified ✅")

            st.subheader("ML Security Check")

            time = st.selectbox("Login Time", ["Normal", "Odd"])
            location = st.selectbox("Location", ["Same", "New"])
            device = st.selectbox("Device", ["Known", "New"])

            time_val = 0 if time == "Normal" else 1
            loc_val = 0 if location == "Same" else 1
            dev_val = 0 if device == "Known" else 1

            if st.button("Final Verification"):
                prediction = model.predict([[time_val, loc_val, dev_val]])

                if prediction[0] == 1:
                    st.success("Login Successful ✅ (Safe User)")
                else:
                    st.error("Suspicious Login ❌ (Access Denied)")
        else:
            st.error("Invalid OTP ❌")