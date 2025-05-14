import pandas as pd

def load_and_clean_excel(file):
    # קריאה מדילוג על שלוש שורות ראשונות
    df = pd.read_excel(file, skiprows=3)

    # בחירת עמודות רלוונטיות
    df = df[["תאריך חיוב", "סכום חיוב", "קטגוריה", "שם בית העסק"]]

    # שינוי שמות לעבודה נוחה
    df.columns = ["Date", "Amount", "Category", "Business"]

    # המרה לתאריך ומיון
    df["Date"] = pd.to_datetime(df["Date"],dayfirst = True, errors="coerce")
    df = df.dropna(subset=["Date"])
    
    # חישוב חודש
    df["Month"] = df["Date"].dt.to_period("M").astype(str)

    return df
