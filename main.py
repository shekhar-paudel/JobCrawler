import time
from db.database import setup_db
from crawlers.uber.uber_fetch_jobs import uber_fetch_jobs
from crawlers.uber.uber_save_jobs import uber_save_new_jobs
from messenger.telegram.telegram import send_telegram_message
from logs.logging_config import logger
def main():

    setup_db()
    logger.info("Database setup complete.")
    while True:
        try:
            logger.info("Fetching Uber Jobs...")
            data = uber_fetch_jobs()
            if data and "data" in data and "results" in data["data"]:
                logger.info("Saving New Uber Jobs...")
                new_jobs = uber_save_new_jobs(data["data"]["results"])
                for job in new_jobs:
                    message = f"Uber Posted New Job: {job}"
                    print(message)
                    logger.info("Sending Telegram Message...")
                    send_telegram_message(message)
            time.sleep(1800)  # Wait 30 Minutes
        except KeyboardInterrupt:
            logger.warning("KeyboardInterrupt detected. Exiting...")
            break
        except Exception as e:
            logger.error(f"Error: {e}", exc_info=True)
            continue

if __name__ == "__main__":
    main()
