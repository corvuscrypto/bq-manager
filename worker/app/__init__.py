"""
App for the worker which grabs metadata
from BQ periodically.
"""
import datetime
import time

from structlog import get_logger

from bq_models import initialize as init_conn
from bq_models.internal import InternalState

from app.config import Config
from app.log_config import initialize as init_logger
from app.processes import SchemaSynchronizer
from app.google import get_client


logger = get_logger(__name__)


def initialize():
    init_logger()
    logger.info("Initializing Mongo Connection")
    init_conn(Config.Mongo.host, Config.Mongo.port)
    logger.info("Starting main program loop")
    main_loop()


def main_loop():
    synchronizer = SchemaSynchronizer(get_client())
    # check if internal status is there
    state = InternalState.objects.first()
    if state is None:
        state = InternalState()
        state.save()
    while True:
        state.update(
            status="updating",
            last_refresh=datetime.datetime.now()
        )
        synchronizer.sync()
        state.update(
            status="idle",
        )
        logger.info("sleeping for 30 minutes")
        time.sleep(30 * 60)
