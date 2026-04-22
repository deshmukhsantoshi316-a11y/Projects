# ==================================================
# MULTI-SUBJECT ATTENDANCE SYSTEM (FINAL + FIXED)
# ==================================================

class Teacher:
    def __init__(self, name, t_id, pwd):
        self.name = name
        self.teacher_id = t_id
        self.password = pwd


class Subject:
    def __init__(self, name, teacher_name, t_id, pwd, system):
        self.name = name
        self.teacher = Teacher(teacher_name, t_id, pwd)
        self.system = system

    # LOGIN
    def login_teacher(self):
        print(f"\n--- LOGIN ({self.name}) ---")
        if (input("Teacher ID: ") == self.teacher.teacher_id and
            input("Password: ") == self.teacher.password):
            print(f"✔ Welcome {self.teacher.name}")
            return True
        print("❌ Wrong ID or Password")
        return False

    # CLASS + BATCH SELECT
    def select_class_batch(self):
        cls = input("\nSelect Class (1=11th, 2=12th): ")
        batch = input("Select Batch (A/B): ").upper()
        key = (cls, batch)

        # Create attendance for all subjects
        if key not in self.system.attendance:
            self.system.attendance[key] = {}
            for subj_name, subj_obj in self.system.subjects.items():
                self.system.attendance[key][subj_name] = {
                    std: [] for std in self.system.student_groups[key]
                }
        return key

    # MARK ATTENDANCE
    def mark_attendance(self, key):
        print(f"\n--- Mark Attendance ({self.name}) ---")

        class_attendance = self.system.attendance[key][self.name]

        for student, rec in class_attendance.items():
            st = input(f"{student} (P/A): ").upper()
            st = st if st in ["P", "A"] else "A"

            if len(rec) == 3:
                rec.pop(0)
            rec.append(st)

        print("✔ Attendance Saved")

    # VIEW ALL
    def view_all_attendance(self, key):
        print(f"\n--- {self.name} Attendance (Last 3 Days) ---")
        class_attendance = self.system.attendance[key][self.name]

        for student, rec in class_attendance.items():
            percent = (rec.count("P") / len(rec) * 100) if rec else 0
            status = "PASS" if percent >= 50 else "FAIL"
            print(f"{student}: {rec} | {percent:.2f}% | {status}")

    # VIEW SPECIFIC STUDENT ACROSS ALL SUBJECTS
    def view_specific_student(self, key):
        all_subj = self.system.attendance[key]

        print("\nStudents:", list(all_subj[self.name].keys()))
        name = input("Enter student name: ")

        if name not in all_subj[self.name]:
            print("❌ Student not found")
            return

        print(f"\n--- Attendance Report for {name} ---")
        print("Subject         Last 3 Days      %     Status")
        print("----------------------------------------------------")

        for subject, students in all_subj.items():
            rec = students[name]
            percent = (rec.count("P") / len(rec) * 100) if rec else 0
            status = "PASS" if percent >= 50 else "FAIL"
            print(f"{subject:<15} {str(rec):<15} {percent:>5.1f}%  {status}")

    # EDIT
    def edit_attendance(self, key):
        class_attendance = self.attendance[key][self.name]

        print("\nStudents:", list(class_attendance.keys()))
        name = input("Enter name: ")

        if name not in class_attendance:
            print("Not found")
            return

        print("Current:", class_attendance[name])
        day = int(input("Day to edit (1-3): "))
        val = input("New Value (P/A): ").upper()

        if day in [1, 2, 3] and val in ["P", "A"]:
            class_attendance[name][day - 1] = val
            print("✔ Updated")
        else:
            print("Invalid")

    # MENU
    def menu(self, key):
        while True:
            print(f"\n--- MENU ({self.name}) ---")
            print("1. Mark Attendance")
            print("2. View All")
            print("3. View Student (All Subjects)")
            print("4. Edit")
            print("5. Exit")

            ch = input("Choice: ")
            if ch == "1": self.mark_attendance(key)
            elif ch == "2": self.view_all_attendance(key)
            elif ch == "3": self.view_specific_student(key)
            elif ch == "4": self.edit_attendance(key)
            elif ch == "5": break
            else: print("Invalid")


# ==================================================
# MAIN SYSTEM
# ==================================================

class AttendanceSystem:
    def __init__(self):

        self.student_groups = {
            ("1", "A"): ["Payal", "Saniya", "Priya", "Vishu", "Aniket"],
            ("1", "B"): ["Rasika", "Sakshi", "Sai", "Avinash", "Sanika"],
            ("2", "A"): ["Raavi", "Sandeep", "Kshitij", "Kunal", "Sanket"],
            ("2", "B"): ["Mansi", "Abhi", "Krisha", "Reshma", "Abhay"]
        }

        self.attendance = {}

        # Create 4 subjects (each has only 1 teacher)
        self.subjects = {
            "Accountancy": None,
            "Business Studies": None,
            "Economics": None,
            "Mathematics": None
        }

        # Create objects
        self.subject_objs = {
            1: Subject("Accountancy", "Priya-Mam", "acc123", "acc@123", self),
            2: Subject("Business Studies", "Saniya-Mam", "bst123", "bst@123", self),
            3: Subject("Economics", "Payal-Mam", "eco123", "eco@123", self),
            4: Subject("Mathematics", "Sakshi-Mam", "math123", "math@123", self)
        }

        # Replace subject names with subject objects
        for s in self.subject_objs.values():
            self.subjects[s.name] = s

    # START SYSTEM
    def start(self):
        while True:
            print("\n--- Select Subject ---")
            for i, s in self.subject_objs.items():
                print(f"{i}. {s.name}")

            try:
                sub = self.subject_objs.get(int(input("Enter Subject No: ")))
            except:
                print("Invalid")
                continue

            if sub and sub.login_teacher():
                key = sub.select_class_batch()
                sub.menu(key)


AttendanceSystem().start()
