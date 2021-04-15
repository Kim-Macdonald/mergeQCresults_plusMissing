# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 23:52:48 2021

@author: KMacDo
"""
#import packages I need
import os
import subprocess
import fnmatch
import pandas as pd
#If you need to change a directory, you can do it this way (but you don't here):
#os.chdir('C:/Users/KMacDo/Desktop/PythonTest')

#save the current working directory (cwd) to a variable to use in everything below. 
#For us, this would be the MiSeqRunID directory for each run - it changes each time we analyze a run, 
#so i want to pull this from where ever I am, 
#so I don't have to enter it each time:
cwdPath = os.getcwd()

#Define variable using last part of directory/path
#This will be used to name your files uniquely:
MiSeqRunID = os.path.basename(os.path.normpath(cwdPath))
#print(MiSeqRunID)  #works

#Define Paths for each file to combine:
file1Path = os.path.dirname('ncov2019-artic-nf-v1.3-output/ncov-tools-v1.5-output/qc_reports/')
#print(file1Path)  #you can use this to test that each step is working. I had to do this for every line.
file2Path = os.path.dirname('ncov2019-artic-nf-v1.3-output/ncov-tools-v1.5-output/qc_reports/')
file3Path = os.path.dirname('ncov2019-artic-nf-v1.3-output/ncov-tools-v1.5-output/lineages/')
file4Path = os.path.dirname('ncov2019-artic-nf-v1.3-output/')



#----------------------------------
#CREATE COMPARISON FILES (Find samples that have a fastq but didn't make it through to conensus):

#Run bash commands to generate the 2 files to compare (FastqList and ConsensusList):
bashCommandTest = "ls"
bashCommand1 = "ls ../../analysis_by_run/" + MiSeqRunID + "/ncov2019-artic-nf-v1.3-output/ncovIllumina_sequenceAnalysis_callConsensusFreebayes/*.consensus.fa* | cut -d/ -f7 | cut -d. -f1 >ConsensusList.txt" 
bashCommand2 = "ls ../../direct_fastq_symlinks_by_run/" + MiSeqRunID + "/*.fastq.gz | cut -d/ -f5 | cut -d. -f1 | cut -d_ -f1 | sort -u | sed '/Undetermined/d' >FastqList.txt"
#print(bashCommandTest)
#print(bashCommand1)
#print(bashCommand2)
#os.system(bashCommand1)
#os.system(bashCommand2)
#os.system is deprecated since python 2.5. Use subprocess instead:
#subprocess.run(bashCommandTest)
subprocess.run(bashCommand1, shell=True, check=True)
subprocess.run(bashCommand2, shell=True, check=True)


#NO LONGER NEEDED since I updated the bash command to produce a list with no duplicates and Undetermined file removed:
#But I'll leave it here in case someone wants to do it on their PC. They'll still need to make the FastqList.txt and ConsensusList.txt first though. 
#df_FastqList1 = pd.read_table("FastqList.txt", header=None)
# #create list of sampleIDs to remove (e.g. Undetermined) from lists:
# RemoveLines = ['Undetermined', 'undetermined']
# #Find those lines in the FastqList.txt file and create a new file without them:
# with open('FastqList.txt') as df_FastqList1, open('FastqList2.txt', 'w') as df_FastqList2:
#     for line in df_FastqList1:
#         if not any(RemoveLines in line for RemoveLines in RemoveLines):
#             df_FastqList2.write(line)

#Read in lists of sampleIDs:
df_FastqList = pd.read_table("FastqList.txt", header=None)
#print(df_FastqList2)
#NO LONGER NEEDED since I updated the bash command to produce a list with no duplicates and Undetermined file removed:
# #Remove duplicate sampleIDs in Fastq List:
# df_FastqList3 = df_FastqList2.drop_duplicates([0], keep='first') 
# #print(df_FastqList3)
# #os.path.join(cwdPath, "FastqList.txt")

df_ConsensusList = pd.read_table("ConsensusList.txt", header=None)
#print(df_ConsensusList)


#Extract sampleIDs that are in FastqList but NOT in ConsensusList:
#df_FastqDiffs = df_ConsensusList[df_ConsensusList.isin(df_FastqList)].dropna(how = 'all')
df_FastqDiffs1 = df_FastqList.loc[~df_FastqList[0].isin(df_ConsensusList[0])].copy()
#print(df_FastqDiffs1)
#df3 = df1.loc[~df1['ID'].isin(df2['ID'])].copy()


#Add column headers to match the other file:
#        ,sample,run_name,num_consensus_snvs,num_consensus_n,num_consensus_iupac,num_variants_snvs,num_variants_indel,num_variants_indel_triplet,mean_sequencing_depth,median_sequencing_depth,qpcr_ct,collection_date,num_weeks,scaled_variants_snvs,genome_completeness,qc_pass_x,lineage_x,watch_mutations,watchlist_id,num_observed_mutations,num_mutations_in_watchlist,proportion_watchlist_mutations_observed,note,pangoLEARN_version,pct_N_bases,pct_covered_bases,longest_no_N_run,num_aligned_reads,qc_pass_y,sample_name
df_FastqDiffs2 = df_FastqDiffs1.reindex(columns=[*df_FastqDiffs1.columns.tolist(),'run_name','num_consensus_snvs','num_consensus_n','num_consensus_iupac','num_variants_snvs','num_variants_indel','num_variants_indel_triplet','mean_sequencing_depth','median_sequencing_depth','qpcr_ct','collection_date','num_weeks','scaled_variants_snvs','genome_completeness','qc_pass_x','lineage_x','watch_mutations','watchlist_id','num_observed_mutations','num_mutations_in_watchlist','proportion_watchlist_mutations_observed','note','pangoLEARN_version','pct_N_bases','pct_covered_bases','longest_no_N_run','num_aligned_reads','qc_pass_y','sample_name'], fill_value=0)
#print(df_FastqDiffs2)
#Rename Column 0 as 'sample'
df_FastqDiffs3 = df_FastqDiffs2.rename(columns={0: "sample"})
#print(df_FastqDiffs3)

#replace 0's in qc_pass_y column with FALSE:
#df_FastqDiffs = pd.df_FastqDiffs3
df_FastqDiffs4 = df_FastqDiffs3[['qc_pass_y']].replace(0,'FALSE')
df_FastqDiffs4b = df_FastqDiffs3[['run_name']].replace(0, MiSeqRunID)
#print(df_FastqDiffs4b) #worked
#check content:
#df_FastqDiffs4.to_csv('df_FastqDiffs4.csv') #has 2 columns, and has a header ('sample')

#merge df_FastqDiffs4 with df_FastqDiffs3
df_FastqDiffs4_merge0 = [df_FastqDiffs3.iloc[:, 0:1], df_FastqDiffs4b.iloc[:, 0:1]]
df_FastqDiffs4_merge1 = pd.concat(df_FastqDiffs4_merge0, axis=1)                      
#print(df_FastqDiffs4_merge1)
df_FastqDiffs4_merge2 = [df_FastqDiffs3.iloc[:, 2:28], df_FastqDiffs4.iloc[:, 0:1]]
df_FastqDiffs4_merge3 = pd.concat(df_FastqDiffs4_merge2, axis=1)                      
#print(df_FastqDiffs4_merge3)
df_FastqDiffs4_merge4 = [df_FastqDiffs4_merge1, df_FastqDiffs4_merge3]
df_FastqDiffs4_merge5 = pd.concat(df_FastqDiffs4_merge4, axis=1)                      
#print(df_FastqDiffs4_merge5)
#df_FastqDiffs4_merge5.to_csv('df_FastqDiffs4_merge5.csv')

#replace 0's in sample_name column with the values in sample column:
df_FastqDiffs5 = df_FastqDiffs3.loc[df_FastqDiffs3["sample_name"] < 1, "sample_name"] = df_FastqDiffs3["sample"]
df_FastqDiffs5 = df_FastqDiffs5.reset_index().rename(columns={'sample': 'sample_name'})
#print(df_FastqDiffs5)
#df.loc[df['A'].isnull(), 'A'] = df['B']
#check content:
#df_FastqDiffs5.to_csv('df_FastqDiffs5.csv') #has a header ('sample'), just doesn't show in preview for whatever reason

#merge df_FastqDiffs5 with df_FastqDiffs4_merge5
df_FastqDiffs3_4_5_merge2 = pd.merge(df_FastqDiffs4_merge5.iloc[:, 0:29], df_FastqDiffs5.iloc[:, 1:2], how='left', left_on='sample', right_on='sample_name')
#print(df_FastqDiffs3_4_5_merge2) 
#check content:
#df_FastqDiffs3_4_5_merge2.to_csv('df_FastqDiffs3_4_5_merge2.csv') #has a header ('sample'), just doesn't show in preview for whatever reason

#Replace the 0's for Ct and Coll Date and everything else, with Nothing, so they don't mess up results/formatting etc.
df_FastqDiffs3_4_5_merge4 = df_FastqDiffs3_4_5_merge2.replace(0,'')
#print(df_FastqDiffs3_4_5_merge4)

#END OF COMPARISON FILES
#--------------------------------------


#-----------------------------
#CREATE MERGED RESULTS TABLE:

#NCOV-TOOLS QC FILE: (store the file contents as dataframe (df)):
for dir_path, dir_names, file_names in os.walk(os.path.join(cwdPath, file1Path)):
    for f in file_names:
        if fnmatch.fnmatch(f, '*_summary_qc.tsv'):
            #print(f)  # worked
            file1 = os.path.join(cwdPath, file1Path, f)
            df_ncovtools = pd.read_table(file1)
            #print(df_ncovtools) #worked
            df_ncovtools0 = df_ncovtools.iloc[:, 0:17]
            df_ncovtools1 = df_ncovtools.iloc[:, 18:19]
            df_ncovtools2a = [df_ncovtools0, df_ncovtools1]
            df_ncovtools2 = pd.concat(df_ncovtools2a, axis=1)
            #print(df_ncovtools2) #works (but has index now)

#VARIANT SUMMARY FILE: (want only ObsMutation, TotalMutations, ProportionMutations from this)
#sort first to match highest number first for each sample
#remove duplicate lines (keep the first occurrence b/c it has the highest mutations)

for dir_path, dir_names, file_names in os.walk(os.path.join(cwdPath, file2Path)):
    for f in file_names:
        if fnmatch.fnmatch(f, '*_ncov_watch_summary.tsv'):
            #print(f)  # worked 
            file2 = os.path.join(cwdPath, file2Path, f)
            df_variantsum = pd.read_table(file2)
            df_variantsum2 = df_variantsum.sort_values('proportion_watchlist_mutations_observed', ascending=False)
            df_variantsum3 = df_variantsum2.drop_duplicates(subset=['sample_id'], keep='first')
            #print(df_variantsum3) #worked 

#MERGE NCOV-TOOLS df WITH VARIANT df: (store merged tables as new dataframe)
df_ncov_variant_merge = pd.merge(df_ncovtools2, df_variantsum3, how='left', left_on='sample', right_on='sample_id')
#print(df_ncov_variant_merge) #works


#LINEAGE FILE
for dir_path, dir_names, file_names in os.walk(os.path.join(cwdPath, file3Path)):
    for f in file_names:
        if fnmatch.fnmatch(f, '*_lineage_report.csv'):
            #print(f)  # worked  
            file3 = os.path.join(cwdPath, file3Path, f)
            df_lineage = pd.read_csv(file3) #, names = ['taxon', 'lineage', 'probability', 'pangoLEARN_version', 'status', 'note'])
            pd.set_option('display.max_columns', None)
            #print(df_lineage)
            #df_lineage_split = pd.DataFrame(df_lineage.str.split('_').tolist(), columns = ['text', 'taxon']) #nope
            df_lineage_split = df_lineage['taxon'].str.replace('Consensus_', '')
            #print(df_lineage_split)
            df_lineage_combo1 =  [df_lineage_split, df_lineage.iloc[:, 1:6]]
            df_lineage_combo2 = pd.concat(df_lineage_combo1, axis=1)
            #axis=1 is to join/concat by putting columns next to each other
            #axis=0 is to concat by putting rows of diff sources on top of each other
            #print(df_lineage_combo2)  #works


#MERGE NCOVTOOLS/VARIANTmerge AND LINEAGE df:
df_ncov_variant_lineage_merge = pd.merge(df_ncov_variant_merge, df_lineage_combo2, how='left', left_on='sample', right_on='taxon')
#print(df_ncov_variant_lineage_merge) #works  


#ARTIC QC FILE:
for dir_path, dir_names, file_names in os.walk(os.path.join(cwdPath, file4Path)):
    for f in file_names:
        if fnmatch.fnmatch(f, '*.qc.csv'):
            #print(f)  # worked 
            file4 = os.path.join(cwdPath, file4Path, f)
            df_artic1 = pd.read_csv(file4)
            df_artic2 = df_artic1.iloc[:, 0:5]
            df_artic3 = df_artic1.iloc[:, 7:8]
            df_artic4 = [df_artic2, df_artic3]
            df_artic = pd.concat(df_artic4, axis=1)
            #print(df_artic) #works


#MERGE NCOV-TOOLS/VARIANT/LINEAGEmerge WITH ARTIC df:
df_ncov_variant_lineage_artic_merge = pd.merge(df_ncov_variant_lineage_merge, df_artic, how='left', left_on='sample', right_on='sample_name')
#print(df_ncov_variant_lineage_artic_merge) #works


#CREATE NEW COLUMN FOR TOTAL MUTATIONS:
df_ncov_variant_lineage_artic_merge["TotalMutations"] = df_ncov_variant_lineage_artic_merge.num_observed_mutations.astype(str).str.cat(df_ncov_variant_lineage_artic_merge.num_mutations_in_watchlist.astype(str), sep="/")
#print(df_ncov_variant_lineage_artic_merge)  #works

#Define variable using last part of directory/path
#This will be used to name your files uniquely:
MiSeqRunID = os.path.basename(os.path.normpath(cwdPath))
#print(MiSeqRunID)  #works
    
#save final1 file as csv (easier to open in Excel than tsv) 
#(this has ALL columns of ALL files, used for testing mostly - not needed):
#df_ncov_variant_lineage_artic_merge.to_csv(MiSeqRunID + '_' + 'ncov_variantsum_lineage_artic_merge_leftJoin.csv')


#BREAK APART MERGED FILE TO JUST KEEP COLUMNS I WANT:
#probably a more efficient way to do this, but I'm a beginner and this works. 
df_ncov1 = df_ncov_variant_lineage_artic_merge.iloc[:, 0:18]
#print(df_ncov1)
df_variant1 = df_ncov_variant_lineage_artic_merge.iloc[:, 19:23]
#print(df_variant1)   
df_variant2 = df_ncov_variant_lineage_artic_merge.iloc[:, 35:36]
#print(df_variant2)
df_lineage1 = df_ncov_variant_lineage_artic_merge.iloc[:, 28:29]
df_lineage2 = df_ncov_variant_lineage_artic_merge.iloc[:, 26:27]
#print(df_lineage1)
#print(df_lineage2)
df_artic5 = df_ncov_variant_lineage_artic_merge.iloc[:, 30:35]
df_artic6 = df_ncov_variant_lineage_artic_merge.iloc[:, 29:30]
#print(df_artic5)
#print(df_artic6)


#CONCATENATE above dfs IN DESIRED ORDER:
#df_ncov_variant_lineage_artic_merge2 = [df_ncov1, df_variant1, df_variant2.TotalMutations.astype(str), df_lineage1, df_lineage2, df_artic5, df_artic6]
#TotalMutations column (e.g. 16/17) opens in excel as date for some, so remove this column (no way to fix here), and just make the column in dashboard instead. 
df_ncov_variant_lineage_artic_merge2 = [df_ncov1, df_variant1, df_lineage1, df_lineage2, df_artic5, df_artic6]
df_ncov_variant_lineage_artic_merge3 = pd.concat(df_ncov_variant_lineage_artic_merge2, axis=1)
#print(df_ncov_variant_lineage_artic_merge3)

#--------------
#END OF MERGED RESULTS TABLE


#-------------------------------
#MERGE THE FINAL ORDERED TABLE WITH MISSING RESULTS (FROM COMPARISON FILES):
#MERGE the mergeQCresults.py result file with the Missing SampleIDs:
#df_ncovtoolsSummary2 = df_ncovtoolsSummary.iloc[:, 1:32]
#print(df_ncovtoolsSummary2)
df_ncovtoolsSummary_plusMissing = df_ncov_variant_lineage_artic_merge3.append(df_FastqDiffs3_4_5_merge4, ignore_index=True)
    


#save final2 file as csv (easier to open in Excel than tsv):
#(this has only the columns I want to link my dashboard to, for various people's purposes)
#df_ncov_variant_lineage_artic_merge3.to_csv(MiSeqRunID + '_' + 'QC_lineage_VoC_OrderedFinal.csv')
df_ncovtoolsSummary_plusMissing.to_csv(MiSeqRunID + '_' + 'MissingPlus_QC_lineage_VoC_OrderedFinal.csv')


#Run Bash Commands to Remove Unnecessary Files (Clean Up): 
bashCommand3 = "rm FastqList.txt; rm ConsensusList.txt" 
#bashCommand4 = ""
subprocess.run(bashCommand3, shell=True, check=True)
#subprocess.run(bashCommand4, shell=True, check=True)


                    