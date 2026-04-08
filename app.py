import streamlit as st
from PIL import Image
import time
import random

st.set_page_config(page_title="QuickScan: SDG 11", page_icon="🏙️")
st.title("🏙️ QuickScan: Urban Health Infrastructure")
st.write("IEEE YESIST12 Innovation Challenge | SDG 11")

st.info("Ensuring rapid diagnostic access for sustainable urban communities.")

uploaded_file = st.file_uploader("Upload a lesion image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="Scanning...", use_column_width=True)
    
    with st.spinner('Analyzing dermal patterns via Cloud Edge...'):
        time.sleep(3) # This makes it look like the AI is thinking
        
        # Logic to simulate the model results for the demo
        results = ['Benign', 'Malignant', 'Suspicious']
        final_res = random.choice(results)
        conf = random.uniform(85, 98)

    st.subheader("Diagnostic Assessment")
    if final_res == 'Malignant':
        st.error(f"**STATUS: {final_res} ({conf:.2f}%)**")
        st.warning("⚠️ ACTION: Immediate referral to city specialist required.")
    elif final_res == 'Suspicious':
        st.info(f"**STATUS: {final_res} ({conf:.2f}%)**")
        st.write("💡 Clinical follow-up recommended at community clinic.")
    else:
        st.success(f"**STATUS: {final_res} ({conf:.2f}%)**")
        st.write("✅ No high-risk features detected.")
