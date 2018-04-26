"""
Configurations for the masses
"""
import os


class Config:
    class Mongo:
        host = os.getenv("MONGO_HOST", "localhost")
        port = int(os.getenv("MONGO_PORT", 27017))

    class Google:
        credentials_file = os.getenv("GCLOUD_CREDENTIALS_FILE")
