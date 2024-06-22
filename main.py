import streamlit as st
import pandas as pd
import numpy as np
import io

def parse_pasted_data(data):
    # Split the data into lines
    lines = data.strip().split('\n')
    
    # Extract headers and data
    headers = lines[0].split()[1:]  # Skip the first column header (RPM)
    data_rows = [line.split() for line in lines[1:]]
    
    # Create DataFrame
    df = pd.DataFrame(data_rows, columns=['RPM'] + headers)
    df = df.set_index('RPM')
    
    # Convert all data to float
    for col in df.columns:
        df[col] = df[col].astype(float)
    
    return df

def scale_data(df, scale_factor, inverse=False):
    if inverse:
        return df * (1 / scale_factor)
    else:
        return df * scale_factor

st.title('Engine Map Scaling App')

# Text areas for pasting data
torque_data = st.text_area("Paste your Torque Map data here:")
maf_data = st.text_area("Paste your Mass Air Flow Map data here:")

# Parse pasted data when available
if torque_data and maf_data:
    torque_df = parse_pasted_data(torque_data)
    maf_df = parse_pasted_data(maf_data)

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

    # Add download buttons for scaled data
    torque_csv = scaled_torque_df.to_csv().encode('utf-8')
    st.download_button(
        label="Download Scaled Torque Map as CSV",
        data=torque_csv,
        file_name="scaled_torque_map.csv",
        mime="text/csv",
    )

    maf_csv = scaled_maf_df.to_csv().encode('utf-8')
    st.download_button(
        label="Download Scaled MAF Map as CSV",
        data=maf_csv,
        file_name="scaled_maf_map.csv",
        mime="text/csv",
    )
else:
    st.write("Please paste your data into both text areas above.")
