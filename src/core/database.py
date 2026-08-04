import os

from dotenv import load_dotenv
from pymongo import MongoClient

from core.logger import logger


load_dotenv()


class Database:

    def __init__(self):

        logger.info("Connecting to MongoDB")

        self.client = MongoClient(
            os.getenv("MONGODB_URI"),
            serverSelectionTimeoutMS=5000
        )

        self.client.admin.command("ping")

        logger.info("MongoDB connected successfully")

        self.db = self.client[os.getenv("DATABASE_NAME")]

        self.collection = self.db[os.getenv("COLLECTION_NAME")]

    def save_report(self, report):

        result = self.collection.insert_one(report)

        logger.info(f"Report saved: {report['report_id']}")

        return str(result.inserted_id)

    def get_report(self, report_id):

        logger.info(f"Fetching report: {report_id}")

        return self.collection.find_one({"report_id": report_id})