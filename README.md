# **AIP Waypoints Extractor**

This tool extracts **VFR waypoints** from an **AIP (Aeronautical Information Publication) PDF**, **generates separate CSV files per Australian State**, and also **creates three KML files** per state.

## **Overview**
Many official AIP documents provide waypoints in **PDF format**, which is difficult to work with programmatically. This script automates the process of:

1. **Extracting, cleaning, and structuring** waypoint data into a **machine-readable format**.  
2. **Grouping** waypoints by state and saving them into **CSV files**.  
3. **Generating KML** versions for each state (labels by Name, Code, and Code-Name).

## **Features**
✔ **Extracts** waypoint name, state, code, latitude, and longitude from a PDF  
✔ **Groups** data by state into separate CSV files  
✔ **Generates** three KML files per state for easy viewing in Google Earth  
✔ **Filters out** unnecessary headers and page numbers  

## **Installation**
1. Ensure you have **Python 3.8+** installed.
2. Install dependencies:
   ```bash
   pip install pdfplumber pandas

## **Usage**
1. **Obtain the Waypoints from AIP ERSA VFR - GEN** (from official sources). An example of the expected data is included as a PDF in this repo.
2. **Ensure the file contains VFR waypoints** in the expected format. Use only the VFR Waypoints page of AIP, don't try and parse any other section of the document.
3. **Run the script**:
   ```bash
   python main.py
   ```
4. The extracted waypoints will be saved to `waypoints_filtered.csv`.

## **Example Output (CSV Format)**
| Waypoint          | State | Code | Latitude  | Longitude  |
|------------------|------|------|-----------|------------|
| ABEAM KUNOTH    | NT   | KNO  | 233230S   | 1333300E   |
| ADELAIDE CBD    | SA   | ACTY | 345600S   | 1383600E   |
| ALTONA SOUTH    | VIC  | ALTS | 375244S   | 1444836E   |

## **Notes**
- The script assumes the **standard AIP format** for VFR waypoints.
- If the output is missing waypoints, the formatting in the PDF may vary slightly.
- Modify the filtering conditions in `extract-and-convert.py` if necessary.
- Extracted data is available in the waypoints_by_state directory, as both csv and kml files.

## **Contributing**
Feel free to open issues or submit pull requests if you have improvements!

## **License**
MIT License

