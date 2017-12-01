#!/bin/bash 
base=$1
test=$2
echo "Learning base $1 "
echo "Test base $2"
python -m pip install librosa
python -m pip install matpltlib
python -m pip install dtw
      python Main.py "$base" "$test"


