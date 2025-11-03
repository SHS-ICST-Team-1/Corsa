# Usage Examples

## Quick Start

### 1. Basic Usage (Interactive Mode)

Run the interactive application:

```bash
python course_analyzer.py
```

This will guide you through:
- Uploading a course PDF (optional)
- Answering 10 interest questions
- Entering graduation requirements
- Viewing personalized course recommendations

### 2. Automated Demo (Non-Interactive)

See the system in action without manual input:

```bash
python demo.py
```

### 3. Run Tests

Verify all components are working:

```bash
python test_analyzer.py
```

## Advanced Usage

### Using with OpenAI API

For AI-powered recommendations, set your OpenAI API key:

```bash
export OPENAI_API_KEY='sk-your-api-key-here'
python course_analyzer.py
```

Or create a `.env` file:
```
OPENAI_API_KEY=sk-your-api-key-here
```

### Creating Sample PDFs

Generate a sample course catalog PDF:

```bash
# Install reportlab first
pip install reportlab

# Generate sample PDF
python create_sample_pdf.py
```

Then use it with the analyzer:
```bash
python course_analyzer.py
# When prompted, enter: sample_courses.pdf
```

### Programmatic Usage

You can also use the components programmatically:

```python
from course_analyzer import (
    PDFParser,
    InterestQuestionnaire,
    CourseTokenizer,
    AIEvaluator
)

# Parse courses
parser = PDFParser()
courses = parser.parse_pdf("your_courses.pdf")

# Define interests and requirements
interest_scores = {'Computer Science': 9, 'Mathematics': 6}
requirements = {'total_credits': 120, 'Computer Science': 12}

# Get recommendations
evaluator = AIEvaluator()
recommendations = evaluator.evaluate_courses(
    courses,
    interest_scores,
    requirements,
    top_n=5
)

# Display results
for rec in recommendations:
    print(f"{rec['code']}: {rec['name']} (Score: {rec['score']})")
```

## Example Interactive Session

```
============================================================
COURSE SELECTION FUTURISTIC AI ANALYZER 3000
============================================================

Step 0: Upload Course Selection Book
------------------------------------------------------------
Enter path to course selection PDF (press Enter to use sample data): 

Step 1: Parsing Course Data
------------------------------------------------------------
Loaded 10 courses from the database.

Step 2: Interest Assessment
------------------------------------------------------------
Please answer the following questions to help us understand your interests.

Question 1/10: Do you enjoy working with technology and computers?
Valid answers: yes, no
Your answer: yes

Question 2/10: Are you interested in solving mathematical problems?
Valid answers: yes, no
Your answer: yes

...

Your Interest Scores:
  Computer Science: 9
  Mathematics: 6
  Physics: 4

Step 2.5: Graduation Requirements
------------------------------------------------------------
Please provide information about your graduation requirements.

Total credits required for graduation: 120

How many credits do you need in each category?
Computer Science: 12
Mathematics: 8
English: 6
...

Step 3: Processing Course Data
------------------------------------------------------------
Processed course data: 205 tokens

Step 4: AI Course Evaluation
------------------------------------------------------------
Analyzing courses based on your interests and requirements...

============================================================
RECOMMENDED COURSES
============================================================

1. CS101: Introduction to Computer Science
   Score: 135.0
   Reasons:
     - Matches your interest in Computer Science (score: 90.0)
     - Fulfills Computer Science requirement (12 credits needed)
     - No prerequisites required
     - Foundational course

...
```

## Troubleshooting

### Missing Dependencies

If you see warnings about missing libraries:

```bash
pip install -r requirements.txt
```

### PDF Parsing Issues

If PDF parsing fails:
- Check that the PDF file exists and is readable
- Try using the sample data (just press Enter when prompted)
- Verify pdfplumber is installed: `pip install pdfplumber`

### OpenAI API Errors

If OpenAI integration fails:
- The system will automatically fall back to rule-based recommendations
- Check that your API key is valid
- Ensure you have API credits available

### Network Issues

The system works offline:
- Sample course data is built-in
- Rule-based recommendations don't require internet
- Only OpenAI integration requires network access
