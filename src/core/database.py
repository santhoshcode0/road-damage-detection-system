import os

import certifi
from dotenv import load_dotenv
from pymongo import MongoClient

from core.logger import logger


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv()


class Database:

    def __init__(self):

        logger.info(
            "Connecting to MongoDB"
        )

        # --------------------------------------------------
        # MongoDB connection
        # --------------------------------------------------

        self.client = MongoClient(
            os.getenv("MONGODB_URI"),
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=5000
        )

        # --------------------------------------------------
        # Test connection
        # --------------------------------------------------

        self.client.admin.command(
            "ping"
        )

        logger.info(
            "MongoDB connected successfully"
        )

        # --------------------------------------------------
        # Database and collection
        # --------------------------------------------------

        self.db = self.client[
            os.getenv("DATABASE_NAME")
        ]

        self.collection = self.db[
            os.getenv("COLLECTION_NAME")
        ]

        # --------------------------------------------------
        # Create indexes
        # --------------------------------------------------

        self.create_image_hash_index()


    # --------------------------------------------------
    # Image hash index
    # --------------------------------------------------

    def create_image_hash_index(self):

        """
        Creates a unique index for image hashes.

        sparse=True allows older reports that do not
        contain image_hash to remain valid.
        """

        self.collection.create_index(
            "image_hash",
            unique=True,
            sparse=True
        )

        logger.info(
            "Image hash index ready"
        )


    # --------------------------------------------------
    # Save report
    # --------------------------------------------------

    def save_report(self, report):

        result = self.collection.insert_one(
            report
        )

        logger.info(
            f"Report saved: {report['report_id']}"
        )

        return str(
            result.inserted_id
        )


    # --------------------------------------------------
    # Get report
    # --------------------------------------------------

    def get_report(self, report_id):

        logger.info(
            f"Fetching report: {report_id}"
        )

        return self.collection.find_one(
            {
                "report_id": report_id
            }
        )


    # --------------------------------------------------
    # Get report by image hash
    # --------------------------------------------------

    def get_report_by_image_hash(
        self,
        image_hash
    ):

        logger.info(
            f"Checking image hash: {image_hash}"
        )

        return self.collection.find_one(
            {
                "image_hash": image_hash
            }
        )


    # --------------------------------------------------
    # Get all reports
    # --------------------------------------------------

    def get_all_reports(self):

        logger.info(
            "Fetching all reports"
        )

        return list(
            self.collection
            .find()
            .sort(
                "created_at",
                -1
            )
        )


    # --------------------------------------------------
    # Get recent reports
    # --------------------------------------------------

    def get_recent_reports(
        self,
        limit=3
    ):

        logger.info(
            f"Fetching latest {limit} reports"
        )

        return list(
            self.collection
            .find()
            .sort(
                "created_at",
                -1
            )
            .limit(limit)
        )


    # --------------------------------------------------
    # Get next report number
    # --------------------------------------------------

    def get_next_report_number(self):

        return (
            self.collection.count_documents({})
            + 1
        )


    # --------------------------------------------------
    # Get dashboard statistics
    # --------------------------------------------------

    def get_stats(self):

        reports = list(
            self.collection.find()
        )

        total_reports = len(
            reports
        )

        total_damages = sum(
            r.get(
                "detection_result",
                {}
            ).get(
                "total_damages",
                0
            )
            for r in reports
        )

        pending_reports = sum(
            1
            for r in reports
            if r.get("status") == "Pending"
        )

        completed_reports = sum(
            1
            for r in reports
            if r.get("status") == "Completed"
        )

        return {
            "total_reports": total_reports,
            "total_damages": total_damages,
            "pending_reports": pending_reports,
            "completed_reports": completed_reports
        }


    # --------------------------------------------------
    # Update report status
    # --------------------------------------------------

    def update_status(
        self,
        report_id,
        status
    ):

        self.collection.update_one(
            {
                "report_id": report_id
            },
            {
                "$set": {
                    "status": status
                }
            }
        )

        logger.info(
            f"Updated {report_id} to {status}"
        )