import streamlit as st
import sqlite3
import pandas as pd
import io
from datetime import datetime

# 1. Database Setup
conn = sqlite3.connect('maison_balkiss_pro.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS ai_projects 
             (id INTEGER PRIMARY KEY, client TEXT, service TEXT, deadline TEXT, 
              total REAL, advance REAL, status TEXT)''')
conn.commit()

st.set_page_config(page_title="Maison Balkiss AI", layout="wide")

tech_services = ["AI & INNOVATION", "BRANDING & AI", "SMART TOURISM 4.0", "TECH ACADEMY 4.0", "ATELIERS", "Consulting"]

st.sidebar.title("👑 Maison Balkiss AI")
admin_mode = st.sidebar.checkbox("🔒 Admin Dashboard")

st.title("⚜️ AI Business Management System")
tab1, tab2, tab3 = st.tabs(["🚀 New Project", "📅 Project Pipeline", "📊 Finance & Admin"])

with tab1:
    st.subheader("📩 Register New AI Project")
    with st.form("tech_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            client = st.text_input("👤 Client Name")
            service = st.selectbox("🛠️ Service Type", tech_services)
            total = st.number_input("💰 Budget", min_value=0.0)
        with c2:
            deadline = st.date_input("📅 Deadline")
            advance = st.number_input("💵 Advance Payment", min_value=0.0)
            curr = st.selectbox("💱 Currency", ["USD", "EUR", "MAD"])
        
        if st.form_submit_button("✅ Save Project"):
            if client:
                c.execute("INSERT INTO ai_projects (client, service, deadline, total, advance, status) VALUES (?, ?, ?, ?, ?, ?)",
                          (client, service, deadline.strftime("%Y-%m-%d"), total, advance, "In Progress"))
                conn.commit()
                st.success(f"✅ Project for {client} saved!")

with tab2:
    st.subheader("📅 Project Pipeline")
    df = pd.read_sql_query("SELECT client as 'Client', service as 'Service', deadline as 'Deadline', status as 'Status' FROM ai_projects", conn)
    st.dataframe(df, use_container_width=True)

with tab3:
    if admin_mode:
        pwd = st.text_input("Admin Password", type="password")
        if pwd == "12345678ouafaa@":
            full_df = pd.read_sql_query("SELECT * FROM ai_projects", conn)
            st.write("### 📊 Financial Insights")
            st.dataframe(full_df, use_container_width=True)
            
            # --- Excel Download Logic ---
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                full_df.to_excel(writer, index=False, sheet_name='Projects')
            
            st.download_button(
                label="📥 Download Full Report (Excel)",
                data=buffer.getvalue(),
                file_name=f"Balkiss_AI_Report_{datetime.now().strftime('%Y-%m-%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.info("Enter password to access reports.")
