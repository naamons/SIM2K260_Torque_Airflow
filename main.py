import streamlit as st
import pandas as pd
import io

# Function to calculate correlation and add scaling factor
def calculate_and_display_results(df_top_map, df_bottom_map, scaling_factor):
    # Ensure the data is numerical
    df_top_map = df_top_map.apply(pd.to_numeric, errors='coerce')
    df_bottom_map = df_bottom_map.apply(pd.to_numeric, errors='coerce')
    
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

# Axis data based on provided example
rpm_values = [550, 650, 800, 1000, 1300, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5200, 5500, 6000, 6600]
mg_stk_values = [20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340]
nm_values = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850]

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
            df_top_map = pd.read_csv(io.StringIO(top_map_data), header=None)
            df_bottom_map = pd.read_csv(io.StringIO(bottom_map_data), header=None)
            
            # Assign the axis data
            df_top_map.columns = mg_stk_values
            df_top_map.index = rpm_values
            df_bottom_map.columns = nm_values
            df_bottom_map.index = rpm_values
            
            # Calculate and display results
            calculate_and_display_results(df_top_map, df_bottom_map, scaling_factor)
        
        except Exception as e:
            st.error(f"Error processing data: {e}")
    else:
        st.error("Please paste data for both maps.")
