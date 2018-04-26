"""
Processor for Project information
"""
from structlog import get_logger
from bq_models.project import Project


logger = get_logger(__name__)


class ProjectProcessor:
    def __init__(self, google_client):
        self.google_client = google_client
        self.model = Project
        self.projects = Project.objects

    def sync_with_bq(self):
        logger.info("Syncing projects with BigQuery")
        new_projects = []
        for project in self.google_client.list_projects():
            name = project.friendly_name
            project_obj = Project.objects(name=name).first()
            if project_obj is None:
                project_obj = Project(name=name)
                project_obj.save()
                logger.info("Added project", project=name)
            new_projects.append(project_obj)
        self.projects = new_projects
        logger.info("Project info updated")
