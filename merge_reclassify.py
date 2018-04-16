"""Module that merges all binary country rasters from an input directory and makes one \
mosaic of 1 = Pixel of interest; 0 = land; NoData = sea AND 1 = Pixel of interest \
; NoData = Land and Sea. 
This module will only work with OSGEO folder containing scripts at C:/OSGeo4W64/bin/
"""
import os
import subprocess


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

	def list_tiffs(self):
		"""Function to list tiffs for every country in the chosen directory \
		which match the input wildcard.

		Arguments:
		None

		Returns:
		List of absolute filenames."""
		tiffs = [] #list to return
		#List the folders in the path
		list_of_folders = os.listdir(self.path_to_countries)
		for folder in list_of_folders:
			#List the tiffs in the folders and if wildcard match, append to list.
			for tif in os.listdir(os.path.join(self.path_to_countries, folder)):
				if tif.endswith(self.raster_wildcard):
					tiffs.append(os.path.join(self.path_to_countries, folder, tif))
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
		command = "C:/OSGeo4W64/bin/gdalbuildvrt.exe -input_file_list {0} {1}".format(list_file, vrt_name) #Command to call gdal
		subprocess.call(command, shell=True)
		os.remove(list_file)
		
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
		print("Done")
		#############TEST3####################################
		self.create_vrt()
		print("Done")


#test_obj = Merge(r'E:\Merge_script\Merge_UGM\datain\WP515640_Global\Raster\Covariates\UGM\2000-2012', "2001.tif", \
#	r'E:\Merge_script\Merge_UGM\dataout', "merge_2001")
#test_obj.test_function()

for year in range(2001, 2012, 1):
	test_obj = Merge(r'E:\Merge_script\Merge_UGM\datain\WP515640_Global\Raster\Covariates\UGM\2000-2012', "{0}.tif".format(year), \
		r'E:\Merge_script\Merge_UGM\dataout', "merge_{0}".format(year))
	test_obj.test_function()
