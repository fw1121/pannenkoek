# **Pannenkoek** 
v0.1.6  
  
Subset a Qiime biom file to LEfSe-ready format

A tool to create LEfSe-ready tables from your main OTU table in QIIME. LEfSe is a great tool for microbial diversity analysis, but there are many repetitive steps if you want to analyze multiple time points between two groups. Pannenkoek was made to simplify that process. You can input your main OTU biom file, Treatment group column name and Timepoint column name and it will do the hard work summarizing the table, removing the unused metadata fields, and create multiple tables based on time.

## Get Started

```

pip install https://github.com/twbattaglia/pannenkoek/zipball/master

```



## Dependencies  
R has to be initialized from the command line first to install packages. So just run R. (seriously)  
```


# 1) Initialize R in terminal by running the command 'R'
$ R

# 2) Run the command below to install the necessary packages. You may get an error stating, 'packages ‘splines’, ‘stats4’ are not available (as a binary package for R version 3.1.3)' but this can be ignored.
$ install.packages(c('splines','stats4','survival','mvtnorm','modeltools','coin','MASS'), repos = "http://cran.us.r-project.org")


  
```
Start a new terminal session to exit out of R



### Running the Command  

```
# Example Command
pannenkoek.py -i INPUT_BIOM.biom -o OUTPUT_FOLDER/ -m MAPPING_FILE.txt -level 7
-class colTreatment -split colDay -compare CON,Group1 -a 0.01

```


```

usage: pannenkoek.py [-h] [-v] [-i INPUT] [-o OUTPUT] [-m MAPPING]
                     [-s SUBJECTID] [-c CLASSID] [-sc SUBCLASSID] [-l LEVEL]
                     [-spl SPLITBY] [-comp COMPARE] [-t] [-nl]
                     [-a ANOVA_CUTOFF] [-e LDA_CUTOFF] [-strict STRICTNESS]

Summarize taxa and subset by time.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -i INPUT, -input INPUT
                        Location of the Biom/OTU file to subset and use for
                        LEfSe analysis.(Must be .biom format)
  -o OUTPUT, -output OUTPUT
                        Directory to place all the files.
  -m MAPPING, -map MAPPING
                        Location of the mapping file associated with Biom
                        File.
  -s SUBJECTID, -subject SUBJECTID
                        By Default = #SampleID. Only change if your SampleID
                        header differs.
  -c CLASSID, -class CLASSID
                        This will be the column within your mapping file that
                        has the data which differentiates between groups. This
                        is typically the Treatment column of your data. When
                        formatting the data for LEfSe analysis, this will be
                        the column used as a class. When choosing particular
                        comparisons with "-compare" this classID columns is
                        where it looks for the variables. Choose wisely.
  -sc SUBCLASSID, -subclass SUBCLASSID
                        This will be used in similar way to the classID, but
                        is typically reserved for another level of
                        comparisons. See the use of subclasses with LEfSe
                        data. "http://genomebiology.com/2011/12/6/r60"
  -l LEVEL, -level LEVEL
                        level to use for summarize_taxa.py.
  -spl SPLITBY, -split SPLITBY
                        This is the column name of the variable to use for
                        splitting the table. The table is split over a
                        variable to reduce the amount of work to create a new
                        formatted lefse table for each timepoint of an
                        experiment. This is one of the core features of
                        pannenkoek. Choose the column which will create the
                        analysis you want.
  -comp COMPARE, -compare COMPARE
                        This option lets you select a comparison between
                        variables found in your provded classID column. For
                        example if you had 3 different experimental groups and
                        you wanted to only see the comparisons between Control
                        and Group2 over time you can input, "Control,Group2"
                        in this field and it will subset and only include the
                        sampleIDs that are from either group. This option is
                        very useful for experiments with multiple groups.
  -t, --notranspose     If you do not want the data tranposed, add this option
                        to the command. Default = False
  -nl, --nolefse        If you only want subsetted tables and no formatted or
                        lefse-run data, add this option to the command.
                        Default = False
  -a ANOVA_CUTOFF, -anovap ANOVA_CUTOFF
                        Change the cutoff for significance between OTUs.
                        Default is 0.05.
  -e LDA_CUTOFF, -effect_size LDA_CUTOFF
                        Change the cutoff for effect size. Default is 2.
  -strict STRICTNESS, -strictness STRICTNESS
                        Change the strictness of the comparisons. Can be
                        changed to less strict(1). Default is 0 (more-strict).
```
