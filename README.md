# Scholarship Eligibility Screening System

A Python-based project that screens university scholarship applications using predefined, deterministic rules.

## Project Overview

The system validates student records, checks scholarship conditions, assigns an eligibility category, calculates a score out of 100, ranks applicants, explains decisions, and generates a dated screening report.

**This project does not use AI/ML, databases, APIs, recursion, or third-party libraries.**

## Scholarship Rules

### Mandatory conditions
- CGPA must be at least 7.00.
- Attendance must be at least 75%.
- Annual family income must not exceed Rs. 5,00,000.
- Backlogs must not exceed 1.
- Enrollment status must be Active.

### Classifications
- **Highly Eligible:** All mandatory conditions pass, CGPA is at least 8.50, and attendance is at least 85%.
- **Eligible:** All mandatory conditions pass.
- **Conditionally Eligible:** CGPA is from 6.75 (inclusive) to below 7.00, and all other mandatory conditions pass.
- **Not Eligible:** One or more critical mandatory conditions fail.

Additional considerations are merit (CGPA >= 8.50), attendance >= 90%, extracurricular achievement, first-generation learner status, and disability status.

## Scoring Method

The project uses a transparent, custom score out of 100. This is a ranking aid designed for this project and is not an official university award formula.

| Component | Maximum |
|---|---:|
| Academic performance | 40 |
| Attendance | 20 |
| Financial condition | 20 |
| Backlog record | 10 |
| Additional considerations | 10 |
| **Total** | **100** |

## Project Structure

```text
Scholarship-Eligibility-Screening-System/
│
├── main.py
├── data/
│   └── sample_students.py
├── reports/
│   └── .gitkeep
├── README.md
└── .gitignore
```

## Requirements

- Python 3.8 or later
- No external package installation is required.

## How to Run

1. Download or clone this repository.
2. Open the project folder in VS Code or a terminal.
3. Run:

```bash
python main.py
```

4. Select an option from the menu.
5. Choose option 10 to generate and save a screening report in the `reports` folder.

## Python Concepts Demonstrated

- Variables, data types and operators
- Comparison and logical operators
- `if`, `elif` and `else`
- `for` and `while` loops
- Lists, tuples and dictionaries
- String methods: `strip()`, `lower()`, `upper()`, `title()`
- User-defined functions
- Function arguments and return values
- Lambda functions for ranking
- `datetime` module for date and time
- File handling for report generation
- Input validation and exception handling

## Important Notes

- Sample records are stored in a list of dictionaries in `data/sample_students.py`.
- New applications added while the program is running are held in memory. They are not permanently stored after the program closes.
- Generated text reports are saved in `reports/`.
- The scoring formula is illustrative. A university should approve its own scoring and award policy before using the system for actual scholarship decisions.

## Future Improvements

- Add permanent file-based storage using Python's built-in CSV or JSON modules.
- Add a graphical user interface.
- Export reports in additional formats.

## Author

Add your name, roll number, course and institution here.
