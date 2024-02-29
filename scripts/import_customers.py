import typer
import json

from sqlmodel import Session
from typing import Iterator, List, Tuple, Dict

from app.utils.logger import logger_config
from app.database import engine
from app.api.customers.models import Customer


logger = logger_config(__name__)

session = Session(engine)


def to_json_generator(file_handler: str) -> Iterator[Dict]:
    """Generate an Iterator object from a row converted to dict."""

    for row in file_handler:
        try:
            loaded_json = json.loads(row)
            if not loaded_json.get("language") in ("de", "en"):
                logger.info(
                    "Language changed to English as default value for row: "
                    "{}".format(row)
                )
                loaded_json["language"] = "en"

            yield loaded_json

        except Exception as error:
            logger.error(
                "Failed to load str to json in row: {}".format(repr(error)))
            continue


def append_if_exists_generator(
        list_dicts_handler: List[Dict]) -> Iterator[Dict]:
    """Generate an Iterator object if item exists in the database."""

    for item in list_dicts_handler:
        try:
            exists = bool(session.get(Customer, item.get('customer_id')))
        except Exception as error:
            logger.error(
                "Failed to execute query in db with id {}: {}".format(
                    item.get('customer_id'), repr(error)))
            continue

        if not exists:
            yield item


def process_customer_block(
        list_of_dicts: List[Dict],
        inserted_rows: int, skipped_rows: int) -> Tuple:
    """Process a block of items and return a tuple with counters."""

    bulk_list_to_insert = [
        Customer(**item) for item in append_if_exists_generator(list_of_dicts)]

    session.add_all(bulk_list_to_insert)
    session.commit()

    inserted_rows = len(bulk_list_to_insert)
    skipped_rows = len(list_of_dicts) - inserted_rows

    return inserted_rows, skipped_rows


def import_customer_json_file(file_path: str) -> None:
    """Main function that triggers an import from a file."""

    chunks: int = 1000
    counter: int = 0
    block_counter: int = 0

    inserted_rows: int = 0
    skipped_rows: int = 0

    total_inserted_rows: int = 0
    total_skipped_rows: int = 0
    block_to_process = []

    try:
        database_export_file = open(file_path, 'r')
    except FileNotFoundError as error:
        logger.error("File not found: %s", repr(error))
        return

    for row in to_json_generator(database_export_file):
        block_to_process.append(row)

        counter += 1
        if len(block_to_process) == chunks:
            inserted_rows, skipped_rows = process_customer_block(
                block_to_process, inserted_rows, skipped_rows)

            block_counter += block_counter
            block_to_process = []

            total_inserted_rows += inserted_rows
            total_skipped_rows += skipped_rows

            logger.info((
                "Items Procceced: {} Items "
                "Inserted: {} Items Skipped: {}").format(
                    counter, inserted_rows, skipped_rows))

    database_export_file.close()

    logger.info((
        "Total Items Procceced: {} Total Items "
        "Inserted: {} Total Items Skipped: {}").format(
        counter, total_inserted_rows, total_skipped_rows))


if __name__ == "__main__":
    typer.run(import_customer_json_file)
