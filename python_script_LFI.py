# Landfast ice net gradient difference algorithmic processing. 

# Author: David A. Jensen
# Date Created: 15 Sept 2019
# Date Modified: 26 May 2025 

# Please place this python script in a folder with three concurrent SAR images acquired within a 20 day window. The images must be in .tif format. If using Sentinel-1 EW imagery acquired from the Alaska Satellite Facility's Data Portal, use S1_EW_batchprocessing.xml included with this repo to process downloaded data into geotiff format, setting the output folder as the same folder this script is located.

# Import native python modules


import subprocess
import sys
import os

def install_and_import(package, import_name=None):
    """Check if a package is installed, if not, install it, then import it."""
    import_name = import_name or package
    try:
        return __import__(import_name)
    except ImportError:
        print(f"Package '{package}' not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return __import__(import_name)

# Check/install needed packages
rasterio = install_and_import("rasterio")
np = install_and_import("numpy")
scipy = install_and_import("scipy")

from rasterio.enums import Resampling
from rasterio.windows import Window
from rasterio.plot import reshape_as_raster, reshape_as_image
from scipy.ndimage import convolve
from rasterio import warp

def get_script_path():
    """Return directory where this script is located."""
    return os.path.dirname(os.path.realpath(__file__))

def main():
    dir_path = get_script_path()
    print(f"\033[38;2;0;255;255mUsing directory:\033[0m {dir_path}\n")
    
    # Delete any preexisting gradient.tif file(s)
    for file in os.listdir(dir_path):
        if file.lower().endswith('.tif') and 'gradient' in file.lower():
            gradient_path = os.path.join(dir_path, file)
            print(f"\033[38;2;255;0;0mDeleting existing gradient file:\033[0m {gradient_path}")
            os.remove(gradient_path)

    if not os.path.isdir(dir_path):
        raise FileNotFoundError(f"Directory does not exist: {dir_path}")

    tif_files = [f for f in os.listdir(dir_path) if f.lower().endswith('.tif')]
    if len(tif_files) < 3:
        raise RuntimeError("Fewer than three '.tif' files found in the directory.")

    # Full paths
    r1_path = os.path.join(dir_path, tif_files[0])
    r2_path = os.path.join(dir_path, tif_files[1])
    r3_path = os.path.join(dir_path, tif_files[2])

    print(f"\033[38;2;0;255;255mReading rasters:\033[0m\n{r1_path}\n{r2_path}\n{r3_path}\n")

    # Read rasters
    with rasterio.open(r1_path) as src1:
        rast1_data = src1.read(1)
        rast1_meta = src1.meta.copy()

    with rasterio.open(r2_path) as src2:
        rast2_data = src2.read(1)
        # Resample rast2 to rast1
        rast2_data = rasterio.warp.reproject(
            source=rast2_data,
            destination=np.empty_like(rast1_data),
            src_transform=src2.transform,
            src_crs=src2.crs,
            dst_transform=src1.transform,
            dst_crs=src1.crs,
            resampling=Resampling.bilinear
        )[0]

    print("Resampling 50% Complete.")

    with rasterio.open(r3_path) as src3:
        rast3_data = src3.read(1)
        # Resample rast3 to rast1
        rast3_data = rasterio.warp.reproject(
            source=rast3_data,
            destination=np.empty_like(rast1_data),
            src_transform=src3.transform,
            src_crs=src3.crs,
            dst_transform=src1.transform,
            dst_crs=src1.crs,
            resampling=Resampling.bilinear
        )[0]

    print("Resampling 100% Complete.")

    # Create gradient kernels
    m = np.array([-0.5, 0, 0.5])
    m1 = np.array([[0, -0.5, 0],
                   [0,    0, 0],
                   [0,  0.5, 0]])
    m2 = np.array([[0, 0, 0],
                   [-0.5, 0, 0.5],
                   [0, 0, 0]])

    print("\033[38;2;0;255;255mPreparing data for horizontal and vertical gradient calculation...\033[0m")

    # Horizontal gradients (convolve rows)
    LFI_igrad1 = convolve(rast1_data, m1, mode='nearest')
    LFI_jgrad1 = convolve(rast1_data, m2, mode='nearest')
    LFI_igrad2 = convolve(rast2_data, m1, mode='nearest')
    LFI_jgrad2 = convolve(rast2_data, m2, mode='nearest')
    LFI_igrad3 = convolve(rast3_data, m1, mode='nearest')
    LFI_jgrad3 = convolve(rast3_data, m2, mode='nearest')

    print("\033[38;2;0;255;255mPreparation complete.\033[0m")

    print("\033[38;2;0;255;255mConducting horizontal field calculation...\033[0m")
    LFI_hori1 = np.abs(LFI_jgrad1 - LFI_jgrad2)
    LFI_hori2 = np.abs(LFI_jgrad1 - LFI_jgrad3)
    LFI_hori3 = np.abs(LFI_jgrad2 - LFI_jgrad3)
    LFI_hori_field = LFI_hori1 + LFI_hori2 + LFI_hori3
    print("\033[38;2;0;255;255mHorizontal field calculation complete.\033[0m")

    print("\033[38;2;0;255;255mConducting vertical field calculation...\033[0m")
    LFI_vert1 = np.abs(LFI_igrad1 - LFI_igrad2)
    LFI_vert2 = np.abs(LFI_igrad1 - LFI_igrad3)
    LFI_vert3 = np.abs(LFI_igrad2 - LFI_igrad3)
    LFI_vert_field = LFI_vert1 + LFI_vert2 + LFI_vert3
    print("\033[38;2;0;255;255mVertical field calculation complete.\033[0m")

    print("\033[38;2;0;255;255mPerforming magnitude calculation...\033[0m")
    LFI_mag = np.sqrt(LFI_vert_field**2 + LFI_hori_field**2)

    mag_out = os.path.join(dir_path, "gradient.tif")
    print(f"\033[38;2;0;255;255mAlgorithm complete. Writing out magnitude GeoTIFF...\033[0m\nWriting output raster to: {mag_out}")

    rast1_meta.update(dtype=rasterio.float32, count=1, compress='lzw')

    with rasterio.open(mag_out, 'w', **rast1_meta) as dst:
        dst.write(LFI_mag.astype(rasterio.float32), 1)

if __name__ == "__main__":
    main()

