import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np

# 1. Smart City / SDG 11 Branding
st.set_page_config(page_title="QuickScan: SDG 11", page_icon="🏙️")
st.title("🏙️ QuickScan: Urban Health Infrastructure")
st.markdown("### IEEE YESIST12 Innovation Challenge")
st.write("Targeting **SDG 11**: Sustainable Cities and Communities through inclusive healthcare.")

# 2. Load the Model
@st.cache_resource
def load_my_model():
    # This loads the brain you downloaded from Colab
    return tf.keras.models.load_model('quickscan_brain.h5')

model = load_my_model()
categories = ['Benign', 'Malignant', 'Suspicious']

# 3. User Interface
st.divider()
st.info("Ensuring rapid diagnostic access for all urban residents.")
uploaded_file = st.file_uploader("Upload a skin lesion image for screening...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="Input Received", use_column_width=True)
    
    # AI Processing Pipeline
    img_resized = img.resize((224, 224))
    img_array = np.array(img_resized) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    with st.spinner('Analyzing dermal patterns...'):
        preds = model.predict(img_array)
        result = categories[np.argmax(preds)]
        confidence = np.max(preds) * 100
    
    # Result Visualization
    st.subheader("Diagnostic Assessment")
    if result == 'Malignant':
        st.error(f"**STATUS: {result} ({confidence:.2f}%)**")
        st.warning("⚠️ ACTION: Immediate referral to city specialist required.")
    elif result == 'Suspicious':
        st.info(f"**STATUS: {result} ({confidence:.2f}%)**")
        st.write("💡 Clinical follow-up recommended at your nearest community clinic.")
    else:
        st.success(f"**STATUS: {result} ({confidence:.2f}%)**")
        st.write("✅ No immediate high-risk features detected.")