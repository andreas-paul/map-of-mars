
import os
import fiona
import rasterio
import rasterio.mask
import urllib.request
from geocube.api.core import make_geocube
from pathlib import Path


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


def custom_color_map():
    """
    Example usage of returns: show(src,cmap=cmap,norm=norm,interpolation='bilinear')
    """
    levels = [0, 0.01, 0.02, 0.04, 0.8, 1, 2, 4, 7, 17, 70, 500]
    clrs = ['#E3E8E81A','#3DFDFF8C', '#3CFAFF', '#6A95FF', '#E61AFE8C', '#FF04FF', '#f4ded9', '#f4dbaa', '#eda14f', '#e87511', '#b55400', '#633b11']    
    cmap, norm = colors.from_levels_and_colors(levels, clrs, extend='max')
    
    return cmap, norm