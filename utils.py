import os
import fiona
import rasterio
import rasterio.mask
import urllib.request
from pathlib import Path
from colour import Color
from geocube.api.core import make_geocube
from matplotlib.colors import LinearSegmentedColormap


def get_dem_data(path: Path, local_file_name: Path):
    if not os.path.exists(local_file_name):
        urllib.request.urlretrieve(path, local_file_name)


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
    if not os.path.exists(path_to_raster):
        with rasterio.open(path_to_raster, "w", **meta) as dest:
            dest.write(img)
        
    
def rasterize_vector(path_to_vector: Path, out_file_name: Path, feature_name: str, resolution: tuple = (-0.0001, 0.0001)):    
    out_grid = make_geocube(vector_data=path_to_vector, resolution=resolution)
    out_grid[feature_name].rio.to_raster(out_file_name)


def make_ramp( ramp_colors ):    
    color_ramp = LinearSegmentedColormap.from_list( 'my_list', [ Color( c1 ).rgb for c1 in ramp_colors ] )
    return color_ramp
