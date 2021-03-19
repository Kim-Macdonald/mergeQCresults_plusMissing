# mergeQCresults_plusMissing

## Description
Replaces the need to use merge_ncov_qc_results and MergeQCResultsWithRemovedSamples separately. Use this instead. 

Combines results from artic, ncovtools, pangolin, and ncov-watch into 1 table, and adds any samples removed (no consensus made) to the end (.append)


Merges (left Join) the result fields from the following artic & ncov-tools qc summaries, pangolin, and ncov-watch into 1 csv file. Does the same for the missing samples (in fastq files but not consensus files) and appends them to the bottom. 

    *_summary_qc.tsv (ncov-tools qc summary)

    *_ncov_watch_summary.tsv (VoC mutations summary) (in qc_reports directory, not the ncov_watch directory)

    *_lineage_report.csv (pangolin lineage report)

    *.qc.csv (artic qc summary)

We use the following pipelines to produce the result files shown above: BCCDC-PHL/ncov2019-artic-nf (forked from connor-lab/ncov2019-artic-nf) and BCCDC-PHL/ncov-tools (forked from jts/ncov-tools)


## Example of output (click to open in new window and enlarge):

![GithubMergedTablePic4_paint](https://user-images.githubusercontent.com/72042148/109568525-e676d880-7a9b-11eb-8a7c-c830b917622b.png)

Note: sometimes the the 2nd last column (qc_pass_y) of the output file has values of 1 and 0 instead of TRUE and FALSE. They should still sort the same, but if you need the TRUE/FALSE values and not 1/0, then you may want to edit the script. I haven't looked into the cause yet. 

# 

## Assumed Directory Structure:

![Github_AssumedDirectoryStructure_paint4](https://user-images.githubusercontent.com/72042148/109568432-c6471980-7a9b-11eb-928f-19019ad8ef31.png)




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

