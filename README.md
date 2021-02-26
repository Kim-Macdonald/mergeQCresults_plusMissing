# mergeQCresults_plusMissing
Combines results from artic, ncovtools, pangolin, and ncov-watch into 1 table, and adds any samples removed (no consensus made) to the end (.append)

Use this one script instead of merge_ncov_qc_results and MergeQCResultsWithRemovedSamples together. 

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

