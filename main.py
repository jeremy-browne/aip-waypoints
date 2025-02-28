import pdfplumber
import pandas as pd

# Path to your PDF file
pdf_path = "ERSA.book2.pdf"

waypoints = []

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

# Save to CSV
csv_path = "waypoints_filtered.csv"
df.to_csv(csv_path, index=False)

print(f"Extracted {len(waypoints)} waypoints and saved to {csv_path}")
