import logging
import sys

from app.donation_csv import DonationCSV
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

    config = Configuration()
    donation_csv = DonationCSV(config)
    donation_csv.generate_donation_csv()


if __name__ == '__main__':
    main()