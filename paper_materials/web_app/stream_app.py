
import streamlit as st
import os
import py3Dmol

# Function to list all .xyz files in a directory
def list_xyz_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.xyz')]

# Function to read and return the content of an XYZ file
def read_xyz_file(xyz_file_path):
    with open(xyz_file_path, 'r') as file:
        return file.read()

# Set the page to wide mode
#st.set_page_config(layout="wide")

# Streamlit app starts here
st.title('Systematic Improvement of Redox Potential Calculation of Fe(III)/Fe(II) Complexes Using a Three-Layer Micro-solvation Model')
st.markdown('## Supplementary Information Visualizer')

# Directory containing the .xyz files
xyz_files_directory = 'xyz_files/'

# List all .xyz files in the directory
xyz_files = list_xyz_files(xyz_files_directory)

# Dropdown to select an XYZ file
selected_file = st.selectbox('Select an XYZ file', xyz_files)

# Style options as radio buttons
style_options = {
    'Stick': {'stick': {}},
    'Ball and Stick': {'stick': {}, 'sphere': {'radius': 0.5}},
    'Spacefill': {'sphere': {}}
}
selected_style = st.radio('Select visualization style', list(style_options.keys()))

# Button to visualize the selected XYZ file
if st.button('Visualize'):
    # Full path to the selected file
    full_path_to_file = os.path.join(xyz_files_directory, selected_file)

    # Read the selected XYZ file
    xyz_content = read_xyz_file(full_path_to_file)
    scale = 1

    width = int(640.0*scale)
    height = int(480.0*scale)

    # Visualize the molecule using py3Dmol
    xyzview = py3Dmol.view(width=width, height=height)
    xyzview.addModel(xyz_content, 'xyz')
    xyzview.setStyle(style_options[selected_style])  # Use the selected style
    xyzview.zoomTo()

    # Display the visualization in Streamlit
    xyzview.show()
    st.components.v1.html(xyzview._make_html(), width=width, height=height, scrolling=False)
