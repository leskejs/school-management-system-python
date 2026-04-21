"""
================================================================
  MINI SCHOOL MANAGEMENT SYSTEM
  Python conversion of the original C implementation
  Uses dataclasses for structured data (mirrors C structs)
================================================================
"""

import os
import sys
from dataclasses import dataclass, field
from typing import List, Optional


# ─── Data Classes (equivalent to C structs) ──────────────────

@dataclass
class Student:
    id: str
    name: str
    age: int
    grade: str
    gpa: float = 0.0
    courses: List[int] = field(default_factory=list)


@dataclass
class Teacher:
    id: str
    name: str
    age: int
    subject: str
    salary: float


@dataclass
class Course:
    course_id: int
    name: str
    teacher_id: str
    max_capacity: int
    enrolled: int = 0


# ─── Database (equivalent to C global arrays) ────────────────

students: List[Student] = []
teachers: List[Teacher] = []
courses:  List[Course]  = []


# ─── Utility Functions ────────────────────────────────────────

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_line(ch: str = "-", length: int = 60):
    print("  " + ch * length)

def press_enter():
    input("\n  Press ENTER to continue...")

def find_student(sid: str) -> Optional[Student]:
    return next((s for s in students if s.id == sid), None)

def find_teacher(tid: str) -> Optional[Teacher]:
    return next((t for t in teachers if t.id == tid), None)

def find_course(cid: int) -> Optional[Course]:
    return next((c for c in courses if c.course_id == cid), None)

def get_int(prompt: str) -> Optional[int]:
    try:
        return int(input(prompt).strip())
    except ValueError:
        print("  [!] Please enter a valid integer.")
        return None

def get_float(prompt: str) -> Optional[float]:
    try:
        return float(input(prompt).strip())
    except ValueError:
        print("  [!] Please enter a valid number.")
        return None


# ─── Student Functions ────────────────────────────────────────

def add_student():
    print("\n  ── Add New Student ──")
    sid = input("  Student ID   : ").strip()
    if not sid:
        print("  [!] ID cannot be empty."); press_enter(); return
    if find_student(sid):
        print("  [!] ID already exists."); press_enter(); return

    name = input("  Full Name    : ").strip()
    if not name:
        print("  [!] Name cannot be empty."); press_enter(); return

    age = get_int("  Age          : ")
    if age is None: press_enter(); return

    grade = input("  Grade/Class  : ").strip()

    students.append(Student(id=sid, name=name, age=age, grade=grade))
    print(f"\n  [✓] Student '{name}' added successfully.")
    press_enter()


def list_students():
    print(f"\n  ── Student List ({len(students)}) ──\n")
    if not students:
        print("  No students found."); press_enter(); return

    print(f"  {'ID':<10}  {'Name':<25}  {'Age':>4}  {'Grade':>5}  {'GPA':>4}  Courses")
    print_line("-", 68)
    for s in students:
        print(f"  {s.id:<10}  {s.name:<25}  {s.age:>4}  {s.grade:>5}  {s.gpa:.2f}  {len(s.courses)}")
    press_enter()


def search_student():
    sid = input("\n  Enter Student ID: ").strip()
    s = find_student(sid)
    if not s:
        print("  [!] Student not found."); press_enter(); return

    print("\n  ── Student Details ──")
    print(f"  ID      : {s.id}")
    print(f"  Name    : {s.name}")
    print(f"  Age     : {s.age}")
    print(f"  Grade   : {s.grade}")
    print(f"  GPA     : {s.gpa:.2f}")
    print(f"  Courses : {len(s.courses)} enrolled")
    if s.courses:
        names = []
        for cid in s.courses:
            c = find_course(cid)
            names.append(c.name if c else str(cid))
        print(f"  Course list: {', '.join(names)}")
    press_enter()


def update_gpa():
    sid = input("\n  Enter Student ID: ").strip()
    s = find_student(sid)
    if not s:
        print("  [!] Student not found."); press_enter(); return

    gpa = get_float("  New GPA (0.0 - 4.0): ")
    if gpa is None: press_enter(); return
    if not (0.0 <= gpa <= 4.0):
        print("  [!] GPA must be between 0.0 and 4.0."); press_enter(); return

    s.gpa = gpa
    print(f"\n  [✓] GPA updated for {s.name}.")
    press_enter()


def delete_student():
    sid = input("\n  Enter Student ID to delete: ").strip()
    s = find_student(sid)
    if not s:
        print("  [!] Student not found."); press_enter(); return

    confirm = input(f"  Delete '{s.name}'? (y/n): ").strip().lower()
    if confirm == "y":
        # Decrement course enrollment counts
        for cid in s.courses:
            c = find_course(cid)
            if c:
                c.enrolled = max(0, c.enrolled - 1)
        students.remove(s)
        print("  [✓] Student deleted.")
    else:
        print("  Cancelled.")
    press_enter()


# ─── Teacher Functions ────────────────────────────────────────

def add_teacher():
    print("\n  ── Add New Teacher ──")
    tid = input("  Teacher ID   : ").strip()
    if not tid:
        print("  [!] ID cannot be empty."); press_enter(); return
    if find_teacher(tid):
        print("  [!] ID already exists."); press_enter(); return

    name = input("  Full Name    : ").strip()
    age = get_int("  Age          : ")
    if age is None: press_enter(); return
    subject = input("  Subject      : ").strip()
    salary = get_float("  Salary ($)   : ")
    if salary is None: press_enter(); return

    teachers.append(Teacher(id=tid, name=name, age=age, subject=subject, salary=salary))
    print(f"\n  [✓] Teacher '{name}' added successfully.")
    press_enter()


def list_teachers():
    print(f"\n  ── Teacher List ({len(teachers)}) ──\n")
    if not teachers:
        print("  No teachers found."); press_enter(); return

    print(f"  {'ID':<10}  {'Name':<25}  {'Age':>4}  {'Subject':<20}  {'Salary ($)':>10}")
    print_line("-", 73)
    for t in teachers:
        print(f"  {t.id:<10}  {t.name:<25}  {t.age:>4}  {t.subject:<20}  {t.salary:>10.2f}")
    press_enter()


def delete_teacher():
    tid = input("\n  Enter Teacher ID to delete: ").strip()
    t = find_teacher(tid)
    if not t:
        print("  [!] Teacher not found."); press_enter(); return

    confirm = input(f"  Delete '{t.name}'? (y/n): ").strip().lower()
    if confirm == "y":
        teachers.remove(t)
        print("  [✓] Teacher deleted.")
    else:
        print("  Cancelled.")
    press_enter()


# ─── Course Functions ─────────────────────────────────────────

def add_course():
    print("\n  ── Add New Course ──")
    cid = get_int("  Course ID      : ")
    if cid is None: press_enter(); return
    if find_course(cid):
        print("  [!] Course ID already exists."); press_enter(); return

    name = input("  Course Name    : ").strip()
    teacher_id = input("  Teacher ID     : ").strip()
    max_cap = get_int("  Max Capacity   : ")
    if max_cap is None: press_enter(); return

    courses.append(Course(course_id=cid, name=name, teacher_id=teacher_id, max_capacity=max_cap))
    print(f"\n  [✓] Course '{name}' added successfully.")
    press_enter()


def list_courses():
    print(f"\n  ── Course List ({len(courses)}) ──\n")
    if not courses:
        print("  No courses found."); press_enter(); return

    print(f"  {'ID':<6}  {'Course Name':<25}  {'Teacher ID':<10}  {'Enrolled':>8}  {'Capacity':>8}")
    print_line("-", 63)
    for c in courses:
        print(f"  {c.course_id:<6}  {c.name:<25}  {c.teacher_id:<10}  {c.enrolled:>8}  {c.max_capacity:>8}")
    press_enter()


# ─── Enrollment Functions ─────────────────────────────────────

def enroll_student():
    print("\n  ── Enroll Student in Course ──")
    sid = input("  Student ID : ").strip()
    s = find_student(sid)
    if not s:
        print("  [!] Student not found."); press_enter(); return

    cid = get_int("  Course ID  : ")
    if cid is None: press_enter(); return
    c = find_course(cid)
    if not c:
        print("  [!] Course not found."); press_enter(); return

    if cid in s.courses:
        print("  [!] Already enrolled in this course."); press_enter(); return
    if c.enrolled >= c.max_capacity:
        print("  [!] Course is at full capacity."); press_enter(); return

    s.courses.append(cid)
    c.enrolled += 1
    print(f"\n  [✓] {s.name} enrolled in '{c.name}'.")
    press_enter()


def unenroll_student():
    print("\n  ── Unenroll Student from Course ──")
    sid = input("  Student ID : ").strip()
    s = find_student(sid)
    if not s:
        print("  [!] Student not found."); press_enter(); return

    cid = get_int("  Course ID  : ")
    if cid is None: press_enter(); return

    if cid not in s.courses:
        print("  [!] Student is not enrolled in that course."); press_enter(); return

    s.courses.remove(cid)
    c = find_course(cid)
    if c:
        c.enrolled = max(0, c.enrolled - 1)
    print("  [✓] Unenrolled successfully.")
    press_enter()


# ─── Reports ──────────────────────────────────────────────────

def report_top_students():
    if not students:
        print("\n  No students."); press_enter(); return

    sorted_students = sorted(students, key=lambda s: s.gpa, reverse=True)
    print("\n  ── Top Students by GPA ──\n")
    print(f"  {'Rank':>4}  {'Name':<25}  {'GPA':>5}  {'Grade':>4}")
    print_line("-", 43)
    for i, s in enumerate(sorted_students[:10], start=1):
        print(f"  {i:>4}  {s.name:<25}  {s.gpa:.2f}  {s.grade:>4}")
    press_enter()


def report_course_capacity():
    print("\n  ── Course Capacity Report ──\n")
    if not courses:
        print("  No courses."); press_enter(); return

    for c in courses:
        pct = int(c.enrolled / c.max_capacity * 100) if c.max_capacity > 0 else 0
        filled = pct // 5
        bar = "#" * filled + "." * (20 - filled)
        print(f"  [{pct:>3}%] {c.name:<25}  {c.enrolled}/{c.max_capacity} seats")
        print(f"         [{bar}]\n")
    press_enter()


def report_summary():
    print("\n  ══════════════════════════════════")
    print("       SCHOOL SUMMARY REPORT")
    print("  ══════════════════════════════════")
    print(f"  Total Students : {len(students)}")
    print(f"  Total Teachers : {len(teachers)}")
    print(f"  Total Courses  : {len(courses)}")

    if students:
        avg_gpa = sum(s.gpa for s in students) / len(students)
        print(f"  Average GPA    : {avg_gpa:.2f}")

    total_enrolled = sum(c.enrolled for c in courses)
    print(f"  Total Enrolled : {total_enrolled} seat(s)")
    print("  ══════════════════════════════════")
    press_enter()


# ─── Sub-menus ────────────────────────────────────────────────

def menu_students():
    while True:
        clear_screen()
        print("\n  ┌─────────────────────────────┐")
        print("  │      STUDENT MANAGEMENT     │")
        print("  └─────────────────────────────┘")
        print("  1. Add Student")
        print("  2. List All Students")
        print("  3. Search Student")
        print("  4. Update GPA")
        print("  5. Delete Student")
        print("  6. Enroll in Course")
        print("  7. Unenroll from Course")
        print("  0. Back")
        choice = input("  > ").strip()

        if   choice == "1": add_student()
        elif choice == "2": list_students()
        elif choice == "3": search_student()
        elif choice == "4": update_gpa()
        elif choice == "5": delete_student()
        elif choice == "6": enroll_student()
        elif choice == "7": unenroll_student()
        elif choice == "0": break
        else: print("  [!] Invalid choice."); press_enter()


def menu_teachers():
    while True:
        clear_screen()
        print("\n  ┌─────────────────────────────┐")
        print("  │      TEACHER MANAGEMENT     │")
        print("  └─────────────────────────────┘")
        print("  1. Add Teacher")
        print("  2. List All Teachers")
        print("  3. Delete Teacher")
        print("  0. Back")
        choice = input("  > ").strip()

        if   choice == "1": add_teacher()
        elif choice == "2": list_teachers()
        elif choice == "3": delete_teacher()
        elif choice == "0": break
        else: print("  [!] Invalid choice."); press_enter()


def menu_courses():
    while True:
        clear_screen()
        print("\n  ┌─────────────────────────────┐")
        print("  │      COURSE MANAGEMENT      │")
        print("  └─────────────────────────────┘")
        print("  1. Add Course")
        print("  2. List All Courses")
        print("  0. Back")
        choice = input("  > ").strip()

        if   choice == "1": add_course()
        elif choice == "2": list_courses()
        elif choice == "0": break
        else: print("  [!] Invalid choice."); press_enter()


def menu_reports():
    while True:
        clear_screen()
        print("\n  ┌─────────────────────────────┐")
        print("  │          REPORTS            │")
        print("  └─────────────────────────────┘")
        print("  1. Top Students by GPA")
        print("  2. Course Capacity Report")
        print("  3. Summary Report")
        print("  0. Back")
        choice = input("  > ").strip()

        if   choice == "1": report_top_students()
        elif choice == "2": report_course_capacity()
        elif choice == "3": report_summary()
        elif choice == "0": break
        else: print("  [!] Invalid choice."); press_enter()


# ─── Seed Demo Data ───────────────────────────────────────────

def seed_demo_data():
    teachers.extend([
        Teacher(id="T001", name="Dr. Alice Johnson", age=45, subject="Mathematics", salary=5500.0),
        Teacher(id="T002", name="Mr. Robert Chen",   age=38, subject="Physics",     salary=4800.0),
    ])
    courses.extend([
        Course(course_id=101, name="Advanced Mathematics", teacher_id="T001", max_capacity=30),
        Course(course_id=102, name="Physics 101",          teacher_id="T002", max_capacity=25),
        Course(course_id=103, name="English Literature",   teacher_id="T001", max_capacity=20),
    ])
    students.extend([
        Student(id="S001", name="Emma Wilson", age=16, grade="10A", gpa=3.80),
        Student(id="S002", name="Liam Patel",  age=15, grade="9B",  gpa=3.20),
        Student(id="S003", name="Sophia Tan",  age=17, grade="11A", gpa=3.95),
    ])


# ─── Main ─────────────────────────────────────────────────────

def main():
    seed_demo_data()
    while True:
        clear_screen()
        print()
        print_line("=", 38)
        print("    MINI SCHOOL MANAGEMENT SYSTEM")
        print_line("=", 38)
        print("  1.  Student Management")
        print("  2.  Teacher Management")
        print("  3.  Course Management")
        print("  4.  Reports")
        print("  0.  Exit")
        print_line("-", 38)
        choice = input("  Choice: ").strip()

        if   choice == "1": menu_students()
        elif choice == "2": menu_teachers()
        elif choice == "3": menu_courses()
        elif choice == "4": menu_reports()
        elif choice == "0":
            print("\n  Goodbye!\n"); sys.exit(0)
        else:
            print("  [!] Invalid choice."); press_enter()


if __name__ == "__main__":
    main()
