# **AIP Waypoints Extractor**

This tool extracts **VFR waypoints** from an **AIP (Aeronautical Information Publication) PDF** and converts them into structured **CSV format**.

## **Overview**
Many official AIP documents provide waypoints in **PDF format**, which is difficult to work with programmatically. This script automates the process of **extracting, cleaning, and structuring** waypoint data from the PDF into a **machine-readable format**.

## **Features**
✔ Extracts **waypoint name, state, code, latitude, and longitude**  
✔ Filters out **unnecessary headers and page numbers**  
✔ Outputs **clean CSV data** for easy use in other applications  

## **Installation**
Ensure you have **Python 3.8+** installed, then install dependencies:
```bash
pip install pdfplumber pandas
```

## **Usage**
1. **Obtain the AIP waypoints PDF** (from official sources).
2. **Ensure the file contains VFR waypoints** in the expected format.
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
- Modify the filtering conditions in `main.py` if necessary.

## **Contributing**
Feel free to open issues or submit pull requests if you have improvements!

## **License**
MIT License

