#!/usr/bin/env python
#-----------------------
# @ Thomas W. Battaglia
# @ tb1280@nyu.edu
#-----------------------
import subprocess
import os
import argparse
import pandas as pd



# Declare Arguments
def getArgs(argv=None):
	parser = argparse.ArgumentParser(description='Summarize taxa and subset by time.', add_help=True)
	parser.add_argument('-v', '--version', action='version', version='0.1.6')

	parser.add_argument('-i', '-input', action="store", dest="input", help='Location of the Biom/OTU file to subset and use for LEfSe analysis.(Must be .biom format)')
	parser.add_argument('-o', '-output', action="store", dest="output", help='Directory to place all the files.')
	parser.add_argument('-m', '-map', action="store", dest="mapping", help='Location of the mapping file associated with Biom File.')

	parser.add_argument('-s', '-subject', action="store", dest="subjectID", default = '#SampleID', help='By Default = #SampleID. Only change if your SampleID header differs.')

	parser.add_argument('-c', '-class', action="store", dest="classID", help='This will be the column within your mapping file that has the data which differentiates between groups. This is typically the Treatment column of your data. When formatting the data for LEfSe analysis, this will be the column used as a class. When choosing particular comparisons with "-compare" this classID columns is where it looks for the variables. Choose wisely.')

	parser.add_argument('-sc', '-subclass', action="store", dest="subclassID", default = "NA", help='This will be used in similar way to the classID, but is typically reserved for another level of comparisons. See the use of subclasses with LEfSe data. "http://genomebiology.com/2011/12/6/r60"')

	parser.add_argument('-l', '-level', action="store", dest="level", default = 6, help='level to use for summarize_taxa.py.')

	parser.add_argument('-spl','-split', action="store", dest="splitby", help='This is the column name of the variable to use for splitting the table. The table is split over a variable to reduce the amount of work to create a new formatted lefse table for each timepoint of an experiment. This is one of the core features of pannenkoek. Choose the column which will create the analysis you want.')

	parser.add_argument('-comp', '-compare', action="store", dest="compare", default = '', help='This option lets you select a comparison between variables found in your provded classID column. For example if you had 3 different experimental groups and you wanted to only see the comparisons between Control and Group2 over time you can input, "Control,Group2" in this field and it will subset and only include the sampleIDs that are from either group. This option is very useful for experiments with multiple groups.')

	parser.add_argument('-t', '--notranspose', dest="transpose", action="store_true", default = False, help='If you do not want the data tranposed, add this option to the command. Default = False')



	# Running Lefse Arguments
	parser.add_argument('-nl', '--nolefse', dest="nolefse", action="store_true", default = False, help='If you only want subsetted tables and no formatted or lefse-run data, add this option to the command. Default = False')

	parser.add_argument('-a', '-anovap', action="store", dest="anova_cutoff", default = 0.05, help='Change the cutoff for significance between OTUs. Default is 0.05.')

	parser.add_argument('-e','-effect_size', action="store", dest="lda_cutoff", default = 2, help='Change the cutoff for effect size. Default is 2.')

	parser.add_argument('-strict', '-strictness', action="store", dest="strictness", default = 0, help='Change the strictness of the comparisons. Can be changed to less strict(1). Default is 0 (more-strict).')

	return parser.parse_args(argv)


# Main function
def convert2Lefse(input, output, map, level, subjectID, classID, subclassID, compare, split_by, nolefse, anova_cutoff, lda_cutoff, strictness, notranspose):


	## Error handing
	# If values inputed for options does not exist, error out and explain error.
	# Level
	# Class
	# Spliting factor
	# Comparison doesn't exist

	# Tranposing the data stops lefse from running
	if notranspose:
		nolefse = True
		print "Data will not be tranposed, but LEfSe will not run."


	## Create Directories
	# Create Main Output Directory
	print ("Creating Directories")

	# Main output Directory
	if not os.path.exists(os.path.dirname(output)):
		os.makedirs(os.path.dirname(output))

	# Create folder for summarize_taxa output
	sum_taxa_output = output + "/sum_taxa_L" + str(level) + '/'
	if not os.path.exists(sum_taxa_output):
		os.makedirs(sum_taxa_output)

	if not nolefse:

		# Create folder for Lefse output
		lefse_output = output + "/lefse_output/"
		if not os.path.exists(lefse_output):
			os.makedirs(lefse_output)

		# Create folder for formatting lefse output
		format_lefse_out = lefse_output + "format_lefse/"
		if not os.path.exists(format_lefse_out):
			os.makedirs(format_lefse_out)

		# Create folder for formatting lefse output
		run_lefse_out = lefse_output + "run_lefse/"
		if not os.path.exists(run_lefse_out):
			os.makedirs(run_lefse_out)


	# Run Sumarize taxa (Update to have qiime functions)
	print ("Summarizing Taxa Abundances.")
	subprocess.call(['summarize_taxa.py', '-i', input, '-o', sum_taxa_output, '-m', map, '-L', level, "-d |"])

	# Retrieve the file location from summarize_taxa output
	sumtaxa_file_name = map.replace('.txt', '_L' + str(level) + '.txt')
	sumtaxa_fileloc = sum_taxa_output + os.path.basename(sumtaxa_file_name)

	# Import tables into pandas
	sum_taxa = pd.read_table(sumtaxa_fileloc)
	mapdf = pd.read_table(map)

	# Fix whitespace in header issue
	#print sum_taxa.columns

	## Choose which columns to keep and reorder.
	# If subclass does not exist, dont add it to the tokeep column numbers
	if subclassID == "NA":
		subjectID_pos = sum_taxa.columns.get_loc(subjectID)
		classID_pos = sum_taxa.columns.get_loc(classID)
		bacteria_pos = range((len(mapdf.columns)),len(sum_taxa.columns))
		to_keep = [subjectID_pos,classID_pos] + bacteria_pos
	else:
		subjectID_pos = sum_taxa.columns.get_loc(subjectID)
		classID_pos = sum_taxa.columns.get_loc(classID)
		subclassID_pos = sum_taxa.columns.get_loc(subclassID)
		bacteria_pos = range((len(mapdf.columns)),len(sum_taxa.columns))
		to_keep = [subjectID_pos,classID_pos,subclassID_pos] + bacteria_pos



	## Process comparisons
	compare_list = compare.split(',')

	# If split is NA, just create subsetted OTU Tables
	#if()

	## Process splitting factors
	print ("Splitting data by " + str(split_by))
	split_by_values = set(sum_taxa[split_by])


	# Loop through the chosen split column. Typically time.
	for split in split_by_values:

		# If there is no comparison to be made, include all variable in the classID column.
		if len(compare_list)==1:

			if notranspose:
				# Table = Time, Columns to keep, tranposed
				table = sum_taxa.loc[sum_taxa[str(split_by)] == split].iloc[:,to_keep]
				table_out = sum_taxa_output + str(split) + '_input.txt'
				table.to_csv(table_out, sep = '\t', header = True, index = False)
			else:
				table = sum_taxa.loc[sum_taxa[str(split_by)] == split].iloc[:,to_keep].transpose()
				table_out = sum_taxa_output + str(split) + '_input.txt'
				table.to_csv(table_out, sep = '\t', header = False, index = True)


		# If theres something in the list, proceed to subsetting by comparisons
		elif len(compare_list)>1:

			# Check no tranpose parameter
			if notranspose:
				table = sum_taxa.loc[sum_taxa[classID].isin(compare_list)].loc[sum_taxa[split_by] == split].iloc[:,to_keep]
				table_out = sum_taxa_output + str(split) + '_' + compare.replace(',','_') + '_input.txt'
				table.to_csv(table_out, sep = '\t', header = True, index = False)
			else:
				# Sort by comparisons, then time, then remove all unecassary metadata then tranpose.
				table = sum_taxa.loc[sum_taxa[classID].isin(compare_list)].loc[sum_taxa[split_by] == split].iloc[:,to_keep].transpose()
				table_out = sum_taxa_output + str(split) + '_' + compare.replace(',','_') + '_input.txt'
				table.to_csv(table_out, sep = '\t', header = False, index = True)
		else:
			print "I dont know what you did, but you somehow broke it."



		# Run lefse when nolefse is false
		if not nolefse:

			# format lefse output file location
			format_file_out = format_lefse_out + os.path.basename(table_out).replace('_input.txt', '_format.txt')
			print("Formatting data for LEfSe.")

			# Run formatting script. Take into account for a lack of subclassID
			if subclassID == "NA":
				subprocess.call(['pannenkoek/lefse/format_input.py', table_out, format_file_out, '-u 1', '-c 2', '-o 1000000'])
			else:
				subprocess.call(['pannenkoek/lefse/format_input.py', table_out, format_file_out, '-u 1', '-c 2', '-s 3', '-o 1000000'])


			# run lefse output file location
			run_file_out = run_lefse_out + os.path.basename(format_file_out).replace('_format.txt', '.txt')

			# Run lefse analysis
			print("Running LEfSe analysis.")
			subprocess.call(['pannenkoek/lefse/run_lefse.py', format_file_out, run_file_out, '-a', str(anova_cutoff), '-l', str(lda_cutoff), '-y', str(strictness)])

	print ("Finished.")




# Initialize Main Function
if __name__ == "__main__":

	# Initalize arguments
	argvals = None
	args = getArgs(argvals)

	# Run!
	convert2Lefse(args.input, args.output, args.mapping, str(args.level), str(args.subjectID), str(args.classID), str(args.subclassID), str(args.compare), str(args.splitby), args.nolefse, float(args.anova_cutoff), float(args.lda_cutoff), int(args.strictness), args.transpose)
