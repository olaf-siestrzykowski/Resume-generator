import markdown
import pdfkit
from pathlib import Path
import re
import sys
import os
import argparse

def parse_markdown(markdown_file):
    """Parse markdown file and extract CV data"""
    with open(markdown_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extract name
    name_match = re.search(r'# (.*?)[\r\n]', content)
    name = name_match.group(1) if name_match else "Name Not Found"
    
    # Extract title
    title_match = re.search(r'## (.*?)[\r\n]', content)
    title = title_match.group(1) if title_match else "Title Not Found"
    
    # Extract contact info
    contact_match = re.search(r'Contact: (.*?)[\r\n]', content)
    contact_info = contact_match.group(1) if contact_match else ""
    
    # Extract personal statement
    statement_match = re.search(r'## DATA ANALYST\n\n(.*?)\n\n##', content, re.DOTALL)
    statement = statement_match.group(1) if statement_match else ""
    
    # Extract sections
    skills_match = re.search(r'## Skills\n\n(.*?)\n\n##', content, re.DOTALL)
    skills = skills_match.group(1) if skills_match else ""
    
    work_exp_match = re.search(r'## Work Experience\n\n(.*?)\n\n##', content, re.DOTALL)
    work_exp = work_exp_match.group(1) if work_exp_match else ""
    
    education_match = re.search(r'## Education\n\n(.*?)\n\n##', content, re.DOTALL)
    education = education_match.group(1) if education_match else ""
    
    projects_match = re.search(r'## Projects\n\n(.*?)\n\n##', content, re.DOTALL)
    projects = projects_match.group(1) if projects_match else ""
    
    courses_match = re.search(r'## Courses\n\n(.*?)$', content, re.DOTALL)
    courses = courses_match.group(1) if courses_match else ""
    
    return {
        'name': name,
        'title': title,
        'contact_info': contact_info,
        'statement': statement,
        'skills': skills,
        'work_exp': work_exp,
        'education': education,
        'projects': projects,
        'courses': courses
    }

def generate_html(cv_data):
    """Generate HTML with styling similar to the original PDF"""
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{cv_data['name']} - CV</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                color: #333;
                line-height: 1.5;
            }}
            .container {{
                display: flex;
                width: 100%;
            }}
            .left-column {{
                width: 70%;
                padding: 40px;
            }}
            .right-column {{
                width: 30%;
                background-color: #f0f0f0;
                padding: 40px 20px;
            }}
            .name {{
                font-size: 32px;
                font-weight: bold;
                margin-bottom: 0;
                color: #2a3c85;
            }}
            .title {{
                font-size: 24px;
                margin-top: 5px;
                margin-bottom: 20px;
                color: #2a3c85;
            }}
            .contact {{
                margin-bottom: 20px;
            }}
            .section-title {{
                font-size: 20px;
                font-weight: bold;
                margin-top: 25px;
                margin-bottom: 15px;
                color: #2a3c85;
                text-transform: uppercase;
            }}
            .job-title {{
                font-weight: bold;
                margin-bottom: 5px;
            }}
            ul {{
                padding-left: 20px;
                margin-top: 5px;
            }}
            li {{
                margin-bottom: 5px;
            }}
            .skills-list {{
                list-style-type: none;
                padding-left: 0;
            }}
            .skills-list li {{
                margin-bottom: 10px;
                font-weight: bold;
            }}
            .skills-list li span {{
                font-weight: normal;
                color: #666;
            }}
            .statement {{
                font-style: italic;
                margin-bottom: 20px;
            }}
            .project {{
                margin-bottom: 20px;
            }}
            .project-title {{
                font-weight: bold;
                margin-bottom: 5px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="left-column">
                <h1 class="name">{cv_data['name']}</h1>
                <h2 class="title">{cv_data['title']}</h2>
                
                <div class="contact">
                    {cv_data['contact_info']}
                </div>
                
                <div class="statement">
                    {cv_data['statement']}
                </div>
                
                <div>
                    <h3 class="section-title">Work Experience</h3>
                    {markdown.markdown(cv_data['work_exp'])}
                </div>
                
                <div>
                    <h3 class="section-title">Education</h3>
                    {markdown.markdown(cv_data['education'])}
                </div>
                
                <div>
                    <h3 class="section-title">Projects</h3>
                    {markdown.markdown(cv_data['projects'])}
                </div>
                
            </div>
            <div class="right-column">
                <div>
                    <h3 class="section-title">Skills</h3>
                    {markdown.markdown(cv_data['skills'])}
                </div>
                
                <div>
                    <h3 class="section-title">Courses</h3>
                    {markdown.markdown(cv_data['courses'])}
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html_template

def generate_pdf(markdown_file, output_file=None):
    """Generate PDF from markdown file"""
    if not output_file:
        output_file = Path(markdown_file).stem + '.pdf'
    
    # Parse markdown
    cv_data = parse_markdown(markdown_file)
    
    # Generate HTML
    html_content = generate_html(cv_data)
    
    # Save HTML temporarily
    temp_html_file = 'temp_cv.html'
    with open(temp_html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Convert HTML to PDF
    try:
        pdfkit.from_file(temp_html_file, output_file)
        print(f"PDF generated successfully: {output_file}")
    except Exception as e:
        print(f"Error generating PDF: {e}")
        print("Make sure wkhtmltopdf is installed and in your PATH")
    
    # Clean up temporary file
    if os.path.exists(temp_html_file):
        os.remove(temp_html_file)

def main():
    parser = argparse.ArgumentParser(description='Generate PDF CV from markdown file')
    parser.add_argument('markdown_file', help='Path to markdown CV file')
    parser.add_argument('-o', '--output', help='Output PDF file path (optional)')
    
    args = parser.parse_args()
    
    generate_pdf(args.markdown_file, args.output)

if __name__ == "__main__":
    main()