from utils.openai_lib import client
from time import time

prompt = """
What are the dimensions of this building?

What are the locations of all walls? Output the locations in
the format of a list of tuples of points, example

[
    [
        [x_start, y_start],
        [x_end, y_end],
    ),
]
where the points indicate the coordinates of the start/end
of a 1 dimensional wall segment, relative to the top left
of the floor plan, in meters.

Do the same for doors and windows, using the same format above

Return the response in JSON format without any explanation

Use the format: 
{
    "width": $x,
    "length": $y,
    "walls": $wall_points_list,
    "doors": $door_points_list,
    "windows": $window_door_list
}

Where
- $x is the width of the building
- $y is the length

Output distances in meters
"""

def read_file_as_string(file_path):
    with open(file_path, 'r') as file:
        file_content = file.read()
    return file_content

def get_floorplan_details(floorplan_image_path: str):
    response = client.get_image_details(prompt=prompt, image_path="images/test2.webp")

    width = response["width"]
    length = response["length"]
    walls = response["walls"]
    doors = response["doors"]
    windows = response["windows"]

    return width, length, walls, doors, windows

def generate_idf_file(floorplan_image_path: str, floorplan_csv_path: str):
    width, length, walls, doors, windows = get_floorplan_details(floorplan_image_path=floorplan_image_path)
    sample_file_data = read_file_as_string("SampleOfficeBuilding.idf")

    floorplan_csv_data = read_file_as_string(floorplan_csv_path)

    prompt = f"""
    Using the provided data below, generate a .idf file matching the example 
    format:

    {sample_file_data}

    - Building width = {width} meters
    - Building length = {length} meters
    - Wall locations (points in meters):
      {walls}
    - Door locations (points in meters):
      {doors}
    - Window locations (points in meters):
      {windows}

    Other floorplan metadata (csv):
    {floorplan_csv_data}

    Infer any missing details, don't add any comments or explanations
    """

    messages = [
        {"type": "text", "text": prompt},
    ]

    response = client.get_response(messages=messages)

    with open(f"output_idf_files/{int(time())}.idf", 'w') as file:
    # Write the string content to the file
        file.write(response)


generate_idf_file("images/test2.webp", floorplan_csv_path="building_properties_example.csv")


