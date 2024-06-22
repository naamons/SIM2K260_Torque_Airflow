import streamlit as st
import pandas as pd
import numpy as np
import io

def load_excel_data(uploaded_file):
    try:
        # Read Excel file
        xls = pd.ExcelFile(uploaded_file)
        
        # Check if both required sheets are present
        if 'Torque Map' not in xls.sheet_names or 'MAF Map' not in xls.sheet_names:
            st.error("Excel file must contain sheets named 'Torque Map' and 'MAF Map'")
            return None, None

        # Read Torque Map
        torque_df = pd.read_excel(xls, 'Torque Map', index_col=0)
        
        # Read MAF Map
        maf_df = pd.read_excel(xls, 'MAF Map', index_col=0)
        
        # Convert all data to float
        for df in [torque_df, maf_df]:
            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Drop any columns or rows that are entirely NaN
            df.dropna(how='all', axis=1, inplace=True)
            df.dropna(how='all', axis=0, inplace=True)
        
        return torque_df, maf_df
    except Exception as e:
        st.error(f"Error loading Excel file: {str(e)}")
        return None, None

def scale_data(df, scale_factor, inverse=False):
    if inverse:
        return df * (1 / scale_factor)
    else:
        return df * scale_factor

st.title('Engine Map Scaling App')

# File uploader
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file is not None:
    torque_df, maf_df = load_excel_data(uploaded_file)

    if torque_df is not None and maf_df is not None:
        # Sidebar for user input
        scale_factor = st.sidebar.slider('Scaling Factor', 0.5, 2.0, 1.0, 0.1)

        # Scale the data
        scaled_torque_df = scale_data(torque_df, scale_factor)
        scaled_maf_df = scale_data(maf_df, scale_factor, inverse=True)

        # Display original and scaled data for Torque Map
        st.subheader('Torque Map')
        col1, col2 = st.columns(2)
        with col1:
            st.write("Original")
            st.dataframe(torque_df)
        with col2:
            st.write("Scaled")
            st.dataframe(scaled_torque_df)

        # Display original and scaled data for MAF Map
        st.subheader('Mass Air Flow Map')
        col1, col2 = st.columns(2)
        with col1:
            st.write("Original")
            st.dataframe(maf_df)
        with col2:
            st.write("Scaled")
            st.dataframe(scaled_maf_df)

        # Visualization of scaling
        st.subheader('Visualization of Scaling')
        chart_data = pd.DataFrame({
            'Original Torque': torque_df.iloc[:, 0],
            'Scaled Torque': scaled_torque_df.iloc[:, 0],
            'Original MAF': maf_df.iloc[:, 0],
            'Scaled MAF': scaled_maf_df.iloc[:, 0]
        })
        st.line_chart(chart_data)

        # Create a BytesIO object to store the Excel file
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            scaled_torque_df.to_excel(writer, sheet_name='Scaled Torque Map')
            scaled_maf_df.to_excel(writer, sheet_name='Scaled MAF Map')
        output.seek(0)

        # Add download button for scaled data
        st.download_button(
            label="Download Scaled Maps as Excel",
            data=output,
            file_name="scaled_engine_maps.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
else:
    st.write("Please upload an Excel file containing 'Torque Map' and 'MAF Map' sheets.")
