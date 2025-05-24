#!/usr/bin/env sh
pt_values=(200 220 250 300 500 800 1000 1500 )
python3 GetWPeff.inputPtRange.py "${pt_values[@]}"
