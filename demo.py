#!/usr/bin/env python3
"""
Automated demo script for the Course Selection Analyzer.

This script runs through the entire workflow with pre-configured answers
to demonstrate the system without requiring interactive input.
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


def main():
    """Run automated demo."""
    print("=" * 60)
    print("COURSE SELECTION FUTURISTIC AI ANALYZER 3000")
    print("AUTOMATED DEMO")
    print("=" * 60)
    print()
    
    # Step 0 & 1: Load sample course data
    print("Step 0-1: Loading Course Data")
    print("-" * 60)
    parser = PDFParser()
    courses = parser.parse_pdf("")  # Use sample data
    print(f"Loaded {len(courses)} courses from the database.")
    print("\nSample courses:")
    for course in courses[:3]:
        print(f"  - {course['code']}: {course['name']}")
    print()
    
    # Step 2: Simulate interest questionnaire with pre-set answers
    print("Step 2: Interest Assessment (Simulated)")
    print("-" * 60)
    print("Simulating student interested in Computer Science and Math...\n")
    
    # Manually calculate interest scores based on predefined profile
    interest_scores = {
        'Computer Science': 9,  # High interest
        'Mathematics': 6,       # Medium interest
        'Physics': 4,           # Some interest
        'English': 2            # Low interest
    }
    
    print("Interest Scores:")
    for category, score in sorted(interest_scores.items(), key=lambda x: x[1], reverse=True):
        print(f"  {category}: {score}")
    print()
    
    # Step 2.5: Simulate graduation requirements
    print("Step 2.5: Graduation Requirements (Simulated)")
    print("-" * 60)
    requirements = {
        'total_credits': 120,
        'Computer Science': 12,
        'Mathematics': 8,
        'English': 6,
        'Physics': 4,
        'History': 3,
        'Art': 3,
        'General': 0,
        'completed_credits': 30
    }
    
    print("Graduation Requirements:")
    for key, value in requirements.items():
        print(f"  {key}: {value}")
    print()
    
    # Step 3: Tokenize data
    print("Step 3: Processing Course Data")
    print("-" * 60)
    tokenizer = CourseTokenizer()
    tokenized_data = tokenizer.tokenize_courses(courses)
    token_count = tokenizer.count_tokens(tokenized_data)
    print(f"Processed course data: {token_count} tokens")
    print()
    
    # Step 4: AI Evaluation
    print("Step 4: AI Course Evaluation")
    print("-" * 60)
    print("Analyzing courses based on interests and requirements...")
    evaluator = AIEvaluator()
    recommendations = evaluator.evaluate_courses(
        courses,
        interest_scores,
        requirements,
        top_n=5
    )
    print()
    
    # Display results
    print("=" * 60)
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
    print("Demo complete!")
    print("=" * 60)
    print()
    print("To run the interactive version, use: python course_analyzer.py")
    print()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
