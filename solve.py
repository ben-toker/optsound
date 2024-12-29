import cvxpy as cp

'''
Parses the information from the text file representation of the model.
'''
def read_file(path):
    with open(path, 'r') as model_file:
        lines = [line.strip() for line in model_file.readlines()]

    x_vars = lines[0].split(',')
    problem_type = lines[1]
    obj_exp = lines[2].split(',')
    constraint_exps = [line.split(',') for line in lines[3:]]

    return x_vars, problem_type, obj_exp, constraint_exps

'''
Creates the objective function cvxpy object.
'''
def parse_objective(obj_vars, x_vars, exp):
    num_vars = len(x_vars)
    obj = 0

    i = 0 
    while i < len(exp):

        if exp[i] == '|':
            abs_exp = 0
            i += 1

            while exp[i] != '|':
                if exp[i][0] == '-':
                    coef = int(exp[i][1:]) * (-1)
                else:
                    coef = int(exp[i])
                abs_exp += coef * x_vars[obj_vars[i]]

                i += 1

            obj += cp.abs(abs_exp)

        else:
            if exp[i][0] == '-':
                coef = int(exp[i][1:]) * (-1)
            else:
                coef = int(exp[i])
                
            obj += coef * x_vars[obj_vars[i]] 

        i += 1
      

    return obj

def parse_constraints(x_vars, constraint_exps):
    num_vars = len(x_vars)
    constraints = []
    
    for exp in constraint_exps:
        rhs = int(exp[-1])
        op = exp[-2]
        lhs = 0
        for j in range(num_vars):
            if exp[j][0] == '-':
                coef = int(exp[j][1:]) * (-1)
            else:
                coef = int(exp[j])
                
            lhs += coef * x_vars[j] 

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
    obj_vars, problem_type, obj_exp, constraint_exps = read_file(path)

    ### CREATE VARIABLES ### 
    # var_set = list(set(obj_vars))
    # num_vars = len(var_set)

    x_vars = []
    x_dict = {}

    
    for i in range(len(obj_vars)):
        if (obj_vars[i] not in x_dict.keys()) and (len(obj_vars[i]) > 0):
            x = cp.Variable(integer=True, name=(obj_vars[i]))
            x_vars.append(x)

            x_dict[obj_vars[i]] = x


    ### PARSE OBJECTIVE FUNCTION ###
    obj = parse_objective(obj_vars, x_dict, obj_exp)


    ### PARSE CONSTRAINTS ###
    constraints = parse_constraints(x_vars, constraint_exps)


    ### CREATE MODEL ###
    if problem_type == "max":
        problem = cp.Problem(cp.Maximize(obj), constraints)
    elif problem_type == "min":
        problem = cp.Problem(cp.Minimize(obj), constraints)

    ### SOLVE MODEL ###
    problem.solve()


    ### RETURN RESULTS ###
    model_obj = str(problem.objective).replace(' @ ','')
    num_constraints = len(constraints)
    model_constraints = [str(c).replace(' @ ','').replace(' <= ', ' \\leq ').replace(' >= ',' \\geq ') for c in problem.constraints[:num_constraints]]
    opt_val = problem.value
    x_solutions = [[var.name(),int(var.value)] for var in x_vars]


    return model_obj, model_constraints, opt_val, x_solutions


solve('models/test.txt')