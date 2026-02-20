
def pdf_reader(file_path):
    from PyPDF2 import PdfReader
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


def show_pdf(file_path):
    import streamlit as st
    with open(file_path, "rb") as f:
        base64_pdf = f.read()
    st.download_button("Download Resume", base64_pdf)


def course_recommender(course_list):
    return course_list


# ********** Tech RoadMap **********

class Tech:

    def fetch_data(self):
        jobRoles = [
            "Backend Developer",
            "Frontend Developer",
            "Data Analyst",
            "ML Engineer",
            "DevOps Engineer"
        ]

        courses = [
            "Computer Science",
            "Information Technology",
            "Software Engineering"
        ]

        degree = ["B.Tech", "M.Tech", "BCA", "MCA"]

        return jobRoles, courses, degree

    def tfresherRoadmap(self, interest, education, degree):

        return {
            "roles": [interest],
            "companies": ["TCS", "Infosys", "Wipro", "Cognizant"]
        }


# ********** Non-Tech RoadMap **********

class NonTech:

    def fetch_data(self):

        jobRoles = [
            "HR Executive",
            "Graphic Designer",
            "Content Writer",
            "Digital Marketer"
        ]

        courses = [
            "Marketing Management",
            "Business Administration",
            "BA"
        ]

        return jobRoles, courses

    def jobOpportunity(self, interest, education):

        return {
            "companies": ["HCL", "Deloitte", "Accenture"]
        }


# ********** Job Listings **********

import random


def job_openings(role, location):

    cities = [
        "Bangalore",
        "Hyderabad",
        "Chennai",
        "Pune",
        "Mumbai",
        "Delhi",
        "Noida",
        "Gurgaon",
        "Ahmedabad",
        "Kolkata",
        "Coimbatore",
        "Visakhapatnam",
        "Indore",
        "Jaipur",
        "Lucknow",
        "Nagpur"
    ]

    platforms = [
        {
            "name": "Indeed",
            "base_url": "https://in.indeed.com/jobs?q="
        },
        {
            "name": "LinkedIn",
            "base_url": "https://www.linkedin.com/jobs/search/?keywords="
        },
        {
            "name": "Naukri",
            "base_url": "https://www.naukri.com/"
        },
        {
            "name": "Monster",
            "base_url": "https://www.monsterindia.com/srp/results?query="
        },
        {
            "name": "Shine",
            "base_url": "https://www.shine.com/job-search/"
        }
    ]

    # Salary ranges based on role type
    tech_high_salary_roles = [
        "Machine Learning Engineer",
        "AI Engineer",
        "Cloud Engineer",
        "DevOps Engineer"
    ]

    tech_mid_salary_roles = [
        "Backend Developer",
        "Frontend Developer",
        "Full Stack Developer",
        "Python Developer",
        "Java Developer"
    ]

    non_tech_roles = [
        "HR Executive",
        "Content Writer",
        "Graphic Designer",
        "Digital Marketer",
        "Sales Executive"
    ]

    job_list = []

    if role == "Select Job Role":
        role = "Software Engineer"

    selected_cities = cities

    if location and location.strip() != "":
        selected_cities = [
            city for city in cities
            if city.lower() == location.lower()
        ]

    for city in selected_cities:

        for _ in range(2):  # 2 listings per city

            if role in tech_high_salary_roles:
                min_salary = random.randint(8, 15)
                max_salary = random.randint(18, 30)
            elif role in tech_mid_salary_roles:
                min_salary = random.randint(5, 10)
                max_salary = random.randint(12, 20)
            elif role in non_tech_roles:
                min_salary = random.randint(3, 6)
                max_salary = random.randint(7, 12)
            else:
                min_salary = random.randint(4, 8)
                max_salary = random.randint(10, 15)

            salary_range = f"₹{min_salary} LPA - ₹{max_salary} LPA"

            platform = random.choice(platforms)

            if platform["name"] == "Naukri":
                link = platform["base_url"] + role.replace(" ", "-").lower() + "-jobs"
            elif platform["name"] == "Shine":
                link = platform["base_url"] + role.replace(" ", "-").lower()
            else:
                link = (
                    platform["base_url"]
                    + role.replace(" ", "+")
                    + "&location="
                    + city
                )

            job_list.append({
                "title": role,
                "location": city,
                "salary": salary_range,
                "platform": platform["name"],
                "link": link
            })

    return job_list

