# mergeQCresults_plusMissing
Combines results from artic, ncovtools, pangolin, and ncov-watch into 1 table, and adds any samples removed (no consensus made) to the end (.append)

Use this one script instead of merge_ncov_qc_results and MergeQCResultsWithRemovedSamples together. 

Merges (left Join) the result fields from the following artic & ncov-tools qc summaries, pangolin, and ncov-watch into 1 csv file. Does the same for the missing samples (in fastq files but not consensus files) and appends them to the bottom. 

*_summary_qc.tsv (ncov-tools qc summary)

*_ncov_watch_summary.tsv (VoC mutations summary) (in qc_reports directory, not the ncov_watch directory)

*_lineage_report.csv (pangolin lineage report)

*.qc.csv (artic qc summary)

![image](https://user-images.githubusercontent.com/72042148/109368160-0b294100-784d-11eb-98ec-7ec25b0cfcc3.png)


<b>To Run:</b>

1st set up environment with pandas (done on sabin already)

cd to directory with result files

    (for BCCDC: cd projects/covid-19_production/analysis_by_run/[MiSeqRunID] )

    conda activate pandas

    python3 path/to/script/mergeQCresults_plusMissing.py
    
    conda deactivate

To run/loop through all MiSeqRunID directories:

    conda activate pandas

    (For BC:) cd projects/covid-19_production/analysis_by_run/

    for dir in /projects/covid-19_production/analysis_by_run/*/; do cd $dir; python3 /path/to/script/mergeQCresults_PlusMissing.py;  cd ..; done

