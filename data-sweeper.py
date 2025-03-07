import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Streamlit Page Configuration
st.set_page_config(page_title="Data Sweeper", layout="wide")

# Tailwind-inspired CSS for Dark Mode
st.markdown(
    """
    <style>
        body {
            background-color: #111827;
            color: #E5E7EB;
            font-family: 'Inter', sans-serif;
        }
        .block-container {
            background: #1F2937;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
        }
        h1 {
            color: #3B82F6;
            font-size: 2.5rem;
            font-weight: bold;
        }
        .stButton>button {
            background: #3B82F6;
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            transition: 0.3s;
            font-weight: bold;
        }
        .stButton>button:hover {
            background: #2563EB;
        }
        .stDataFrame {
            border-radius: 10px;
            overflow: hidden;
        }
        .stDownloadButton>button {
            background: #10B981;
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
        }
        .stDownloadButton>button:hover {
            background: #059669;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# App Title
st.title("🚀 Data Sweeper")

# File Uploader
uploaded_files = st.file_uploader("📂 Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

# File Processing
if uploaded_files:
    for file in uploaded_files:
        file_extension = os.path.splitext(file.name)[-1].lower()
        
        # Read file as Pandas DataFrame
        if file_extension == ".csv":
            df = pd.read_csv(file)
        elif file_extension == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file type: {file_extension}")
            continue
        
        # File Info
        st.write(f"📄 **File Name:** {file.name}")
        st.write(f"📏 **File Size:** {file.size / 1024:.2f} KB")
        st.write("🔍 **Preview of Data:**")
        st.dataframe(df.head())

        # Data Cleaning
        st.subheader("🛠 Data Cleaning Options")
        if st.checkbox(f"🧹 Clean Data - {file.name}"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"🚮 Remove Duplicates"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates Removed!")
            with col2:
                if st.button(f"🔄 Fill Missing Values"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing Values Filled!")

        # Data Conversion
        st.subheader("🔄 Convert & Download")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"📥 Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_extension, ".csv")
                mime_type = "text/csv"
            else:
                df.to_excel(buffer, index=False, engine='openpyxl')
                file_name = file.name.replace(file_extension, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            st.download_button(
                label=f"⬇️ Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("🎉 All files processed successfully!")
