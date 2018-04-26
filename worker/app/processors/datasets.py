"""
Dataset processor
"""
from structlog import get_logger
from bq_models.dataset import Dataset


logger = get_logger(__name__)


class DatasetProcessor:
    def __init__(self, google_client, project_processor):
        self.google_client = google_client
        self.datasets = Dataset.objects
        self.project_processor = project_processor

    def sync(self):
        self.project_processor.sync()
        self.sync_with_bq()

    def sync_with_bq(self):
        client = self.google_client
        projects = self.project_processor.projects
        new_dataset_list = []
        # loop over projects
        for project in projects:
            # set client project as the project we are scanning
            client.project = project.name
            logger.info("fetching datasets for project", project=project.name)
            # create a quick-lookup of db-held databases
            db_datasets = {
                x.name: x
                for x in self.datasets
                if x.project == project.id
            }
            # create a set which will contain names of datasets
            # synced from BigQuery
            bq_datasets = set()
            # loop over datasets we get back from the client for the project
            for dataset in client.list_datasets():
                dataset = client.get_dataset(dataset)
                data = {
                    "project": project.id,
                    "name": dataset.dataset_id,
                    "created": dataset.created,
                    "modified": dataset.modified
                }
                obj = None
                # if the dataset isn't in the db, insert new object
                if data['name'] not in db_datasets:
                    obj = Dataset(
                        **data
                    )
                    obj.save()
                    logger.info("Added dataset", dataset=dataset.dataset_id)
                # otherwise just update
                else:
                    obj = db_datasets[dataset.dataset_id]
                    obj.update(**data)
                    logger.info("Updated dataset", dataset=dataset.dataset_id)
                # add the dataset name to our set
                bq_datasets.add(obj.name)
                # add to the replacement list
                new_dataset_list.append(obj)
            logger.info("updated datasets for project", project=project.name)
            logger.info(
                "Deleting datasets from db that no longer exist in BigQuery"
            )
            # now delete all objects that aren't in BQ anymore
            Dataset.objects(
                project=project.id,
                name={"$nin": list(bq_datasets)}
            )
        # to be used for saving a db trip later
        self.datasets = new_dataset_list
        logger.info("updated datasets for all projects")
