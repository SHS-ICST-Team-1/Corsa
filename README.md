# Course Selection Futuristic AI Analyzer 3000

A high-end web application that helps students select courses based on their interests and graduation requirements using **Claude 3.5 Sonnet** AI-powered analysis. Features include an interactive course selection workflow and a comprehensive GPA calculator.

## 🎯 Features

### Course Selection System
- **PDF Upload & Parsing**: Upload your course selection book in PDF format and automatically extract course information
- **Interactive Interest Assessment**: Answer 10 weighted questions to identify your interests and preferred subject areas
- **Graduation Requirements**: Input your specific graduation requirements to ensure you stay on track
- **AI-Powered Analysis**: Uses Claude 3.5 Sonnet (with rule-based fallback) to recommend the best courses for you
- **Smart Tokenization**: Efficiently processes course data for AI analysis

### GPA Calculator
- **Semester GPA Calculation**: Calculate GPA for current semester courses
- **Cumulative GPA Tracking**: Track overall GPA including previous coursework
- **Multiple Course Support**: Add unlimited courses with grades and credits
- **Real-time Calculations**: Instant GPA updates as you input data
- **Grade Scale**: Full A+ to F grade scale support (4.0 scale)

## 🚀 Quick Start

### Web Application

1. Install dependencies:
```bash
pip install -r requirements_web.txt
```

2. (Optional) Set up Claude API key for AI-powered recommendations:
```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

Or create a `.env` file:
```
ANTHROPIC_API_KEY=your-api-key-here
```

3. Run the web server:
```bash
python app.py
```

4. Open your browser to:
```
http://localhost:5000
```

### Command Line Interface

For CLI version:
```bash
pip install -r requirements.txt
python course_analyzer.py
```

## 🖥️ Web Interface

The web application features a modern, high-end design with:

- **Dark theme** with gradient accents
- **Responsive layout** that works on desktop and mobile
- **Smooth animations** and transitions
- **Intuitive step-by-step workflow**
- **Real-time feedback** and loading states

### Course Selection Workflow

1. **Upload Course Catalog**
   - Drag & drop PDF file or click to browse
   - Or use built-in sample data for testing

2. **Interest Assessment**
   - Answer 10 questions about your interests
   - Questions are weighted (1-3 points)
   - Covers technology, math, arts, sciences, and more

3. **Graduation Requirements**
   - Enter total credits required
   - Specify required credits per category
   - Input already completed credits

4. **Get Recommendations**
   - Receive top 5 personalized course recommendations
   - Each recommendation includes:
     - Score and ranking
     - Course details (code, name, description)
     - Detailed reasons for recommendation

### GPA Calculator

1. Enter current GPA and credits (if applicable)
2. Add courses with:
   - Course name
   - Grade (A+ to F)
   - Credit hours
3. Click "Calculate GPA" to see:
   - Semester GPA
   - Cumulative GPA
   - Total credits

## 🤖 AI Integration

### Claude 3.5 Sonnet

The application uses **Claude 3.5 Sonnet** (`claude-3-5-sonnet-20241022`), Anthropic's most advanced AI model:

- Superior reasoning and analysis
- Better understanding of academic contexts
- More nuanced course recommendations
- Faster response times

### Fallback System

If no API key is provided, the system automatically uses a sophisticated rule-based algorithm:

- **Interest Match Scoring** (0-90 points): Matches courses to your interests
- **Requirement Fulfillment** (20 points): Prioritizes courses needed for graduation
- **Prerequisites Check** (15 points): Favors courses with no prerequisites
- **Foundation Bonus** (10 points): Recommends introductory courses

## 📁 Project Structure

```
Corsa/
├── app.py                  # Flask web application
├── course_analyzer.py      # Core logic (CLI version)
├── templates/
│   └── index.html         # Web interface
├── static/
│   ├── css/
│   │   └── style.css      # Modern CSS styling
│   └── js/
│       └── app.js         # Frontend JavaScript
├── requirements_web.txt    # Web app dependencies
├── requirements.txt        # CLI dependencies
├── test_analyzer.py        # Unit tests
├── demo.py                # CLI demo
└── README.md              # This file
```

## 🔧 API Endpoints

- `GET /` - Main web interface
- `POST /upload-pdf` - Upload and parse PDF
- `POST /use-sample-data` - Load sample courses
- `GET /get-questions` - Fetch interest questions
- `POST /submit-answers` - Process questionnaire answers
- `POST /submit-requirements` - Store graduation requirements
- `POST /get-recommendations` - Generate recommendations
- `POST /calculate-gpa` - Calculate GPA
- `GET /health` - Health check

## 📊 Sample Output

### Course Recommendations

```
#1. CS101: Introduction to Computer Science
Score: 135.0
✓ Matches your interest in Computer Science (score: 90.0)
✓ Fulfills Computer Science requirement (12 credits needed)
✓ No prerequisites required
✓ Foundational course

#2. MATH101: Calculus I
Score: 105.0
✓ Matches your interest in Mathematics (score: 60.0)
✓ Fulfills Mathematics requirement (8 credits needed)
✓ No prerequisites required
✓ Foundational course
```

### GPA Calculation

```
Semester GPA: 3.45
Cumulative GPA: 3.52
Total Credits: 45
```

## 🛠️ Dependencies

### Web Application
- `Flask==3.0.0` - Web framework
- `anthropic==0.7.8` - Claude AI integration
- `PyPDF2==3.0.1` - PDF manipulation
- `pdfplumber==0.10.3` - Advanced PDF extraction
- `python-dotenv==1.0.0` - Environment variables
- `Werkzeug==3.0.1` - WSGI utilities

### CLI Application
- `PyPDF2==3.0.1` - PDF manipulation
- `pdfplumber==0.10.3` - Advanced PDF extraction
- `openai==1.3.0` - OpenAI API (optional)
- `python-dotenv==1.0.0` - Environment variables
- `tiktoken==0.5.1` - Token counting

## 🎨 Design Principles

- **High-End Modern Design**: Premium dark theme with gradients and smooth animations
- **User-Centric**: Intuitive workflow with clear visual feedback
- **Responsive**: Works seamlessly on desktop, tablet, and mobile
- **Accessible**: High contrast ratios and semantic HTML
- **Performance**: Optimized loading and smooth interactions

## 🔐 Security

- File upload size limited to 16MB
- Secure filename handling
- Session-based state management
- API key protection via environment variables
- No client-side API key exposure

## 📱 Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License

## 🎓 Perfect For

- **Students**: Plan your semester and track your GPA
- **Academic Advisors**: Recommend courses based on student profiles
- **Institutions**: Integrate into course planning systems
- **Developers**: Extend and customize for your needs

---

**Powered by Claude 3.5 Sonnet** 🚀
