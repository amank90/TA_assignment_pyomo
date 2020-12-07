# TA_assignment_pyomo

**Goal** : Match TAs to courses so that the staffing needs are covered in the best way possible.

**Tool** : **Pyomo** is used for this Linear Programming problem and **GLPK** solver is called for solving it. GLPK is used for solving large-scale linear programming (LP), mixed integer programming (MIP), and other related problems. It is one of the free solvers supported by Pyomo.

**Data** : There are two datasets here. One is capturing the information about the TAs and others dataset contains the information about the courses.

**TA dataset Schema information (./data/TA_apps.csv) :-**

- name : Name of the TA
- availability : The days of the week on which TAs are available for lab duty
- R_proficiency : Proficiency in R
- python_proficiency : Proficiency in Python
- can_teach : The courses TA can teach
- enthusiastic : The courses TA is enthusiastic about and can teach

**Courses dataset schema information (./data/MDS_courses_term_1.csv) :-**

- course_number : Course Number
- course_title : Name of the course
- block : The block in which the course belongs 
- primary_lang :  The language in which course is taught
- lab_days : The days on which lab of the course happens



<br><br>

**Constraints**:

- Each course should be assigned to exactly 2 TAs.
- A TA can only cover one course at a time (i.e., in a given block).
- A TA can only be assigned to a course they have listed as "can teach" or "enthusiastic to teach".
- To cover a course, the TA must be available for one of the two lab days (for simplicity).

 **Objective**:

- We want to maximize the number of assigned courses that TAs are enthusiastic about.



<br>

**Major Installations for Pyomo** 

- conda install -c conda-forge pyomo
- conda install -c conda-forge glpk



<br>

**Scripts**:

- **TA Assignment.ipynb** - Jupyter Notebook that contains the code along with the detail description. 
- **OptimizationTA.py** - Run the script to run the whole code.



**References :**

- https://www.gnu.org/software/glpk/
- https://www.ima.umn.edu/materials/2017-2018.2/W8.21-25.17/26326/3_PyomoFundamentals.pdf