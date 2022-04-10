
#Author: David A. Jensen
#Date Created: 15 Sept 2019
#Date Modified: 18 Jun 2020

#For this script to run, user modification is required. 
#Please add the path to a directory containing your three SAR images on line 16. 
#The output net gradient difference will be deposited in this directory. 

#Load required packages
library(raster)
library(rgdal)
library(ff)
  
#Set directory path where three SAR images are contained. SAR imagery is expected to be in '.tif' format. USER INPUT REQUIRED
dir_path<- 'PASTE PATH HERE'

#Sort paths for individual rasters. 
dir_list<- list.files(dir_path, full.names = TRUE, pattern = '[.]tif$')
r1_path<- paste(dir_list[1])
r2_path<- paste(dir_list[2])
r3_path<- paste(dir_list[3])


#Read in rasters
rast1<- raster(r1_path)
rast2<- raster(r2_path)
rast3<- raster(r3_path)
    
#Resample rast2 and rast3 to match rast1. (This takes a while but is essential for calculating net gradient difference)
rast2<- resample(rast2, rast1)
rast3<- resample(rast3, rast1)
  
#Create Matricies for gradient calculation
m<- matrix(c(-1/2,0,1/2))
m1<- cbind(0,m,0)
m2<- rbind(0,t(m),0)
  
#Prep data for horizontal and vertical field calculation. 
LFI_igrad1<- focal(rast1, m1)
LFI_jgrad1<- focal(rast1, m2)
LFI_igrad2<- focal(rast2, m1)
LFI_jgrad2<- focal(rast2, m2)
LFI_igrad3<- focal(rast3, m1)
LFI_jgrad3<- focal(rast3, m2)
rm(rast1, rast2, rast3) 
rm(m, m1, m2)
  
#Horizontal field calculation
LFI_hori1<- abs(LFI_jgrad1-LFI_jgrad2)
LFI_hori2<- abs(LFI_jgrad1-LFI_jgrad3)
LFI_hori3<- abs(LFI_jgrad2-LFI_jgrad3)
rm(LFI_jgrad1, LFI_jgrad2, LFI_jgrad3)
LFI_hori_field<- LFI_hori1 + LFI_hori2 + LFI_hori3
rm(LFI_hori1, LFI_hori2, LFI_hori3)
  
#Vertical field calculation
LFI_vert1<- abs(LFI_igrad1-LFI_igrad2)
LFI_vert2<- abs(LFI_igrad1-LFI_igrad3)
LFI_vert3<- abs(LFI_igrad2-LFI_igrad3)
rm(LFI_igrad1, LFI_igrad2, LFI_igrad3)
LFI_vert_field<- LFI_vert1 + LFI_vert2 + LFI_vert3
rm(LFI_vert1, LFI_vert2, LFI_vert3)
  
  
#Magnitude calculation
LFI_mag<- sqrt((LFI_vert_field^2)+(LFI_hori_field^2))
rm(LFI_vert_field, LFI_hori_field)
  
mag_out<- paste(dir_path, 'gradient.tif', sep = "")
writeRaster(LFI_mag, filename = mag_out, format = 'GTiff', overwrite = TRUE)
rm(LFI_mag)


