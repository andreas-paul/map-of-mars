
import os
import fiona
import rasterio
import rasterio.mask
import urllib.request
from pathlib import Path


def get_dem_data(path: Path, local_file_name: Path):
    if not os.path.exists(local_file_name):
        print("Downloading file")
        urllib.request.urlretrieve(path, local_file_name)
        print("Finished downloading file")
    else:
        print("File exists.")


def load_shapefile(path_to_shp: Path):
    with fiona.open(path_to_shp, "r") as shapefile:
        shapes = [feature["geometry"] for feature in shapefile]
    return shapes


def crop_raster(path_to_raster: Path, shapes: list):
    with rasterio.open(path_to_raster) as src:
        out_img, out_transform = rasterio.mask.mask(src, shapes, crop=True)
        out_meta = src.meta
        out_meta.update({"driver": "GTiff", 
                        "height": out_img.shape[1], 
                        "width": out_img.shape[2],
                        "transform": out_transform})
    return out_img, out_transform, out_meta


def save_raster(path_to_raster: Path, meta, img):
    with rasterio.open(path_to_raster, "w", **meta) as dest:
        dest.write(img)
        
    