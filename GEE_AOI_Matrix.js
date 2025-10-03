// =============================================
// Google Earth Engine – Generalized AOI Matrix Export
// =============================================

// ---- User parameters ----
var SCALE_M = 3000; // pixel size in meters (e.g., 3 km)
var EXPORT_DESC = 'AOI_Matrix_' + (SCALE_M/1000) + 'km';
var EXPORT_FOLDER = 'AOI_Matrix_Outputs'; // Google Drive folder
var AOI_ASSET = 'users/your_username/Your_AOI_SHP'; // <-- Replace with your uploaded shapefile asset path

// ---- Load AOI ----
var aoi = ee.FeatureCollection(AOI_ASSET);
var aoiGeom = aoi.geometry();
Map.centerObject(aoi, 6);

// ---- Create inside=1, boundary=2 ----
var inside = ee.Image.constant(1).clip(aoiGeom).rename('zone');

var boundary = ee.Image(0).toByte().paint({
  featureCollection: aoi,
  color: 2,
  width: 1 // pixel-based width; final appearance depends on export scale
}).rename('zone');

// ---- Combine (0 outside, 1 inside, 2 boundary) ----
var base = ee.Image(0).rename('zone');
var raster = base
  .where(inside.eq(1), 1)
  .where(boundary.eq(2), 2)
  // Slight buffer to keep edge pixels during coarse resampling
  .clip(aoiGeom.buffer(50));

// ---- Visualization for quick QA ----
Map.addLayer(raster, {min: 0, max: 2, palette: ['white','green','red']}, 'AOI Matrix');

// ---- Export to Google Drive (GeoTIFF) ----
Export.image.toDrive({
  image: raster,
  description: EXPORT_DESC,
  folder: EXPORT_FOLDER,
  fileNamePrefix: EXPORT_DESC,
  region: aoiGeom.bounds(),
  scale: SCALE_M,
  crs: 'EPSG:4326', // ensures lat/lon degrees for easier downstream labeling
  maxPixels: 1e13
});
