import pandas as pd
import json
from io import BytesIO

def load_and_clean_excel(file):
    df = pd.read_excel(file, skiprows=3)
    df = df[["תאריך חיוב", "סכום חיוב", "קטגוריה", "שם בית העסק"]]
    df.columns = ["Date", "Amount", "Category", "Business"]
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["Date"])
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df = df.dropna(subset=["Amount"])
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    return df

def save_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Expenses')
    output.seek(0)
    return output

def save_budget(budget_dict):
    with open("budget.json", "w", encoding="utf-8") as f:
        json.dump(budget_dict, f, ensure_ascii=False, indent=2)

def load_budget():
    try:
        with open("budget.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}
