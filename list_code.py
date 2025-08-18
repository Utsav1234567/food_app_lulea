# -*- coding: utf-8 -*-
"""
Created on Mon Aug 18 23:04:48 2025

@author: utsav
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.title("🍲 Luleå Home Kitchen – Weekly Orders")

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
    
    # Append to CSV
    if not os.path.exists("orders.csv"):
        pd.DataFrame([new_order]).to_csv("orders.csv", index=False)
    else:
        pd.DataFrame([new_order]).to_csv("orders.csv", mode="a", header=False, index=False)
    
    st.success("✅ Order submitted! Please pay via Swish.")
