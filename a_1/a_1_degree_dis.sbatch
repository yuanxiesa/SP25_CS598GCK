#!/bin/bash
#Sample Batch Job Script

#SBATCH --time=12:00:00			   # Job run time (hh:mm:ss)
#SBATCH --mail-user="fu5@illinois.edu"   # Email address to alert when job starts/finishes
#SBATCH --job-name=fu5_freq_list   # Name of job
#SBATCH --account=25sp-cs598gck-eng          # Account
#SBATCH --partition=eng-instruction       # Parititon
#SBATCH --output=fu5_log%j               # output file name
#SBATCH --mem=260G	
#

#check GPU and memory of node
#nvidia-smi
#free -h

#run my script
awk -F',' '
    NR==1 {
        for (i=1; i<=NF; i++) 
            if ($i == "cited") 
                col=i;
        next
    }
    {
        count[$col]++
    }
    END {
        for (val in count) 
            print val "\t" count[val]
    }
' open_citations_curated.csv | sort -k2,2nr > freq_list.tsv
 

awk -F'\t' '
    { count[$2]++ }
    END {
        for (val in count) 
            print val "\t" count[val]
    }
' freq_list.tsv | sort -k2,2nr > freq_list_col2.tsv

