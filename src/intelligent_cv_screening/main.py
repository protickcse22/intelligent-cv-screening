import os
import json

from src.intelligent_cv_screening.utils import utils
from src.intelligent_cv_screening.crew import crew

if __name__ == "__main__":
    base_path = os.getcwd()
    cv_folder = os.path.join(base_path, "knowledge", "resumes")
    linkedin_folder = os.path.join(base_path, "knowledge", "linkedin")

    job_description = "Python developer with 5 years of experience in Django, REST APIs, and PostgreSQL."

    matched_candidates = utils.match_cv_linkedin(cv_folder, linkedin_folder)
    print(f"Total matched candidates: {len(matched_candidates)}")

    for idx, (name, files) in enumerate(matched_candidates.items(), start=1):
        print(f"\n--- Run {idx} ({name}) ---")
        print(f"CV: {files['cv']}")
        print(f"LinkedIn: {files['linkedin']}")
        if idx == 2:
            break

        result = crew.kickoff(
            inputs={
                "cv_file_path": files["cv"],
                "linkedin_file_path": files["linkedin"],
                "job_description": job_description
            }
        )
        result_json = result.json_dict
        # Upload CV and result_json to existing Odoo recruitment job
        if result_json and str(result_json["verdict"]).lower() == "reject" or str(result_json["verdict"]).lower() == "select":
            try:
                print(f"🔄 Uploading CV and complete screening results for {name} to existing Odoo job...")
                from src.intelligent_cv_screening.utils.odoo_manager import OdooManager

                odoo_manager = OdooManager()
                applicant_id = odoo_manager.upload_cv_to_existing_job(
                    cv_file_path=files["cv"],
                    candidate_name=name,
                    job_name="Python developer",  # Upload to existing job
                    verdict_data=result_json  # Pass the complete JSON structure
                )
                if applicant_id:
                    print(f"✅ Successfully uploaded {name}'s CV and complete screening data to Python developer job")
                    print(f"   📊 Data uploaded:")
                    print(f"      • Verdict: {result_json.get('verdict', 'Unknown')}")
                    print(f"   📄 Applicant ID: {applicant_id}")
                else:
                    print(f"❌ Failed to upload {name}'s data to Odoo job")
            except Exception as e:
                print(f"❌ Error uploading to Odoo job: {str(e)}")
                import traceback

                traceback.print_exc()
        else:
            print(f"✅ {name} processing complete - no upload needed (verdict: {result_json})")
