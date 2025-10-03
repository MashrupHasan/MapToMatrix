# AOI Matrix Workflow (Google Earth Engine + Colab)

This repository provides a **generalized workflow** to generate an Area of Interest (AOI) raster grid from a shapefile in **Google Earth Engine (GEE)** and convert it into a **labeled matrix text file** with latitude/longitude coordinates using **Google Colab**.

---

## Features
- **Google Earth Engine (JavaScript):**
  - Upload AOI shapefile.
  - Export raster grid with class values:
    - `0` → Outside AOI  
    - `1` → Inside AOI  
    - `2` → Boundary  
  - Save GeoTIFF to Google Drive at chosen resolution.

- **Google Colab (Python):**
  - Convert exported GeoTIFF to `.txt` matrix.
  - Append latitude labels on the right and longitude labels at the bottom.
  - Adjustable label density for wide rasters.

---

## Repository Structure
```
AOI-Matrix-Workflow/
│
├── GEE_AOI_Matrix.js          # GEE export script
├── Colab_Write_Matrix.py      # Colab conversion script
├── example/
│   ├── Example_SHP.zip        # Sample shapefile
│   ├── Example_Matrix.txt     # Example AOI matrix
│   └── Example_Map.jpg        # AOI visualization
├── README.md                  # Documentation
├── LICENSE                    # License (MIT by default)
└── .gitignore                 # Ignore unnecessary files
```

---

## Workflow

### 1. Upload AOI shapefile to GEE
1. Open [Google Earth Engine Code Editor](https://code.earthengine.google.com).
2. Upload your shapefile to **Assets**.
3. Update `AOI_ASSET` path in `GEE_AOI_Matrix.js`.

### 2. Run GEE script
- Open `GEE_AOI_Matrix.js` in the GEE editor.  
- Update parameters:  
  - AOI asset path  
  - Pixel size (default = 3000 m ≈ 3 km)  
  - Export folder  
- Run the script → outputs **GeoTIFF** in Google Drive.

### 3. Run Colab script
- Open [Google Colab](https://colab.research.google.com).  
- Upload `Colab_Write_Matrix.py` or paste code.  
- Update input/output paths.  
- Run the notebook → outputs `.txt` matrix with labeled coordinates.

---

## Example Output

```
00000001111100000000   45.572
00000001111100000000   45.545
00000001111100000000   45.518
... (rows) ...
-122.500   -122.475   -122.450   ...
```

---

## License
MIT License. See [LICENSE](LICENSE).
