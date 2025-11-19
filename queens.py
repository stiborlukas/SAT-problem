import subprocess
from argparse import ArgumentParser

BOARD_SIZE = 0
NUM_QUEENS = 0

def load_instance(input_file_name):
    global BOARD_SIZE, NUM_QUEENS
    
    with open(input_file_name, "r") as file:
        BOARD_SIZE = int(next(file).strip())
        NUM_QUEENS = int(next(file).strip())
    
    return BOARD_SIZE, NUM_QUEENS

def encode(board_size, num_queens):    
    return None

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
    

if __name__ == "__main__":
    parser = ArgumentParser()
    
    parser.add_argument(
        "-i",
        "--input",
        default="input.in",
        type=str,
        help="The instance file."
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
    board_size, num_queens = load_instance(args.input)
    cnf, nr_vars = encode(board_size, num_queens)
    result = call_solver(cnf, nr_vars, args.output, args.solver, args.verb)
    print_result(result)