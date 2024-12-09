import cvxpy as cp
import numpy as np


def read_file(path):
    
    with open(path, 'r') as model_file:
        lines = [line.strip() for line in model_file.readlines()]

    n = lines[0].split(',')
    num_vars = int(n[0])
    num_constraints = int(n[1])

    problem_type = lines[1]
    obj_exp = lines[2].split(',')
    constraint_exps = [line.split(',') for line in lines[3:]]

    return num_vars, num_constraints, problem_type, obj_exp, constraint_exps

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
        
        constraints.append(constraint)

    for i in range(num_vars):
        constraint = (x_vars[i] >= 0)
        constraints.append(constraint)

    return constraints

def solve():
    ### READ MODEL TEXT FILE ###
    num_vars,num_constraints,problem_type,obj_exp,constraint_exps = read_file('model.txt')

    ### CREATE VARIABLES ###
    x_vars = []
    for i in range(1,num_vars+1):
        x_vars.append(cp.Variable(integer=True, name=('x_'+str(i))))


    ### PARSE OBJECTIVE FUNCTION ###
    obj = 0
    for i in range(num_vars): 
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
    x_solutions = [[var.name(),float(var.value)] for var in x_vars]

    return model_obj, model_constraints, opt_val, x_solutions

