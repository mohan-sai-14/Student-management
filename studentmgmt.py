import tkinter as tk
from tkinter import messagebox, simpledialog, font
from datetime import datetime

class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role

class Student:
    def __init__(self, student_id, name, dob):
        self.student_id = student_id
        self.name = name
        self.dob = dob
        self.courses = {}        # course_id -> grade
        self.attendance = {}     # course_id -> {date: status}
        self.fees_paid = 0
        self.fees_due = 15000     # default fees

class Course:
    def __init__(self, course_id, title):
        self.course_id = course_id
        self.title = title

class SMSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("500x450")
        self.root.resizable(False, False)

        self.custom_font = font.Font(family="Segoe UI", size=11)
        self.title_font = font.Font(family="Segoe UI", size=16, weight="bold")

        # Preloaded users
        self.users = {
            'admin': User('admin', 'Admin'),
            'teacher1': User('teacher1', 'Teacher'),
            'student1': User('student1', 'Student'),
            'student2': User('student2', 'Student'),
            'student3': User('student3', 'Student')
        }
        # Preloaded students (Indian names)
        self.students = {
            'student1': Student('student1', 'Rohit ', '2005-03-25'),
            'student2': Student('student2', 'Anjali ', '2004-08-17'),
            'student3': Student('student3', 'Amit ', '2005-12-05'),
        }
        # Preloaded courses (Indian context)
        self.courses = {
            'MATH101': Course('MATH101', 'Mathematics'),
            'ENG102': Course('ENG102', 'English Literature'),
            'PHY103': Course('PHY103', 'Physics'),
        }

        # Preload some attendance and grades
        self.students['student1'].attendance = {
            'MATH101': {'2025-08-01': 'P', '2025-08-02': 'A'},
            'ENG102': {'2025-08-01': 'P'}
        }
        self.students['student1'].courses = {'MATH101': 'A', 'ENG102': 'B+'}
        self.students['student1'].fees_paid = 10000

        self.students['student2'].attendance = {
            'PHY103': {'2025-08-01': 'P', '2025-08-02': 'P'}
        }
        self.students['student2'].courses = {'PHY103': 'A-'}
        self.students['student2'].fees_paid = 12000

        self.logged_in_user = None

        self.login_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login_screen(self):
        self.clear_window()
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(frame, text="Student Management System", font=self.title_font).pack(pady=(0, 20))

        tk.Label(frame, text="Username:", font=self.custom_font).pack(anchor='w')
        self.username_entry = tk.Entry(frame, font=self.custom_font)
        self.username_entry.pack(fill='x', pady=(0,15))

        login_btn = tk.Button(frame, text="Login", font=self.custom_font, bg="#4CAF50", fg="white", command=self.handle_login)
        login_btn.pack(fill='x')

        self.username_entry.focus()

    def handle_login(self):
        username = self.username_entry.get().strip()
        user = self.users.get(username)
        if user:
            self.logged_in_user = user
            messagebox.showinfo("Login Success", f"Welcome {user.role} '{user.username}'")
            self.show_main_menu()
        else:
            messagebox.showerror("Login Failed", "User not found")

    def show_main_menu(self):
        self.clear_window()
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True, fill='both')

        role = self.logged_in_user.role
        tk.Label(frame, text=f"{role} Menu", font=self.title_font).pack(pady=(0, 15))

        btn_opts = {'font': self.custom_font, 'width': 25, 'pady': 7}

        if role == 'Admin':
            tk.Button(frame, text="Add Student", bg="#2196F3", fg="white", command=self.add_student, **btn_opts).pack(pady=3)
            tk.Button(frame, text="View Students", bg="#2196F3", fg="white", command=self.view_students, **btn_opts).pack(pady=3)
            tk.Button(frame, text="Add Course", bg="#2196F3", fg="white", command=self.add_course, **btn_opts).pack(pady=3)
            tk.Button(frame, text="View Courses", bg="#2196F3", fg="white", command=self.view_courses, **btn_opts).pack(pady=3)
            tk.Button(frame, text="Logout", bg="#f44336", fg="white", command=self.logout, **btn_opts).pack(pady=20)

        elif role == 'Teacher':
            tk.Button(frame, text="Mark Attendance", bg="#2196F3", fg="white", command=self.mark_attendance, **btn_opts).pack(pady=3)
            tk.Button(frame, text="Record Grades", bg="#2196F3", fg="white", command=self.record_grades, **btn_opts).pack(pady=3)
            tk.Button(frame, text="View Students", bg="#2196F3", fg="white", command=self.view_students, **btn_opts).pack(pady=3)
            tk.Button(frame, text="Logout", bg="#f44336", fg="white", command=self.logout, **btn_opts).pack(pady=20)

        elif role == 'Student':
            tk.Button(frame, text="View Profile", bg="#2196F3", fg="white", command=self.view_profile, **btn_opts).pack(pady=3)
            tk.Button(frame, text="View Attendance", bg="#2196F3", fg="white", command=self.view_attendance, **btn_opts).pack(pady=3)
            tk.Button(frame, text="View Grades", bg="#2196F3", fg="white", command=self.view_grades, **btn_opts).pack(pady=3)
            tk.Button(frame, text="View Fees", bg="#2196F3", fg="white", command=self.view_fees, **btn_opts).pack(pady=3)
            tk.Button(frame, text="Logout", bg="#f44336", fg="white", command=self.logout, **btn_opts).pack(pady=20)

    def logout(self):
        self.logged_in_user = None
        messagebox.showinfo("Logout", "Logged out successfully")
        self.login_screen()

    def add_student(self):
        sid = simpledialog.askstring("Add Student", "Enter Student ID (e.g., student4):")
        if not sid:
            return
        if sid in self.students:
            messagebox.showerror("Error", "Student ID already exists")
            return
        name = simpledialog.askstring("Add Student", "Enter Student Name:")
        dob = simpledialog.askstring("Add Student", "Enter Date of Birth (YYYY-MM-DD):")
        try:
            datetime.strptime(dob, "%Y-%m-%d")
        except:
            messagebox.showerror("Error", "Invalid date format")
            return
        self.students[sid] = Student(sid, name, dob)
        self.users[sid] = User(sid, 'Student')  # auto create user for student
        messagebox.showinfo("Success", f"Student {name} added successfully")

    def view_students(self):
        if not self.students:
            messagebox.showinfo("Students", "No students found")
            return
        data = ""
        for s in self.students.values():
            data += f"ID: {s.student_id}\nName: {s.name}\nDOB: {s.dob}\n\n"
        self.popup_text("Students List", data)

    def add_course(self):
        cid = simpledialog.askstring("Add Course", "Enter Course ID (e.g., CHEM104):")
        if not cid:
            return
        if cid in self.courses:
            messagebox.showerror("Error", "Course ID already exists")
            return
        title = simpledialog.askstring("Add Course", "Enter Course Title:")
        self.courses[cid] = Course(cid, title)
        messagebox.showinfo("Success", f"Course {title} added successfully")

    def view_courses(self):
        if not self.courses:
            messagebox.showinfo("Courses", "No courses found")
            return
        data = ""
        for c in self.courses.values():
            data += f"ID: {c.course_id} - Title: {c.title}\n"
        self.popup_text("Courses List", data)

    def mark_attendance(self):
        course_id = simpledialog.askstring("Attendance", "Enter Course ID:")
        if course_id not in self.courses:
            messagebox.showerror("Error", "Invalid Course ID")
            return
        date = simpledialog.askstring("Attendance", "Enter Date (YYYY-MM-DD):")
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except:
            messagebox.showerror("Error", "Invalid date format")
            return

        for student in self.students.values():
            status = simpledialog.askstring("Attendance", f"Mark attendance for {student.name} (P/A):")
            if not status or status.upper() not in ['P', 'A']:
                status = 'A'
            student.attendance.setdefault(course_id, {})
            student.attendance[course_id][date] = status.upper()
        messagebox.showinfo("Success", "Attendance recorded")

    def record_grades(self):
        course_id = simpledialog.askstring("Grades", "Enter Course ID:")
        if course_id not in self.courses:
            messagebox.showerror("Error", "Invalid Course ID")
            return
        for student in self.students.values():
            grade = simpledialog.askstring("Grades", f"Enter grade for {student.name} (e.g., A, B+):")
            if grade:
                student.courses[course_id] = grade.upper()
        messagebox.showinfo("Success", "Grades recorded")

    def view_profile(self):
        sid = self.logged_in_user.username
        student = self.students.get(sid)
        if not student:
            messagebox.showerror("Error", "Profile not found")
            return
        data = f"ID: {student.student_id}\nName: {student.name}\nDOB: {student.dob}"
        self.popup_text("Profile", data)

    def view_attendance(self):
        sid = self.logged_in_user.username
        student = self.students.get(sid)
        if not student or not student.attendance:
            messagebox.showinfo("Attendance", "No attendance records found")
            return
        data = ""
        for course_id, records in student.attendance.items():
            data += f"Course: {course_id} - {self.courses[course_id].title}\n"
            for date, status in sorted(records.items()):
                data += f"  {date}: {'Present' if status=='P' else 'Absent'}\n"
            data += "\n"
        self.popup_text("Attendance Records", data)

    def view_grades(self):
        sid = self.logged_in_user.username
        student = self.students.get(sid)
        if not student or not student.courses:
            messagebox.showinfo("Grades", "No grades found")
            return
        data = ""
        for course_id, grade in student.courses.items():
            data += f"{course_id} - {self.courses[course_id].title}: {grade}\n"
        self.popup_text("Grades", data)

    def view_fees(self):
        sid = self.logged_in_user.username
        student = self.students.get(sid)
        if not student:
            messagebox.showerror("Error", "Profile not found")
            return
        due = student.fees_due - student.fees_paid
        data = f"Fees Paid: ₹{student.fees_paid}\nFees Due: ₹{due if due > 0 else 0}"
        self.popup_text("Fees Information", data)

    def popup_text(self, title, content):
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("450x350")
        popup.resizable(False, False)

        text = tk.Text(popup, wrap='word', font=self.custom_font)
        text.pack(padx=10, pady=10, fill='both', expand=True)
        text.insert('1.0', content)
        text.config(state='disabled')

        btn = tk.Button(popup, text="Close", font=self.custom_font, command=popup.destroy, bg="#f44336", fg="white")
        btn.pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = SMSApp(root)
    root.mainloop()
