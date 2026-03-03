def generate_summary(job_title, matched_skills):
    summary = f"Backend/Game-focused developer applying for {job_title}. "
    summary += "Experienced in " + ", ".join(matched_skills) + "."
    return summary