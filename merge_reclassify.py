"""Module that merges all binary country rasters from an input directory and makes one \
mosaic of 1 = Pixel of interest; 0 = land; NoData = sea AND 1 = Pixel of interest \
; NoData = Land and Sea. """

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
		   						used to name output. 
		"""
		self.path_to_countries = path_to_countries
		self.raster_wildcard = raster_wildcard
		self.path_to_save_name = path_to_save_name
		if save_name == None:
			self.save_name = self.raster_wildcard
		else:
			self.save_name = save_name

	def test_function(self):
		"""Function to test module"""
		print("Path to countries: {0}".format(self.path_to_countries))
		print("Raster wildcard: {0}".format(self.raster_wildcard))
		print("Path to save: {0}".format(self.path_to_save_name))
		print("Optional save name: {0}".format(self.save_name))
		print("Done")

test_obj = Merge("test_to_countries", "*_wildcard", "test_to_save")
test_obj.test_function()