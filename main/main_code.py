"""
Scholarship Eligibility Screening System
A deterministic, rule-based Python project.
Uses only Python's standard library.
"""

from datetime import datetime
from data.sample_students import students

# Scholarship rules
MIN_CGPA = 7.00
MIN_ATTENDANCE = 75
MAX_INCOME = 500000
MAX_BACKLOGS = 1
CONDITIONAL_CGPA = 6.75

# A tuple is used to store the mandatory rule names.
MANDATORY_RULES = (
    "Academic", "Attendance", "Family income", "Backlogs", "Enrollment"
)


def validate_student(student):
    """Return a list of data validation errors."""
    errors = []

    if not student.get("student_id") or not student["student_id"].strip():
        errors.append("Student ID cannot be blank.")

    if not student.get("name") or not student["name"].strip():
        errors.append("Student name cannot be blank.")

    if not student.get("programme") or not student["programme"].strip():
        errors.append("Programme cannot be blank.")

    if not isinstance(student.get("semester"), int) or student["semester"] < 1:
        errors.append("Semester must be a positive whole number.")

    if not isinstance(student.get("cgpa"), (int, float)) or not 0 <= student["cgpa"] <= 10:
        errors.append("CGPA must be between 0 and 10.")

    if not isinstance(student.get("attendance"), (int, float)) or not 0 <= student["attendance"] <= 100:
        errors.append("Attendance must be between 0 and 100.")

    if not isinstance(student.get("family_income"), (int, float)) or student["family_income"] < 0:
        errors.append("Family income cannot be negative.")

    if not isinstance(student.get("backlogs"), int) or student["backlogs"] < 0:
        errors.append("Backlogs must be a non-negative whole number.")

    if not student.get("category") or not student["category"].strip():
        errors.append("Category cannot be blank.")

    for field in ("extracurricular", "first_generation", "disability"):
        if not isinstance(student.get(field), bool):
            errors.append(field.replace("_", " ").title() + " must be Yes or No.")

    if str(student.get("enrollment", "")).strip().title() not in ("Active", "Inactive"):
        errors.append("Enrollment must be Active or Inactive.")

    return errors


def check_academic_eligibility(student):
    return student["cgpa"] >= MIN_CGPA


def check_attendance_eligibility(student):
    return student["attendance"] >= MIN_ATTENDANCE


def check_income_eligibility(student):
    return student["family_income"] <= MAX_INCOME


def check_backlog_eligibility(student):
    return student["backlogs"] <= MAX_BACKLOGS


def check_enrollment(student):
    return student["enrollment"].strip().title() == "Active"


def calculate_score(student):
    """
    Calculate a transparent score out of 100.
    The score is a project-defined ranking aid, not an official award formula.
    """
    academic_points = (student["cgpa"] / 10) * 40
    attendance_points = (student["attendance"] / 100) * 20

    income_ratio = student["family_income"] / MAX_INCOME
    income_points = max(0, 20 * (1 - income_ratio))

    if student["backlogs"] == 0:
        backlog_points = 10
    elif student["backlogs"] == 1:
        backlog_points = 5
    else:
        backlog_points = 0

    additional_points = 0
    if student["cgpa"] >= 8.50:
        additional_points += 3
    if student["attendance"] >= 90:
        additional_points += 2
    if student["extracurricular"]:
        additional_points += 2
    if student["first_generation"] or student["disability"]:
        additional_points += 3

    total = academic_points + attendance_points + income_points
    total += backlog_points + additional_points

    return round(total, 2)


def calculate_eligibility(student):
    """Screen one valid student and return a result dictionary."""
    academic = check_academic_eligibility(student)
    attendance = check_attendance_eligibility(student)
    income = check_income_eligibility(student)
    backlogs = check_backlog_eligibility(student)
    enrollment = check_enrollment(student)

    checks = {
        "Academic": academic,
        "Attendance": attendance,
        "Family income": income,
        "Backlogs": backlogs,
        "Enrollment": enrollment
    }

    # All mandatory conditions must pass for normal eligibility.
    all_mandatory_pass = (
        academic and attendance and income and backlogs and enrollment
    )

    # Conditional rule follows the example in the project brief:
    # CGPA is marginally below 7.00, while every other mandatory rule passes.
    other_conditions_pass = attendance and income and backlogs and enrollment
    conditional_case = (
        CONDITIONAL_CGPA <= student["cgpa"] < MIN_CGPA
        and other_conditions_pass
    )

    if all_mandatory_pass and student["cgpa"] >= 8.50 and student["attendance"] >= 85:
        status = "Highly Eligible"
    elif all_mandatory_pass:
        status = "Eligible"
    elif conditional_case:
        status = "Conditionally Eligible"
    else:
        status = "Not Eligible"

    score = calculate_score(student)

    return {
        "student": student,
        "checks": checks,
        "status": status,
        "score": score
    }


def generate_explanation(result):
    """Create a readable explanation of the student's screening result."""
    student = result["student"]
    checks = result["checks"]
    explanation = []

    for rule_name, passed in checks.items():
        if passed:
            explanation.append(rule_name + " requirement: PASS.")
        else:
            explanation.append(rule_name + " requirement: FAIL.")

    if result["status"] == "Highly Eligible":
        explanation.append(
            "All mandatory conditions are satisfied. The student also has "
            "CGPA of at least 8.50 and attendance of at least 85%."
        )
    elif result["status"] == "Eligible":
        explanation.append("All mandatory scholarship conditions are satisfied.")
    elif result["status"] == "Conditionally Eligible":
        explanation.append(
            "CGPA is between 6.75 and below 7.00. All other mandatory "
            "conditions are satisfied. The application needs special review."
        )
    else:
        failed_rules = [name for name, passed in checks.items() if not passed]
        explanation.append(
            "The student is not eligible because these mandatory conditions "
            "were not satisfied: " + ", ".join(failed_rules) + "."
        )

    if student["cgpa"] >= 8.50:
        explanation.append("Merit consideration: Yes.")
    else:
        explanation.append("Merit consideration: No.")

    if student["attendance"] >= 90:
        explanation.append("High attendance consideration: Yes.")

    if student["extracurricular"]:
        explanation.append("Extracurricular achievement: Yes.")

    if student["first_generation"] or student["disability"]:
        explanation.append("Special consideration: Yes.")

    return explanation


def display_students():
    """Display all stored application records."""
    print("\n" + "=" * 105)
    print("STUDENT APPLICATION RECORDS")
    print("=" * 105)

    if not students:
        print("No applications found.")
        return

    for student in students:
        print(
            f'{student["student_id"]} | {student["name"]} | '
            f'{student["programme"]} | Semester {student["semester"]} | '
            f'CGPA: {student["cgpa"]} | Attendance: {student["attendance"]}%'
        )


def screen_one_student(student):
    """Validate and screen one student."""
    errors = validate_student(student)

    print("\nStudent:", student.get("name", "Unknown"))
    if errors:
        print("DATA VALIDATION FAILED:")
        for error in errors:
            print("-", error)
        return None

    result = calculate_eligibility(student)
    print("Eligibility:", result["status"])
    print("Eligibility score:", result["score"], "/ 100")
    print("Explanation:")
    for item in generate_explanation(result):
        print("-", item)

    return result


def screen_all_students():
    """Screen every valid application and return all screening results."""
    results = []
    invalid_count = 0

    for student in students:
        errors = validate_student(student)
        if errors:
            invalid_count += 1
            print("\nInvalid record:", student.get("student_id", "Unknown"))
            for error in errors:
                print("-", error)
        else:
            results.append(calculate_eligibility(student))

    print("\nScreening completed.")
    print("Valid applications:", len(results))
    print("Invalid applications:", invalid_count)
    return results


def search_student():
    """Search by student ID or student name."""
    search_value = input("Enter student ID or name: ").strip().lower()

    found = False
    for student in students:
        if (search_value == student["student_id"].lower()
                or search_value in student["name"].lower()):
            screen_one_student(student)
            found = True

    if not found:
        print("No matching student found.")


def display_by_status(results, required_status):
    """Display applicants belonging to a particular status."""
    found = False
    print("\n" + required_status.upper())
    print("-" * 75)

    for result in results:
        if result["status"] == required_status:
            student = result["student"]
            print(
                student["student_id"], "|", student["name"],
                "| Score:", result["score"]
            )
            found = True

    if not found:
        print("No students in this category.")


def rank_eligible_students(results):
    """
    Rank Highly Eligible, Eligible and Conditionally Eligible applicants.
    Not Eligible applicants are excluded from the ranking.
    Lambda is used to sort by score in descending order.
    """
    ranked = [
        result for result in results
        if result["status"] != "Not Eligible"
    ]

    ranked.sort(key=lambda item: item["score"], reverse=True)

    print("\nRANKING OF APPLICANTS")
    print("=" * 85)

    if not ranked:
        print("No eligible applicants to rank.")
        return

    for position, result in enumerate(ranked, start=1):
        student = result["student"]
        print(
            position, ".", student["name"],
            "| ID:", student["student_id"],
            "| Status:", result["status"],
            "| Score:", result["score"]
        )


def generate_report(all_results=None):
    """Generate a consolidated report and save it as a text file."""
    if all_results is None:
        all_results = screen_all_students()

    now = datetime.now()
    report_lines = []

    report_lines.append("=" * 90)
    report_lines.append("UNIVERSITY SCHOLARSHIP ELIGIBILITY SCREENING REPORT")
    report_lines.append("=" * 90)
    report_lines.append("Generated on: " + now.strftime("%d-%m-%Y"))
    report_lines.append("Generated at: " + now.strftime("%I:%M:%S %p"))
    report_lines.append("Total stored applications: " + str(len(students)))
    report_lines.append("Valid applications screened: " + str(len(all_results)))
    report_lines.append("")

    counts = {
        "Highly Eligible": 0,
        "Eligible": 0,
        "Conditionally Eligible": 0,
        "Not Eligible": 0
    }

    for result in all_results:
        counts[result["status"]] += 1

    report_lines.append("ELIGIBILITY SUMMARY")
    for status, count in counts.items():
        report_lines.append(status + ": " + str(count))

    report_lines.append("")
    report_lines.append("DETAILED APPLICANT RESULTS")
    report_lines.append("-" * 90)

    for result in all_results:
        student = result["student"]
        report_lines.append(
            f'{student["student_id"]} | {student["name"]} | '
            f'{result["status"]} | Score: {result["score"]}/100'
        )
        for explanation in generate_explanation(result):
            report_lines.append("  - " + explanation)
        report_lines.append("")

    ranked = [
        result for result in all_results
        if result["status"] != "Not Eligible"
    ]
    ranked.sort(key=lambda item: item["score"], reverse=True)

    report_lines.append("APPLICANT RANKING")
    report_lines.append("-" * 90)
    for position, result in enumerate(ranked, start=1):
        student = result["student"]
        report_lines.append(
            f'{position}. {student["name"]} ({student["student_id"]}) '
            f'- {result["score"]}/100 - {result["status"]}'
        )

    report_lines.append("")
    report_lines.append("Note: Scores are based on the project's defined scoring method.")
    report_lines.append("Final scholarship awards should be confirmed by the university.")
    report_lines.append("=" * 90)

    report_text = "\n".join(report_lines)
    print("\n" + report_text)

    filename = "reports/scholarship_report_" + now.strftime("%Y%m%d_%H%M%S") + ".txt"
    with open(filename, "w", encoding="utf-8") as report_file:
        report_file.write(report_text)

    print("\nReport saved to:", filename)


def get_yes_no(prompt):
    """Read a Yes/No answer and return True or False."""
    while True:
        answer = input(prompt + " (Yes/No): ").strip().lower()
        if answer in ("yes", "y"):
            return True
        elif answer in ("no", "n"):
            return False
        else:
            print("Please enter Yes or No.")


def add_student():
    """Accept a new application from the user."""
    print("\nENTER NEW STUDENT APPLICATION")

    student = {
        "student_id": input("Student ID: ").strip().upper(),
        "name": input("Student name: ").strip().title(),
        "programme": input("Programme: ").strip().upper(),
        "semester": 0,
        "cgpa": 0.0,
        "attendance": 0.0,
        "family_income": 0.0,
        "backlogs": 0,
        "category": input("Category: ").strip().title(),
        "extracurricular": False,
        "first_generation": False,
        "disability": False,
        "enrollment": input("Enrollment (Active/Inactive): ").strip().title()
    }

    try:
        student["semester"] = int(input("Semester: "))
        student["cgpa"] = float(input("CGPA: "))
        student["attendance"] = float(input("Attendance percentage: "))
        student["family_income"] = float(input("Annual family income: "))
        student["backlogs"] = int(input("Number of backlogs: "))
    except ValueError:
        print("Invalid number entered. Application was not added.")
        return

    student["extracurricular"] = get_yes_no("Extracurricular achievement")
    student["first_generation"] = get_yes_no("First-generation learner")
    student["disability"] = get_yes_no("Disability status")

    errors = validate_student(student)
    if errors:
        print("\nApplication not added. Please correct these errors:")
        for error in errors:
            print("-", error)
        return

    # Prevent duplicate student IDs.
    for old_student in students:
        if old_student["student_id"].lower() == student["student_id"].lower():
            print("This student ID already exists.")
            return

    students.append(student)
    print("Application added successfully.")


def display_summary(results):
    """Display counts for all four eligibility classifications."""
    counts = {
        "Highly Eligible": 0,
        "Eligible": 0,
        "Conditionally Eligible": 0,
        "Not Eligible": 0
    }

    for result in results:
        counts[result["status"]] += 1

    print("\nSCHOLARSHIP SCREENING SUMMARY")
    print("-" * 45)
    for status, count in counts.items():
        print(status + ":", count)

    print("Total valid applications:", len(results))


def main():
    """Main menu. The while loop keeps the application running."""
    while True:
        print("\n" + "=" * 55)
        print(" SCHOLARSHIP ELIGIBILITY SCREENING SYSTEM")
        print("=" * 55)
        print("1. Display All Applications")
        print("2. Screen Individual Student")
        print("3. Screen All Students")
        print("4. Search Student")
        print("5. Display Eligible Students")
        print("6. Display Highly Eligible Students")
        print("7. Rank Eligible Students")
        print("8. Display Scholarship Summary")
        print("9. Display Screening Date and Time")
        print("10. Generate and Save Screening Report")
        print("11. Add New Student Application")
        print("12. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            display_students()

        elif choice == "2":
            student_id = input("Enter student ID: ").strip().lower()
            found = False
            for student in students:
                if student["student_id"].lower() == student_id:
                    screen_one_student(student)
                    found = True
                    break
            if not found:
                print("Student ID not found.")

        elif choice == "3":
            screen_all_students()

        elif choice == "4":
            search_student()

        elif choice == "5":
            results = screen_all_students()
            for status in ("Eligible", "Highly Eligible", "Conditionally Eligible"):
                display_by_status(results, status)

        elif choice == "6":
            results = screen_all_students()
            display_by_status(results, "Highly Eligible")

        elif choice == "7":
            results = screen_all_students()
            rank_eligible_students(results)

        elif choice == "8":
            results = screen_all_students()
            display_summary(results)

        elif choice == "9":
            now = datetime.now()
            print("Screening date:", now.strftime("%d-%m-%Y"))
            print("Screening time:", now.strftime("%I:%M:%S %p"))

        elif choice == "10":
            results = screen_all_students()
            generate_report(results)

        elif choice == "11":
            add_student()

        elif choice == "12":
            print("Thank you for using the Scholarship Screening System.")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 12.")


if __name__ == "__main__":
    main()
