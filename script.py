import csv
import os
import time
from google import genai

# 1. Apni Gemini API Key yahan paste karein
GEMINI_API_KEY = "#add key"

client = genai.Client(api_key=GEMINI_API_KEY)


def get_company_insights_with_gemini(company_name, focus_area=""):
    prompt = f"""
    Analyze the company '{company_name}' (Focus Area: '{focus_area}').
    Provide a concise summary in two specific sections:

    1. Current & Past Key Projects/Services: (List 2-3 main projects, technologies, or client domains)
    2. Main Competitors: (List 3-4 direct market competitors)

    Format your output strictly as:
    PROJECTS: <brief projects summary>
    COMPETITORS: <list of competitors>
    """

    # Automatic Retry (Up to 3 attempts if server is busy)
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            text = response.text.strip()

            projects = "Information not found"
            competitors = "Information not found"

            lines = text.split("\n")
            for line in lines:
                if line.startswith("PROJECTS:"):
                    projects = line.replace("PROJECTS:", "").strip()
                elif line.startswith("COMPETITORS:"):
                    competitors = line.replace("COMPETITORS:", "").strip()

            return projects, competitors

        except Exception as e:
            # Agar 503 Server Heavy error aaye toh wait karke dobara try karein
            if attempt < max_retries - 1:
                print(
                    f"Server busy for {company_name}. Retrying in 3 seconds... (Attempt {attempt+1})"
                )
                time.sleep(3)
            else:
                return f"Error: {str(e)}", f"Error: {str(e)}"


def automate_company_research(
    input_csv="company.csv", output_csv="companies_output.csv"
):
    processed_data = []

    if not os.path.exists(input_csv):
        print(f"Error: '{input_csv}' file nahi mili!")
        return

    with open(input_csv, mode="r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            company = row["company_name"]
            focus = row.get("focus_area", "")
            print(f"Processing via Gemini AI: {company}...")

            projects, competitors = get_company_insights_with_gemini(
                company, focus
            )

            processed_data.append(
                {
                    "company_name": company,
                    "website": row.get("website", ""),
                    "focus_area": focus,
                    "project_insights": projects,
                    "competitor_insights": competitors,
                }
            )

            time.sleep(2)  # Safe delay between API calls

    fieldnames = [
        "company_name",
        "website",
        "focus_area",
        "project_insights",
        "competitor_insights",
    ]
    with open(output_csv, mode="w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(processed_data)

    print(
        f"\nTask Complete! High-quality results saved in '{output_csv}' file."
    )


if __name__ == "__main__":
    automate_company_research()