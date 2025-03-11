import sqlite3
from datetime import datetime
def deepgram_save_new_jobs(jobs):
    conn = sqlite3.connect("db/jobs.db")
    cursor = conn.cursor()
    new_jobs = []
    for job in jobs:
        cursor.execute("SELECT Id FROM DeepgramJobs WHERE Id = ?", (job["id"],))
        if cursor.fetchone() is None:
            cursor.execute('''INSERT INTO DeepgramJobs (Id, Title, DepartmentName, LocationName, WorkplaceType, EmploymentType, isListed, isConfidential, TeamNames, SecondaryLocationNames, CompensationTierSummary, CompensationTiers, ApplicationDeadline, CompensationTierGuideUrl, ScrapeableCompensationSalarySummary, DescriptionHtml, JobAddedDate)
                              VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', 
                           (job["id"], job["title"], job["departmentName"], job["locationName"], job["workplaceType"], job["employmentType"], job["isListed"], job["isConfidential"], 
                            str(job["teamNames"]), str(job["secondaryLocationNames"]), job["compensationTierSummary"], str(job["compensationTiers"]), job["applicationDeadline"], 
                            job["compensationTierGuideUrl"], job["scrapeableCompensationSalarySummary"], job["descriptionHtml"], datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            new_jobs.append(job)
    conn.commit()
    conn.close()
    return new_jobs
def deepgram_update_jobs(jobs):
    # Extract job IDs from API results
    current_job_ids = {job['id'] for job in jobs}
    
    # Connect to the database
    conn = sqlite3.connect("db/jobs.db")
    cursor = conn.cursor()
    
    # Fetch existing job IDs and titles from the database where JobRemovedDate is NULL
    cursor.execute("SELECT id, title FROM DeepgramJobs WHERE JobRemovedDate IS NULL")
    existing_jobs = cursor.fetchall()
    existing_job_ids = {job[0] for job in existing_jobs}
    
    # Find job IDs that are in the database but not in the API response
    removed_job_ids = existing_job_ids - current_job_ids
    
    # Update JobRemovedDate for removed jobs and collect their titles
    removed_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    removed_job_titles = []
    for job_id, title in existing_jobs:
        if job_id in removed_job_ids:
            cursor.execute('''UPDATE DeepgramJobs
                              SET JobRemovedDate = ?
                              WHERE id = ?''', (removed_date, job_id))
            removed_job_titles.append(title)
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()
    
    return removed_job_titles       
