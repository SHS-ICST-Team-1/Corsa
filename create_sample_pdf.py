#!/usr/bin/env python3
"""
Create a sample course catalog PDF for testing.
Requires reportlab: pip install reportlab
"""

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("reportlab not installed. Install with: pip install reportlab")


def create_sample_pdf(filename="sample_courses.pdf"):
    """Create a sample course catalog PDF."""
    if not REPORTLAB_AVAILABLE:
        print("Cannot create PDF without reportlab")
        return False
    
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title = Paragraph("Sample Course Catalog", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 0.3*inch))
    
    # Sample courses
    courses = [
        {
            'code': 'CS101',
            'name': 'Introduction to Computer Science',
            'description': 'Fundamental concepts of programming and computer science. '
                          'Topics include algorithms, data structures, and problem-solving.',
            'credits': 3,
            'prerequisites': 'None'
        },
        {
            'code': 'CS201',
            'name': 'Data Structures',
            'description': 'Advanced study of data structures including trees, graphs, '
                          'and hash tables. Analysis of algorithms.',
            'credits': 3,
            'prerequisites': 'CS101'
        },
        {
            'code': 'MATH101',
            'name': 'Calculus I',
            'description': 'Introduction to differential calculus. Limits, derivatives, '
                          'and applications.',
            'credits': 4,
            'prerequisites': 'None'
        },
        {
            'code': 'MATH201',
            'name': 'Calculus II',
            'description': 'Introduction to integral calculus. Integration techniques '
                          'and applications.',
            'credits': 4,
            'prerequisites': 'MATH101'
        },
        {
            'code': 'ENG101',
            'name': 'English Composition',
            'description': 'Writing and critical thinking. Essay composition and analysis.',
            'credits': 3,
            'prerequisites': 'None'
        },
    ]
    
    for course in courses:
        # Course code and name
        course_title = Paragraph(
            f"<b>{course['code']}: {course['name']}</b>",
            styles['Heading2']
        )
        story.append(course_title)
        story.append(Spacer(1, 0.1*inch))
        
        # Course details
        details = f"""
        <b>Credits:</b> {course['credits']}<br/>
        <b>Prerequisites:</b> {course['prerequisites']}<br/>
        <b>Description:</b> {course['description']}
        """
        details_para = Paragraph(details, styles['Normal'])
        story.append(details_para)
        story.append(Spacer(1, 0.3*inch))
    
    # Build PDF
    doc.build(story)
    print(f"Created sample PDF: {filename}")
    return True


if __name__ == "__main__":
    create_sample_pdf()
