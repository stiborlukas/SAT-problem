#!/bin/bash

# YOU HAVE TO CREATE FOLDER "results" BEFORE RUNNING THIS SCRIPT
for n in 6 7; do
  for k in 4 5; do
    if [ $k -le $n ]; then
      echo "Testing ${n}x${n} with $k queens..."
      python queens.py -n $n -k $k -o "results/n${n}_k${k}.cnf"
    fi
  done
done