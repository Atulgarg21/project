import csv
import os
import time
from google import genai

# 1. Apni Gemini API Key yahan paste karein
GEMINI_API_KEY = "#add your api key"


# 2. AAPKI EXACT SKILL SET (Yahan apni technical skills & role define karein)
MY_SKILLS = """
- Core Skills: Python, SQL, Web Development (React, Node.js), Cloud Architecture (AWS)
- Knowledge/Background: Software Design, Relational Database Design, System Modularity, Data Structures
- Preferred Roles: Software Engineering Intern, Full-Stack Developer, Python/Backend Developer, Database Engineer
"""

client = genai.Client(api_key=GEMINI_API_KEY)


def evaluate_and_draft_email(company_name, focus_area, projects):
    """Pehle skill match check karega. Agar fit hoga tabhi cold email draft karega."""
    prompt = f"""
    You are an expert tech recruiter and career advisor.
    
    Target Company: '{company_name}'
    Company Focus Area: {focus_area}
    Company Projects: {projects}

    Candidate Profile & Skills:
    {MY_SKILLS}

    TASK:
    Step 1: Determine if the company's work matches the candidate's skill set (Python, Full-stack, Database/SQL, Cloud).
    Step 2: 
    - If MATCH IS WEAK/IRRELEVANT (e.g. pure hardware, pure video editing, non-tech): 
      Output ONLY: "NO_MATCH"
    
    - If MATCH IS GOOD: 
      Draft a concise, high-converting cold email (under 120 words) connecting candidate skills to company projects.
      Format strictly as:
      MATCH: YES
      SUBJECT: <Catchy personalized subject line>
      BODY: <Professional email body>
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"


def process_targeted_drafts(
    input_csv="companies_output.csv", output_csv="relevant_emails.csv"
):
    if not os.path.exists(input_csv):
        print(f"Error: '{input_csv}' file nahi mili!")
        return

    matched_emails = []

    with open(input_csv, mode="r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)

        for row in reader:
            company = row["company_name"]
            focus = row.get("focus_area", "")
            projects = row.get("project_insights", "")

            print(f"\n🔍 Evaluating skill match for: {company}...")

            result = evaluate_and_draft_email(company, focus, projects)

            if "NO_MATCH" in result:
                print(
                    f"❌ SKIPPED: {company} (Skill set match nahi hua/Irrelevant)"
                )
            else:
                print(f"✅ MATCH FOUND! Drafting Mail for {company}:\n")
                print("-" * 50)
                print(result)
                print("-" * 50)

                row["drafted_email"] = result
                matched_emails.append(row)

            time.sleep(1.5)  # API delay

    # Sirf matched companies ka output new CSV me save hoga
    if matched_emails:
        fieldnames = list(matched_emails[0].keys())
        with open(
            output_csv, mode="w", newline="", encoding="utf-8"
        ) as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(matched_emails)

        print("\n" + "🎉 " * 5)
        print(
            f"Done! Sirf relevant companies ke mails '{output_csv}' me save ho gaye hain."
        )
    else:
        print("\nKisi bhi company se skill match nahi hua.")


if __name__ == "__main__":
    process_targeted_drafts()