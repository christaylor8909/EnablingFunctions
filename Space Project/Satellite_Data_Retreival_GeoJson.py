# Satellite Data Modeling Master Script
# Project: SPACE PROJECT
# Purpose: Download, visualize, and model satellite data (e.g., vegetation cover classification)

# === INSTALL DEPENDENCIES ===
# pip install sentinelsat rasterio geopandas scikit-learn matplotlib

import os
import numpy as np
import matplotlib.pyplot as plt
import rasterio
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from sklearn.ensemble import RandomForestClassifier
from datetime import date

# === CONFIGURATION ===
SENTINEL_USER = os.getenv('SENTINEL_USER', 'your_username')  # Use env variable or fallback
SENTINEL_PASSWORD = os.getenv('SENTINEL_PASSWORD', 'your_password')
GEOJSON_PATH = 'map.geojson'  # path to your AOI file
SAVE_DIR = 'downloads'  # directory to save satellite imagery
START_DATE = '20240101'
END_DATE = '20240531'

# === SETUP API CONNECTION ===
if not os.path.exists(GEOJSON_PATH):
    raise FileNotFoundError(f"AOI file not found: {GEOJSON_PATH}. Please provide a valid GeoJSON file.")

try:
    api = SentinelAPI(SENTINEL_USER, SENTINEL_PASSWORD, 'https://scihub.copernicus.eu/dhus')
    footprint = geojson_to_wkt(read_geojson(GEOJSON_PATH))
except Exception as e:
    raise RuntimeError(f"API connection or AOI loading failed: {e}")

print("🔍 Searching for Sentinel-2 products...")
products = api.query(
    footprint,
    date=(START_DATE, END_DATE),
    platformname='Sentinel-2',
    processinglevel='Level-1C',
    cloudcoverpercentage=(0, 30)
)

# === DOWNLOAD THE FIRST PRODUCT ===
if not products:
    raise Exception("No products found for the given parameters.")

product_id = list(products.keys())[0]
print(f"⬇️ Downloading product: {product_id}")
api.download(product_id, directory_path=SAVE_DIR)

# === READ DOWNLOADED IMAGE ===
tif_path = None
for root, dirs, files in os.walk(SAVE_DIR):
    for file in files:
        if file.endswith('.tif'):
            tif_path = os.path.join(root, file)
            break
    if tif_path:
        break

if tif_path is None:
    raise FileNotFoundError("No .tif file found in the downloaded product.")

print(f"🖼️ Opening image: {tif_path}")
with rasterio.open(tif_path) as src:
    # Sentinel-2: Band 4=Red, 3=Green, 2=Blue
    band_count = src.count
    if band_count >= 4:
        bands = [src.read(b) for b in [4, 3, 2]]
    else:
        bands = [src.read(i) for i in range(1, min(4, band_count+1))]
    rgb_stack = np.stack(bands, axis=-1)

# === DISPLAY RGB IMAGE ===
rgb_display = rgb_stack.astype(np.float32)
if rgb_display.max() > 0:
    rgb_display /= rgb_display.max()  # Normalize to [0, 1] for display

plt.imshow(rgb_display)
plt.title('RGB Composite (Bands 4-3-2)')
plt.axis('off')
plt.show()

# === MODELING (DUMMY EXAMPLE) ===
n_samples = min(1000, rgb_stack.shape[0] * rgb_stack.shape[1])
X = rgb_stack.reshape(-1, 3)[:n_samples]
y = np.random.randint(0, 2, n_samples)  # 0 = Urban, 1 = Vegetation

clf = RandomForestClassifier()
clf.fit(X, y)

# === PREDICTION ===
predictions = clf.predict(rgb_stack.reshape(-1, 3))
pred_image = predictions.reshape(rgb_stack.shape[:2])

# === DISPLAY PREDICTION ===
plt.imshow(pred_image, cmap='Greens')
plt.title('Vegetation Prediction')
plt.axis('off')
plt.show()

print("✅ Modeling complete. You can now refine labels and export results.")# === DISPLAY RGB IMAGE ===
rgb_display = rgb_stack.astype(np.float32)
if rgb_display.max() > 0:
    rgb_display /= rgb_display.max()  # Normalize to [0, 1] for display

plt.imshow(rgb_display)
plt.title('RGB Composite (Bands 4-3-2)')
plt.axis('off')
plt.show()