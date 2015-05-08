Pannenkoek
=======================

A tool to create lefse ready tables from your main OTU table in QIIME. LEfSe is a great tool for microbial diversity analysis, but there are many repetitive steps if you want to analyze multiple time points between two groups. Pannenkoek was made to simplify that process. You can input your main OTU biom file, Treatment group column name and Timepoint column name and it will do the hard work summarizing the table, removing the unused metadata fields, and create multiple tables based on time.


# v0.1.6
- needed a new shebang header. 

# v0.1.5
- bug fix for the bug that was introduced trying to fix a bug fix

# v0.1.4
- bug fix for pip installation

# v0.1.3
- bug fix for version option

# v0.1.2
- fixed lefse output to contain the name of the factor to split by. It will allow better header names for pretty_lefse.py

# v0.1.1
*Added the option to no-transpose the data (--notranspose)
-lefse is not run when data is chosen to be transposed. This is due to the way the table must be formatted.

*Also fixed a typo with subclassID argument

*Added some error handing so make errors much more clearer.

# v0.1.0
First release of something that can be described as a python package
