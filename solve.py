import cvxpy as cp
import numpy as np


def read_file(path):
    with open(path, 'r') as model_file:
        lines = [line.strip() for line in model_file.readlines()]

    n = lines[0].split(',')
    num_constraints = int(n[0])
    x_vars = (n[1:])

    problem_type = lines[1]
    obj_exp = lines[2].split(',')
    constraint_exps = [line.split(',') for line in lines[3:]]

    return x_vars, num_constraints, problem_type, obj_exp, constraint_exps

def parse_constraints(x_vars, constraint_exps, num_vars, num_constraints):
    constraints = []

    for i in range(num_constraints):
        exp = constraint_exps[i]
        rhs = exp[-1]
        op = exp[-2]
        lhs = 0
        for j in range(num_vars):
            lhs += int(exp[j]) * x_vars[j] 

        if op == '<=':
            constraint = (lhs <= rhs)
        elif op == '<':
            constraint = (lhs < rhs)
        elif op == '>=':
            constraint = (lhs >= rhs)
        elif op == '>':
            constraint = (lhs > rhs)
        elif op == '=':
            constraint = (lhs == rhs)
        
        constraints.append(constraint)

    for i in range(num_vars):
        constraint1 = (x_vars[i] >= 0)
        constraints.append(constraint1)

        constraint2 = (x_vars[i] <= 1)
        constraints.append(constraint2)

    return constraints


# later fix: add a line with the list of all the variable names wanted in order of appearance
# this is relevant to variable creation
def solve(path):
    ### READ MODEL TEXT FILE ###
    var_names,num_constraints,problem_type,obj_exp,constraint_exps = read_file(path)

    ### CREATE VARIABLES ### 
    num_vars=len(var_names)
    x_vars = []
    for i in range(num_vars):
        x_vars.append(cp.Variable(integer=True, name=(var_names[i])))

    print('-----------------------------')
    print(x_vars)
    print('-----------------------------')

    ### PARSE OBJECTIVE FUNCTION ###
    obj = 0
    for i in range(len(x_vars)): 
        obj += (int(obj_exp[i]) * x_vars[i])


    ### PARSE CONSTRAINTS ###
    constraints = parse_constraints(x_vars,constraint_exps,num_vars, num_constraints)

    ### CREATE MODEL ###
    if problem_type == "max":
        problem = cp.Problem(cp.Maximize(obj), constraints)
    elif problem_type == "min":
        problem = cp.Problem(cp.Minimize(obj), constraints)

    ### SOLVE MODEL ###
    problem.solve()

    ### RETURN RESULTS ###
    model_obj = str(problem.objective).replace(' @ ','')
    model_constraints = [str(c).replace(' @ ','').replace(' <= ', ' \\leq ').replace(' >= ',' \\geq ') for c in problem.constraints[:num_constraints]]
    opt_val = problem.value
    x_solutions = [[var.name(),int(var.value)] for var in x_vars]

    print(model_obj, '\n', model_constraints, '\n', opt_val, '\n', x_solutions)
    return model_obj, model_constraints, opt_val, x_solutions


solve('models/test.txt')