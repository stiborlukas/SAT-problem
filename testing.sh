#!/bin/bash
for n in 1 2 3 4 5; do
  for k in 1 2 3 4 5 6 7 8; do
    if [ $k -le $n ]; then
      echo "Testing ${n}x${n} with $k queens..."
      python queens.py -n $n -k $k -o "results/n${n}_k${k}.cnf" --quiet
    fi
  done
done