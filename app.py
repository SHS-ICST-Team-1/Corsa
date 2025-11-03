"""
Course Selection AI Analyzer - Web Application
High-end web interface with Claude 3.5 Sonnet and GPA Calculator
"""

from flask import Flask, render_template, request, jsonify, session
import os
import json
from typing import List, Dict, Optional
import secrets
from werkzeug.utils import secure_filename
from course_analyzer import PDFParser, InterestQuestionnaire, GraduationRequirements, CourseTokenizer

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Claude 3.5 Sonnet Integration
class ClaudeAIEvaluator:
    """AI Evaluator using Claude 3.5 Sonnet model."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')
        self.use_claude = False
        
        if self.api_key:
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=self.api_key)
                self.use_claude = True
            except ImportError:
                print("Warning: anthropic not installed. Using rule-based evaluation.")
        else:
            print("Note: No Anthropic API key provided. Using rule-based evaluation.")
    
    def evaluate_courses(
        self,
        courses: List[Dict],
        interest_scores: Dict[str, float],
        requirements: Dict,
        top_n: int = 5
    ) -> List[Dict]:
        """Evaluate and recommend courses using Claude or rule-based system."""
        if self.use_claude:
            return self._evaluate_with_claude(courses, interest_scores, requirements, top_n)
        else:
            return self._evaluate_rule_based(courses, interest_scores, requirements, top_n)
    
    def _evaluate_with_claude(
        self,
        courses: List[Dict],
        interest_scores: Dict[str, float],
        requirements: Dict,
        top_n: int
    ) -> List[Dict]:
        """Evaluate courses using Claude 3.5 Sonnet."""
        tokenizer = CourseTokenizer()
        courses_text = tokenizer.tokenize_courses(courses)
        
        prompt = f"""You are an expert academic advisor helping students select courses. Based on the student's interests and graduation requirements, recommend the top {top_n} courses.

Student Interest Scores:
{json.dumps(interest_scores, indent=2)}

Graduation Requirements:
{json.dumps(requirements, indent=2)}

Available Courses:
{courses_text}

Please recommend {top_n} courses that best match the student's interests and help fulfill their graduation requirements. For each course, provide:
1. Course code
2. Course name
3. Reason for recommendation
4. Score (0-100)

Format your response as a JSON array with objects containing: code, name, score, and reasons (array of strings)."""

        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            content = message.content[0].text
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                recommendations = json.loads(json_match.group())
                return recommendations
            else:
                return self._evaluate_rule_based(courses, interest_scores, requirements, top_n)
        except Exception as e:
            print(f"Error using Claude API: {e}")
            return self._evaluate_rule_based(courses, interest_scores, requirements, top_n)
    
    def _evaluate_rule_based(
        self,
        courses: List[Dict],
        interest_scores: Dict[str, float],
        requirements: Dict,
        top_n: int
    ) -> List[Dict]:
        """Rule-based evaluation fallback."""
        scored_courses = []
        
        for course in courses:
            score = 0
            reasons = []
            
            category = course.get('category', 'General')
            if category in interest_scores:
                category_score = interest_scores[category] * 10
                score += category_score
                reasons.append(f"Matches your interest in {category} (score: {category_score:.1f})")
            
            if category in requirements and requirements[category] > 0:
                req_score = 20
                score += req_score
                reasons.append(f"Fulfills {category} requirement ({requirements[category]} credits needed)")
            
            prereq_count = len(course.get('prerequisites', []))
            if prereq_count == 0:
                prereq_score = 15
                score += prereq_score
                reasons.append("No prerequisites required")
            
            if '101' in course.get('code', ''):
                foundation_score = 10
                score += foundation_score
                reasons.append("Foundational course")
            
            scored_courses.append({
                'course': course,
                'score': score,
                'reasons': reasons
            })
        
        scored_courses.sort(key=lambda x: x['score'], reverse=True)
        
        recommendations = []
        for item in scored_courses[:top_n]:
            recommendations.append({
                'code': item['course']['code'],
                'name': item['course']['name'],
                'description': item['course'].get('description', ''),
                'credits': item['course'].get('credits', 3),
                'score': item['score'],
                'reasons': item['reasons']
            })
        
        return recommendations


# GPA Calculator
class GPACalculator:
    """Calculate GPA from course grades."""
    
    GRADE_POINTS = {
        'A+': 4.0, 'A': 4.0, 'A-': 3.7,
        'B+': 3.3, 'B': 3.0, 'B-': 2.7,
        'C+': 2.3, 'C': 2.0, 'C-': 1.7,
        'D+': 1.3, 'D': 1.0, 'D-': 0.7,
        'F': 0.0
    }
    
    @staticmethod
    def calculate_gpa(grades: List[Dict]) -> Dict:
        """
        Calculate GPA from list of grades.
        
        Args:
            grades: List of dicts with 'grade' and 'credits' keys
            
        Returns:
            Dict with gpa, total_credits, and grade_points
        """
        if not grades:
            return {'gpa': 0.0, 'total_credits': 0, 'grade_points': 0.0}
        
        total_grade_points = 0.0
        total_credits = 0
        
        for grade_entry in grades:
            grade = grade_entry.get('grade', '').upper()
            credits = float(grade_entry.get('credits', 0))
            
            if grade in GPACalculator.GRADE_POINTS:
                grade_points = GPACalculator.GRADE_POINTS[grade]
                total_grade_points += grade_points * credits
                total_credits += credits
        
        gpa = total_grade_points / total_credits if total_credits > 0 else 0.0
        
        return {
            'gpa': round(gpa, 2),
            'total_credits': total_credits,
            'grade_points': round(total_grade_points, 2)
        }
    
    @staticmethod
    def calculate_cumulative_gpa(current_gpa: float, current_credits: float, 
                                  new_grades: List[Dict]) -> Dict:
        """Calculate cumulative GPA including new grades."""
        current_grade_points = current_gpa * current_credits
        
        new_result = GPACalculator.calculate_gpa(new_grades)
        new_grade_points = new_result['grade_points']
        new_credits = new_result['total_credits']
        
        total_credits = current_credits + new_credits
        total_grade_points = current_grade_points + new_grade_points
        
        cumulative_gpa = total_grade_points / total_credits if total_credits > 0 else 0.0
        
        return {
            'cumulative_gpa': round(cumulative_gpa, 2),
            'total_credits': total_credits,
            'total_grade_points': round(total_grade_points, 2),
            'semester_gpa': new_result['gpa']
        }


@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')


@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    """Handle PDF upload and parse courses."""
    if 'pdf' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['pdf']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and file.filename.endswith('.pdf'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        parser = PDFParser()
        courses = parser.parse_pdf(filepath)
        
        # Store in session
        session['courses'] = courses
        
        return jsonify({
            'success': True,
            'courses': courses,
            'count': len(courses)
        })
    
    return jsonify({'error': 'Invalid file type. Please upload a PDF.'}), 400


@app.route('/use-sample-data', methods=['POST'])
def use_sample_data():
    """Use sample course data."""
    parser = PDFParser()
    courses = parser.parse_pdf('')
    
    session['courses'] = courses
    
    return jsonify({
        'success': True,
        'courses': courses,
        'count': len(courses)
    })


@app.route('/get-questions', methods=['GET'])
def get_questions():
    """Get interest assessment questions."""
    questionnaire = InterestQuestionnaire()
    questions = []
    
    for i, q_data in enumerate(questionnaire.questions):
        questions.append({
            'id': i,
            'question': q_data['question'],
            'options': list(q_data['categories'].keys()),
            'weight': q_data['weight']
        })
    
    return jsonify({'questions': questions})


@app.route('/submit-answers', methods=['POST'])
def submit_answers():
    """Process questionnaire answers and calculate interest scores."""
    data = request.json
    answers = data.get('answers', [])
    
    questionnaire = InterestQuestionnaire()
    category_scores = {}
    
    for answer_data in answers:
        q_id = answer_data.get('question_id')
        answer = answer_data.get('answer', '').lower()
        
        if q_id < len(questionnaire.questions):
            q_data = questionnaire.questions[q_id]
            categories = q_data['categories'].get(answer, [])
            weight = q_data['weight']
            
            for category in categories:
                if category not in category_scores:
                    category_scores[category] = 0
                category_scores[category] += weight
    
    session['interest_scores'] = category_scores
    
    return jsonify({
        'success': True,
        'interest_scores': category_scores
    })


@app.route('/submit-requirements', methods=['POST'])
def submit_requirements():
    """Store graduation requirements."""
    data = request.json
    requirements = data.get('requirements', {})
    
    session['requirements'] = requirements
    
    return jsonify({
        'success': True,
        'requirements': requirements
    })


@app.route('/get-recommendations', methods=['POST'])
def get_recommendations():
    """Generate course recommendations."""
    courses = session.get('courses', [])
    interest_scores = session.get('interest_scores', {})
    requirements = session.get('requirements', {})
    
    if not courses:
        return jsonify({'error': 'No courses loaded. Please upload a PDF or use sample data.'}), 400
    
    evaluator = ClaudeAIEvaluator()
    recommendations = evaluator.evaluate_courses(
        courses,
        interest_scores,
        requirements,
        top_n=5
    )
    
    return jsonify({
        'success': True,
        'recommendations': recommendations
    })


@app.route('/calculate-gpa', methods=['POST'])
def calculate_gpa():
    """Calculate GPA from grades."""
    data = request.json
    grades = data.get('grades', [])
    current_gpa = data.get('current_gpa', 0.0)
    current_credits = data.get('current_credits', 0.0)
    
    calculator = GPACalculator()
    
    if current_credits > 0:
        result = calculator.calculate_cumulative_gpa(current_gpa, current_credits, grades)
    else:
        result = calculator.calculate_gpa(grades)
    
    return jsonify({
        'success': True,
        'result': result
    })


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'model': 'claude-3-5-sonnet-20241022'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
