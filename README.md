# Course Selection Futuristic AI Analyzer 3000

A Python-based application that helps students select courses based on their interests and graduation requirements using AI-powered analysis.

## Features

- **PDF Upload & Parsing**: Upload your course selection book in PDF format and automatically extract course information
- **Interactive Interest Assessment**: Answer a series of questions to identify your interests and preferred subject areas
- **Graduation Requirements**: Input your specific graduation requirements to ensure you stay on track
- **AI-Powered Analysis**: Uses OpenAI's GPT models (with rule-based fallback) to recommend the best courses for you
- **Smart Tokenization**: Efficiently processes course data for AI analysis

## Installation

1. Clone the repository:
```bash
git clone https://github.com/SHS-ICST-Team-1/Corsa.git
cd Corsa
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Set up OpenAI API key for AI-powered recommendations:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

Or create a `.env` file:
```
OPENAI_API_KEY=your-api-key-here
```

## Usage

Run the application:
```bash
python course_analyzer.py
```

The application will guide you through the following steps:

### Step 0: Upload Course Selection Book
- Provide the path to your course selection PDF
- Or press Enter to use sample course data

### Step 1: PDF Parsing
- The system automatically extracts course information from the PDF
- Extracts: course codes, names, descriptions, credits, prerequisites, and categories

### Step 2: Interest Assessment
- Answer 10 questions about your interests and preferences
- Questions cover topics like technology, mathematics, arts, and more
- Your answers are weighted to calculate interest scores by category

### Step 2.5: Graduation Requirements
- Enter total credits required for graduation
- Specify required credits per category (CS, Math, English, etc.)
- Input already completed credits

### Step 3: Data Processing
- Course data is tokenized and prepared for AI analysis
- Token count is displayed for transparency

### Step 4: AI Evaluation
- AI analyzes all courses based on your profile
- Recommends top 5 courses with scores and detailed reasons
- Considers both interests and graduation requirements

## Sample Output

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

...

============================================================
RECOMMENDED COURSES
============================================================

1. CS101: Introduction to Computer Science
   Score: 48.0
   Reasons:
     - Matches your interest in Computer Science (score: 30.0)
     - Fulfills Computer Science requirement (12 credits needed)
     - No prerequisites required
     - Foundational course

2. MATH101: Calculus I
   Score: 35.0
   Reasons:
     - Matches your interest in Mathematics (score: 20.0)
     - No prerequisites required
     - Foundational course

...
```

## Components

### PDFParser
Extracts course information from PDF course catalogs. Falls back to sample data if PDF parsing fails.

### InterestQuestionnaire
Interactive 20-questions style assessment to understand student interests across multiple categories.

### GraduationRequirements
Collects information about degree requirements and tracks progress toward graduation.

### CourseTokenizer
Converts course data into tokenized format suitable for AI processing. Supports tiktoken for accurate token counting.

### AIEvaluator
Evaluates courses using either:
- OpenAI GPT models (when API key is provided)
- Rule-based scoring system (fallback)

## Dependencies

- `PyPDF2`: PDF manipulation
- `pdfplumber`: Advanced PDF text extraction
- `openai`: OpenAI API integration
- `python-dotenv`: Environment variable management
- `tiktoken`: Token counting for AI models

## Configuration

The application works out of the box with sample data and rule-based recommendations. For enhanced AI-powered recommendations:

1. Obtain an OpenAI API key from https://platform.openai.com/
2. Set the `OPENAI_API_KEY` environment variable
3. Run the application as normal

## Development

The application is structured in a modular way with clear separation of concerns:

- Each step of the process is implemented as a separate class
- All classes can be used independently or as part of the main workflow
- Graceful fallbacks ensure the system works even without all dependencies

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.