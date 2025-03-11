import requests

url_board = "https://jobs.ashbyhq.com/api/non-user-graphql?op=ApiJobBoardWithTeams"
url_job = "https://jobs.ashbyhq.com/api/non-user-graphql?op=ApiJobPosting"
headers = {
    "Content-Type": "application/json",
}

def get_jobs():
    data = {
        "operationName": "ApiJobBoardWithTeams",
        "variables": {"organizationHostedJobsPageName": "Deepgram"},
        "query": """
        query ApiJobBoardWithTeams($organizationHostedJobsPageName: String!) {
          jobBoard: jobBoardWithTeams(organizationHostedJobsPageName: $organizationHostedJobsPageName) {
            jobPostings {
              id
              __typename
            }
            __typename
          }
        }
        """
    }
    response = requests.post(url_board, json=data, headers=headers)
    return [job["id"] for job in response.json().get("data", {}).get("jobBoard", {}).get("jobPostings", [])]

def get_job_details(job_id):
    data = {
        "operationName": "ApiJobPosting",
        "variables": {"organizationHostedJobsPageName": "Deepgram", "jobPostingId": job_id},
        "query": """
        query ApiJobPosting($organizationHostedJobsPageName: String!, $jobPostingId: String!) {
          jobPosting(
            organizationHostedJobsPageName: $organizationHostedJobsPageName
            jobPostingId: $jobPostingId
          ) {
            id
            title
            departmentName
            locationName
            workplaceType
            employmentType
            isListed
            isConfidential
            teamNames
            secondaryLocationNames
            compensationTierSummary
            compensationTiers {
              id
              title
              tierSummary
            }
            applicationDeadline
            compensationTierGuideUrl
            scrapeableCompensationSalarySummary
            descriptionHtml
          }
        }
        """
    }
    response = requests.post(url_job, json=data, headers=headers)
    return response.json().get("data", {}).get("jobPosting", {})



def deepgram_fetch_jobs():
    job_ids = get_jobs()
    jobs = []
    for job_id in job_ids:
        job_details = get_job_details(job_id)
        #print(job_details)
        jobs.append(job_details)
    return jobs
