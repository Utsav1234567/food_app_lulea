# -*- coding: utf-8 -*-
"""
Created on Mon Aug 18 23:04:48 2025

@author: utsav
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import os
import smtplib
from email.mime.text import MIMEText

st.title("🍲 Luleå Home Kitchen – Weekly Orders")


project_folder = r"C:\Users\utsadh\OneDrive - Luleå University of Technology\Desktop\our business"





# Menu (static for now)
menu = {
    "Chicken Momo": {"price": 95, "allergens": "Wheat, Soy"},
    "Veg Dal-Bhat": {"price": 90, "allergens": "None (may contain traces of nuts)"},
    "Achar": {"price": 35, "allergens": "Mustard"},
    "Kheer (Rice Pudding)": {"price": 40, "allergens": "Milk"}
}

st.header("This Week’s Menu")
for dish, details in menu.items():
    st.write(f"**{dish}** – {details['price']} SEK  \n_Allergens: {details['allergens']}_")

# Option to choose Admin or Customer
mode = st.radio("Select Mode", ["Customer", "Admin"])

# Function to send email
def send_email(order_details):
    sender_email = "utsav.adhikari1234@gmail.com"
    sender_password = "vonw tduk mdbp jacm"  # use Gmail App Password
    receiver_email = "utsav.adhikari1234@gmail.com"

    subject = "New Luleå Home Kitchen Order"
    body = f"New Order Received:\n\n{order_details}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        st.info("📧 Notification sent to admin email.")
    except Exception as e:
        st.error(f"❌ Failed to send email: {e}")

if mode == "Customer":
    st.header("Place Your Order")
    name = st.text_input("Full Name")
    phone = st.text_input("Phone Number")
    dish = st.selectbox("Select Dish", list(menu.keys()))
    qty = st.number_input("Quantity", min_value=1, max_value=10, step=1)
    pickup = st.radio("Pickup or Delivery?", ["Pickup", "Delivery (+20 SEK)"])
    comments = st.text_area("Comments / Allergies")

    if st.button("Submit Order"):
        new_order = {
            "Timestamp": datetime.now(),
            "Name": name,
            "Phone": phone,
            "Dish": dish,
            "Quantity": qty,
            "Pickup/Delivery": pickup,
            "Comments": comments
        }

        # Save to CSV
        if not os.path.exists("orders.csv"):
            pd.DataFrame([new_order]).to_csv("orders.csv", index=False)
        else:
            pd.DataFrame([new_order]).to_csv("orders.csv", mode="a", header=False, index=False)

        st.success("✅ Order submitted! Please pay via Swish.")

        # Send email notification
        order_text = "\n".join([f"{k}: {v}" for k, v in new_order.items()])
        send_email(order_text)

elif mode == "Admin":
    st.header("Admin Panel – View Orders")
    password = st.text_input("Enter admin password", type="password")

    if password == "luleadmin123":  # set your own secure password
        if os.path.exists("orders.csv"):
            df = pd.read_csv("orders.csv")
            st.write("### All Orders")
            st.dataframe(df)

            # Export button
            if st.button("Export All Orders to Excel"):
                excel_file = "all_orders.xlsx"
                df.to_excel(excel_file, index=False)
                st.success(f"✅ Orders exported to {excel_file} in the project folder!")
        else:
            st.info("No orders yet.")
    else:
        st.warning("❌ Incorrect password")
