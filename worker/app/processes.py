"""
Module to define process functions for better
code separation.
"""
from structlog import get_logger

from app.processors.projects import ProjectProcessor
from app.processors.datasets import DatasetProcessor
from app.processors.tables import TableProcessor


logger = get_logger(__name__)


class SchemaSynchronizer:
    def __init__(self, client):
        self.project_processor = ProjectProcessor(client)
        self.dataset_processor = DatasetProcessor(
            client,
            self.project_processor
        )
        self.table_processor = TableProcessor(
            client,
            self.dataset_processor
        )

    def sync(self):
        logger.info("Synchronizing with BQ")
        self.table_processor.sync()
