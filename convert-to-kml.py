import pandas as pd
from xml.etree.ElementTree import Element, SubElement, ElementTree

# Load CSV file
csv_file = "waypoints_filtered.csv"  # Replace with your actual file path
df = pd.read_csv(csv_file)

# Create KML root elements for three versions
kml_name = Element("kml", xmlns="http://www.opengis.net/kml/2.2")
document_name = SubElement(kml_name, "Document")

kml_code = Element("kml", xmlns="http://www.opengis.net/kml/2.2")
document_code = SubElement(kml_code, "Document")

kml_code_name = Element("kml", xmlns="http://www.opengis.net/kml/2.2")
document_code_name = SubElement(kml_code_name, "Document")

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

# Convert waypoints for all KML versions
for _, row in df.iterrows():
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

# Save KML files
kml_file_name = "waypoints_name.kml"
tree_name = ElementTree(kml_name)
tree_name.write(kml_file_name, encoding="utf-8", xml_declaration=True)

kml_file_code = "waypoints_code.kml"
tree_code = ElementTree(kml_code)
tree_code.write(kml_file_code, encoding="utf-8", xml_declaration=True)

kml_file_code_name = "waypoints_code_name.kml"
tree_code_name = ElementTree(kml_code_name)
tree_code_name.write(kml_file_code_name, encoding="utf-8", xml_declaration=True)

print(f"Converted CSV to KML with Waypoint Name: {kml_file_name}")
print(f"Converted CSV to KML with Waypoint Code: {kml_file_code}")
print(f"Converted CSV to KML with Code - Name format: {kml_file_code_name}")
