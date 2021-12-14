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

src = rasterio.open("data/RGB-byte-masked-mola-dem.tif")
plt.imshow(src.read(1), cmap="Reds_r")
plt.show()

colormap = make_ramp(['#000000', '#000000', '#FFFFFF'] )

src = rasterio.open("data/RGB-byte-masked-mola-dem.tif")
plt.imshow(src.read(1), cmap=colormap)
plt.show()

