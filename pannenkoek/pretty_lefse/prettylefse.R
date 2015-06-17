#################################################################
# pretty_lefse
# 4/2/15
# NYUMC Blaser Lab

# Thomas W. Battaglia
# thomas.battaglia@nyumc.org

### Summary
### Method

# version 0.2
###################################################################


## load required libraries
if (!require("reshape")) {
  install.packages("reshape", repos="http://cran.rstudio.com/") 
}
if (!require("argparse")) {
  install.packages("argparse", repos="http://cran.rstudio.com/") 
}
if (!require("gtools")) {
  install.packages("gtools", repos="http://cran.rstudio.com/") 
}
suppressPackageStartupMessages(library(reshape))
suppressPackageStartupMessages(library(argparse))
suppressPackageStartupMessages(library(gtools))


## Get Command Line Arguments
# create parser object
parser <- ArgumentParser()

# specify desired input options
parser$add_argument("-i", "--input", 
                    nargs = 1, 
                    help = "Folder or file in which the LEfSe results are stored. The program will recognize if there are one or more files that need to be processed")

parser$add_argument("-o", "--output", 
                    nargs = 1, 
                    help = "Folder or file in which the results (table) are to be stored. A folder with each timepoint's filtered table will be created in the same directory chosen.")


parser$add_argument("-c", "--control", 
                    nargs = 1, 
                    help = "The name of the group which is considered to be control. This allows the program to convert the control group to a negative fold change.")


# Apply command line options
args <- parser$parse_args()


# Useful for debugging
print(paste("Input folder selected:", args$input))
print(paste("Output folder selected:", args$output))
print(paste("Control group name:", args$control))


## Run Pretty Lefse Function
# Test Files
args$input = "/Users/Tom/GoogleDrive/Research/Bioinformatics/anjej_lefse/5.3_genderOTUs/female_con_stat/lefse_output/run_lefse"
args$output = "/Users/Tom/GoogleDrive/Research/Bioinformatics/anjej_lefse/5.3_genderOTUs/female_con_stat/lefse_output/pretty_lefse"
args$control = "control_no"


# Import the directory of files
input_files_full <- list.files(args$input, full.names = T)

# Gather file names (.lefse_res|.txt) and remove extention.
input_files_names <- list.files(args$input, full.names = F)

# Remove extentions from files.
input_files_names <- unlist(lapply(input_files_names, function(x) unlist(strsplit(x, split = ".", fixed = T))[1]))


# Stop if nothing is in the input folder
if (!file.exists(args$input)) {
  stop(paste("No files were found in the entered directory!"))
}

# Import each result(file) into a list
ls_files <- lapply(input_files_full, function(x) read.delim(x, header = T))
names(ls_files) <- input_files_names


# Apply Filtering Function
filter_tables <- function(dataset){
  col <- c("Feature", "Log_Class_Avg", "Class", "Effect_Size", "p_value")
  colnames(dataset) <- col
  dataset_sorted <- subset(dataset, Class!= "")
  return(dataset_sorted)
}
ls_files_filtered <- lapply(ls_files, function(x) filter_tables(x)) 


# Write results to output directory
output_dir <- paste(args$output, "/", sep = "")
dir.create(output_dir)
for(i in 1:length(ls_files_filtered)){
  write.table(x = ls_files_filtered[[i]], 
              file = paste(output_dir, paste(names(ls_files_filtered[i]), "txt", sep = "."), 
                           sep = ""), 
              row.names = F, 
              quote = F, 
              sep = "\t")
}


# Check to make sure how many factors are present.
for (i in 1:length(ls_files_filtered)){
  factorNum = length(levels(factor(ls_files_filtered[[i]]$Class)))
  if (factorNum > 2) {
    stop(paste("Too many factors. Cannot combine properly (yet). Stopping now."))
  }
}


# Relevel
for(i in 1:length(ls_files_filtered)){
  ls_files_filtered[[i]]$Class <- relevel(ls_files_filtered[[i]]$Class, ref = as.character(args$control))
}


# Sort the table based on effect size.
sort_table <- function(dataset){
  
  # Relevel the factors to take into account the chosen group
  if(length(levels(factor(dataset$Class)))<=1){
    dataset_sorted <- dataset[ ,c("Feature", "Effect_Size")]    
  }
  
  else{
    dataset$Class <- relevel(dataset$Class, ref = args$control)
    
    # If the group is considered control, change LDA effect size to negative.
    for (i in 1:dim(dataset)[1]){
      
      # Change Control to Negative
      if(dataset$Class[i] == as.character(args$control)){
          dataset$Effect_Size[i] <- (dataset$Effect_Size[i] * -1)
      }
      
    }
    # Subset table to Feature and Effect Size
    dataset_sorted <- dataset[ ,c("Feature", "Effect_Size")]
  }
  return(dataset_sorted)
}

# Apply Function to each item in the dataset
ls_files_sorted <- lapply(ls_files_filtered, function(x) sort_table(x))


# Change "Effect_Size" Name to the list name.
for (i in 1:length(ls_files_sorted)){
  colnames(ls_files_sorted[[i]])[2] <- names(ls_files_sorted)[[i]] 
}

# Merge together
results <- merge_recurse(ls_files_sorted)

# Sort by feature names
results_sorted <- results[order(results$Feature), ]

# Remove K__Bacteria
results_sorted$Feature <- gsub(pattern = "k__Bacteria.", replacement = "", x = results_sorted$Feature, fixed = T)

# Change '.' to '|'
results_sorted$Feature <- gsub(pattern = ".", replacement = "|", x = results_sorted$Feature, fixed = T)

# Change NA's
results_sorted[is.na(results_sorted)] <- "-"


# Write results to disk
write.table(x = results_sorted, 
            file = paste(args$output, "Combined_output.txt", 
                         sep = "/"), 
            row.names = F, 
            sep = "\t",
            quote = F)

message("Process Completed!")





