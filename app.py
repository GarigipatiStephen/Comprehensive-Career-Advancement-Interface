import streamlit as st
import random
import time
import os
from PIL import Image
from pyresparser import ResumeParser
from streamlit_tags import st_tags
from courses import (
    ds_course, web_course, android_course,
    ios_course, uiux_course,
    resume_videos, interview_videos, degrees
)
from utils import pdf_reader, show_pdf
import utils
from model import ResumeModel


st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="./Logo/recommend.png",
)

model = ResumeModel()


# MAIN FUNCTION

def run():

    img = Image.open("./Logo/RESUM.png")
    st.image(img)

    st.sidebar.markdown("## Menu")
    activities = ["Tech RoadMap", "Non-Tech RoadMap", "Resume Scoring"]
    choice = st.sidebar.selectbox("Choose among the given options:", activities)

   
    # ********** TECH ROADMAP **********
   

    if choice == "Tech RoadMap":

        st.title("Career Guidance For Tech People")

        techObj = utils.Tech()
        jobRoles, courses, degree = techObj.fetch_data()

        candidate_interest = st.selectbox("Select Job Role", jobRoles)
        preferred_location = st.text_input("Enter Preferred City")

        candidate_education = st.selectbox(
            "Select the Course Completed/Undergoing", courses
        )

        candidate_degree = st.selectbox(
            "Select the Degree Level", degrees["scieng"]
        )

        if st.button("Submit"):

            mapData = techObj.tfresherRoadmap(
                candidate_interest,
                candidate_education,
                candidate_degree,
            )

            if mapData:

                st.header("Suggested Roles")
                for role in mapData["roles"]:
                    st.write(role)

                st.header("Companies You Can Apply")
                for company in mapData["companies"]:
                    st.write(company)

                job_list = utils.job_openings(
                    candidate_interest,
                    preferred_location
                )

                st.header("Job Listings")

                cols = st.columns(2)

                for index, job in enumerate(job_list):
                    with cols[index % 2]:
                        st.markdown(
                            f"""
                            <div style='background-color:#111;padding:20px;
                            border-radius:15px;margin-bottom:20px;
                            box-shadow:0 0 10px rgba(0,0,0,0.4);'>
                                <h4 style='color:#4fc3f7'>{job['title']}</h4>
                                <p><b>Location:</b> {job['location']}</p>
                                <p><b>Salary:</b> {job['salary']}</p>
                                <p><b>Platform:</b> {job['platform']}</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        st.link_button("View Job", job["link"])

    # ********** NON-TECH ROADMAP **********


    elif choice == "Non-Tech RoadMap":

        st.title("Career Guidance For Non-Tech People")

        nontechObj = utils.NonTech()
        jobRoles, courses = nontechObj.fetch_data()

        candidate_interest = st.selectbox("Select Job Role", jobRoles)
        preferred_location = st.text_input("Enter Preferred City")

        candidate_education = st.selectbox(
            "Select the Course Completed/Undergoing", courses
        )

        candidate_degree = st.selectbox(
            "Select the Degree Level", degrees["arts"]
        )

        if st.button("Submit"):

            mapData = nontechObj.jobOpportunity(
                candidate_interest,
                candidate_education
            )

            if mapData:

                st.header("Companies You Can Apply")
                for company in mapData["companies"]:
                    st.write(company)

                job_list = utils.job_openings(
                    candidate_interest,
                    preferred_location
                )

                st.header("Job Listings")

                cols = st.columns(2)

                for index, job in enumerate(job_list):
                    with cols[index % 2]:
                        st.markdown(
                            f"""
                            <div style='background-color:#111;padding:20px;
                            border-radius:15px;margin-bottom:20px;
                            box-shadow:0 0 10px rgba(0,0,0,0.4);'>
                                <h4 style='color:#f48fb1'>{job['title']}</h4>
                                <p><b>Location:</b> {job['location']}</p>
                                <p><b>Salary:</b> {job['salary']}</p>
                                <p><b>Platform:</b> {job['platform']}</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        st.link_button("View Job", job["link"])

    # ********** RESUME SCORING **********

    elif choice == "Resume Scoring":

        st.header("Resume Analysis")

        pdf_file = st.file_uploader("Upload your Resume", type=["pdf"])

        if pdf_file is not None:

            upload_folder = "Uploaded_Resumes"
            os.makedirs(upload_folder, exist_ok=True)

            save_path = os.path.join(upload_folder, pdf_file.name)

            with open(save_path, "wb") as f:
                f.write(pdf_file.getbuffer())

            show_pdf(save_path)

            resume_data = ResumeParser(save_path).get_extracted_data()

            if not resume_data:
                st.error("Could not extract resume data.")
                return

            resume_text = pdf_reader(save_path)
            text_lower = resume_text.lower()

            st.success(f"Hello {resume_data.get('name', 'Candidate')}")

            if "experience" in text_lower:
                st.success("You are at Experienced level!")
            elif "internship" in text_lower:
                st.success("You are at Intermediate level!")
            else:
                st.info("You are at Fresher level!")

            skills = resume_data.get("skills", [])
            st.subheader("Your Current Skills")
            st_tags(label="", text="", value=skills, key="skills")

            predicted_domain, scores = model.predict_domain(skills)
            st.success(f"Our analysis says you are looking for {predicted_domain} Jobs")

        
            # ********** COURSE RECOMMENDATIONS **********
        

            st.header("Courses & Certificates Recommendations")

            if predicted_domain == "Data Science":
                course_list = ds_course
            elif predicted_domain == "Web Development":
                course_list = web_course
            elif predicted_domain == "Android Development":
                course_list = android_course
            elif predicted_domain == "IOS Development":
                course_list = ios_course
            elif predicted_domain == "UI-UX Development":
                course_list = uiux_course
            else:
                course_list = []

            num_courses = st.slider(
                "Choose Number of Course Recommendations:",
                1, 10, 5
            )

            for i, course in enumerate(course_list[:num_courses]):
                course_name, course_link = course
                st.markdown(
                    f"({i+1}) <a href='{course_link}' target='_blank' "
                    f"style='color:#4fc3f7;text-decoration:none;'>"
                    f"{course_name}</a>",
                    unsafe_allow_html=True
                )

            # ********** RESUME TIPS & SCORE **********

            st.header("Resume Tips & Ideas")

            resume_score = 0

            if "objective" in text_lower or "summary" in text_lower:
                resume_score += 6
                st.success("[+] Objective/Summary added")
            else:
                st.error("[-] Add Objective/Summary")

            if "education" in text_lower:
                resume_score += 12
                st.success("[+] Education added")
            else:
                st.error("[-] Add Education section")

            if "experience" in text_lower:
                resume_score += 16
                st.success("[+] Experience added")
            else:
                st.warning("[-] Add Work Experience")

            if "internship" in text_lower:
                resume_score += 6
                st.success("[+] Internship added")
            else:
                st.warning("[-] Add Internship")

            if "skills" in text_lower:
                resume_score += 7
                st.success("[+] Skills added")
            else:
                st.warning("[-] Add Skills section")

            if "project" in text_lower:
                resume_score += 19
                st.success("[+] Projects added")
            else:
                st.warning("[-] Add Projects")

            st.header("Resume Score")

            percentage_score = int((resume_score / 66) * 100)

            my_bar = st.progress(0)
            for i in range(percentage_score):
                time.sleep(0.01)
                my_bar.progress(i + 1)


            percentage_score = int((resume_score / 66) * 100)

            st.success(f"Your Resume Writing Score: {percentage_score}/100")
            # Professional Grade Feedback
            if percentage_score >= 85:
                st.success("🔥 Excellent Resume!")
            elif percentage_score >= 60:
                st.info("👍 Good Resume, but can be improved.")
            else:
                st.warning("⚠ Needs Improvement. Add missing sections.")


            st.header("Bonus Resume Writing Video")
            st.video(random.choice(resume_videos))

            st.header("Bonus Interview Tips Video")
            st.video(random.choice(interview_videos))


run()
