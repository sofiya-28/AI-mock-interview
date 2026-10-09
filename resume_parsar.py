def extract_resume_sections(resume_text):

    skills = []
    projects = []
    experience = []

    current_section = None

    lines = resume_text.split("\n")

    skill_keywords = [
        "skills",
        "technical skills",
        "core competencies",
        "technologies"
    ]

    project_keywords = [
        "projects",
        "academic projects",
        "personal projects"
    ]

    experience_keywords = [
        "experience",
        "work experience"
    ]

    stop_sections = [
        "education",
        "certifications",
        "summary",
        "achievements"
    ]

    bullets = ["•", "-", "*"]

    for line in lines:

        line = line.strip()

        # Remove bullet symbols
        for bullet in bullets:
            if line.startswith(bullet):
                line = line[len(bullet):]
                line = line.strip()

        lower_line = line.lower()

        # Detect section start

        if any(keyword in lower_line for keyword in skill_keywords):
            current_section = "skills"
            continue

        if any(keyword in lower_line for keyword in project_keywords):
            current_section = "projects"
            continue

        if any(keyword in lower_line for keyword in experience_keywords):
            current_section = "experience"
            continue

        if any(keyword in lower_line for keyword in stop_sections):
            current_section = None
            continue

        if not line:
            continue

        # Handle comma-separated skills

        if current_section == "skills":

            if "," in line:
                items = line.split(",")
                for item in items:
                    skills.append(item.strip())
            else:
                skills.append(line)

        elif current_section == "projects":
            projects.append(line)

        elif current_section == "experience":
            experience.append(line)

    return skills, projects, experience