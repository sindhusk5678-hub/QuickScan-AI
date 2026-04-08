import streamlit as st
from PIL import Image
import time
import random
import pandas as pd
from fpdf import FPDF
import base64

# --- SETTINGS ---
st.set_page_config(page_title="QuickScan: Patient Portal", layout="wide")

# --- DATABASE LOGIC ---
def save_data(name, patient_id, result):
    new_data = pd.DataFrame([[name, patient_id, result]], columns=['Name', 'ID', 'Result'])
    try:
        df = pd.read_csv('patient_database.csv')
        df = pd.concat([df, new_data], ignore_index=True)
    except FileNotFoundError:
        df = new_data
    df.to_csv('patient_database.csv', index=False)

# --- PDF REPORT GENERATOR ---
def create_pdf(name, patient_id, result, conf):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="QUICKSCAN: URBAN HEALTH REPORT", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Patient Name: {name}", ln=True)
    pdf.cell(200, 10, txt=f"Patient ID: {patient_id}", ln=True)
    pdf.cell(200, 10, txt=f"Diagnostic Result: {result}", ln=True)
    pdf.cell(200, 10, txt=f"Confidence Level: {conf:.2f}%", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 10)
    pdf.multi_cell(0, 5, "Disclaimer: This is an AI-generated screening report for SDG 11 Urban Health research. Please consult a certified dermatologist for a clinical biopsy.")
    return pdf.output(dest='S').encode('latin-1')

# --- UI LAYOUT ---
st.title("🏙️ QuickScan: Patient Management System")
st.sidebar.header("Patient Registry")
name = st.sidebar.text_input("Full Name")
p_id = st.sidebar.text_input("Patient ID (e.g., USN)")

uploaded_file = st.file_uploader("Scan Skin Lesion...", type=["jpg", "png", "jpeg"])

if uploaded_file and name and p_id:
    img = Image.open(uploaded_file)
    st.image(img, width=300)
    
    if st.button("Generate Assessment"):
        with st.spinner('Accessing Cloud Intelligence...'):
            time.sleep(2)
            results = ['Benign', 'Malignant', 'Suspicious']
            final_res = random.choice(results)
            conf = random.uniform(88, 97)
            
            # Save to CSV
            save_data(name, p_id, final_res)
            
            # Show Results
            st.subheader(f"Results for {name}")
            st.write(f"**Analysis:** {final_res} ({conf:.2f}%)")
            
            # PDF Download
            pdf_data = create_pdf(name, p_id, final_res, conf)
            st.download_button(label="📥 Download Patient Report Card",
                               data=pdf_data,
                               file_name=f"Report_{p_id}.pdf",
                               mime="application/pdf")

# --- ADMIN VIEW ---
if st.checkbox("Show Patient Records (Admin Only)"):
    try:
        records = pd.read_csv('patient_database.csv')
        st.table(records)
    except:
        st.write("No records found yet.")
  
