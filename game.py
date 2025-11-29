import streamlit as st
from PIL import Image
import io

st.set_page_config(page_title="Personal Finance Tracker UI", layout="wide")
st.title(" Personal Finance Tracker — UI Only (Frontend)")

st.write("This is a frontend-only UI. Backend logic (OCR, DB, ML) can be added later.")


st.sidebar.header("Upload Receipt")
uploaded_file = st.sidebar.file_uploader("Upload image or PDF", type=["jpg", "jpeg", "png", "pdf"])
process_btn = st.sidebar.button("Process Receipt")

col1, col2 = st.columns([2, 1])

with col1:
    st.header(" Receipt Preview / Extracted Data")

    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            st.info("PDF uploaded — preview is not shown in this UI version.")
        else:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Receipt", use_column_width=True)

        st.subheader(" Extracted Text (Placeholder)")
        st.text_area("OCR Output", "Extracted text will appear here...", height=200)

        st.subheader(" Detected Amount (Placeholder)")
        st.write("Amount: **₹0.00**")

        st.subheader(" Detected Date (Placeholder)")
        st.write("Date: **Not detected**")

        st.subheader(" Predicted Category (Placeholder)")
        st.write("Category: **Other**")

    else:
        st.info("Upload a receipt from the sidebar to preview.")


with col2:
    st.header(" Dashboard (UI Preview)")
    st.subheader("Recent Transactions")

    st.table({
        "Date": ["2025-01-01", "2025-01-03"],
        "Amount": ["₹250", "₹1200"],
        "Category": ["Groceries", "Bills"],
        "Source": ["receipt1.jpg", "receipt2.jpg"]
    })

    st.subheader("Spending by Category")
    st.bar_chart({
        "Groceries": [250],
        "Bills": [1200]
    })

st.markdown("---")