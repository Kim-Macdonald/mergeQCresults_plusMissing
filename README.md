# mergeQCresults_plusMissing

## Description
Combines results from artic, ncovtools, pangolin, and ncov-watch into 1 table, and adds any samples removed (no consensus made) to the end (.append)

Use this one script instead of merge_ncov_qc_results and MergeQCResultsWithRemovedSamples together. 

Merges (left Join) the result fields from the following artic & ncov-tools qc summaries, pangolin, and ncov-watch into 1 csv file. Does the same for the missing samples (in fastq files but not consensus files) and appends them to the bottom. 

    *_summary_qc.tsv (ncov-tools qc summary)

    *_ncov_watch_summary.tsv (VoC mutations summary) (in qc_reports directory, not the ncov_watch directory)

    *_lineage_report.csv (pangolin lineage report)

    *.qc.csv (artic qc summary)


## Example of output (click to open in new window and enlarge):

![Github_AssumedDirectoryStructure_paint4](https://user-images.githubusercontent.com/72042148/109568432-c6471980-7a9b-11eb-928f-19019ad8ef31.png)



## Assumed Directory Structure:

![Github_AssumedDirectoryStructure_paint3](https://user-images.githubusercontent.com/72042148/109567783-c1ce3100-7a9a-11eb-9190-918b0373c893.png)




# To Run:

1st set up environment with pandas, and any other dependencies (done on sabin already)

      conda create -n pandas pandas 

cd to directory with result files

    (for BC: cd path/to/AnalysisDirectory/[MiSeqRunID] )

    conda activate pandas

    python3 path/to/script/mergeQCresults_plusMissing.py
    
    conda deactivate

# To run/loop through all MiSeqRunID directories:

    conda activate pandas

    (For BC:) cd path/to/AnalysisDirectory/

    for dir in /path/to/AnalysisDirectory/*/; do cd $dir; python3 /path/to/script/mergeQCresults_PlusMissing.py;  cd ..; done
    
    conda deactivate

