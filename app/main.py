import os
import logging
import requests
from app.database import get_session
from app.models import Teddy360

log_level = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("app.log")],
)

logger = logging.getLogger(__name__)


def fetch_data():
    response = requests.get("https://jsonplaceholder.typicode.com/todos/")

    logger.info(f"HTTP GET Response Status: {response.status_code}")

    if response.status_code == 200:
        logger.info("Data fetched successfully")
        return response.json()
    else:
        logger.error(f"Failed to fetch data: {response.status_code}")
        return []


def store_data(data):
    logger.info("Starting to store data in the database")

    session = get_session()

    try:
        for item in data:
            if item["completed"]:
                teddy_item = Teddy360(
                    id=item["id"],
                    userId=item["userId"],
                    title=item["title"],
                    completed=item["completed"],
                )
                session.merge(teddy_item)
                logger.debug(f"Stored item: {item['id']} - {item['title']}")

        session.commit()
        logger.info("Data stored successfully")

    except Exception as e:
        logger.error(f"Error while storing data: {e}")
        session.rollback()
    finally:
        session.close()
        logger.info("Database session closed")


def main():
    logger.info("Starting the application")

    try:
        logger.info("Fetching data...")
        data = fetch_data()
        logger.info(f"Fetched {len(data)} records")
    except Exception as e:
        logger.error(f"Error fetching data: {e}")

    try:
        logger.info("Storing data in the database...")
        store_data(data)
        logger.info("Data stored successfully")
    except Exception as e:
        logger.error(f"Error storing data: {e}")

    logger.info("Application finished successfully")


if __name__ == "__main__":
    main()
