import os
import re

def get_pdf_files(folder_path):
    return sorted(
        [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]
    )

def normalize_name(filename):
    base = os.path.splitext(filename)[0]
    base = re.sub(r'(_cv|_linkedin)', '', base, flags=re.IGNORECASE)
    return base.strip().lower()

def match_cv_linkedin(cv_folder, linkedin_folder):
    cv_files = get_pdf_files(cv_folder)
    linkedin_files = get_pdf_files(linkedin_folder)

    matches = {}
    for cv_file in cv_files:
        name = normalize_name(os.path.basename(cv_file))
        matches[name] = {"cv": cv_file, "linkedin": None}

    for li_file in linkedin_files:
        name = normalize_name(os.path.basename(li_file))
        if name in matches:
            matches[name]["linkedin"] = li_file
        else:
            matches[name] = {"cv": None, "linkedin": li_file}

    return {n: p for n, p in matches.items() if p["cv"] and p["linkedin"]}
