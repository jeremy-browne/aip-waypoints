import pdfplumber
import pandas as pd
import argparse
import os
from xml.etree.ElementTree import Element, SubElement, ElementTree

# Set up argument parser
parser = argparse.ArgumentParser(description="Extract waypoints from an AIP PDF file, save them per state, and convert to KML.")
parser.add_argument("pdf_path", type=str, help="Path to the AIP PDF file")

# Parse arguments
args = parser.parse_args()
pdf_path = args.pdf_path

waypoints = []

# Open and process the PDF
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            lines = text.split("\n")
            
            for line in lines:
                line = line.strip()

                # **Filter out headers and irrelevant lines**
                if not line or "WAYPOINT STATE CODE LAT LONG" in line or "VFR WAYPOINTS" in line or "GEN" in line:
                    continue

                # **Split the line dynamically**
                parts = line.split()
                
                if len(parts) < 5:
                    print(f"Skipping unmatched line: {line}")  # Debugging output
                    continue  # Skip lines that don't have enough parts

                # Extract columns dynamically
                waypoint = " ".join(parts[:-4])  # Name might have multiple words
                state = parts[-4]
                code = parts[-3]
                lat = parts[-2]
                lon = parts[-1]

                # Store extracted data
                waypoints.append([waypoint, state, code, lat, lon])

# Convert to DataFrame
df = pd.DataFrame(waypoints, columns=["Waypoint", "State", "Code", "Latitude", "Longitude"])

# Create output directory
output_dir = "waypoints_by_state"
os.makedirs(output_dir, exist_ok=True)

# Function to convert DMS (Degrees, Minutes, Seconds) to Decimal Degrees
def dms_to_decimal(dms, waypoint, code):
    if not isinstance(dms, str) or len(dms) < 7:
        print(f"Skipping invalid coordinate: {dms} (Waypoint: {waypoint}, Code: {code})")
        return None  # Skip invalid coordinates

    direction = dms[-1]  # Last character should be N, S, E, or W
    dms = dms[:-1]  # Remove direction letter
    
    try:
        if len(dms) == 6:  # Latitude (DDMMSS)
            degrees = int(dms[:2])
            minutes = int(dms[2:4])
            seconds = int(dms[4:])
        elif len(dms) == 7:  # Longitude (DDDMMSS)
            degrees = int(dms[:3])
            minutes = int(dms[3:5])
            seconds = int(dms[5:])
        else:
            print(f"Skipping invalid DMS format: {dms} (Waypoint: {waypoint}, Code: {code})")
            return None

        decimal = degrees + (minutes / 60) + (seconds / 3600)

        # South & West should be negative
        if direction in ["S", "W"]:
            decimal = -decimal

        return decimal

    except ValueError:
        print(f"Skipping invalid numeric values in: {dms} (Waypoint: {waypoint}, Code: {code})")
        return None

# Process each state separately
for state, state_df in df.groupby("State"):
    state_csv_path = os.path.join(output_dir, f"waypoints_{state}.csv")
    state_df.to_csv(state_csv_path, index=False)
    print(f"Saved {len(state_df)} waypoints to {state_csv_path}")

    # Create KML root elements for three versions
    kml_name = Element("kml", xmlns="http://www.opengis.net/kml/2.2")
    document_name = SubElement(kml_name, "Document")

    kml_code = Element("kml", xmlns="http://www.opengis.net/kml/2.2")
    document_code = SubElement(kml_code, "Document")

    kml_code_name = Element("kml", xmlns="http://www.opengis.net/kml/2.2")
    document_code_name = SubElement(kml_code_name, "Document")

    # Convert waypoints for all KML versions
    for _, row in state_df.iterrows():
        lat_decimal = dms_to_decimal(row["Latitude"], row["Waypoint"], row["Code"])
        lon_decimal = dms_to_decimal(row["Longitude"], row["Waypoint"], row["Code"])

        # Skip entries where coordinates couldn't be parsed
        if lat_decimal is None or lon_decimal is None:
            continue

        # Placemark for Name-based KML
        placemark_name = SubElement(document_name, "Placemark")
        name = SubElement(placemark_name, "name")
        name.text = row["Waypoint"]  # Use Waypoint name as label
        description = SubElement(placemark_name, "description")
        description.text = f"Code: {row['Code']}"  # Show Code in description
        point = SubElement(placemark_name, "Point")
        coordinates = SubElement(point, "coordinates")
        coordinates.text = f"{lon_decimal},{lat_decimal},0"

        # Placemark for Code-based KML
        placemark_code = SubElement(document_code, "Placemark")
        code = SubElement(placemark_code, "name")
        code.text = row["Code"]  # Use Code as label
        description = SubElement(placemark_code, "description")
        description.text = f"Waypoint: {row['Waypoint']}"  # Show Name in description
        point = SubElement(placemark_code, "Point")
        coordinates = SubElement(point, "coordinates")
        coordinates.text = f"{lon_decimal},{lat_decimal},0"

        # Placemark for Code-Name format KML
        placemark_code_name = SubElement(document_code_name, "Placemark")
        code_name = SubElement(placemark_code_name, "name")
        code_name.text = f"{row['Code']} - {row['Waypoint']}"  # Use "CODE - NAME" as label
        description = SubElement(placemark_code_name, "description")
        description.text = f"State: {row['State']}"  # Show State in description
        point = SubElement(placemark_code_name, "Point")
        coordinates = SubElement(point, "coordinates")
        coordinates.text = f"{lon_decimal},{lat_decimal},0"

    # Generate filenames based on state
    kml_file_name = os.path.join(output_dir, f"waypoints_{state}_name.kml")
    kml_file_code = os.path.join(output_dir, f"waypoints_{state}_code.kml")
    kml_file_code_name = os.path.join(output_dir, f"waypoints_{state}_code_name.kml")

    # Save KML files
    tree_name = ElementTree(kml_name)
    tree_name.write(kml_file_name, encoding="utf-8", xml_declaration=True)

    tree_code = ElementTree(kml_code)
    tree_code.write(kml_file_code, encoding="utf-8", xml_declaration=True)

    tree_code_name = ElementTree(kml_code_name)
    tree_code_name.write(kml_file_code_name, encoding="utf-8", xml_declaration=True)

    print(f"Generated KML files for {state}:")
    print(f" - {kml_file_name} (Waypoint Name as Label)")
    print(f" - {kml_file_code} (Waypoint Code as Label)")
    print(f" - {kml_file_code_name} (CODE - NAME as Label)")

print("Processing complete! All waypoints saved per state in CSV and KML formats.")
