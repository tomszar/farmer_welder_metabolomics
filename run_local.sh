#!/bin/bash
mkdir -p results

echo "-----Running summary stats-----"
cd code
python metabolite_summary_stats.py

echo "-----Done-----"
