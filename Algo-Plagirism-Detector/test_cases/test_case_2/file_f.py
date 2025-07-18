"""
Copy of E with comments added/removed, whitespace changes.
"""

# Student class for managing student information
class Student:
    # Initialize a student with ID, name, and grades
    def __init__(self, student_id, name, grades=None):
        self.student_id = student_id
        self.name = name
        self.grades = grades or {}
    
    # Add a grade for a course
    def add_grade(self, course, grade):
        self.grades[course] = grade
    
    # Get the grade for a course
    def get_grade(self, course):
        return self.grades.get(course, None)
    
    # Calculate the GPA
    def get_gpa(self):
        if not self.grades:
            return 0.0
        
        total = sum(self.grades.values())
        return total / len(self.grades)
    
    # String representation of the student
    def __str__(self):
        return f"Student(id={self.student_id}, name={self.name}, gpa={self.get_gpa():.2f})"


# Course class for managing course information
class Course:
    # Initialize a course with ID, name, and credits
    def __init__(self, course_id, name, credits):
        self.course_id = course_id
        self.name = name
        self.credits = credits
        self.students = []
    
    # Add a student to the course
    def add_student(self, student):
        self.students.append(student)
    
    # Calculate the average grade for the course
    def get_average_grade(self):
        if not self.students:
            return 0.0
        
        total = 0.0
        count = 0
        
        for student in self.students:
            grade = student.get_grade(self.course_id)
            if grade is not None:
                total += grade
                count += 1
        
        return total / count if count > 0 else 0.0
    
    # String representation of the course
    def __str__(self):
        return f"Course(id={self.course_id}, name={self.name}, credits={self.credits})"


def main():
    # Create students
    alice = Student(1, "Alice")
    bob = Student(2, "Bob")
    charlie = Student(3, "Charlie")
    
    # Create courses
    math = Course("MATH101", "Introduction to Mathematics", 3)
    physics = Course("PHYS101", "Introduction to Physics", 4)
    
    # Add students to courses
    math.add_student(alice)
    math.add_student(bob)
    physics.add_student(alice)
    physics.add_student(charlie)
    
    # Add grades
    alice.add_grade("MATH101", 85)
    alice.add_grade("PHYS101", 90)
    bob.add_grade("MATH101", 75)
    charlie.add_grade("PHYS101", 80)
    
    # Print information
    print(alice)
    print(bob)
    print(charlie)
    print(f"Average grade for {math.name}: {math.get_average_grade()}")
    print(f"Average grade for {physics.name}: {physics.get_average_grade()}")


if __name__ == "__main__":
    main()
