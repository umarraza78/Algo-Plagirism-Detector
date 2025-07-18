"""
Copy of E with large block of code moved/reordered.
"""

def main():
    """Main function to test the classes."""
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


class Course:
    """Class representing a course."""
    
    def __init__(self, course_id, name, credits):
        """Initialize a course with ID, name, and credits."""
        self.course_id = course_id
        self.name = name
        self.credits = credits
        self.students = []
    
    def add_student(self, student):
        """Add a student to the course."""
        self.students.append(student)
    
    def get_average_grade(self):
        """Calculate the average grade for the course."""
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
    
    def __str__(self):
        """String representation of the course."""
        return f"Course(id={self.course_id}, name={self.name}, credits={self.credits})"


class Student:
    """Class representing a student."""
    
    def __init__(self, student_id, name, grades=None):
        """Initialize a student with ID, name, and grades."""
        self.student_id = student_id
        self.name = name
        self.grades = grades or {}
    
    def add_grade(self, course, grade):
        """Add a grade for a course."""
        self.grades[course] = grade
    
    def get_grade(self, course):
        """Get the grade for a course."""
        return self.grades.get(course, None)
    
    def get_gpa(self):
        """Calculate the GPA."""
        if not self.grades:
            return 0.0
        
        total = sum(self.grades.values())
        return total / len(self.grades)
    
    def __str__(self):
        """String representation of the student."""
        return f"Student(id={self.student_id}, name={self.name}, gpa={self.get_gpa():.2f})"


if __name__ == "__main__":
    main()
