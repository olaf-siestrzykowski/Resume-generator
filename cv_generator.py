import json
import os
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageTemplate, Frame
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.graphics.shapes import Drawing, Line
from reportlab.platypus.doctemplate import BaseDocTemplate


@dataclass
class PersonalInfo:
    name: str
    email: str
    phone: str
    location: str
    linkedin: str = ""
    github: str = ""
    portfolio: str = ""


@dataclass
class WorkExperience:
    title: str
    company: str
    period: str
    responsibilities: List[str]
    technologies: List[str] = None


@dataclass
class Project:
    name: str
    description: str
    technologies: List[str]
    achievements: List[str]


@dataclass
class Education:
    degree: str
    institution: str
    period: str
    details: str = ""


@dataclass
class CVData:
    personal_info: PersonalInfo
    summary: str
    work_experience: List[WorkExperience]
    projects: List[Project]
    education: List[Education]
    skills: Dict[str, List[str]]
    courses: List[str]
    languages: List[str]
    additional: List[str]


class CVGenerator:
    def __init__(self, cv_data: CVData):
        self.cv_data = cv_data
        self.colors = {
            'primary': HexColor('#000000'),  # Black for main text
            'secondary': HexColor('#000000'),  # Black for headers
            'green': HexColor('#00AA00'),  # Bright green for separator lines
            'text': HexColor('#000000'),  # Black text
            'gray_bg': HexColor('#F0F0F0'),  # Light gray background
            'white': HexColor('#FFFFFF')
        }
        self.styles = self._create_styles()

    def _create_styles(self):
        """Create custom styles for the CV"""
        styles = getSampleStyleSheet()

        # Header style (large name at top)
        styles.add(ParagraphStyle(
            name='CVHeader',
            parent=styles['Heading1'],
            fontSize=28,
            textColor=self.colors['primary'],
            spaceAfter=8,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold'
        ))

        # Contact info style
        styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=styles['Normal'],
            fontSize=11,
            textColor=self.colors['text'],
            alignment=TA_LEFT,
            spaceAfter=4,
            leftIndent=0
        ))

        # Section header style (like "Projects", "Work Experience", etc.)
        styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=self.colors['primary'],
            spaceBefore=16,
            spaceAfter=8,
            fontName='Helvetica-Bold'
        ))

        # Job title/Project title style
        styles.add(ParagraphStyle(
            name='JobTitle',
            parent=styles['Normal'],
            fontSize=12,
            textColor=self.colors['primary'],
            spaceBefore=8,
            spaceAfter=2,
            fontName='Helvetica-Bold'
        ))

        # Company/Period style
        styles.add(ParagraphStyle(
            name='Company',
            parent=styles['Normal'],
            fontSize=11,
            textColor=self.colors['text'],
            spaceAfter=4,
            fontName='Helvetica'
        ))

        # Period style
        styles.add(ParagraphStyle(
            name='Period',
            parent=styles['Normal'],
            fontSize=10,
            textColor=self.colors['text'],
            spaceAfter=4,
            fontName='Helvetica'
        ))

        # Bullet point style
        styles.add(ParagraphStyle(
            name='BulletPoint',
            parent=styles['Normal'],
            fontSize=10,
            textColor=self.colors['text'],
            leftIndent=0,
            spaceAfter=2,
            bulletIndent=0,
            fontName='Helvetica'
        ))

        # Skills style
        styles.add(ParagraphStyle(
            name='Skills',
            parent=styles['Normal'],
            fontSize=10,
            textColor=self.colors['text'],
            spaceAfter=2,
            fontName='Helvetica'
        ))

        # Summary style
        styles.add(ParagraphStyle(
            name='Summary',
            parent=styles['Normal'],
            fontSize=11,
            textColor=self.colors['text'],
            spaceAfter=4,
            fontName='Helvetica',
            leading=14
        ))

        return styles

    def customize_for_job(self, job_keywords: List[str], job_type: str) -> 'CVData':
        """Customize CV data based on job requirements"""
        customized_data = CVData(
            personal_info=self.cv_data.personal_info,
            summary=self._customize_summary(job_keywords, job_type),
            work_experience=self._prioritize_experience(job_keywords, job_type),
            projects=self._prioritize_projects(job_keywords, job_type),
            education=self.cv_data.education,
            skills=self._prioritize_skills(job_keywords, job_type),
            courses=self._prioritize_courses(job_keywords, job_type),
            languages=self.cv_data.languages,
            additional=self.cv_data.additional
        )
        return customized_data

    def _customize_summary(self, job_keywords: List[str], job_type: str) -> str:
        """Customize summary based on job type"""
        base_summary = self.cv_data.summary

        if job_type.lower() in ['data analyst', 'data scientist', 'analytics']:
            return f"Data Analyst with strong expertise in Python, SQL, and Power BI, passionate about transforming data into actionable insights. Experienced in automating data workflows and delivering business-focused analytics solutions."
        elif job_type.lower() in ['python developer', 'software developer', 'backend developer']:
            return f"Python Developer with experience in Django, APIs, and data processing. Skilled in building scalable applications and automating complex workflows using modern Python frameworks."
        elif job_type.lower() in ['business analyst', 'business intelligence']:
            return f"Business Analyst with strong technical background in data analysis, process automation, and stakeholder collaboration. Experienced in translating business requirements into technical solutions."
        else:
            return base_summary

    def _prioritize_experience(self, job_keywords: List[str], job_type: str) -> List[WorkExperience]:
        """Prioritize and customize work experience based on job requirements"""
        experiences = []
        for exp in self.cv_data.work_experience:
            # Create customized responsibilities based on job type
            if job_type.lower() in ['data analyst', 'data scientist', 'analytics']:
                responsibilities = [
                    "Automated data flows by integrating CRM systems with reporting tools via APIs, reducing manual processing time by 70%",
                    "Developed end-to-end data pipelines from extraction to visualization using Python, SQL, and Power BI",
                    "Collaborated with stakeholders to define KPIs and delivered actionable business insights through custom dashboards",
                    "Performed data analysis and visualization to support strategic decision-making processes"
                ]
            elif job_type.lower() in ['python developer', 'software developer']:
                responsibilities = [
                    "Developed Python applications for data processing and automation using Django and APIs",
                    "Implemented web scraping solutions and data extraction tools using BeautifulSoup and Pandas",
                    "Built and maintained automated workflows integrating multiple systems and databases",
                    "Collaborated with technical teams to deliver scalable software solutions"
                ]
            else:
                responsibilities = exp.responsibilities

            experiences.append(WorkExperience(
                title=exp.title,
                company=exp.company,
                period=exp.period,
                responsibilities=responsibilities,
                technologies=exp.technologies
            ))

        return experiences

    def _prioritize_projects(self, job_keywords: List[str], job_type: str) -> List[Project]:
        """Prioritize projects based on job relevance"""
        projects = self.cv_data.projects.copy()

        # Score projects based on relevance to job keywords
        for project in projects:
            project.relevance_score = 0
            project_text = f"{project.name} {project.description} {' '.join(project.technologies)}"

            for keyword in job_keywords:
                if keyword.lower() in project_text.lower():
                    project.relevance_score += 1

        # Sort by relevance score (highest first)
        projects.sort(key=lambda x: getattr(x, 'relevance_score', 0), reverse=True)

        # Remove the scoring attribute before returning
        for project in projects:
            if hasattr(project, 'relevance_score'):
                delattr(project, 'relevance_score')

        return projects

    def _prioritize_skills(self, job_keywords: List[str], job_type: str) -> Dict[str, List[str]]:
        """Prioritize skills based on job requirements"""
        skills = self.cv_data.skills.copy()

        # Define skill priorities based on job type
        if job_type.lower() in ['data analyst', 'data scientist', 'analytics']:
            priority_order = ['Data Analysis', 'Programming', 'Databases', 'Visualization', 'Tools', 'Other']
        elif job_type.lower() in ['python developer', 'software developer']:
            priority_order = ['Programming', 'Databases', 'Tools', 'Data Analysis', 'Visualization', 'Other']
        else:
            priority_order = list(skills.keys())

        # Reorder skills dictionary
        ordered_skills = {}
        for category in priority_order:
            if category in skills:
                ordered_skills[category] = skills[category]

        # Add any remaining categories
        for category, skill_list in skills.items():
            if category not in ordered_skills:
                ordered_skills[category] = skill_list

        return ordered_skills

    def _create_green_line(self, width=None):
        """Create a green horizontal line separator"""
        if width is None:
            width = 7.5 * inch  # Approximate A4 width minus margins

        drawing = Drawing(width, 4)
        line = Line(0, 2, width, 2)
        line.strokeColor = self.colors['green']
        line.strokeWidth = 2
        drawing.add(line)
        return drawing

    def _prioritize_courses(self, job_keywords: List[str], job_type: str) -> List[str]:
        """Prioritize courses based on job relevance"""
        courses = self.cv_data.courses.copy()

        # Score courses based on relevance
        scored_courses = []
        for course in courses:
            score = 0
            for keyword in job_keywords:
                if keyword.lower() in course.lower():
                    score += 1
            scored_courses.append((course, score))

        # Sort by score (highest first)
        scored_courses.sort(key=lambda x: x[1], reverse=True)

        return [course for course, _ in scored_courses]

    def generate_pdf(self, output_path: str, customized_data: CVData = None):
        """Generate PDF CV with gray background"""
        if customized_data is None:
            customized_data = self.cv_data

        # Create custom document template with gray background
        class GrayBackgroundDocTemplate(BaseDocTemplate):
            def __init__(self, filename, **kwargs):
                BaseDocTemplate.__init__(self, filename, **kwargs)

            def handle_pageBegin(self):
                # Draw gray background
                self.canv.setFillColor(self.colors['gray_bg'])
                self.canv.rect(0, 0, self.pagesize[0], self.pagesize[1], fill=1, stroke=0)
                BaseDocTemplate.handle_pageBegin(self)

        # Create document with gray background
        doc = SimpleDocTemplate(output_path, pagesize=A4, topMargin=0.75 * inch, bottomMargin=0.75 * inch,
                                leftMargin=0.75 * inch, rightMargin=0.75 * inch)

        # Override the canvas to add gray background
        def add_background(canvas, doc):
            canvas.setFillColor(self.colors['gray_bg'])
            canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)

        story = []

        # Header - Name (large, bold, left-aligned)
        story.append(Paragraph(customized_data.personal_info.name, self.styles['CVHeader']))
        story.append(Spacer(1, 0.1 * inch))

        # Contact info (left-aligned, multiple lines)
        story.append(Paragraph(customized_data.personal_info.email, self.styles['ContactInfo']))
        story.append(Paragraph(customized_data.personal_info.phone, self.styles['ContactInfo']))
        story.append(Paragraph(customized_data.personal_info.location, self.styles['ContactInfo']))
        if customized_data.personal_info.portfolio:
            story.append(Paragraph(customized_data.personal_info.portfolio, self.styles['ContactInfo']))

        story.append(Spacer(1, 0.2 * inch))

        # Summary section
        story.append(self._create_green_line())
        story.append(Spacer(1, 0.05 * inch))
        story.append(Paragraph("Professional Summary", self.styles['SectionHeader']))
        story.append(Paragraph(customized_data.summary, self.styles['Summary']))
        story.append(Spacer(1, 0.1 * inch))

        # Work Experience
        story.append(self._create_green_line())
        story.append(Spacer(1, 0.05 * inch))
        story.append(Paragraph("Work Experience", self.styles['SectionHeader']))

        for exp in customized_data.work_experience:
            story.append(Paragraph(exp.title, self.styles['JobTitle']))
            story.append(Paragraph(exp.period, self.styles['Period']))

            # Responsibilities without bullet points, just simple text
            for responsibility in exp.responsibilities:
                story.append(Paragraph(responsibility, self.styles['BulletPoint']))

            story.append(Spacer(1, 0.1 * inch))

        # Projects
        story.append(self._create_green_line())
        story.append(Spacer(1, 0.05 * inch))
        story.append(Paragraph("Projects", self.styles['SectionHeader']))

        for project in customized_data.projects:
            story.append(Paragraph(project.name, self.styles['JobTitle']))
            story.append(Paragraph(project.description, self.styles['BulletPoint']))

            for achievement in project.achievements:
                story.append(Paragraph(achievement, self.styles['BulletPoint']))

            story.append(Spacer(1, 0.1 * inch))

        # Skills
        story.append(self._create_green_line())
        story.append(Spacer(1, 0.05 * inch))
        story.append(Paragraph("Skills", self.styles['SectionHeader']))

        for category, skills in customized_data.skills.items():
            story.append(Paragraph(category, self.styles['JobTitle']))
            skills_text = ", ".join(skills)
            story.append(Paragraph(skills_text, self.styles['Skills']))
            story.append(Spacer(1, 0.05 * inch))

        # Education
        story.append(self._create_green_line())
        story.append(Spacer(1, 0.05 * inch))
        story.append(Paragraph("Education", self.styles['SectionHeader']))

        for edu in customized_data.education:
            story.append(Paragraph(edu.degree, self.styles['JobTitle']))
            story.append(Paragraph(edu.institution, self.styles['Company']))
            if edu.details:
                story.append(Paragraph(edu.details, self.styles['BulletPoint']))
            story.append(Spacer(1, 0.05 * inch))

        # Courses
        if customized_data.courses:
            story.append(self._create_green_line())
            story.append(Spacer(1, 0.05 * inch))
            story.append(Paragraph("Courses", self.styles['SectionHeader']))

            for course in customized_data.courses:
                story.append(Paragraph(course, self.styles['BulletPoint']))

        # Languages & Additional in one line sections
        additional_sections = []
        if customized_data.languages:
            additional_sections.append(("Languages", customized_data.languages))
        if customized_data.additional:
            additional_sections.append(("Additional", customized_data.additional))

        for section_name, items in additional_sections:
            story.append(self._create_green_line())
            story.append(Spacer(1, 0.05 * inch))
            story.append(Paragraph(section_name, self.styles['SectionHeader']))

            items_text = " | ".join(items)
            story.append(Paragraph(items_text, self.styles['Skills']))

        # Build with background
        doc.build(story, onFirstPage=add_background, onLaterPages=add_background)
        print(f"CV generated successfully: {output_path}")


class CVManager:
    def __init__(self, data_file: str = "cv_data.json"):
        self.data_file = data_file
        self.cv_data = self._load_or_create_data()

    def _load_or_create_data(self) -> CVData:
        """Load CV data from file or create default data"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return self._dict_to_cv_data(data)
        else:
            # Create default data based on your CV
            return self._create_default_data()

    def _create_default_data(self) -> CVData:
        """Create default CV data based on your current CV"""
        return CVData(
            personal_info=PersonalInfo(
                name="Olaf Siestrzykowski",
                email="olaf.siestrzykowski@gmail.com",
                phone="796694177",
                location="Warsaw, PL",
                portfolio="Portfolio available upon request"
            ),
            summary="Data Analyst with strong expertise in Python, Excel, SQL and Power BI. Enthusiastic about pursuing opportunities that enhance capabilities in data analysis and visualization. Dedicated to staying updated with latest technological advancements.",
            work_experience=[
                WorkExperience(
                    title="Junior Sales Analyst",
                    company="Absolvent",
                    period="2023-2025",
                    responsibilities=[
                        "Automated data flows by integrating CRM (via API) with reporting tools, reducing manual data entry time",
                        "Acted as key technical resource in small team, working independently on end-to-end data processes",
                        "Collaborated with managers to define metrics and track performance, delivering business-focused reports"
                    ],
                    technologies=["Python", "SQL", "Power BI", "APIs", "Google Sheets", "Looker Studio", "Zapier", "Jira", ""]
                ),
                WorkExperience(
                    title="Civil Engineer",
                    company="Mota Engil Central Europe",
                    period="2020-2022",
                    responsibilities=[
                        "Preparation of 20+ Interim Payment Certificates monthly",
                        "I improved data driven decision making by harnessing advanced Excel functions, enabling accurate problem analysis and driving strategic insights",
                        "Comprehensive monthly analysis of Production and Costs, resulting in improved efficiency and cost savings",
                        "Technological Projects, Weekly and Monthly Reports"
                    ],
                    technologies=["Excel", "Power Query", "AutoCAD"]
                ),

            ],
            projects=[
                Project(
                    name="Dance School Website",
                    description="Full-stack web development project with modern features",
                    technologies=["Python", "Django", "HTML/CSS", "JavaScript"],
                    achievements=[
                        "Configured SSL Certificate and domain connection (DNS)",
                        "Implemented Google Maps view and blog features"
                    ]
                ),
                Project(
                    name="Unveiling the Shinobi Secrets (Naruto Wiki Analysis)",
                    description="Data analysis and web scraping project",
                    technologies=["Python", "BeautifulSoup", "Pandas", "Data Visualization"],
                    achievements=[
                        "Scraped valuable insights from multiple wiki pages",
                        "Extracted, transformed data and visualized it ensuring clear understanding",
                        "Delivered actionable insights through data analysis"
                    ]
                )
            ],
            education=[
                Education(
                    degree="Bachelor of Science in Civil Engineering",
                    institution="Lublin University of Technology",
                    period="Completed"
                )
            ],
            skills={
                "Programming": ["Python (Pandas, Django, BS4, APIs)", "VBA"],
                "Data Analysis": ["Excel (Power Query, Power Pivot)", "SQL (PostgreSQL, MySQL)", "Power BI",
                                  "Looker Studio"],
                "Tools & Technologies": ["Git", "Linux", "Zapier"],
                "Other": ["Data Visualization", "API Integration", "Web Scraping"]
            },
            courses=[
                "Microsoft Excel - PowerQuery | VBA",
                "The Complete SQL Bootcamp 2022: Go from Zero to Hero",
                "Data Manipulation in Python: Master Python, Numpy & Pandas",
                "Power BI: Basics | Desktop | Advanced | Data Modeling"
            ],
            languages=["English - B2", "Polish - Native"],
            additional=["Driving Licence", "Continuously learning new technologies"]
        )

    def _dict_to_cv_data(self, data: dict) -> CVData:
        """Convert dictionary to CVData object"""
        return CVData(
            personal_info=PersonalInfo(**data['personal_info']),
            summary=data['summary'],
            work_experience=[WorkExperience(**exp) for exp in data['work_experience']],
            projects=[Project(**proj) for proj in data['projects']],
            education=[Education(**edu) for edu in data['education']],
            skills=data['skills'],
            courses=data['courses'],
            languages=data['languages'],
            additional=data['additional']
        )

    def save_data(self):
        """Save CV data to file"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(self.cv_data), f, indent=2, ensure_ascii=False)

    def generate_cv_for_job(self, job_title: str, job_keywords: List[str], output_dir: str = "generated_cvs"):
        """Generate customized CV for specific job"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Create CV generator
        generator = CVGenerator(self.cv_data)

        # Customize data for job
        customized_data = generator.customize_for_job(job_keywords, job_title)

        # Generate filename
        safe_job_title = "".join(c for c in job_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"CV_{safe_job_title}_{timestamp}.pdf"
        output_path = os.path.join(output_dir, filename)

        # Generate PDF
        generator.generate_pdf(output_path, customized_data)

        return output_path


def main():
    """Main function to demonstrate usage"""
    # Initialize CV Manager
    cv_manager = CVManager()

    # Save initial data
    cv_manager.save_data()

    # Example job applications
    job_applications = [
        {
            "title": "Data Analyst",
            "keywords": ["python", "sql", "power bi", "data analysis", "pandas", "excel", "visualization"]
        },
        {
            "title": "Python Developer",
            "keywords": ["python", "django", "api", "backend", "web development", "database", "git"]
        },
        {
            "title": "Business Analyst",
            "keywords": ["business analysis", "sql", "excel", "power bi", "stakeholder management", "requirements"]
        }
    ]

    # Generate CVs for different job types
    print("Generating customized CVs...")
    for job in job_applications:
        output_path = cv_manager.generate_cv_for_job(
            job_title=job["title"],
            job_keywords=job["keywords"]
        )
        print(f"Generated CV for {job['title']}: {output_path}")

    print("\nCV generation complete!")
    print("You can also use the CVManager class to:")
    print("1. Update your CV data in cv_data.json")
    print("2. Generate new CVs with: cv_manager.generate_cv_for_job('Job Title', ['keywords'])")


if __name__ == "__main__":
    main()