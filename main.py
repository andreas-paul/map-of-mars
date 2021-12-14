#%%
import rasterio
from pathlib import Path
import matplotlib.pyplot as plt
from blend_modes import blending_functions
from utils import get_dem_data, load_shapefile, crop_raster, save_raster, make_ramp



dem_path: Path = Path("https://planetarymaps.usgs.gov/mosaic/Mars_MGS_MOLA_DEM_mosaic_global_463m.tif")
cropped_raster_path: Path = Path("data/RGB-byte-masked-mola-dem.tif")
output_raster_path: Path = Path("data/mola_dem.tif")
shp_path: Path = Path("data/extent.shp")


get_dem_data(dem_path, output_raster_path)
shapes = load_shapefile(shp_path)
img, transform, meta = crop_raster(output_raster_path, shapes)
save_raster(cropped_raster_path, meta, img)

cm_reds = make_ramp(['#bd4628', '#c15033', '#c45a3f', '#c8644b', '#cc6e56', '#cf7962', 
                    '#d3836e', '#d78d7a', '#db9785', '#dea291', '#e2ac9d', '#e6b6a8', 
                    '#e9c0b4', '#edcac0', '#f1d5cc', '#f4dfd7', '#f8e9e3', '#fcf3ef', '#fffdfa'])

cm_grays = make_ramp(['#000000', '#000000', '#FFFFFF'] )

src = rasterio.open("data/RGB-byte-masked-mola-dem.tif")
plt.imshow(src.read(1), cmap=cm_reds)
plt.axis('off')
plt.Axes(fig, [0,0,1,1]) # Remove whitespace

src = rasterio.open("data/RGB-byte-masked-mola-dem.tif")
plt.imshow(src.read(1), cmap=cm_grays)
plt.axis('off')
plt.Axes(fig, [0,0,1,1])
