import sqlite3

def setup_db():
    conn = sqlite3.connect("db/jobs.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS UberJobs (
                        Id INTEGER PRIMARY KEY,
                        Title TEXT,
                        Description TEXT,
                        Department TEXT,
                        Type TEXT,
                        ProgramAndPlatform TEXT,
                        LocationCountry TEXT,
                        LocationRegion TEXT,
                        LocationCity TEXT,
                        LocationCountryName TEXT,
                        Featured BOOLEAN,
                        Level TEXT,
                        CreationDate TEXT,
                        UpdatedDate TEXT,
                        Team TEXT,
                        PortalId TEXT,
                        IsPipeline BOOLEAN,
                        StatusId TEXT,
                        StatusName TEXT,
                        UniqueSkills TEXT,
                        TimeType TEXT,
                        AllLocations TEXT,
                        JobRemovedDate TEXT)''')
    conn.commit()
    conn.close()
