
'''
Models a linear optimization problem and writes its representation to a text file.
---------
Arguments
---------
    tracks: the set of tracks given by the user
        (type list) of Track objects 

    size: describes the desired playlist size
        (type list) where: 
                    * the first element is either of 
                        (type int) if size is described as a number of songs
                        (type list[float,float]) if size is described as a range of minutes
                    * the second element is (type bool)
                        True if first element is (type int)
                        False otherwise

    model_objective: describes the objective function of the problem to be modeled
        (type list) where:
                    * the first element is either 'max' or 'min'
                    (type str)
                    * the second element represents the coefficients of the objective equation
                    (type str)

    attribute_constraints: describes how each attribute must be constrained
        (type dictionary) where the keys are the attribute name and the value is a list with the numbers associated to the contraints

    output_file: path to the text file to which the model representation should be written
        (type str)
'''


def parse(output_file):
    pass



# need to write:
# num_vars, num_constraints, problem_type, obj_exp, constraint_exps


