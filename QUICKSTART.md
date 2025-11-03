# Quick Reference Guide

## File Structure

```
Corsa/
├── course_analyzer.py      # Main application
├── demo.py                 # Non-interactive demo
├── test_analyzer.py        # Component tests
├── create_sample_pdf.py    # PDF generator utility
├── requirements.txt        # Python dependencies
├── README.md              # Full documentation
├── USAGE.md               # Usage examples
├── .gitignore             # Git ignore rules
└── QUICKSTART.md          # This file
```

## Quick Start Commands

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the interactive application
python course_analyzer.py

# 3. Or run the automated demo
python demo.py

# 4. Run tests
python test_analyzer.py
```

## What Each Component Does

### Step 0: Upload Course Selection Book
- User provides a PDF path or uses sample data
- **File**: PDFParser class in course_analyzer.py

### Step 1: PDF Parser
- Extracts course information from PDF
- Falls back to 10 sample courses if PDF unavailable
- **File**: PDFParser class in course_analyzer.py

### Step 2: 20 Questions System
- 10 questions about interests and preferences
- Calculates weighted scores for each subject category
- **File**: InterestQuestionnaire class in course_analyzer.py

### Step 2.5: Graduation Requirements
- Collects total credits needed
- Collects credits needed per category
- Tracks completed credits
- **File**: GraduationRequirements class in course_analyzer.py

### Step 3: Data Tokenizer
- Converts course data to structured text format
- Counts tokens for AI processing
- **File**: CourseTokenizer class in course_analyzer.py

### Step 4: AI Evaluation
- Analyzes courses using AI (OpenAI) or rule-based system
- Generates top 5 course recommendations
- Provides detailed reasoning for each recommendation
- **File**: AIEvaluator class in course_analyzer.py

## Key Features

✓ **No Setup Required**: Works with sample data out of the box
✓ **Graceful Fallbacks**: Continues working even if dependencies are missing
✓ **Dual Recommendation Modes**: AI-powered (with API key) or rule-based
✓ **Offline Capable**: Rule-based system works without internet
✓ **Extensible**: Easy to add more courses, questions, or evaluation criteria

## Sample Output

```
RECOMMENDED COURSES
------------------------------------------------------------

1. CS101: Introduction to Computer Science
   Score: 135.0
   Reasons:
     - Matches your interest in Computer Science (score: 90.0)
     - Fulfills Computer Science requirement (12 credits needed)
     - No prerequisites required
     - Foundational course
```

## Common Workflows

### Using Sample Data (Fastest)
```bash
python demo.py
```

### Interactive Session
```bash
python course_analyzer.py
# Press Enter at PDF prompt to use sample data
# Answer the 10 questions
# Enter your graduation requirements
# View recommendations
```

### With OpenAI Integration
```bash
export OPENAI_API_KEY='your-key'
python course_analyzer.py
```

### Testing
```bash
python test_analyzer.py
```

## Need Help?

- See `README.md` for full documentation
- See `USAGE.md` for detailed usage examples
- Check sample courses in `PDFParser._parse_mock_data()` method

## Scoring System

The rule-based evaluator scores courses based on:

1. **Interest Match** (0-90 points): Category interest score × 10
2. **Requirement Match** (20 points): Does it fulfill a requirement?
3. **Prerequisites** (15 points): No prerequisites = easier to take now
4. **Foundation Course** (10 points): Bonus for 101-level courses

Higher scores = better recommendations!
