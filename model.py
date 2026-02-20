
class ResumeModel:

    def __init__(self):
        self.domain_keywords = {
            "Data Science": ["python", "machine learning", "tensorflow", "pandas", "numpy"],
            "Web Development": ["react", "django", "html", "css", "javascript"],
            "Android Development": ["android", "kotlin", "java", "flutter"],
            "IOS Development": ["ios", "swift", "xcode"],
            "UI-UX Development": ["figma", "adobe xd", "prototyping", "wireframe"]
        }

    def predict_domain(self, skills_list):
        scores = {}

        for domain, keywords in self.domain_keywords.items():
            score = 0
            for skill in skills_list:
                if skill.lower() in keywords:
                    score += 1
            scores[domain] = score

        predicted_domain = max(scores, key=scores.get)
        return predicted_domain, scores
