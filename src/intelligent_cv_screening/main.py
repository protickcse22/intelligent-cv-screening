import os
import json

from src.intelligent_cv_screening.utils import utils
from src.intelligent_cv_screening.crew import crew

if __name__ == "__main__":
    base_path = os.getcwd()
    cv_folder = os.path.join(base_path, "knowledge", "resumes")
    print(base_path)
    print(cv_folder)
    linkedin_folder = os.path.join(base_path, "knowledge", "linkedin")

    job_description = "Python developer with 5 years of experience in Django, REST APIs, and PostgreSQL."

    matched_candidates = utils.match_cv_linkedin(cv_folder, linkedin_folder)
    print(f"Total matched candidates: {len(matched_candidates)}")

    for idx, (name, files) in enumerate(matched_candidates.items(), start=1):
        print(f"\n--- Run {idx} ({name}) ---")
        print(f"CV: {files['cv']}")
        print(f"LinkedIn: {files['linkedin']}")
        if idx == 1:
            continue

        result = crew.kickoff(
            inputs={
                "cv_file_path": files["cv"],
                "linkedin_file_path": files["linkedin"],
                "job_description": job_description
            }
        )
        result_json = result.json_dict
        print(result_json)
        print(result_json['verdict'])
        print("-" * 80)