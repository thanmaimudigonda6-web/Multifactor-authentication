# 🔐 Multi-Factor Authentication (FIXED VERSION)

import streamlit as st
import random
import pandas as pd
from sklearn.linear_model import LogisticRegression

st.set_page_config(page_title="Secure Authentication System", page_icon="🔐", layout="wide")

page_bg_img = """
<style>
.stApp {
    background-image:https://img.freepik.com/premium-photo/enhancing-user-interface-security-with-multifactor-authentication-secure-login-concept-user-interface-security-multifactor-authentication-secure-login-cybersecurity-measures_918839-326655.jpg?w=2000
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}

.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.55);
    z-index: -1;
}

.css-1d391kg, .css-ffhzg2 {
    background: rgba(255, 255, 255, 0.9) !important;
}

h1, h2, h3, h4, h5, h6, p, label, div, span {
    color: #ffffff !important;
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

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

if "otp" not in st.session_state:
    st.session_state.otp = None

if "otp_verified" not in st.session_state:
    st.session_state.otp_verified = False

st.title("🔐 Multi-Factor Authentication System")

password = st.text_input("Enter Password", type="password")

if st.button("Login"):
    if password != USER_PASSWORD:
        st.error("Wrong Password ❌")
    else:
        st.success("Password Verified ✅")
        otp = random.randint(1000, 9999)
        st.session_state.otp = otp
        st.session_state.otp_verified = False
        st.info(f"Your OTP is: {otp}") 

if st.session_state.otp is not None:
    user_otp = st.text_input("Enter OTP")

    if st.button("Verify OTP"):
        if str(user_otp) == str(st.session_state.otp):
            st.success("OTP Verified ✅")
            st.session_state.otp_verified = True
        else:
            st.error("Invalid OTP ❌")

if st.session_state.otp_verified:

    st.subheader("🔍 ML Security Check")

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

if st.button("Reset 🔄"):
    st.session_state.otp = None
    st.session_state.otp_verified = False
    st.success("System Reset Successful ✅")