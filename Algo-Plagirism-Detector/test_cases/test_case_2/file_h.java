/**
 * Code in a different programming language.
 */

public class Student {
    private int studentId;
    private String name;
    private java.util.Map<String, Integer> grades;
    
    /**
     * Initialize a student with ID, name, and grades.
     */
    public Student(int studentId, String name) {
        this.studentId = studentId;
        this.name = name;
        this.grades = new java.util.HashMap<>();
    }
    
    /**
     * Add a grade for a course.
     */
    public void addGrade(String course, int grade) {
        this.grades.put(course, grade);
    }
    
    /**
     * Get the grade for a course.
     */
    public Integer getGrade(String course) {
        return this.grades.get(course);
    }
    
    /**
     * Calculate the GPA.
     */
    public double getGpa() {
        if (this.grades.isEmpty()) {
            return 0.0;
        }
        
        int total = 0;
        for (int grade : this.grades.values()) {
            total += grade;
        }
        
        return (double) total / this.grades.size();
    }
    
    @Override
    public String toString() {
        return String.format("Student(id=%d, name=%s, gpa=%.2f)", 
                            this.studentId, this.name, this.getGpa());
    }
}

public class Course {
    private String courseId;
    private String name;
    private int credits;
    private java.util.List<Student> students;
    
    /**
     * Initialize a course with ID, name, and credits.
     */
    public Course(String courseId, String name, int credits) {
        this.courseId = courseId;
        this.name = name;
        this.credits = credits;
        this.students = new java.util.ArrayList<>();
    }
    
    /**
     * Add a student to the course.
     */
    public void addStudent(Student student) {
        this.students.add(student);
    }
    
    /**
     * Calculate the average grade for the course.
     */
    public double getAverageGrade() {
        if (this.students.isEmpty()) {
            return 0.0;
        }
        
        double total = 0.0;
        int count = 0;
        
        for (Student student : this.students) {
            Integer grade = student.getGrade(this.courseId);
            if (grade != null) {
                total += grade;
                count++;
            }
        }
        
        return count > 0 ? total / count : 0.0;
    }
    
    @Override
    public String toString() {
        return String.format("Course(id=%s, name=%s, credits=%d)", 
                            this.courseId, this.name, this.credits);
    }
}

public class Main {
    public static void main(String[] args) {
        // Create students
        Student alice = new Student(1, "Alice");
        Student bob = new Student(2, "Bob");
        Student charlie = new Student(3, "Charlie");
        
        // Create courses
        Course math = new Course("MATH101", "Introduction to Mathematics", 3);
        Course physics = new Course("PHYS101", "Introduction to Physics", 4);
        
        // Add students to courses
        math.addStudent(alice);
        math.addStudent(bob);
        physics.addStudent(alice);
        physics.addStudent(charlie);
        
        // Add grades
        alice.addGrade("MATH101", 85);
        alice.addGrade("PHYS101", 90);
        bob.addGrade("MATH101", 75);
        charlie.addGrade("PHYS101", 80);
        
        // Print information
        System.out.println(alice);
        System.out.println(bob);
        System.out.println(charlie);
        System.out.println("Average grade for " + math.getName() + ": " + math.getAverageGrade());
        System.out.println("Average grade for " + physics.getName() + ": " + physics.getAverageGrade());
    }
}
