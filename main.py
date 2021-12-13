
from pathlib import Path
from utils import get_dem_data, load_shapefile, crop_raster, save_raster


dem_path: Path = Path("https://planetarymaps.usgs.gov/mosaic/Mars_MGS_MOLA_DEM_mosaic_global_463m.tif")
raster_path: Path = Path("data/mola_dem.tif")
shp_path: Path = Path("data/extent.shp")
cropped_raster_path: Path = Path("data/RGB-byte-masked-mola-dem.tif")


def main():
    pass



if __name__ == "__main__":
    get_dem_data(dem_path, raster_path)
    shapes = load_shapefile(shp_path)
    img, transform, meta = crop_raster(raster_path, shapes)
    save_raster(cropped_raster_path, meta, img)



