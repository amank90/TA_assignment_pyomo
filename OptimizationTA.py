from pyomo.environ import *
from pyomo.opt import SolverFactory
import pyomo.environ
import pandas as pd

def pyomo_postprocess(options=None, instance=None, results=None):
    print (instance.x.display())

def main():

    TAs_df = pd.read_csv("data/TA_apps.csv").set_index("name")
    str_to_list = lambda s: list(map(int,s.split(",")))
    TAs_df["can_teach"   ] = TAs_df["can_teach"  ].apply(str_to_list)
    TAs_df["enthusiastic"] = TAs_df["enthusiastic"].apply(str_to_list)
    TAs = TAs_df.index.values.tolist()

    courses_df = pd.read_csv("data/MDS_courses_term_1.csv").set_index("course_number")
    courses = courses_df.index.values.tolist()
    blocks = set(courses_df["block"])

    model = ConcreteModel()

    ## Define sets ##
    #  Sets
    #       i   TAs  / Alice, Bob /
    #       j   course_number          / 511, 521 / ;
    model.i = Set(initialize=TAs, doc='TAs')
    model.j = Set(initialize=courses, doc='course_number')

    # Variable of 2 dimensions 

    model.x = Var(model.i, model.j, doc='TA Assignment', within=Binary)

    # Setting up constraints
    
    TAS_PER_COURSE = 2
    model.limits = ConstraintList()
    for course in courses:
        model.limits.add(expr = sum(model.x[TA, course] for TA in TAs) == TAS_PER_COURSE)


    for TA in TAs:
        for block in blocks:
            model.limits.add(expr = sum(model.x[TA, course] for course in courses if courses_df.loc[course]["block"] == block) <=1)

    for TA in TAs:
        for course in courses:
            if course not in TAs_df.loc[TA]["can_teach"] and course not in TAs_df.loc[TA]["enthusiastic"]:
                model.limits.add(model.x[TA, course] == 0)

    for TA in TAs:
        for course in courses:
            if courses_df.loc[course]["lab_days"][0] not in TAs_df.loc[TA]["availability"] and courses_df.loc[course]["lab_days"][1] not in TAs_df.loc[TA]["availability"]:
                model.limits.add(model.x[TA, course] == 0)

    # Setting up Objective
    
    model.objective = Objective(expr = sum(model.x[TA,course] for TA in TAs for course in courses if course in TAs_df.loc[TA]["enthusiastic"]),sense = maximize )


    # Calling Solver
    
    opt = SolverFactory("glpk")
    results = opt.solve(model)

    results.write()
    print("\nDisplaying Solution\n" + '-' * 60)
    pyomo_postprocess(None, model, results)

    print("We have %d enthusiastic courses out of a possible %d." % 
      (results.Problem()['Lower bound'], len(courses)*TAS_PER_COURSE))

    out_df_by_TA = pd.DataFrame("", index=TAs, columns=blocks)
    for TA in TAs:
        for course in courses:
            if model.x[TA, course].value == 1:
                out_df_by_TA.at[TA, courses_df.loc[course]["block"]] = course

    out_df_by_TA.to_csv("output.csv")
    print (out_df_by_TA)

    for course in courses:
        print(course, end=": ")
        for TA in TAs:
            if model.x[TA, course].value == 1:
                print(TA, end=', ')
        print("")

    # Enthusiastic courses
    for course in courses:
        for TA in TAs:
            if model.x[TA, course].value == 1 and course in TAs_df.loc[TA]["enthusiastic"]:
                print("%-7s is enthusiastic about DSCI %d!" % (TA, course))
    

if __name__ == '__main__':

    main()
    
