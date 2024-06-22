import streamlit as st
import pandas as pd

# Function to calculate correlation and add scaling factor
def calculate_and_display_results(df_top_map, df_bottom_map, scaling_factor):
    # Calculate the correlation matrix between the two maps
    correlation_matrix = df_top_map.corrwith(df_bottom_map, axis=1)
    
    # Display the DataFrames
    st.write("### Top Map DataFrame")
    st.write(df_top_map)
    
    st.write("### Bottom Map DataFrame")
    st.write(df_bottom_map)
    
    st.write("### Correlation Matrix")
    st.write(correlation_matrix.to_frame('Correlation'))
    
    # Display scaling factor
    st.write(f"### Scaling Factor: {scaling_factor}")
    
    # Apply scaling factor to the top map
    scaled_top_map = df_top_map * scaling_factor
    st.write("### Scaled Top Map DataFrame")
    st.write(scaled_top_map)
    
    # Apply scaling factor to the bottom map
    scaled_bottom_map = df_bottom_map * scaling_factor
    st.write("### Scaled Bottom Map DataFrame")
    st.write(scaled_bottom_map)

# Streamlit app
st.title("Torque and Airflow Map Correlation Calculator")

# Input for Top Map
st.write("## Input Top Map Data")
top_map_data = st.text_area("Paste the Top Map data here (CSV format):", height=200)

# Input for Bottom Map
st.write("## Input Bottom Map Data")
bottom_map_data = st.text_area("Paste the Bottom Map data here (CSV format):", height=200)

# Input for Scaling Factor
scaling_factor = st.number_input("Scaling Factor:", value=1.0)

# Process data when the button is clicked
if st.button("Calculate"):
    if top_map_data and bottom_map_data:
        try:
            # Convert input data to DataFrames
            df_top_map = pd.read_csv(pd.compat.StringIO(top_map_data))
            df_bottom_map = pd.read_csv(pd.compat.StringIO(bottom_map_data))
            
            # Calculate and display results
            calculate_and_display_results(df_top_map, df_bottom_map, scaling_factor)
        
        except Exception as e:
            st.error(f"Error processing data: {e}")
    else:
        st.error("Please paste data for both maps.")
