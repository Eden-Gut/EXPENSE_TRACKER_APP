import streamlit as st
import pandas as pd
from utils import load_and_clean_excel
import plotly.express as px
import os

st.set_page_config(page_title="מעקב הוצאות", layout="wide")

# טען CSS
with open("style/pastel.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("אפליקציית מעקב הוצאות חודשיות")

# העלאת קבצים
prev_file = st.file_uploader("בחרי קובץ הוצאות קיים", type=["xlsx"], key="prev")
new_file = st.file_uploader("בחרי קובץ חדש לחודש נוסף", type=["xlsx"], key="new")

if prev_file and new_file:
    df_prev = load_and_clean_excel(prev_file)
    df_new = load_and_clean_excel(new_file)

    df_all = pd.concat([df_prev, df_new], ignore_index=True)
    df_all["Amount"] = pd.to_numeric(df_all["Amount"], errors="coerce")

    st.subheader("טבלת הוצאות")
    st.dataframe(df_all)

    # גרף הוצאות לפי חודש
    st.subheader("גרף הוצאות לפי חודש")
    monthly = df_all.groupby("Month")["Amount"].sum().reset_index()
    monthly["3mo_avg"] = monthly["Amount"].rolling(window=3).mean()
    fig_bar = px.bar(monthly, x="Month", y="Amount", title="סכום חודשי", text_auto=True)
    fig_bar.add_scatter(x=monthly["Month"], y=monthly["3mo_avg"], mode="lines+markers", name="ממוצע 3 חודשים")
    st.plotly_chart(fig_bar, use_container_width=True)

    # גרף עוגה לפי קטגוריה
    st.subheader("פילוח לפי קטגוריה")
    pie = df_all.groupby("Category")["Amount"].sum().reset_index()
    fig_pie = px.pie(pie, names="Category", values="Amount", title="הוצאות לפי קטגוריה")
    st.plotly_chart(fig_pie, use_container_width=True)

    # KPI - תקציב לקטגוריה
    st.subheader("בדיקת תקציב לפי קטגוריה")
    categories = df_all["Category"].unique()
    for cat in categories:
        col1, col2 = st.columns([3, 1])
        with col1:
            budget = st.number_input(f"הכניסי תקציב חודשי לקטגוריה: {cat}", min_value=0.0, step=10.0)
        with col2:
            spent = df_new[df_new["Category"] == cat]["Amount"].sum()
            if budget > 0:
                color = "green" if spent <= budget else "red"
                st.markdown(f"<div style='color:{color}; font-weight:bold'>הוצאת {spent:.2f} ש״ח | יעד: {budget:.2f}</div>", unsafe_allow_html=True)
