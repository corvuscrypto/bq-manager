"""
Module to define process functions for better
code separation.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed

from structlog import get_logger

from app.google import get_client
from bq_models.dataset import Dataset
from bq_models.project import Project
from bq_models.table import Table


logger = get_logger(__name__)


def update_projects():
    client = get_client()
    projects = client.list_projects()
    for project in projects:
        name = project.friendly_name
        project_obj = Project.objects(name=name).first()
        if project_obj is None:
            logger.info("Adding project")
            project_obj = Project(name=name)
            project_obj.save()
    logger.info("Project info updated")


def update_datasets():
    client = get_client()
    projects = Project.objects
    for project in projects:
        client.project = project.name
        current_datasets = {
            x.name: x
            for x in Dataset.objects(project=project.id)
        }
        bq_datasets = client.list_datasets()
        for dataset in bq_datasets:
            dataset = client.get_dataset(dataset)
            data = {
                "project": project.id,
                "name": dataset.dataset_id,
                "created": dataset.created,
                "modified": dataset.modified
            }
            if dataset.dataset_id not in current_datasets:
                obj = Dataset(
                    **data
                )
                obj.save()
                logger.info("Added dataset %s", dataset.dataset_id)
            else:
                obj = current_datasets[dataset.dataset_id]
                obj.update(**data)
                logger.info("Updated dataset %s", dataset.dataset_id)

        logger.info("updated datasets for project %s", project.name)
    logger.info("updated datasets for all projects")


def get_table(client, table_ref):
    table = client.get_table(table_ref)
    return table


def update_tables():
    client = get_client()
    datasets = Dataset.objects
    project_name_by_id = {x.id: x.name for x in Project.objects}
    for dataset in datasets:
        project_name = project_name_by_id[dataset.project]
        client.project = project_name
        dataset_obj = client.dataset(dataset.name)
        table_refs = client.list_dataset_tables(dataset_obj)
        current_tables = {x.name: x for x in Table.objects(dataset=dataset.id)}
        # maximum overdrive cap'n!!!!!
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = [
                executor.submit(get_table, client, ref)
                for ref in table_refs
            ]
            for future in as_completed(futures):
                table = future.result()
                table_name = table.table_id
                data = {
                    "project": dataset.project,
                    "dataset": dataset.id,
                    "name": table_name,
                    "num_bytes": table.num_bytes,
                    "num_records": table.num_rows,
                    "schema": [x.to_api_repr() for x in table.schema],
                    "created": table.created,
                    "modified": table.modified,
                    "partitioning": table.partitioning_type
                }
                if table_name not in current_tables:
                    obj = Table(
                        project=dataset.project,
                        dataset=dataset.id,
                        name=table_name,
                        num_bytes=table.num_bytes,
                        num_records=table.num_rows,
                        schema=[x.to_api_repr() for x in table.schema],
                        created=table.created,
                        modified=table.modified,
                        partitioning=table.partitioning_type
                    )
                    obj.save()
                    logger.info("Added table %s to the database", table_name)
                else:
                    obj = current_tables[table_name]
                    obj.update(**data)
                    logger.info("Updated table %s", table_name)
    logger.info("All done")
