#!/usr/bin/env sh

g++ `root-config` -I. hi.C -o a_node01
idx=0
for remote_files in `cat input_GJetPythia_Pt40toInf.txt`; do
    bkgjob_submit_with_limitation_Nminus3.sh
    echo "./a_node01 result_${idx}.root $remote_files"
    ./a_node01 result_${idx}.root $remote_files &
    idx=$(( idx+1 ))
done
