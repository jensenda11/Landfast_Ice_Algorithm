
# Detecting Landfast Sea Ice Using Sentinel-1 SAR Imagery

This repository provides a semi-automated method for identifying *landfast sea ice* using Synthetic Aperture Radar (SAR) imagery. Designed primarily for **Sentinel-1 Extra Wide (EW)** images sourced from the **Alaska Satellite Facility (ASF)**, this workflow uses a gradient-based approach to detect areas of **coastal ice that exhibit no motion** over a ~20-day window.

![gif_final](https://github.com/user-attachments/assets/74ce4433-8885-414d-944e-de6230352f10)


## Example Use Case

The python_script_LFI.py script has been applied above to three Sentinel-1 EW images from **March–April 2025** over **Bylot Sound, western Northern Greenland**. The output `gradient.tif` helps users identify where ice remained fixed throughout the 20-day span — allowing for delineation of the landfast ice seaward edge in GIS.  

---

## What's Inside

| File | Description |
|------|-------------|
| `S1_EW_batchprocessing.xml` | SNAP graph for batch pre-processing of Sentinel-1 EW imagery |
| `python_script_LFI.py` | Python script to identify stable coastal sea ice using net gradient difference |

---

## How It Works

1. **Download SAR Imagery**  
   Download three Sentinel-1 EW scenes as zipped `.zip` archives from the [Alaska Satellite Facility Data Portal](https://search.asf.alaska.edu/). These files do **not** need to be unzipped to be loaded into SNAP.

2. **Pre-process in SNAP**  
   Load the `.xml` graph (`S1_EW_batchprocessing.xml`) into ESA's **Sentinel Application Platform (SNAP)**. Use it to batch-process the three zipped scenes. The output should be GeoTIFFs (`.tif`) stored in the same directory as the Python script.

3. **Run the Analysis**  
   Open a terminal in the working directory and run:

        python python_script_LFI.py

   The script calculates **net gradient differences** between the images to flag areas with consistent pixel intensities — indicative of landfast sea ice.

4. **Get Your Output**  
   A new file, `gradient.tif`, will appear in the working directory. It highlights stable ice features along coastlines.

---

## System Requirements

| Spec | Recommended |
|------|-------------|
| RAM  | 32 GB (16 GB minimum) |
| OS   | Linux, macOS, or Windows with Python 3 |
| SNAP | ESA SNAP Toolbox (tested with v9 or later) |
| Python | `numpy`, `gdal`, `rasterio`, `matplotlib` |

> If memory crashes occur, mask the `.tif` images to a smaller **Region of Interest (ROI)** before running the script.

---

## Works Cited

### Foundational Methodology

- Mahoney, A., Eicken, H., Graves, A., Shapiro, L., & Cotter, P. (2004, September). Landfast sea ice extent and variability in the Alaskan Arctic derived from SAR imagery. In IGARSS 2004. 2004 IEEE International Geoscience and Remote Sensing Symposium (Vol. 3, pp. 2146-2149). IEEE.

### Studies Using This Methodology
- Jensen, D., Mahoney, A., & Resler, L. (2020). The annual cycle of landfast ice in the eastern Bering Sea. Cold Regions Science and Technology, 174, 103059.

- Jensen, D. A., Nandan, V., Mahoney, A. R., Yackel, J. J., & Resler, L. M. (2023). Landfast sea ice break out patterns in the northern Bering Sea observed from C-band Synthetic Aperture Radar. International Journal of Applied Earth Observation and Geoinformation, 117, 103183.
  
- Mahoney, A. R., Eicken, H., Gaylord, A. G., & Gens, R. (2014). Landfast sea ice extent in the Chukchi and Beaufort Seas: The annual cycle and decadal variability. Cold Regions Science and Technology, 103, 41-56.

- Meyer, F. J., Mahoney, A. R., Eicken, H., Denny, C. L., Druckenmiller, H. C., & Hendricks, S. (2011). Mapping arctic landfast ice extent using L-band synthetic aperture radar interferometry. Remote Sensing of Environment, 115(12), 3029-3043.





