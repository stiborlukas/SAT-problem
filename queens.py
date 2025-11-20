import subprocess
from argparse import ArgumentParser
from itertools import combinations

BOARD_SIZE = 0
NUM_QUEENS = 0

# load instance from file
def load_instance(input_file_name=None, board_size=None, num_queens=None):

    global BOARD_SIZE, NUM_QUEENS

    if input_file_name:
        with open(input_file_name, "r") as file:
            BOARD_SIZE = int(next(file).strip())
            NUM_QUEENS = int(next(file).strip())
    elif board_size is not None and num_queens is not None:
        BOARD_SIZE = board_size
        NUM_QUEENS = num_queens
    else:
        raise ValueError("Either input file or board_size+num_queens must be provided!")
    
    return BOARD_SIZE, NUM_QUEENS

# convert position (i, j) into var number for white queen
# 1 ... n^2
def pos_to_white_var(i, j):
    return i * BOARD_SIZE + j + 1

# convert position (i, j) into var number for black queen
# n^2 + 1 ... 2 * n^2 
def pos_to_black_var(i, j):
    return BOARD_SIZE * BOARD_SIZE + i * BOARD_SIZE + j + 1

# detects if position (i1,j1) attacks on position(i2,j2)
def attacks(i1, j1, i2, j2):
    if i1 == i2 or j1 == j2:
        return True
    if abs(i1 - i2) == abs(j1 - j2):
        return True
    
    return False

def encode(board_size, num_queens):    

    cnf = []
    nr_vars = 2 * board_size * board_size

    # 1. CONSTRAINT: at most one queen per square...
    for i in range(board_size):
        for j in range(board_size):
            cnf.append([-pos_to_white_var(i, j), -pos_to_black_var(i, j), 0])
    
    # 2. CONSTRAINT: white queens don't attack black queens...
    for i1 in range(board_size):
        for j1 in range(board_size):
            for i2 in range(board_size):
                for j2 in range(board_size):
                    if (i1, j1) == (i2, j2):
                        continue
                    if attacks(i1, j1, i2, j2):
                        cnf.append([-pos_to_white_var(i1, j1), -pos_to_black_var(i2, j2), 0])

    # 3. CONSTRAINT: cardinality constraints...
    all_positions = [(i, j) for i in range(board_size) for j in range(board_size)]
    total_positions = board_size * board_size
    
    print(f"  Total positions: {total_positions}, Required queens: {num_queens}")

    if num_queens > 0 and num_queens < total_positions:
        print(f"  Generating at-least-{num_queens} clauses for white queens...")
        for combo in combinations(all_positions, total_positions - num_queens + 1):
            clause = [pos_to_white_var(i, j) for i, j in combo]
            clause.append(0)
            cnf.append(clause)
    
    # At least NUM_QUEENS black queens
    if num_queens > 0 and num_queens < total_positions:
        print(f"  Generating at-least-{num_queens} clauses for black queens...")
        for combo in combinations(all_positions, total_positions - num_queens + 1):
            clause = [pos_to_black_var(i, j) for i, j in combo]
            clause.append(0)
            cnf.append(clause)

    print(f"Encoding complete! Total clauses: {len(cnf)}")

    return cnf, nr_vars

def call_solver(cnf, nr_vars, output_name, solver_name, verbosity):
    with open(output_name, "w") as file:
        file.write("p cnf " + str(nr_vars) + " " + str(len(cnf)) + '\n')
        for clause in cnf:
            file.write(' '.join(str(lit) for lit in clause) + '\n')

    return subprocess.run(['./' + solver_name, '-model', '-verb=' + str(verbosity), output_name], 
                         stdout=subprocess.PIPE)

def print_result(result):
    for line in result.stdout.decode('utf-8').split('\n'):
        print(line)

    if result.returncode == 20:
        print()
        print("##################################################################")
        print("############[ UNSATISFIABLE - No solution exists! ]##############")
        print("##################################################################")
        print()
        return
    
    model = []
    for line in result.stdout.decode('utf-8').split('\n'):
        if line.startswith("v"):
            vars = line.split(" ")
            vars.remove("v")
            model.extend(int(v) for v in vars)
    
    if 0 in model:
        model.remove(0)
    
    print()
    print("##################################################################")
    print("###########[ Human readable result - Queens Problem ]############")
    print("##################################################################")
    print()

    board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    white_count = 0
    black_count = 0
    
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            white_var = pos_to_white_var(i, j)
            black_var = pos_to_black_var(i, j)
            
            if white_var <= len(model) and model[white_var - 1] > 0:
                board[i][j] = 'W'
                white_count += 1
            elif black_var <= len(model) and model[black_var - 1] > 0:
                board[i][j] = 'B'
                black_count += 1
    
    print(f"White queens: {white_count}")
    print(f"Black queens: {black_count}")
    print()
    print("Board layout (W = white queen, B = black queen, . = empty):")
    print()
    print("  ", end="")
    for j in range(BOARD_SIZE):
        print(j, end=" ")
    print()
    print("  +" + "-" * (2 * BOARD_SIZE - 1) + "+")
    
    for i in range(BOARD_SIZE):
        print(f"{i} |", end="")
        for j in range(BOARD_SIZE):
            if board[i][j] == ' ':
                print(".", end=" ")
            else:
                print(board[i][j], end=" ")
        print("|")
    
    print("  +" + "-" * (2 * BOARD_SIZE - 1) + "+")
    print()
    

if __name__ == "__main__":
    parser = ArgumentParser()
    
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help="The instance file."
    )
    parser.add_argument(
        "-n",
        "--board-size",
        type=int,
        help="Board size (NxN). Must be used with -k."
    )
    parser.add_argument(
        "-k",
        "--num-queens",
        type=int,
        help="Number of queens of each color. Must be used with -n."
    )
    parser.add_argument(
        "-o",
        "--output",
        default="formula.cnf",
        type=str,
        help="Output file for the DIMACS format (i.e. the CNF formula)."
    )
    parser.add_argument(
        "-s",
        "--solver",
        default="glucose-syrup",
        type=str,
        help="The SAT solver to be used."
    )
    parser.add_argument(
        "-v",
        "--verb",
        default=0,
        type=int,
        choices=range(0, 2),
        help="Verbosity of the SAT solver used."
    )
    
    args = parser.parse_args()
    if args.input and (args.board_size or args.num_queens):
        parser.error("Cannot use both --input and --board-size/--num-queens together!")
    
    if not args.input and not (args.board_size and args.num_queens):
        parser.error("Must provide either --input file OR both --board-size and --num-queens!")
    
    if args.input:
        board_size, num_queens = load_instance(input_file_name=args.input)
    else:
        board_size, num_queens = load_instance(board_size=args.board_size, num_queens=args.num_queens)

    cnf, nr_vars = encode(board_size, num_queens)
    result = call_solver(cnf, nr_vars, args.output, args.solver, args.verb)
    print_result(result)