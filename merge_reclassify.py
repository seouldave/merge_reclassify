"""Module that merges all binary country rasters from an input directory and makes one \
mosaic of 1 = Pixel of interest; 0 = land; NoData = sea AND 1 = Pixel of interest \
; NoData = Land and Sea. 
This module will only work with OSGEO folder containing scripts at C:/OSGeo4W64/bin/
"""
import os
import subprocess
import numpy as np
from osgeo import gdal
import time

class Merge:
	"""Class to which merges country rasters from a specified directory and saves \
	the output to a specified directory.

	Functions:
	##########################################TO DO##################################################################################
	"""
	def __init__(self, path_to_countries, raster_wildcard, path_to_save_name, save_name=None):
		"""Function to initialise objects of Merge class
		
		   Arguments:
		   path_to_countries -> path to directory holding country folders
		   raster_wildcard -> String to specify last few characters of file names \
		   						to merge (ie. "_2001.tif")
		   path_to_save_name -> Directory in which to save output.
		   save_name (optional) -> output save file, if not added, wildcard will be \
		   						used to name output. This name should not include file-suffixes \
		   						as they will be added to the output name. (E.g.: wildcard = "2001.tif" + save_name = "2001" \
		   						-> outfile = "2001.tif" )
		"""
		self.path_to_countries = path_to_countries
		self.raster_wildcard = raster_wildcard
		self.path_to_save_name = path_to_save_name
		if save_name == None:
			self.save_name = self.raster_wildcard[:-3]
		else:
			self.save_name = save_name
		self.iso_codes = ['AFG', 'ALA', 'ALB', 'DZA', 'ASM', 'AND', 'AGO', 'AIA',\
		 'ATA', 'ATG', 'ARG', 'ARM', 'ABW', 'AUS', 'AUT', 'AZE', 'BHS', 'BHR', \
		 'BGD', 'BRB', 'BLR', 'BEL', 'BLZ', 'BEN', 'BMU', 'BTN', 'BOL', 'BES', \
		 'BIH', 'BWA', 'BVT', 'BRA', 'IOT', 'BRN', 'BGR', 'BFA', 'BDI', 'CPV', \
		 'KHM', 'CMR', 'CAN', 'CYM', 'CAF', 'TCD', 'CHL', 'CHN', 'COL', 'COM', \
		 'COG', 'COD', 'COK', 'CRI', 'CIV', 'HRV', 'CUB', 'CUW', 'CYP', 'CZE', \
		 'DNK', 'DJI', 'DMA', 'DOM', 'ECU', 'EGY', 'SLV', 'GNQ', 'ERI', 'EST', \
		 'ETH', 'FLK', 'FRO', 'FJI', 'FIN', 'FRA', 'GUF', 'PYF', 'ATF', 'GAB', \
		 'GMB', 'GEO', 'DEU', 'GHA', 'GIB', 'GRC', 'GRL', 'GRD', 'GLP', 'GUM', \
		 'GTM', 'GGY', 'GIN', 'GNB', 'GUY', 'HTI', 'HMD', 'VAT', 'HND', 'HKG', \
		 'HUN', 'ISL', 'IND', 'IDN', 'IRN', 'IRQ', 'IRL', 'IMN', 'ISR', 'ITA', \
		 'JAM', 'JPN', 'JEY', 'JOR', 'KAZ', 'KEN', 'KIR', 'PRK', 'KOR', 'KWT', \
		 'KGZ', 'LAO', 'LVA', 'LBN', 'LSO', 'LBR', 'LBY', 'LIE', 'LTU', 'LUX', \
		 'MAC', 'MKD', 'MDG', 'MWI', 'MYS', 'MDV', 'MLI', 'MLT', 'MHL', 'MTQ', \
		 'MRT', 'MUS', 'MYT', 'MEX', 'FSM', 'MDA', 'MCO', 'MNG', 'MNE', 'MSR', \
		 'MAR', 'MOZ', 'MMR', 'NAM', 'NRU', 'NPL', 'NLD', 'NCL', 'NZL', 'NIC', \
		 'NER', 'NGA', 'NIU', 'NFK', 'MNP', 'NOR', 'OMN', 'PAK', 'PLW', 'PSE', \
		 'PAN', 'PNG', 'PRY', 'PER', 'PHL', 'PCN', 'POL', 'PRT', 'PRI', 'QAT', \
		 'REU', 'ROU', 'RUS', 'RWA', 'BLM', 'SHN', 'KNA', 'LCA', 'MAF', 'SPM', \
		 'VCT', 'WSM', 'SMR', 'STP', 'SAU', 'SEN', 'SRB', 'SYC', 'SLE', 'SGP', \
		 'SXM', 'SVK', 'SVN', 'SLB', 'SOM', 'ZAF', 'SGS', 'SSD', 'ESP', 'LKA', \
		 'SDN', 'SUR', 'SJM', 'SWZ', 'SWE', 'CHE', 'SYR', 'TWN', 'TJK', 'TZA', \
		 'THA', 'TLS', 'TGO', 'TKL', 'TON', 'TTO', 'TUN', 'TUR', 'TKM', 'TCA', \
		 'TUV', 'UGA', 'UKR', 'ARE', 'GBR', 'UMI', 'USA', 'URY', 'UZB', 'VUT', \
		 'VEN', 'VNM', 'VGB', 'VIR', 'WLF', 'ESH', 'YEM', 'ZMB', 'ZWE', 'KOS', 'SPR']

	def list_tiffs(self):
		"""Function to list tiffs for every country in the chosen directory \
		which match the input wildcard.

		Arguments:
		None

		Returns:
		List of absolute filenames."""
		tiffs = [] #list to return
		iso_check = [] #append iso's to list to check all iso's accounted for
		#List the folders in the path
		list_of_folders = os.listdir(self.path_to_countries)
		for folder in list_of_folders:
			iso_check.append(folder[-3:])
			#List the tiffs in the folders and if wildcard match, append to list.
			for tif in os.listdir(os.path.join(self.path_to_countries, folder)):
				if tif.endswith(self.raster_wildcard):
					tiffs.append(os.path.join(self.path_to_countries, folder, tif))
		iso_differences = set(self.iso_codes) - set(iso_check) #Find the difference between input folder and all iso's
		print("There are {0} countries in input and there should be {1}. Missing countries: {2}\
			".format(len(iso_check), len(self.iso_codes), iso_differences))
		return tiffs

	def add_tiffs_to_file(self, tiffs):
		"""Function to write list of tiffs to merge to a txt file.
		
		Arguments:
		tiff -> List of paths to tiffs to merge

		Returns:
		list_path -> Path to txt file
		"""
		file = open(os.path.join(self.path_to_save_name, "{0}_list.txt".format(self.save_name)), 'w')
		for tiff in tiffs:
			file.write(tiff + "\n")
		file.close()

	def create_vrt(self):
		"""Function that calls GDALBuildVRT and creates a VRT of the merged tiffs from the input txt files\
		saved in the output folder

		Arguments:
		None

		Returns:
		None
		"""
		list_file = os.path.join(self.path_to_save_name, "{0}_list.txt".format(self.save_name)) #file holding list of tiffs
		vrt_name = os.path.join(self.path_to_save_name, "{0}.vrt".format(self.save_name)) #Output vrt name
		####NOTE****The below path should be changed dependent on PC running program
		command = "C:/OSGeo4W64/bin/gdalbuildvrt.exe -te -180.001249265 -71.999582844 \
		180.001249295 84.0020831987 -tr 0.00083333333 0.00083333333 -input_file_list {0} {1}".format(list_file, vrt_name) #Command to call gdal
		subprocess.call(command, shell=True)
		os.remove(list_file)


	def multiply_by_L0(self, tiff_path):
		"""
		Function to multiply global raster by L0 (0=land; ND=sea) to ensure missed \
		land pixels are filled in to match mastergrid

		Arguments:
		tiff_path -> Path to merged file
		""" 
		mastergrid_L0 = r'E:\Merge_script\Merge_UGM\mask_0_ND\ccid100m_0_ND_resamp.tif'
		out_tif = os.path.join(self.path_to_save_name, "{0}_1_0_ND.tif".format(self.save_name))
		command = 'C:/Python27/2713/scripts/gdal_calc.py -A {0} -B {1} --outfile={2}\
		--calc="B*(B==0) + A*(A==1)" --NoDataValue=255 --co NUM_THREADS=3\
		 --co COMPRESS=LZW --co PREDICTOR=2 --type=Byte'.format(tiff_path, mastergrid_L0, out_tif)
		##TRY 2 WAYS TO MULTIPLY 
		#command = 'C:/Python27/2713/scripts/gdal_calc.py -A {0} -B {1} --outfile={2}\
		#--calc="B*(A==255) + A*(A==1) + A*(A==0)" --NoDataValue=255 --co NUM_THREADS=3\
		# --co COMPRESS=LZW --co PREDICTOR=2 --type=Byte'.format(tiff_path, mastergrid_L0, out_tif)
		subprocess.call(command, shell=True)

######################THIS FUNCTION NOT NEEDED IF GDAL_CALC WORKS WITH VRT########################
	def convert_vrt_to_tiff(self):
		"""Function to convert VRT file to GeoTiff using GDAL
		
		Arguments:
		None

		Returns:
		None
		"""
		vrt_name = os.path.join(self.path_to_save_name, "{0}.vrt".format(self.save_name))
		tiff_name = os.path.join(self.path_to_save_name, "{0}_1_0_ND_INTERIM.tif".format(self.save_name)) #Interim file still needs to be multiplied by L0 to clip coastline
		command = "C:/OSGeo4W64/bin/gdal_translate.exe -ot Byte -tr 0.00083333333 0.00083333333 -co NUM_THREADS=3 \
		-co COMPRESS=LZW -co PREDICTOR=2 -a_nodata 255 -stats {0} {1}".format(vrt_name, tiff_name)
		subprocess.call(command, shell=True)
		os.remove(vrt_name)

	def reclassify_as_binary(self):
		"""Function to reclassify <1_0_ND> raster as <1_ND>

		Arguments:
		None

		Returns:
		None
		"""
		tiff_1_0_nd = os.path.join(self.path_to_save_name, "{0}_1_0_ND.tif".format(self.save_name))
		tiff_1_nd = os.path.join(self.path_to_save_name, "{0}_1_ND.tif".format(self.save_name))
		##Below command will only work where GDAL bindings are in this path
		command = 'C:/Python27/2713/scripts/gdal_calc.py -A {0} --outfile={1} \
		--calc="A*(A==1) + 255*(A==0)" --co NUM_THREADS=3 --co COMPRESS=LZW --co PREDICTOR=2'.format(tiff_1_0_nd, tiff_1_nd)
		subprocess.call(command, shell=True)
		
	def test_function(self):
		"""Function to test module"""
		#############TEST1##############################################
		#print("Path to countries: {0}".format(self.path_to_countries))
		#print("Raster wildcard: {0}".format(self.raster_wildcard))
		#print("Path to save: {0}".format(self.path_to_save_name))
		#print("Optional save name: {0}".format(self.save_name))
		#############TEST2##########################################
		#print(self.list_tiffs())
		self.add_tiffs_to_file(self.list_tiffs())
		print("Done List")
		#############TEST3####################################
		self.create_vrt()
		print("Vrt Done")
		print("Converting VRT to tiff")
		self.convert_vrt_to_tiff() ##Try to do GDAL_calc multiply_by_L0 first
		print("Converted VRT to tiff - Multiply by mastergrid")
		self.multiply_by_L0(os.path.join(self.path_to_save_name, "{0}_1_0_ND_INTERIM.tif".format(self.save_name)))
		print("1_0 Tiff made - Reclassifying")
		self.reclassify_as_binary()
		print("Binary made")


test_obj = Merge(r'E:\Merge_script\Merge_UGM\datain\WP515640_Global\Raster\Covariates\UGM\2000-2012', "2001.tif", \
	r'E:\Merge_script\Merge_UGM\dataout', "merge_2001")
test_obj.test_function()

for year in range(2001, 2012, 1):
	start = time.time()
	test_obj = Merge(r'E:\Merge_script\Merge_UGM\datain\WP515640_Global\Raster\Covariates\UGM\2000-2012', "{0}.tif".format(year), \
		r'E:\Merge_script\Merge_UGM\dataout', "merge_{0}".format(year))
	test_obj.test_function()
	end = time.time()
	print(end - start)
########################TO DO 19/04 ----> try multiplying VRT with Mastergrid and then extract binary. ############################
######################## Try multi ALSO Check NUM_Threads tag#############################
# start = time.time()
# for year in range(2001, 2004, 1):
# 	start_in_loop = time.time()
# 	first_epoc = Merge(r'Z:\WP515640_Global\Raster\Covariates\UGM\2000-2012', \
# 		"{0}.tif".format(year), r'E:\Merge_script\Merge_UGM\dataout', "Urban_{0}".format(year))
# 	first_epoc.test_function()
# 	end_in_loop = time.time()
# 	print ("{0} took {1} minutes".format(year, (end_in_loop - start_in_loop)/60))
# 	del start_in_loop, first_epoc, end_in_loop

# end = time.time()
# print("Processing took {0} minutes".format((end-start)/60))

