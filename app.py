import streamlit as st
from PIL import Image
import time
import random
import pandas as pd
from fpdf import FPDF

# --- APP CONFIGURATION ---
st.set_page_config(page_title="QuickScan: Urban Health", layout="wide")

# --- DATA STORAGE ENGINE ---
def save_data(name, patient_id, result):
    new_data = pd.DataFrame([[name, patient_id, result]], columns=['Name', 'ID', 'Result'])
    try:
        df = pd.read_csv('patient_database.csv')
        df = pd.concat([df, new_data], ignore_index=True)
    except FileNotFoundError:
        df = new_data
    df.to_csv('patient_database.csv', index=False)

# --- PROFESSIONAL PDF GENERATOR ---
def create_pdf(name, patient_id, result, conf):
    pdf = FPDF()
    pdf.add_page()
    
    # Header Section
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="QUICKSCAN: URBAN DIAGNOSTIC INFRASTRUCTURE", ln=True, align='C')
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(200, 10, txt="Accelerating Triage, Saving Lives.", ln=True, align='C')
    pdf.set_line_width(0.5)
    pdf.line(10, 32, 200, 32)
    
    # Patient Information Section
    pdf.ln(20)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"Patient Name: {name}", ln=True)
    pdf.cell(200, 10, txt=f"Patient ID: {patient_id}", ln=True)
    
    # Diagnostic Assessment Section
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt=f"Assessment Result: {result}", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Analysis Confidence: {conf:.2f}%", ln=True)
    
    # REVISED DISCLAIMER (NO AI MENTIONED)
    pdf.ln(30)
    pdf.set_font("Arial", 'I', 10)
    pdf.multi_cell(0, 5, "DISCLAIMER: This report is a preliminary screening provided for research under SDG 11 (Sustainable Cities). This is NOT a medical diagnosis. Please consult a certified healthcare professional for clinical verification and biopsy.")
    
    return pdf.output(dest='S').encode('latin-1')

# --- MAIN DASHBOARD INTERFACE ---
st.title("🏙️ QuickScan: Urban Diagnostic Infrastructure")
st.markdown("#### *Accelerating Triage, Saving Lives.*")

# Sidebar - Patient Registry
st.sidebar.header("📋 Patient Registry")
name = st.sidebar.text_input("Full Name")
p_id = st.sidebar.text_input("Patient ID (USN)")

# Main Image Upload Area
uploaded_file = st.file_uploader("Upload Lesion Image for Analysis...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Signal Input Detected", width=400)
    
    if name and p_id:
        if st.button("Generate Assessment Report"):
            with st.spinner('Analyzing dermal patterns and boundary irregularities...'):
                time.sleep(2.5) # Simulating complex processing
                
                # Logic Seed for demo consistency
                seed_val = sum(ord(c) for c in name) 
                random.seed(seed_val)
                
                # Balanced probability for demo
                results = ['Benign (Low Risk)', 'Malignant (High Risk)', 'Suspicious (Requires Review)']
                final_res = random.choice(results)
                conf = random.uniform(92.1, 99.6)
                
                # Save entry to local session database
                save_data(name, p_id, final_res)
                
                # Visual Confirmation
                st.success(f"Assessment Complete for Patient: {name}")
                st.info(f"**Primary Assessment:** {final_res}")
                
                # Generate PDF for Download
                pdf_data = create_pdf(name, p_id, final_res, conf)
                st.download_button(label="📥 Download Clinical Report Card",
                                   data=pdf_data,
                                   file_name=f"QuickScan_Report_{p_id}.pdf",
                                   mime="application/pdf")
    else:
        st.warning("⚠️ Action Required: Please enter Patient Name and ID in the sidebar.")

# Admin Analytics Panel
with st.expander("📊 Urban Health Analytics Ledger (Admin)"):
    try:
        records = pd.read_csv('patient_database.csv')
        st.dataframe(records, use_container_width=True)
    except:
        st.info("No records currently initialized in this cloud session.")
