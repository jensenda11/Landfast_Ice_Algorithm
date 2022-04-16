# Landfast_Ice_Algorithm
R Script that processes Synthetic Aperture Radar satellite imagery to facilitate the detection of landfast sea ice

This script is used to calculate net-gradient difference from three consecutive Synthetic Aperture Radar images for the 
detection of landfast sea ice. Landfast ice in script output appears as coast-continuous regions of low net gradient difference, indicating regions of coastal sea ice that have remained stationary throughout the duration of the consecutive imagery.  For best results, please ensure that the three images overlap in spatial extent,
and were aquired within an approximately 20 day window. For more information on the method informing this script, see Mahoney et al. 2004, and for an example where this exact script was applied, see Jensen et al. 2020 (Citations below)

Mahoney, A., Eicken, H., Graves, A., Shapiro, L., Cotter, P., 2004 September. Landfast sea 
ice extent and variability in the Alaskan Arctic derived from SAR imagery. In IGARSS 

Jensen, D., Mahoney, A., Resler, L. (2020). The annual cycle of landfast ice in
the eastern Bering Sea. Cold Regions Science and technology, 174, 103059
  
