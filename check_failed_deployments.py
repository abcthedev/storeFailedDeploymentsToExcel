import requests
import json
import openpyxl
import os

# GitHub repository info
OWNER = 'abcthedev'  # Replace with your GitHub username
REPO = 'storeFailedDeploymentsToExcel'  # Replace with your repository name
TOKEN = os.environ['TOKEN'] # Replace with your GitHub personal access token

# API URL to fetch deployments
url = f"https://api.github.com/repos/{OWNER}/{REPO}/deployments"

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_deployments():
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    # print("Deployments response:", response.json())  # Debugging: Print response from GitHub API
    return response.json()

def get_deployment_status(deployment_id):
    status_url = f"https://api.github.com/repos/{OWNER}/{REPO}/deployments/{deployment_id}/statuses"
    response = requests.get(status_url, headers=headers)
    response.raise_for_status()
    # print(f"Status for deployment {deployment_id}: {response.json()}")  # Debugging: Print statuses for each deployment
    return response.json()

def write_failed_deployments_to_excel(failed_deployments):
    if not failed_deployments:
        print("No failed deployments found.")
        return
    
    # Create an Excel workbook and add failed deployments
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Failed Deployments"
    ws.append(["Deployment ID", "Status", "Description", "Target URL", "Deployment URL", "Repository URL", "Created At"])

    for deployment in failed_deployments:
        ws.append([deployment['id'], deployment['state'], deployment['description'], deployment['target_url'], deployment['deployment_url'], deployment['repository_url'],  deployment['created_at']])

    # Save to file
    wb.save("failed_deployments.xlsx")
    print("Failed deployments report saved as failed_deployments.xlsx")

def main():
    deployments = get_deployments()
    if not deployments:
        print("No deployments found.")
        return

    failed_deployments = []

    for deployment in deployments:
        deployment_id = deployment['id']
        statuses = get_deployment_status(deployment_id)

        for status in statuses:
            if status['state'] == "failure":
                failed_deployments.append({
                    'id': deployment_id,
                    'state': status['state'],
                    'description': status.get('description', 'No description'),
                    'target_url':status['target_url'],
                    'deployment_url':status['deployment_url'],
                    'repository_url':status['repository_url'],
                    'created_at': status['created_at']
                })

    # Write failed deployments to Excel
    write_failed_deployments_to_excel(failed_deployments)

if __name__ == "__main__":
    main()
