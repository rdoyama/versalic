import csv
import logging

from pydantic import BaseModel


logger = logging.getLogger(__name__)


def write_objects_to_csv(objects: list[BaseModel], headers: list[str], separator: str = ";", output: str = "data.csv"):
    dicts = [obj.model_dump(by_alias = True) for obj in objects]
    with open(output, mode='w', newline='', encoding="UTF-8") as f:
        csv_writer = csv.DictWriter(f, fieldnames=headers, delimiter=separator)

        csv_writer.writeheader()
        csv_writer.writerows(dicts)

    logger.info(f"CSV {output} written successfully")