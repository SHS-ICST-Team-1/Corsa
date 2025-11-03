#!/usr/bin/env python3
"""
Example/test script for the Course Selection Analyzer.

This script demonstrates how to use the analyzer programmatically
and can be used for automated testing.
"""

import sys
import os

# Add the current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from course_analyzer import (
    PDFParser,
    InterestQuestionnaire,
    GraduationRequirements,
    CourseTokenizer,
    AIEvaluator
)


def test_pdf_parser():
    """Test the PDF parser with sample data."""
    print("Testing PDF Parser...")
    parser = PDFParser()
    courses = parser.parse_pdf("")  # Use mock data
    
    assert len(courses) > 0, "Should return at least some courses"
    assert 'code' in courses[0], "Course should have a code"
    assert 'name' in courses[0], "Course should have a name"
    
    print(f"✓ Loaded {len(courses)} courses")
    print(f"  Sample: {courses[0]['code']} - {courses[0]['name']}")
    return courses


def test_tokenizer(courses):
    """Test the course tokenizer."""
    print("\nTesting Tokenizer...")
    tokenizer = CourseTokenizer()
    
    # Test single course
    single_text = tokenizer.tokenize_course(courses[0])
    assert len(single_text) > 0, "Should generate text for course"
    
    # Test multiple courses
    all_text = tokenizer.tokenize_courses(courses)
    assert len(all_text) > len(single_text), "All courses should generate more text"
    
    # Test token counting
    token_count = tokenizer.count_tokens(all_text)
    assert token_count > 0, "Should count tokens"
    
    print(f"✓ Tokenized {len(courses)} courses")
    print(f"  Total tokens: {token_count}")
    return tokenizer


def test_evaluator(courses):
    """Test the AI evaluator with sample data."""
    print("\nTesting AI Evaluator...")
    evaluator = AIEvaluator()  # Will use rule-based without API key
    
    # Sample interest scores
    interest_scores = {
        'Computer Science': 9,
        'Mathematics': 6,
        'Physics': 4
    }
    
    # Sample requirements
    requirements = {
        'total_credits': 120,
        'Computer Science': 12,
        'Mathematics': 8,
        'completed_credits': 30
    }
    
    recommendations = evaluator.evaluate_courses(
        courses,
        interest_scores,
        requirements,
        top_n=5
    )
    
    assert len(recommendations) > 0, "Should return recommendations"
    assert 'code' in recommendations[0], "Recommendation should have course code"
    assert 'score' in recommendations[0], "Recommendation should have score"
    
    print(f"✓ Generated {len(recommendations)} recommendations")
    for i, rec in enumerate(recommendations[:3], 1):
        print(f"  {i}. {rec['code']}: {rec.get('name', 'N/A')} (score: {rec['score']:.1f})")
    
    return recommendations


def test_interest_questionnaire():
    """Test the interest questionnaire structure."""
    print("\nTesting Interest Questionnaire...")
    questionnaire = InterestQuestionnaire()
    
    assert len(questionnaire.questions) > 0, "Should have questions"
    assert 'question' in questionnaire.questions[0], "Question should have text"
    assert 'categories' in questionnaire.questions[0], "Question should have categories"
    
    print(f"✓ Questionnaire has {len(questionnaire.questions)} questions")
    print(f"  Sample: {questionnaire.questions[0]['question']}")


def test_graduation_requirements():
    """Test the graduation requirements structure."""
    print("\nTesting Graduation Requirements...")
    grad_req = GraduationRequirements()
    
    # Test that it initializes correctly
    assert grad_req.requirements == {}, "Should start with empty requirements"
    
    print("✓ Graduation requirements system initialized")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Course Selection Analyzer - Component Tests")
    print("=" * 60)
    print()
    
    try:
        # Run tests
        courses = test_pdf_parser()
        test_tokenizer(courses)
        test_evaluator(courses)
        test_interest_questionnaire()
        test_graduation_requirements()
        
        print("\n" + "=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
