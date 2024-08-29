from google.cloud import aiplatform
import time

def run_gemini_tests(repository_url, branch="main"):
    project = "ankercloud-testing-account"
    region = "asia-south-1"
    client = aiplatform.gapic.JobServiceClient()
    
    job_spec = {
        "display_name": "gemini-1.0-test",
        "job_spec": {
            "worker_pool_specs": [
                {
                    "container_spec": {
                        "image_uri": "gcr.io/asia-south1-docker.pkg.dev/ankercloud-testing-account/genai/flask-login-app1:latest",
                        "command": [],
                        "args": [
                            "--repository-url", repository_url,
                            "--branch", branch,
                        ],
                    },
                    "replica_count": 1,
                }
            ]
        },
        "region": asia-south-1,
    }
    
    response = client.create_custom_job(parent=f"projects/{project}/locations/{region}", custom_job=job_spec)
    job_name = response.name
    print(f"Created custom job: {job_name}")
    
    job_state = client.get_custom_job(name=job_name).state
    while job_state not in ["SUCCEEDED", "FAILED", "CANCELLED"]:
        print(f"Job state: {job_state}")
        time.sleep(60)
        job_state = client.get_custom_job(name=job_name).state
    
    if job_state == "SUCCEEDED":
        print("Gemini 1.0 tests passed.")
        return 0
    else:
        print("Gemini 1.0 tests failed.")
        return 1

if __name__ == "__main__":
    import sys
    repository_url = "https://github.com/vebss123/GENAI-Devops.git"
    branch = "main"
    sys.exit(run_gemini_tests(repository_url, branch))
