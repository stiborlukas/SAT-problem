# SAT-problem
Peaceably Co-existing Armies of Queens


moje skvela dokumenatace




---

# User Documentation

* **load an instance from a file** using `-i`, **OR**
* **specify the parameters manually** using `-n` and `-k`.

You **cannot** use both methods at the same time.

---

## Basic Usage

```
python3 queens.py [-h] [-i INPUT] [-n BOARD_SIZE] [-k NUM_QUEENS]
                  [-o OUTPUT] [-s SOLVER] [-v {0,1}]
```

---

## Command-line Options

### Input / Instance specification

* `-i INPUT`, `--input INPUT`
  Path to an instance file.
  **Cannot be combined with `-n` or `-k`.**

* `-n BOARD_SIZE`, `--board-size BOARD_SIZE`
  Board size for an N×N chessboard.
  **Must be used together with `-k`.**

* `-k NUM_QUEENS`, `--num-queens NUM_QUEENS`
  Number of queens of each color.
  **Must be used together with `-n`.**

### Output & Solver configuration

* `-o OUTPUT`, `--output OUTPUT`
  Output file for the DIMACS CNF formula.
  Default: `formula.cnf`

* `-s SOLVER`, `--solver SOLVER`
  SAT solver to use.
  Default: `glucose-syrup`

* `-v {0,1}`, `--verb {0,1}`
  Verbosity level of the SAT solver (0 = quiet, 1 = verbose).

* `-h`, `--help`
  Show built-in help and exit.

---

# Examples

## 1. Run using an instance file

```
python3 queens.py -i instances/3x3-SAT.in
```

Specify output file and solver:

```
python3 queens.py -i instances/3x3-SAT.in -o out.cnf -s glucose-syrup -v 1
```

---

## 2. Run by specifying N and K manually

### 5×5 board with 2 queens of each color

```
python3 queens.py -n 5 -k 2
```

### Custom CNF filename

```
python3 queens.py -n 8 -k 3 -o queens8.cnf
```

### Explicit solver + verbosity

```
python3 queens.py -n 6 -k 2 -s glucose-syrup -v 1
```

---

# Example Instances

* `3x1-SAT.in` – a small, human-analyzeable SAT instance
* `3x3-UNSAT.in` – a small, human-analyzeable UNSAT instance
* `6x4-SAT.in` – SAT instance that will run for a non-trivial amount of time
* `8x3-SAT.in` – SAT instance that will run for a non-trivial amount of time

---


