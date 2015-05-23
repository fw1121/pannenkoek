#!/usr/bin/env python
#-----------------------
# @ Thomas W. Battaglia
# @ tb1280@nyu.edu
#-----------------------
__author__ = "Thomas W. Battaglia"
__credits__ = ["Thomas W. Battaglia"]
__license__ = "BSD"
__maintainer__ = "Thomas W. Battaglia"
__email__ = "tb1280@nyu.edu"

import os
import pandas as pd


def add_meta(input, output, mapping, add, splitID):

	## Imports ---------------------------------------
	# Import results from merged humann2 as dataframe
	path_abun_df = pd.read_table(path_abun, header = 0)

	# Import mapping file as dataframe
	mapping_df = pd.read_table(mapping)


	## Adding the chosen metadata ------------------------------------------------
	# Gather a list of rows from mapping file that match sampleID's in pathway abundance.
	sampleID = list(path_abun_df.columns[1:])
	mappingID = list(mapping_df.iloc[:,0])
	matched_meta = [ mappingID.index(x) if x in mappingID else None for x in sampleID]
	path_abun_df_t = path_abun_df.T


	# Loop through each instance of the chosen metadata variables.
	metadata = []
	for i,name in enumerate(add):
		classID_list = list(mapping_df[name][matched_meta])
		classID_list.insert(0, str(name))
		classID_row = pd.Series(classID_list, index = path_abun_df.columns)
		metadata.append(classID_row)

	# Concatenate all chosen variables.
	metadata_cat = pd.concat(metadata, axis = 1)

	# Merge the variables and dataset together
	path_abun_meta = pd.concat([metadata_cat, path_abun_df_t], axis = 1).T


	# Hot fix. This probably can be done better
	if splitID!="NA":

		# Gather a list of variables matching the splitID column based on the rows found above
		splitID_list = list(mapping_df[splitID][matched_meta])

		# Split the data based on the splitby value if chosen
		split_by_values = set(mapping_df[splitID])

		# Iterate through all factors of chosen splitby value
		outlist = []
		for split in split_by_values:
			indices = [i for i, x in enumerate(splitID_list) if x == split]
			indices.insert(0, 0)
			table = path_abun_meta.iloc[:,indices]
			outlist.append(table)
		return(outlist)

	else:
		return(path_abun_meta)
