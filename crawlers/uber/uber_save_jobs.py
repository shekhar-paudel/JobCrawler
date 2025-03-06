import sqlite3
from datetime import datetime
def uber_save_new_jobs(jobs):
    conn = sqlite3.connect("db/jobs.db")
    cursor = conn.cursor()
    new_jobs = []
    for job in jobs:
        cursor.execute("SELECT Id FROM UberJobs WHERE Id = ?", (job["id"],))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO UberJobs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (job["id"], job["title"], job.get("description", ""),
                            job.get("department", ""), job.get("type", ""), job.get("programAndPlatform", ""),
                            job["location"].get("country", ""), job["location"].get("region", ""), job["location"].get("city", ""),
                            job["location"].get("countryName", ""), job.get("featured", False), job.get("level", ""),
                            job.get("creationDate", ""), job.get("updatedDate", ""),
                            job.get("team", ""), job.get("portalID", ""), job.get("isPipeline", False),
                            job.get("statusID", ""), job.get("statusName", ""),
                            job.get("uniqueSkills", ""), job.get("timeType", ""),
                            str(job.get("allLocations", ""))))
            new_jobs.append(job["title"])
    conn.commit()
    conn.close()
    return new_jobs

def uber_update_jobs(jobs):
    # Extract job IDs from API results
    current_job_ids = {job['id'] for job in jobs}
    
    # Connect to the database
    conn = sqlite3.connect("db/jobs.db")
    cursor = conn.cursor()
    
    # Fetch existing job IDs and titles from the database where JobRemovedDate is NULL
    cursor.execute("SELECT id, title FROM UberJobs WHERE JobRemovedDate IS NULL")
    existing_jobs = cursor.fetchall()
    existing_job_ids = {job[0] for job in existing_jobs}
    
    # Find job IDs that are in the database but not in the API response
    removed_job_ids = existing_job_ids - current_job_ids
    
    # Update JobRemovedDate for removed jobs and collect their titles
    removed_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    removed_job_titles = []
    for job_id, title in existing_jobs:
        if job_id in removed_job_ids:
            cursor.execute('''UPDATE UberJobs
                              SET JobRemovedDate = ?
                              WHERE id = ?''', (removed_date, job_id))
            removed_job_titles.append(title)
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()
    
    return removed_job_titles