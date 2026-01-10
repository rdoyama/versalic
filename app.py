import logging
import sys
import time

from app.donation_from_city_csv import DonationFromCityCSV
from app.donation_to_city_csv import DonationToCityCSV
from config.configuration import Configuration

logger = logging.getLogger(__name__)

def main():
    logging.basicConfig(
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('Logs.log'),
        ],
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] (%(filename)s:%(lineno)d) - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        encoding='utf-8'
    )

    start = time.time()

    config = Configuration()

    if config.get("FILES", "donation_to_city_csv").lower() == "true":
        donation_to_city_csv = DonationToCityCSV(config)
        donation_to_city_csv.generate_donation_csv()

    if config.get("FILES", "donation_from_city_csv").lower() == "true":
        donation_from_city_csv = DonationFromCityCSV(config)
        donation_from_city_csv.generate_donation_csv()

    logger.info(f"Total execution time: {time.time() - start:.2f} seconds")

if __name__ == '__main__':
    main()