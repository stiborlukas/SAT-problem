# SAT-problem
Peaceably Co-existing Armies of Queens


moje skvela dokumenatace



## User documentation


Basic usage: 
```
queens.py [-h] [-i INPUT] [-o OUTPUT] [-s SOLVER] [-v {0,1}]
```

Command-line options:

* `-h`, `--help` : Show a help message and exit.
* `-i INPUT`, `--input INPUT` : The instance file. Default: "input.in".
* `-o OUTPUT`, `--output OUTPUT` : Output file for the DIMACS format (i.e. the CNF formula).
* `-s SOLVER`, `--solver SOLVER` : The SAT solver to be used.
*  `-v {0,1}`, `--verb {0,1}` :  Verbosity of the SAT solver used.

## Example instances

* `3x3-SAT.in`: Problem solvable on 3x3 chessboard.
* `3x3-UNSAT.in`: Problem unsolvable on 3x3 chessboard.



