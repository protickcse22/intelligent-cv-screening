import os
import xmlrpc.client
import base64
import mimetypes
import socket

ODOO_URL = 'http://localhost:8069'
ODOO_DB = 'odoo_hr_db'
ODOO_USERNAME = 'admin'
ODOO_PASSWORD = 'odoo123'


class OdooManager:
    def __init__(self, url=ODOO_URL, db=ODOO_DB, username=ODOO_USERNAME, password=ODOO_PASSWORD):
        """Initialize OdooManager with connection parameters."""
        self.url = url
        self.db = db
        self.username = username
        self.password = password
        self.uid = None
        self.common = None
        self.models = None
        print(f"DEBUG: Initializing OdooManager with URL: {url}, DB: {db}, Username: {username}")
        self._connect()

    def _connect(self):
        """Connect to Odoo instance and authenticate."""
        try:
            print(f"DEBUG: Connecting to Odoo common endpoint at {self.url}/xmlrpc/2/common")
            self.common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
            print(f"DEBUG: Authenticating user '{self.username}' for database '{self.db}'")
            self.uid = self.common.authenticate(self.db, self.username, self.password, {})
            if not self.uid:
                raise ValueError("Authentication failed: Invalid credentials or database")
            print(f"DEBUG: Successfully authenticated as user ID: {self.uid}")
            self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')
            print("DEBUG: Connected to Odoo models endpoint")
        except xmlrpc.client.Fault as fault:
            print(f"ERROR: Odoo XML-RPC fault: {fault.faultCode} - {fault.faultString}")
            raise
        except socket.gaierror as e:
            print(f"ERROR: Network error - Failed to connect to {self.url}: {e}")
            raise ConnectionError(f"Failed to connect to Odoo server: {e}")
        except Exception as e:
            print(f"ERROR: Unexpected error during connection: {e}")
            raise

    def add_cvs(self, cv_path, position):
        """Adds a single CV to the specified position"""
        uid, models = self._connect()
        if not uid:
            return False

        if not os.path.exists(cv_path):
            print(f"❌ CV file not found: {cv_path}")
            return False

        try:
            # Read and encode CV file
            with open(cv_path, 'rb') as f:
                file_data = base64.b64encode(f.read()).decode('utf-8')

            # Extract applicant name from filename
            filename = os.path.basename(cv_path)
            applicant_name = os.path.splitext(filename)[0].replace('_', ' ')

            # Find job position by name
            job_ids = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD,
                                        'hr.job', 'search', [[('name', '=', position)]])

            if not job_ids:
                print(f"❌ Position '{position}' not found")
                return False

            job_id = job_ids[0]

            # Create applicant record
            applicant_data = {
                'name': applicant_name,
                'partner_name': applicant_name,
                'job_id': job_id,
                'email_from': f"{applicant_name.lower().replace(' ', '.')}@example.com",
                'description': f'CV uploaded: {filename}',
            }

            applicant_id = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD,
                                             'hr.applicant', 'create', [applicant_data])

            # Attach CV file
            attachment_data = {
                'name': filename,
                'type': 'binary',
                'datas': file_data,
                'res_model': 'hr.applicant',
                'res_id': applicant_id,
                'mimetype': 'application/pdf' if filename.lower().endswith('.pdf') else 'application/msword'
            }

            models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD,
                              'ir.attachment', 'create', [attachment_data])

            print(f"✅ Added {applicant_name} to {position}")
            return True

        except Exception as e:
            print(f"❌ Error adding CV: {e}")
            return False

    def upload_cv_to_existing_job(self, cv_file_path, candidate_name, job_name, verdict_data):
        """Upload CV to an existing job position with candidate screening data."""
        if not os.path.exists(cv_file_path):
            print(f"❌ CV file not found: {cv_file_path}")
            return False

        try:
            # Read and encode CV file
            with open(cv_file_path, 'rb') as f:
                file_data = base64.b64encode(f.read()).decode('utf-8')

            # Extract filename and applicant name
            filename = os.path.basename(cv_file_path)
            applicant_name = os.path.splitext(filename)[0].replace('_', ' ')

            # Find job position by name
            job_ids = self.models.execute_kw(self.db, self.uid, self.password,
                                           'hr.job', 'search', [[('name', '=', job_name)]])

            if not job_ids:
                print(f"❌ Job position '{job_name}' not found")
                return False

            job_id = job_ids[0]

            # Create applicant record
            applicant_data = {
                'name': f"Application for {job_name} - {candidate_name}",  # Mandatory field: Subject/Application
                'partner_name': candidate_name,
                'job_id': job_id,
                'email_from': f"{candidate_name.lower().replace(' ', '.')}@example.com",
            }

            applicant_id = self.models.execute_kw(self.db, self.uid, self.password,
                                                'hr.applicant', 'create', [applicant_data])

            # Attach CV file
            attachment_data = {
                'name': filename,
                'type': 'binary',
                'datas': file_data,
                'res_model': 'hr.applicant',
                'res_id': applicant_id,
                'mimetype': 'application/pdf' if filename.lower().endswith('.pdf') else 'application/msword'
            }

            self.models.execute_kw(self.db, self.uid, self.password,
                                 'ir.attachment', 'create', [attachment_data])

            # Upload complete screening results as JSON attachment if available
            if verdict_data:
                import json
                json_data = json.dumps(verdict_data, indent=2)
                json_base64 = base64.b64encode(json_data.encode('utf-8')).decode('utf-8')

                json_attachment_data = {
                    'name': f'{candidate_name}_screening_results.json',
                    'datas': json_base64,
                    'res_model': 'hr.applicant',
                    'res_id': applicant_id,
                    'type': 'binary',
                    'description': 'Complete AI Screening Results JSON (verdict, justification, scores, discrepancies)'
                }

                self.models.execute_kw(self.db, self.uid, self.password,
                                     'ir.attachment', 'create', [json_attachment_data])

            print(f"✅ Successfully uploaded CV and screening data for {candidate_name} to {job_name} (Applicant ID: {applicant_id})")
            return applicant_id

        except Exception as e:
            print(f"❌ Error uploading CV or updating applicant data: {e}")
            import traceback
            traceback.print_exc()
            return False

    def list_available_jobs(self):
        """List all available job positions."""
        try:
            job_ids = self.models.execute_kw(self.db, self.uid, self.password,
                                           'hr.job', 'search', [[]])
            jobs = self.models.execute_kw(self.db, self.uid, self.password,
                                        'hr.job', 'read', [job_ids], {'fields': ['id', 'name']})

            if not jobs:
                print("📭 No job positions found")
                return []

            print("📋 Available job positions:")
            for job in jobs:
                print(f"  - {job['name']} (ID: {job['id']})")
            return jobs

        except Exception as e:
            print(f"❌ Error listing job positions: {e}")
            return []

# Example usage
# if __name__ == "__main__":
#     try:
#         print("DEBUG: Starting OdooManager example")
#         base_path = os.getcwd()
#         parent_dir = os.path.dirname(base_path)
#         cv_folder = os.path.join(parent_dir, "knowledge", "resumes")
#         relative_cv_path = os.path.join(cv_folder, "Protick_Kumer_Dey.pdf")
#
#         # Sample result_json data for testing
#         result_json = {
#             "verdict": "Reject",
#             "justification": "The candidate's CV analysis shows a high confidence score of 85, indicating a strong initial match for a Python developer role based on explicit skills like Python, Django, and REST APIs, with a noted gap in PostgreSQL.",
#             "confidence_score": 85,
#             "matching_score": 40,
#             "discrepancies": [
#                 {
#                     "field": "Contact Email",
#                     "cv_value": "protick.kumerdey@gmail.com",
#                     "linkedin_value": "Not Found",
#                     "issue": "Missing in LinkedIn"
#                 },
#                 {
#                     "field": "Skills - Overall Breadth",
#                     "cv_value": "23 skills including Python, Django, REST APIs",
#                     "linkedin_value": "4 skills including Spring Boot",
#                     "issue": "Significant mismatch in skills listed"
#                 }
#             ]
#         }
#
#         # Initialize OdooManager
#         manager = OdooManager()
#         print(f"DEBUG: OdooManager initialized with URL: {manager.url}, DB: {manager.db}")
#
#         # List available jobs first
#         print("📋 Listing available jobs...")
#         manager.list_available_jobs()
#
#         # Upload CV to existing "Python developer" job with verdict data
#         print(f"🔄 Uploading CV with complete screening data: {relative_cv_path}")
#         applicant_id = manager.upload_cv_to_existing_job(
#             cv_file_path=relative_cv_path,
#             candidate_name="Protick Kumer Dey",
#             job_name="Python developer",
#             verdict_data=result_json  # Include the complete JSON data
#         )
#
#         if applicant_id:
#             print(f"✅ Successfully uploaded CV with screening data! Applicant ID: {applicant_id}")
#             print(f"   📊 Uploaded data includes:")
#             print(f"      • Verdict: {result_json['verdict']}")
#             print(f"      • Confidence Score: {result_json['confidence_score']}/100")
#             print(f"      • Matching Score: {result_json['matching_score']}/100")
#             print(f"      • Discrepancies: {len(result_json['discrepancies'])} issues")
#         else:
#             print("❌ Failed to upload CV")
#
#     except Exception as e:
#         print(f"ERROR: Example execution failed: {e}")
#         import traceback
#         traceback.print_exc()
