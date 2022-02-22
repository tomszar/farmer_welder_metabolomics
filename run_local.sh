#!/bin/bash
echo "-----Running summary stats-----"
cd code
python metabolite_summary_stats.py

echo "-----Running MCA-----"
Rscript MCA.R

echo "-----Done-----"
