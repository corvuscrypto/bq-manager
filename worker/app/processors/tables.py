"""
Table Processor
"""
from structlog import get_logger
from concurrent.futures import ThreadPoolExecutor, as_completed

from bq_models.table import Table


logger = get_logger(__name__)


def get_table(client, table_ref):
    table = client.get_table(table_ref)
    return table


class TableProcessor:
    def __init__(self, google_client, dataset_processor):
        self.google_client = google_client
        self.dataset_processor = dataset_processor

    def sync(self):
        self.dataset_processor.sync()
        self.sync_with_bq()

    def sync_with_bq(self):
        client = self.google_client
        datasets = self.dataset_processor.datasets
        project_name_by_id = {
            x.id: x.name
            for x in self.dataset_processor.project_processor.projects
        }
        for dataset in datasets:
            project_name = project_name_by_id[dataset.project]
            client.project = project_name
            dataset_ref = client.dataset(dataset.name)
            table_refs = client.list_dataset_tables(dataset_ref)
            db_tables = {
                x.name: x
                for x in Table.objects(dataset=dataset.id)
            }
            bq_tables = set()
            # Multithread to utilize response time of other requests
            #
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
                    obj = None
                    if table_name not in db_tables:
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
                        logger.info(
                            "Added table to the database",
                            table=table_name
                        )
                    else:
                        obj = db_tables[table_name]
                        obj.update(**data)
                        logger.info("Updated table", table=table_name)
                    # add object to bq table set
                    bq_tables.add(obj.name)
            # delete tables no longer in BQ
            logger.info("Deleting tables no longer in BigQuery")
            Table.objects(
                dataset=dataset.id,
                name={"$nin": list(bq_tables)}
            ).delete()
        logger.info("All done")
