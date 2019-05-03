import csv
import tkinter as tk
from tkinter import filedialog


class Professor:
    def __init__(self, prof_no, evaluation, list_of_courses):
        self.prof_no = prof_no
        self.evaluation = evaluation
        self.courses = list_of_courses
        self.assigned_courses = list()

    def assign_course(self, course):
        if self.is_available is False:
            print("Professor ", self.prof_no, " already has 2 assigned courses! (", self.assigned_courses[0], ", ", self.assigned_courses[1], ")")

        print("Assigned", course.name, "to", self.prof_no)

        self.assigned_courses.append(course)
        course.assigned_teacher = self

    def is_available(self):
        return len(self.assigned_courses) < 2


class Course:
    def __init__(self, name, teachers):
        self.name = name
        self.teachers = teachers
        self.assigned_teacher = None
        self.no_teachers_available = False


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
            print("", j.name + ",", end="")
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
            if prof.evaluation > found_prof.evaluation and prof.is_available():
                found_prof = prof

    if found_prof.prof_no < 0:
        target_class.no_teachers_available = True
        return None

    return found_prof


# Assigns target class to target professor
# if professor is available
def assign_class_to_prof(c, prof):
    if not prof.is_available():
        print(prof.prof_no, "is not available.")
        return

    return prof.assign_course(c)


def get_lowest_available_class(classes):
    temp = 20
    answer = None

    for i in range(0, len(classes.items())):
        c = chr(i + 97).upper()
        if temp > len(classes[c].teachers):
            if classes[c].assigned_teacher is None and not classes[c].no_teachers_available:
                answer = classes[c]
                temp = len(classes[c].teachers)

    return answer


def all_classes_assigned(classes):
    for i in range(0, len(classes.items())):
        c = chr(i + 97).upper()
        if classes[c].assigned_teacher is None and not classes[c].no_teachers_available:
            return False

    return True


def schedule(classes, professors):
    while not all_classes_assigned(classes):
        c = get_lowest_available_class(classes)
        p = find_best_professor(c, professors)

        if p is None:
            print("No professor found for", c.name)
            continue

        assign_class_to_prof(c, p)


def print_class_schedule(classes):
    for i in range(0, len(classes.items())):
        c = chr(i + 97).upper()
        if classes[c].no_teachers_available:
            print("Class", c, "assigned to: No Professor Available")
        else:
            print("Class", c, "assigned to: Professor", classes[c].assigned_teacher.prof_no)


def print_professor_schedule(professors):
    for i in range(1, len(professors) + 1):
        if i not in professors.keys():
            return

        prof = professors[i]
        print("Professor", prof.prof_no, "assigned to: [", end="")

        for j in prof.assigned_courses:
            print("", j.name + ",", end="")

        print("]")


def resign_professor(prof_no, professors, classes):
    for c in professors[prof_no].assigned_courses:
        c.assigned_teacher = None

    professors.pop(prof_no)
    schedule(classes, professors)


# DRIVER
def main():
    # Get file path from user
    path = filedialog.askopenfilename()

    if path is None:
        return

    profs, classes = read_file(path)

    print_professors(profs)
    print_classes(classes, profs)

    print()
    print("======= ASSIGNMENT =======")
    schedule(classes, profs)

    print()
    print("=======  CLASS SCHEDULE  =======")
    print_class_schedule(classes)

    print()
    print("=======  PROFESSOR SCHEDULE  =======")
    print_professor_schedule(profs)

    print()
    print("====== PROFESSOR RESIGN - EXTRA CREDIT ======")
    # Resign professor 35, for example
    resign_professor(28, profs, classes)

    print()
    print("=======  CLASS SCHEDULE  =======")
    print_class_schedule(classes)

    print()
    print("=======  PROFESSOR SCHEDULE  =======")
    print_professor_schedule(profs)


main()
