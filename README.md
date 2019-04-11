# Questions-Generator
Generate a list of question based on total marks and weightage

### How to use
```bash

# simple run
# will take input from user in the run
python question_generator.py

# to run from a file
# takes file input in json format only
python question_generator.py -f 'complete path to the file'
python question_generator.py -file 'complete path to the file'

# to run sample input
# or changes made in inputs file of repo
python question_generator.py -f default
python question_generator.py -file default

```

### Example
```bash

total_questions = 10
question_store = [
	{"question": "Q1", "difficulty": "easy", "marks": "1"},
	{"question": "Q2", "difficulty": "easy", "marks": "2"},
	{"question": "Q3", "difficulty": "medium", "marks": "2"},
	{"question": "Q4", "difficulty": "hard", "marks": "9"},
	{"question": "Q5", "difficulty": "easy", "marks": "3"},
	{"question": "Q6", "difficulty": "hard", "marks": "7"},
	{"question": "Q7", "difficulty": "medium", "marks": "3"},
	{"question": "Q8", "difficulty": "easy", "marks": "3"},
	{"question": "Q9", "difficulty": "medium", "marks": "5"},
	{"question": "Q10", "difficulty": "hard", "marks": "5"}
]

# question_paper_settings
total_marks = 20
difficulty['easy'] = 25
difficulty['medium'] = 50
difficulty['hard'] = 25

# Output
# Selected Question - Q2 , Q5 , Q3 , Q7 , Q9 , Q10

```

*Note: Python 3.7+ has ordered dict by default and will give sequential questions
