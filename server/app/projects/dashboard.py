"""
Functions and views for the project dashboard
"""
from flask import jsonify
from app.utils.decorators import render
from app.utils.google import get_client
import logging


logger = logging.getLogger(__name__)


def add_routes(blueprint):
    """
    Add the routes to the blueprint passed in
    """
    blueprint.add_url_rule(
        "/project/<project>",
        "dashboard",
        view_func=dashboard
    )
    blueprint.add_url_rule(
        "/project/<project>/dataset/list",
        "dataset_list",
        view_func=get_datasets
    )
    blueprint.add_url_rule(
        "/project/<project>/dataset/<dataset>/usage",
        "dataset_usage",
        view_func=get_dataset_usage
    )


def get_datasets(project):
    client = get_client(project)
    datasets = list(client.list_datasets())
    return jsonify({
        "datasets": [d.dataset_id for d in datasets]
    })


def get_dataset_usage(project, dataset):
    client = get_client(project)
    dataset = client.dataset(dataset)
    tables = client.list_dataset_tables(dataset)
    total_bytes = 0
    for table in tables:
        total_bytes += client.get_table(table).num_bytes
    return jsonify({
        "bytes": total_bytes
    })


@render("projects/dashboard.j2")
def dashboard(project):
    """
    Dashboard of the project
    """
    return {
        "project": project,
    }
