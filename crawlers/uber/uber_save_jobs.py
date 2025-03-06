import sqlite3

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
