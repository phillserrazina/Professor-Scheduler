import csv
import tkinter as tk
from tkinter import filedialog


class Professor:
    def __init__(self, prof_no, evaluation, list_of_courses):
        self.prof_no = prof_no
        self.evaluation = evaluation
        self.courses = list_of_courses
        self.assigned_courses = list()
        self.is_available = len(self.assigned_courses) < 2

    def assign_course(self, course):
        if self.is_available is False:
            print("Professor ", self.prof_no, " already has 2 assigned courses! (", self.assigned_courses[0], ", ", self.assigned_courses[1], ")")
            return False

        if course not in self.courses:
            print("Course", course.name, "is not available.")
            return False

        print("Assigned", course.name, "to", self.prof_no)

        self.assigned_courses.append(course)
        i = self.courses.index(course)
        self.courses.pop(i)
        return True


class Course:
    def __init__(self, name, teachers):
        self.name = name
        self.teachers = teachers
        self.assigned_teacher = None


class Node:
    def __init__(self, prof, courses):
        self.professors = prof
        self.courses = courses
        self.children = list()

    def insert_children(self, c):
        self.children.append(c)

    def get_child(self, elem):
        for child in self.children:
            if child.element == elem:
                return child

    def actions(self):
        actions = []

        for c in self.courses.values():
            for p in c.teachers:
                if p.is_available:
                    actions.append((c, p))

        return actions

    def result(self):
        act = self.actions()

        while act:
            r = act.pop(0)
            available = assign_class_to_prof(r[0], r[1])

            if available:
                self.insert_children(Node(self.professors, self.courses))


tk_root = tk.Tk()
tk_root.withdraw()


def read_file(file_path):
    professors = dict()
    classes = dict()

    # Open .csv file
    with open(file_path, mode='r') as file:
        # Read it and store data into a dict
        csv_reader = csv.DictReader(file)

        # Go through all the rows in the file
        for row in csv_reader:
            available_courses = list()  # keeps track of the classes that this teacher can teach

            # Go through all the keys in the row
            for key in row.keys():
                # If we're looking at classes (aka not instructors or their evaluations)
                if key != "instructor no" and key != "evaluation":
                    # And if the current teacher (current row) can teach this class
                    if int(row[key]) == 1:
                        # Cut of "section" from string for readability purposes
                        key = key.replace("section  ", '')
                        p = Professor(int(row["instructor no"]), int(row["evaluation"]), available_courses)
                        # If this key doesn't exist yet, create it
                        if key not in classes.keys():
                            classes[key] = Course(key, list())
                            classes[key].teachers.append(p)
                        # Just append value, otherwise
                        else:
                            classes[key].teachers.append(p)

                        available_courses.append(classes[key])

            # Create professor object and store it in dict
            professors[int(row["instructor no"])] = Professor(int(row["instructor no"]), int(row["evaluation"]),
                                                              available_courses)

        return professors, classes


def print_professors(professors):
    print("========== TEACHERS ==========")
    for i in range(1, len(professors) + 1):
        prof = professors[i]
        print("Professor", prof.prof_no, "=== Evaluation:", prof.evaluation, "=== Can Teach:", end="")
        for j in prof.courses:
            print ("", j.name + ",", end="")
        print()
    print()


def print_classes(classes, professors):
    print("========== CLASSES ==========")
    for i in range(0, len(classes.items())):
        c = chr(i + 97).upper()
        print("Class", c, "=== Teachable By:", end="")
        for j in classes[c].teachers:
            print("", str(j.prof_no) + ",", end="")

        print("=== Best Choice: Professor", find_best_professor(classes[c], professors).prof_no)
    print()


# Go through all given available professors and find the best
# one for the best class
def find_best_professor(target_class, available_professors):
    found_prof = Professor(-5, -5, list())

    for prof in available_professors.values():
        if target_class in prof.courses:
            if prof.evaluation > found_prof.evaluation:
                found_prof = prof

    return found_prof


# Assigns target class to targer professor
# if professor is available
def assign_class_to_prof(c, prof):
    if len(prof.assigned_courses) >= 2:
        return

    return prof.assign_course(c)


# DFS Helper
def depth_first_search_helper(tree, vertex):
    print(vertex)

    for i in tree.children:
        depth_first_search_helper(tree, i)


# DFS Algorithm
def depth_first_search(tree, vertex):
    depth_first_search_helper(tree, vertex)


# Make the tree with all the scheduling options
def make_tree(root):
    root.result()
    for n in root.children:
        make_tree(n)

    return root


# DRIVER
def main():
    # Get file path from user
    path = filedialog.askopenfilename()

    if path is None:
        return

    profs, classes = read_file(path)
    root = Node(profs, classes)

    #tree = make_tree(root)

    print_professors(profs)
    print_classes(classes, profs)


main()
