import streamlit as st
from PIL import Image
import time

def main():
    st.title("Building Sustainability and Regulations Analysis")

    # Step 3: Uploading PDFs
    uploaded_file = st.file_uploader("Upload your floorplan (PDF format)", type="pdf")
    if uploaded_file is not None:
        with open("temp_floorplan.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("File uploaded successfully.")

    # Step 4: User Input for Building Details
    building_type = st.selectbox("Select the Building Type", options=["Residential", "Commercial", "Industrial"])
    occupancy = st.number_input("Occupancy", min_value=1, value=1)
    building_use = st.selectbox("Use of the Building", options=["Office", "Warehouse", "Retail", "Other"])
    materials = st.multiselect("Building Materials", options=["Concrete", "Wood", "Steel", "Glass", "Other"])
    building_age = st.slider("Age of the Building", min_value=0, max_value=100, value=10)

    # Hard-coded image path for the result
    image_path = "/Users/Joy/Desktop/HTG/pic.png"

    # Step 5: Processing Indicator and Displaying Result
    if st.button("Analyze"):
        with st.spinner("Analyzing your provided floorplan/blueprint..."):
            time.sleep(10)  # Simulate time for analysis
        with st.spinner("Creating a surrogate model with the floorplan and information provided..."):
            time.sleep(10)  # Simulate time for model creation
        with st.spinner("Simulating airflow patterns and thermal regulation..."):
            time.sleep(10)  # Simulate time for simulation
        
        st.success("Presenting AI suggestions for new HVAC and sensor placements.")
        
        # Display the specified image as the analysis result
        try:
            image = Image.open(image_path)
            st.image(image, caption="AI Suggestions")
        except Exception as e:
            st.error(f"Error accessing the result image: {e}")

if __name__ == "__main__":
    main()