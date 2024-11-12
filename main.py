"""Import necessary library"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import zipfile
import math
import pandas as pd
import streamlit as st
import geopandas as gpd
import pyproj
from shapely.geometry import Polygon
from shapely.geometry import Point
from shapely.geometry import box
from google.colab import files

"""To get all library version."""

#!pip install session-info

'''import backports
import session_info
session_info.show()

session_info.show(write_req_file=True, req_file_name='requirements.txt')'''

!pip freeze > requirements.txt

"""Hardcoded constant value."""

# Create the data dictionary
data = {
    'SN': range(1, 26),
    'scientific_name': ['Abies spp', 'Acacia catechu', 'Adina cardifolia', 'Albizia spp', 'Alnus nepalensis',
                       'Anogeissus latifolia', 'Bombax ceiba', 'Cedrela toona', 'Dalbergia sissoo',
                       'Eugenia Jambolana', 'Hymenodictyon excelsum', 'Lagerstroemia parviflora',
                       'Michelia champaca', 'Pinus roxburghii', 'Pinus wallichiana', 'Quercus spp',
                       'Schima wallichii', 'Shorea robusta', 'Terminalia alata', 'Trewia nudiflora',
                       'Tsuga spp', 'Terai spp', 'Hill spp', 'Coniferious', 'Broadleaved'],
    'a': [-2.4453, -2.3256, -2.5626, -2.4284, -2.7761, -2.272, -2.3856, -2.1832, -2.1959, -2.5693,
          -2.585, -2.3411, -2.0152, -2.977, -2.8195, -2.36, -2.7385, -2.4554, -2.4616, -2.4585,
          -2.5293, -2.3993, -2.3204, None, None],
    'b': [1.722, 1.6476, 1.8598, 1.7609, 1.9006, 1.7499, 1.7414, 1.8679, 1.6567, 1.8816,
          1.9437, 1.7246, 1.8555, 1.9235, 1.725, 1.968, 1.8155, 1.9026, 1.8497, 1.8043,
          1.7815, 1.7836, 1.8507, None, None],
    'c': [1.0757, 1.0552, 0.8783, 0.9662, 0.9428, 0.9174, 1.0063, 0.7569, 0.9899, 0.8498,
          0.7902, 0.9702, 0.763, 1.0019, 1.1623, 0.7496, 1.0072, 0.8352, 0.88, 0.922,
          1.0369, 0.9546, 0.8223, None, None],
    'a1': [5.4433, 5.4401, 5.4681, 4.4031, 6.019, 4.9502, 4.5554, 4.9705, 4.358, 5.1749,
           5.5572, 5.3349, 3.3499, 6.2696, 5.7216, 4.8511, 7.4617, 5.2026, 4.5968, 5.3475,
           5.2774, 4.8991, 5.5323, None, None],
    'b1': [-2.6902, -2.491, -2.491, -2.2094, -2.7271, -2.3353, -2.3009, -2.3436, -2.1559, -2.3636,
           -2.496, -2.4428, -2.0161, -2.8252, -2.6788, -2.4494, -3.0676, -2.4788, -2.2305, -2.4774,
           -2.6483, -2.3406, -2.4815, None, None],
    's': [0.436, 0.443, 0.443, 0.443, 0.803, 0.443, 0.443, 0.443, 0.684, 0.443,
          0.443, 0.443, 0.443, 0.189, 0.683, 0.747, 0.52, 0.055, 0.443, 0.443,
          0.443, 0.443, 0.443, 0.436, 0.443],
    'm': [0.372, 0.511, 0.511, 0.511, 1.226, 0.511, 0.511, 0.511, 0.684, 0.511,
          0.511, 0.511, 0.511, 0.256, 0.488, 0.96, 0.186, 0.341, 0.511, 0.511,
          0.511, 0.511, 0.511, 0.372, 0.511],
    'bg': [0.355, 0.71, 0.71, 0.71, 1.51, 0.71, 0.71, 0.71, 0.684, 0.71,
           0.71, 0.71, 0.71, 0.3, 0.41, 1.06, 0.168, 0.357, 0.71, 0.71,
           0.71, 0.71, 0.71, 0.355, 0.71],
    'Local_Name': ['Thingre Salla', 'Khayar', 'Karma', 'Siris', 'Uttis', 'Banjhi', 'Simal', 'Tooni',
                   'Sissoo', 'Jamun', 'Bhudkul', 'Botdhayero', 'Chanp', 'Khote Salla', 'Gobre Salla',
                   'Kharsu', 'Chilaune', 'Sal', 'Saj', 'Gamhari', 'Dhupi Salla', 'Terai Spp',
                   'Hill spp', None, None]
}
print(data)

"""wrap constant data in a variable"""

sppVal = pd.DataFrame(data)
sppVal = sppVal.fillna('')

"""For testing purpose to upload file I am using geopandas. when using streamlit comment this code."""

# Set the title of the Streamlit app
st.title("Stem mapping file (CSV File Uploader)")

# Create a file uploader widget
uploaded_file = st.file_uploader("Choose stem mapping CSV file", type="csv")

# Check if a file has been uploaded
if uploaded_file is not None:
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(uploaded_file)

        # Display the DataFrame
        st.write(df)
    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")
else:
    st.write("Please upload a CSV file.")

stemmapping = files.upload()
df = pd.read_csv('TreeLoc.csv')

joined_df = df.merge(sppVal, left_on='species', right_on='scientific_name')

"""copy the joined_df as 'result_df'."""

result_df = joined_df.copy()

def add_calculated_columns(df):
    df['stem_volume'] = (df['a'] + df['b'] * df['dia_cm'].apply(lambda x: math.log(x)) + df['c'] * df['height_m'].apply(lambda x: math.log(x))).apply(math.exp) / 1000
    df['branch_ratio'] = df['dia_cm'].apply(lambda x: 0.1 if x < 10 else 0.2)
    df['branch_volume'] = df['stem_volume'] * df['branch_ratio']
    df['tree_volume'] = df['stem_volume'] + df['branch_volume']
    df['cm10diaratio'] = (df['a1'] + df['b1'] * df['dia_cm'].apply(lambda x: math.log(x))).apply(math.exp)
    df['cm10topvolume'] = df['stem_volume'] * df['cm10diaratio']
    df['gross_volume'] = df['stem_volume'] - df['cm10topvolume']
    df['net_volume'] = df.apply(lambda row: row['gross_volume'] * 0.9 if row['class'] == 'A' else row['gross_volume'] * 0.8, axis=1)
    df['net_volum_cft'] = df['net_volume'] * 35.3147
    df['firewood_m3'] = df['tree_volume'] - df['net_volume']
    df['firewood_chatta'] = df['firewood_m3'] * 0.105944
    return df

"""## Function to perform calculations and add new columns

Apply the function to the dataframe
"""

result_df = add_calculated_columns(df=result_df)

columns_to_drop = ['SN', 'scientific_name', 'a', 'b', 'c', 'a1', 'b1', 's', 'm', 'bg']
result_df = result_df.drop(columns=columns_to_drop)

"""Download the result using streamlit instead of other library."""

'''result_df.to_csv('result_df.csv', index=False)
files.download('result_df.csv')'''

"""Download result using streamlit library."""

# Convert DataFrame to CSV
csv_data = result_df.to_csv(index=False)

# Create a download button
st.download_button(
    label="Download data as CSV",
    data=csv_data,
    file_name='result_df.csv',
    mime='text/csv'
)

"""#convert pandas dataframe to geopandas dataframe"""

result_df['geometry'] = result_df.apply(lambda row: Point(row['LONGITUDE'], row['LATITUDE']), axis=1)

result_gdf = gpd.GeoDataFrame(result_df, geometry='geometry', crs='epsg:4326')

"""Create Bounding box withing tree map extent and will be used to generate grid of twenty meter"""

# Get the total bounds (xmin, ymin, xmax, ymax)
xmin, ymin, xmax, ymax = result_gdf.total_bounds
# Create a Polygon using the bounds
bounding_polygon = box(xmin, ymin, xmax, ymax)
# Optionally, create a GeoDataFrame with the bounding polygon
bounding_gdf = gpd.GeoDataFrame(geometry=[bounding_polygon], crs=result_gdf.crs)

"""user input tree spacing value using streamlit."""

# Set the title of the Streamlit app
st.title("Grid Spacing in meter for Mother Tree")

# Create a number input widget for grid spacing, allowing floats
grid_spacing = st.number_input("Enter Grid Spacing (float)", value=1.0, step=0.1, format="%.2f")

# Display the entered grid spacing
st.write(f"Grid Spacing: {grid_spacing}")

# You can use this grid_spacing value for further calculations or operations
# For example, you might use it to set the spacing in a grid layout

"""Create grid"""

# Assuming 'bounding_gdf' is your GeoDataFrame in 'EPSG:4326'

# Define the grid spacing in meters (20 meters in this case)
spacing_meters = grid_spacing

# Get the bounds of the bounding geometry
xmin, ymin, xmax, ymax = bounding_gdf.total_bounds

# Calculate spacing in degrees based on the center of the bounding box
center_lat = (ymin + ymax) / 2
spacing_degrees = spacing_meters / (111320 * math.cos(math.radians(center_lat)))  # Approximate conversion

# Create a list of x and y coordinates for the grid points
x_coords = []
current_x = xmin
while current_x < xmax:
    x_coords.append(current_x)
    current_x += spacing_degrees

y_coords = []
current_y = ymin
while current_y < ymax:
    y_coords.append(current_y)
    current_y += spacing_degrees

# Create a list of polygons representing the grid cells
polygons = []
for x in x_coords:
    for y in y_coords:
        polygons.append(Polygon([(x, y), (x + spacing_degrees, y),
                                 (x + spacing_degrees, y + spacing_degrees), (x, y + spacing_degrees)]))

# Create a GeoDataFrame from the polygons
grid_gdf = gpd.GeoDataFrame({'geometry': polygons}, crs='EPSG:4326')

# (Optional) Clip the grid to the bounding geometry
grid_gdf = gpd.clip(grid_gdf, bounding_gdf)

# Ensure both GeoDataFrames have the same CRS (Coordinate Reference System)
if grid_gdf.crs != result_gdf.crs:
    result_gdf = result_gdf.to_crs(grid_gdf.crs)

# Perform a spatial join to find intersecting polygons, but keep only the grid cell index
intersected_grid_indices = gpd.sjoin(grid_gdf, result_gdf, how='inner', predicate='intersects').index.unique()

# Select the unique grid cells from grid_gdf based on the indices
selected_polygons_gdf = grid_gdf[grid_gdf.index.isin(intersected_grid_indices)].reset_index(drop=True)

selected_polygons_gdf.plot()

"""create Bounding Box from

#creating centroid gdf
"""

# Prompt the user to enter the EPSG code
epsg_code = st.text_input("Enter EPSG code for projection:", "32633")  # Default to UTM zone 33N as an example

try:
    # Convert the EPSG code from string to integer and project the GeoDataFrame
    projected_gdf = selected_polygons_gdf.to_crs(f"EPSG:{int(epsg_code)}")

    # Calculate centroids in the projected CRS
    centroid_gdf = projected_gdf.copy()
    centroid_gdf['geometry'] = centroid_gdf['geometry'].centroid

    # Project the centroids back to the original CRS if needed
    centroid_gdf = centroid_gdf.to_crs(selected_polygons_gdf.crs)

    # Display results in Streamlit
    st.write("Projected GeoDataFrame:")
    st.write(projected_gdf)
    st.write("Centroid GeoDataFrame:")
    st.write(centroid_gdf)

except ValueError:
    st.error("Please enter a valid EPSG code.")

# Display instructions
st.write("Enter the desired projected CRS (e.g., EPSG:32645):")

# Get user input for projected CRS using Streamlit
projected_crs = st.text_input("Enter EPSG Code:", value="EPSG:4326")

if projected_crs:
    try:
        # Reproject the GeoDataFrames
        centroid_gdf_proj = centroid_gdf.to_crs(projected_crs)
        result_gdf_proj = result_gdf.to_crs(projected_crs)

        # Perform the spatial join in the projected CRS
        joined_gdf = gpd.sjoin_nearest(centroid_gdf_proj, result_gdf_proj, how='left', distance_col='distance')

        # Group by centroid index and get the index of the nearest tree
        nearest_tree_indices = joined_gdf.groupby(joined_gdf.index)['distance'].idxmin()

        # Add 'remark' column to result_gdf
        result_gdf['remark'] = 'Felling Tree'
        result_gdf.loc[nearest_tree_indices, 'remark'] = 'Mother Tree'

        # Display the result GeoDataFrame
        st.write("Updated Result GeoDataFrame:")
        st.write(result_gdf)

    except pyproj.exceptions.CRSError as e:
        st.error(f"Error: Invalid CRS provided. Please enter a valid EPSG code.\nDetails: {e}")

"""The following code needs user input like ('EPSG:32644' or 'EPSG:32645' and so on) This input should use streamlit library. for testing purpose it is being used geopandas library.

#the following code uses geopandas library but it needs to be downloaded using streamlit library. correct the code accordingly.
"""

#result_gdf.to_csv('result_gdf.csv', index=False)
#files.download('result_gdf.csv')

"""using streamlit library download result_gdf"""

def download_csv(gdf, filename):
  """Downloads a GeoDataFrame as a CSV file using Streamlit."""
  # Convert GeoDataFrame to CSV string
  csv = gdf.to_csv(index=False)

  # Create a download button
  st.download_button(
      label=f"Download {filename}.csv",
      data=csv,
      file_name=f"{filename}.csv",
      mime="text/csv"
  )

# Example usage within your Streamlit app
download_csv(result_gdf, "result_gdf")

"""creating error please check seriously"""

# prompt: download "result_gdf" as zip shape file using streamlit

def download_gdf_zip(gdf, filename):
  """Downloads a GeoDataFrame as a zipped shapefile using Streamlit."""
  if not isinstance(gdf, gpd.GeoDataFrame):
    raise TypeError("Input must be a GeoDataFrame.")

  # Create in-memory buffer for the zip file
  zip_buffer = BytesIO()
  with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
      # Write shapefile components to the zip file
      gdf.to_file(filename, driver="ESRI Shapefile")

      for ext in ['.shp', '.shx', '.dbf', '.prj']:
        zipf.write(filename + ext)

  zip_buffer.seek(0)
  st.download_button(
      label=f"Download {filename}.zip",
      data=zip_buffer,
      file_name=f"{filename}.zip",
      mime="application/zip"
  )

# Example usage within your Streamlit app
if st.button('Download Shapefile'):
    download_gdf_zip(result_gdf, "result_gdf")
