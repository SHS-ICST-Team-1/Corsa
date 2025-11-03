#!/usr/bin/env python3
"""
Course Selection Futuristic AI Analyzer 3000

This application helps students select courses based on their interests
and graduation requirements using AI-powered analysis.
"""

import os
import sys
from typing import List, Dict, Optional
import json

# Step 1: PDF Parser
class PDFParser:
    """Parses course selection book PDF and extracts usable data."""
    
    def __init__(self):
        try:
            import pdfplumber
            self.pdfplumber = pdfplumber
        except ImportError:
            print("Warning: pdfplumber not installed. PDF parsing will be limited.")
            self.pdfplumber = None
    
    def parse_pdf(self, pdf_path: str) -> List[Dict]:
        """
        Parse PDF and extract course information.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of course dictionaries with extracted data
        """
        if not self.pdfplumber:
            return self._parse_mock_data()
        
        if not os.path.exists(pdf_path):
            print(f"PDF file not found: {pdf_path}")
            return self._parse_mock_data()
        
        courses = []
        
        try:
            with self.pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        # Extract course information from text
                        courses.extend(self._extract_courses_from_text(text))
        except Exception as e:
            print(f"Error parsing PDF: {e}")
            return self._parse_mock_data()
        
        return courses if courses else self._parse_mock_data()
    
    def _extract_courses_from_text(self, text: str) -> List[Dict]:
        """Extract course information from page text."""
        courses = []
        lines = text.split('\n')
        
        current_course = {}
        for line in lines:
            line = line.strip()
            if not line:
                if current_course:
                    courses.append(current_course)
                    current_course = {}
                continue
            
            # Simple pattern matching for course codes (e.g., CS101, MATH201)
            if len(line.split()) > 0 and any(char.isdigit() for char in line.split()[0]):
                if current_course:
                    courses.append(current_course)
                current_course = {
                    'code': line.split()[0] if line.split() else '',
                    'name': ' '.join(line.split()[1:]) if len(line.split()) > 1 else line,
                    'description': '',
                    'credits': 3,
                    'prerequisites': [],
                    'category': 'General'
                }
            elif current_course:
                current_course['description'] += ' ' + line
        
        if current_course:
            courses.append(current_course)
        
        return courses
    
    def _parse_mock_data(self) -> List[Dict]:
        """Return mock course data for demonstration."""
        return [
            {
                'code': 'CS101',
                'name': 'Introduction to Computer Science',
                'description': 'Fundamental concepts of programming and computer science',
                'credits': 3,
                'prerequisites': [],
                'category': 'Computer Science'
            },
            {
                'code': 'CS201',
                'name': 'Data Structures',
                'description': 'Study of data structures and algorithms',
                'credits': 3,
                'prerequisites': ['CS101'],
                'category': 'Computer Science'
            },
            {
                'code': 'MATH101',
                'name': 'Calculus I',
                'description': 'Introduction to differential calculus',
                'credits': 4,
                'prerequisites': [],
                'category': 'Mathematics'
            },
            {
                'code': 'MATH201',
                'name': 'Calculus II',
                'description': 'Introduction to integral calculus',
                'credits': 4,
                'prerequisites': ['MATH101'],
                'category': 'Mathematics'
            },
            {
                'code': 'ENG101',
                'name': 'English Composition',
                'description': 'Writing and critical thinking',
                'credits': 3,
                'prerequisites': [],
                'category': 'English'
            },
            {
                'code': 'PHY101',
                'name': 'Physics I',
                'description': 'Mechanics and thermodynamics',
                'credits': 4,
                'prerequisites': ['MATH101'],
                'category': 'Physics'
            },
            {
                'code': 'CS301',
                'name': 'Algorithms',
                'description': 'Algorithm design and analysis',
                'credits': 3,
                'prerequisites': ['CS201', 'MATH101'],
                'category': 'Computer Science'
            },
            {
                'code': 'CS401',
                'name': 'Artificial Intelligence',
                'description': 'Introduction to AI concepts and machine learning',
                'credits': 3,
                'prerequisites': ['CS301'],
                'category': 'Computer Science'
            },
            {
                'code': 'HIST101',
                'name': 'World History',
                'description': 'Survey of world history',
                'credits': 3,
                'prerequisites': [],
                'category': 'History'
            },
            {
                'code': 'ART101',
                'name': 'Introduction to Art',
                'description': 'Basic principles of art and design',
                'credits': 3,
                'prerequisites': [],
                'category': 'Art'
            }
        ]


# Step 2: Interactive Question System
class InterestQuestionnaire:
    """20 Questions-style system to narrow down course options based on interests."""
    
    def __init__(self):
        self.questions = [
            {
                'question': 'Do you enjoy working with technology and computers?',
                'categories': {'yes': ['Computer Science'], 'no': []},
                'weight': 3
            },
            {
                'question': 'Are you interested in solving mathematical problems?',
                'categories': {'yes': ['Mathematics', 'Computer Science', 'Physics'], 'no': []},
                'weight': 2
            },
            {
                'question': 'Do you enjoy writing and communication?',
                'categories': {'yes': ['English'], 'no': []},
                'weight': 2
            },
            {
                'question': 'Are you interested in understanding how the physical world works?',
                'categories': {'yes': ['Physics'], 'no': []},
                'weight': 2
            },
            {
                'question': 'Do you have an interest in history and social studies?',
                'categories': {'yes': ['History'], 'no': []},
                'weight': 1
            },
            {
                'question': 'Are you creative and interested in visual arts?',
                'categories': {'yes': ['Art'], 'no': []},
                'weight': 1
            },
            {
                'question': 'Do you want to learn about artificial intelligence and machine learning?',
                'categories': {'yes': ['Computer Science'], 'no': []},
                'weight': 3
            },
            {
                'question': 'Do you prefer theoretical or practical courses?',
                'categories': {'theoretical': ['Mathematics', 'Physics'], 'practical': ['Computer Science', 'Art']},
                'weight': 2
            },
            {
                'question': 'Do you enjoy problem-solving and logical thinking?',
                'categories': {'yes': ['Computer Science', 'Mathematics'], 'no': []},
                'weight': 2
            },
            {
                'question': 'Are you interested in a career in technology?',
                'categories': {'yes': ['Computer Science'], 'no': []},
                'weight': 3
            }
        ]
        self.category_scores = {}
    
    def ask_questions(self) -> Dict[str, float]:
        """
        Ask questions interactively and calculate category scores.
        
        Returns:
            Dictionary mapping categories to scores
        """
        print("\n=== Interest Assessment ===")
        print("Please answer the following questions to help us understand your interests.\n")
        
        for i, q_data in enumerate(self.questions, 1):
            print(f"Question {i}/{len(self.questions)}: {q_data['question']}")
            
            # Determine valid answers based on question
            valid_answers = list(q_data['categories'].keys())
            print(f"Valid answers: {', '.join(valid_answers)}")
            
            answer = input("Your answer: ").strip().lower()
            
            while answer not in valid_answers:
                print(f"Please enter one of: {', '.join(valid_answers)}")
                answer = input("Your answer: ").strip().lower()
            
            # Update category scores
            categories = q_data['categories'].get(answer, [])
            weight = q_data['weight']
            
            for category in categories:
                if category not in self.category_scores:
                    self.category_scores[category] = 0
                self.category_scores[category] += weight
            
            print()
        
        return self.category_scores
    
    def get_recommended_categories(self, top_n: int = 3) -> List[str]:
        """Get top N recommended categories based on scores."""
        sorted_categories = sorted(
            self.category_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return [cat for cat, _ in sorted_categories[:top_n]]


# Step 2.5: Graduation Requirements
class GraduationRequirements:
    """Collect and manage graduation requirements."""
    
    def __init__(self):
        self.requirements = {}
    
    def ask_requirements(self) -> Dict:
        """
        Ask user about their graduation requirements.
        
        Returns:
            Dictionary containing graduation requirements
        """
        print("\n=== Graduation Requirements ===")
        print("Please provide information about your graduation requirements.\n")
        
        try:
            total_credits = int(input("Total credits required for graduation: ").strip() or "120")
        except ValueError:
            total_credits = 120
        
        self.requirements['total_credits'] = total_credits
        
        print("\nHow many credits do you need in each category?")
        categories = ['Computer Science', 'Mathematics', 'English', 'Physics', 'History', 'Art', 'General']
        
        for category in categories:
            try:
                credits = int(input(f"{category}: ").strip() or "0")
                self.requirements[category] = credits
            except ValueError:
                self.requirements[category] = 0
        
        try:
            completed_credits = int(input("\nHow many credits have you already completed? ").strip() or "0")
        except ValueError:
            completed_credits = 0
        
        self.requirements['completed_credits'] = completed_credits
        
        return self.requirements


# Step 3: Data Tokenizer and AI Integration
class CourseTokenizer:
    """Tokenize course data for AI processing."""
    
    def __init__(self):
        self.use_tiktoken = False
        try:
            import tiktoken
            self.encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
            self.use_tiktoken = True
        except ImportError:
            print("Warning: tiktoken not installed. Using simple tokenization.")
    
    def tokenize_course(self, course: Dict) -> str:
        """
        Convert course dictionary to a tokenized string representation.
        
        Args:
            course: Course dictionary
            
        Returns:
            Tokenized string representation
        """
        # Create a structured text representation
        text = f"Course Code: {course.get('code', 'N/A')}\n"
        text += f"Course Name: {course.get('name', 'N/A')}\n"
        text += f"Description: {course.get('description', 'N/A')}\n"
        text += f"Credits: {course.get('credits', 0)}\n"
        text += f"Prerequisites: {', '.join(course.get('prerequisites', [])) or 'None'}\n"
        text += f"Category: {course.get('category', 'General')}\n"
        
        return text
    
    def tokenize_courses(self, courses: List[Dict]) -> str:
        """Tokenize multiple courses into a single string."""
        return "\n---\n".join([self.tokenize_course(course) for course in courses])
    
    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in text."""
        if self.use_tiktoken:
            return len(self.encoding.encode(text))
        else:
            # Simple word count as fallback
            return len(text.split())


# Step 4: AI Evaluator
class AIEvaluator:
    """Use AI to evaluate and recommend courses."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get('OPENAI_API_KEY')
        self.use_openai = False
        
        if self.api_key:
            try:
                import openai
                self.client = openai.OpenAI(api_key=self.api_key)
                self.use_openai = True
            except ImportError:
                print("Warning: openai not installed. Using rule-based evaluation.")
        else:
            print("Note: No OpenAI API key provided. Using rule-based evaluation.")
    
    def evaluate_courses(
        self,
        courses: List[Dict],
        interest_scores: Dict[str, float],
        requirements: Dict,
        top_n: int = 5
    ) -> List[Dict]:
        """
        Evaluate and recommend courses based on interests and requirements.
        
        Args:
            courses: List of available courses
            interest_scores: Category scores from questionnaire
            requirements: Graduation requirements
            top_n: Number of courses to recommend
            
        Returns:
            List of recommended courses with scores
        """
        if self.use_openai:
            return self._evaluate_with_ai(courses, interest_scores, requirements, top_n)
        else:
            return self._evaluate_rule_based(courses, interest_scores, requirements, top_n)
    
    def _evaluate_with_ai(
        self,
        courses: List[Dict],
        interest_scores: Dict[str, float],
        requirements: Dict,
        top_n: int
    ) -> List[Dict]:
        """Evaluate courses using OpenAI API."""
        tokenizer = CourseTokenizer()
        courses_text = tokenizer.tokenize_courses(courses)
        
        prompt = f"""You are a course recommendation system. Based on the student's interests and graduation requirements, recommend the top {top_n} courses.

Student Interest Scores:
{json.dumps(interest_scores, indent=2)}

Graduation Requirements:
{json.dumps(requirements, indent=2)}

Available Courses:
{courses_text}

Please recommend {top_n} courses that best match the student's interests and help fulfill their graduation requirements. For each course, provide:
1. Course code
2. Reason for recommendation
3. Score (0-100)

Format your response as JSON array."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful course recommendation assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Parse AI response
            content = response.choices[0].message.content
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                recommendations = json.loads(json_match.group())
                return recommendations
            else:
                # Fallback to rule-based if parsing fails
                return self._evaluate_rule_based(courses, interest_scores, requirements, top_n)
        except Exception as e:
            print(f"Error using OpenAI API: {e}")
            return self._evaluate_rule_based(courses, interest_scores, requirements, top_n)
    
    def _evaluate_rule_based(
        self,
        courses: List[Dict],
        interest_scores: Dict[str, float],
        requirements: Dict,
        top_n: int
    ) -> List[Dict]:
        """Evaluate courses using rule-based scoring."""
        scored_courses = []
        
        for course in courses:
            score = 0
            reasons = []
            
            # Score based on interest category match
            category = course.get('category', 'General')
            if category in interest_scores:
                category_score = interest_scores[category] * 10
                score += category_score
                reasons.append(f"Matches your interest in {category} (score: {category_score:.1f})")
            
            # Score based on graduation requirements
            if category in requirements and requirements[category] > 0:
                req_score = 20
                score += req_score
                reasons.append(f"Fulfills {category} requirement ({requirements[category]} credits needed)")
            
            # Prefer courses with fewer prerequisites (easier to take now)
            prereq_count = len(course.get('prerequisites', []))
            if prereq_count == 0:
                prereq_score = 15
                score += prereq_score
                reasons.append("No prerequisites required")
            
            # Bonus for foundational courses (101 level)
            if '101' in course.get('code', ''):
                foundation_score = 10
                score += foundation_score
                reasons.append("Foundational course")
            
            scored_courses.append({
                'course': course,
                'score': score,
                'reasons': reasons
            })
        
        # Sort by score and return top N
        scored_courses.sort(key=lambda x: x['score'], reverse=True)
        
        recommendations = []
        for item in scored_courses[:top_n]:
            recommendations.append({
                'code': item['course']['code'],
                'name': item['course']['name'],
                'score': item['score'],
                'reasons': item['reasons']
            })
        
        return recommendations


# Main Application
class CourseSelectionAnalyzer:
    """Main application class for Course Selection Futuristic AI Analyzer 3000."""
    
    def __init__(self):
        self.parser = PDFParser()
        self.questionnaire = InterestQuestionnaire()
        self.grad_requirements = GraduationRequirements()
        self.tokenizer = CourseTokenizer()
        self.evaluator = AIEvaluator()
        self.courses = []
    
    def run(self):
        """Run the complete course selection analysis workflow."""
        print("=" * 60)
        print("COURSE SELECTION FUTURISTIC AI ANALYZER 3000")
        print("=" * 60)
        print()
        
        # Step 0: Ask user to upload course selection book (PDF)
        print("Step 0: Upload Course Selection Book")
        print("-" * 60)
        pdf_path = input("Enter path to course selection PDF (press Enter to use sample data): ").strip()
        print()
        
        # Step 1: Parse PDF
        print("Step 1: Parsing Course Data")
        print("-" * 60)
        self.courses = self.parser.parse_pdf(pdf_path) if pdf_path else self.parser.parse_pdf("")
        print(f"Loaded {len(self.courses)} courses from the database.")
        print()
        
        # Step 2: Interactive questionnaire
        print("Step 2: Interest Assessment")
        print("-" * 60)
        interest_scores = self.questionnaire.ask_questions()
        print("\nYour Interest Scores:")
        for category, score in sorted(interest_scores.items(), key=lambda x: x[1], reverse=True):
            print(f"  {category}: {score}")
        print()
        
        # Step 2.5: Graduation requirements
        print("Step 2.5: Graduation Requirements")
        print("-" * 60)
        requirements = self.grad_requirements.ask_requirements()
        print("\nYour Requirements:")
        for key, value in requirements.items():
            print(f"  {key}: {value}")
        print()
        
        # Step 3: Tokenize data
        print("Step 3: Processing Course Data")
        print("-" * 60)
        tokenized_data = self.tokenizer.tokenize_courses(self.courses)
        token_count = self.tokenizer.count_tokens(tokenized_data)
        print(f"Processed course data: {token_count} tokens")
        print()
        
        # Step 4: AI Evaluation
        print("Step 4: AI Course Evaluation")
        print("-" * 60)
        print("Analyzing courses based on your interests and requirements...")
        recommendations = self.evaluator.evaluate_courses(
            self.courses,
            interest_scores,
            requirements,
            top_n=5
        )
        
        print("\n" + "=" * 60)
        print("RECOMMENDED COURSES")
        print("=" * 60)
        print()
        
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec['code']}: {rec.get('name', 'N/A')}")
            print(f"   Score: {rec['score']:.1f}")
            if 'reasons' in rec and rec['reasons']:
                print("   Reasons:")
                for reason in rec['reasons']:
                    print(f"     - {reason}")
            print()
        
        print("=" * 60)
        print("Analysis complete! Good luck with your course selection!")
        print("=" * 60)


def main():
    """Entry point for the application."""
    try:
        analyzer = CourseSelectionAnalyzer()
        analyzer.run()
    except KeyboardInterrupt:
        print("\n\nAnalysis interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
