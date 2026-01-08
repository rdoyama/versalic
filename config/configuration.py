import datetime
import logging
from configparser import RawConfigParser

logger = logging.getLogger(__name__)

CONFIG_FILTER_KEY = "FILTERS"

class Configuration(RawConfigParser):
    def __init__(self, config_name: str = 'config.ini'):
        RawConfigParser.__init__(self)
        self.read(config_name, encoding="utf-8")
        self.validate_config()

    @staticmethod
    def validate_date(date_text: str):
        if date_text is None or not date_text.strip():
            return
        try:
            datetime.date.fromisoformat(date_text)
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")

    @staticmethod
    def validate_number(donation_value: str):
        if donation_value is None or not donation_value.strip():
            return
        try:
            float(donation_value)
        except ValueError:
            raise ValueError("Incorrect donation value, should be numeric")

    @staticmethod
    def validate_latin(string: str):
        return string.isascii()

    @staticmethod
    def validate_alpha(string: str):
        if string is None or not string.strip():
            raise ValueError(f"Missing mandatory fields")
        if not string.isalpha():
            raise ValueError(f"Incorrect String: {string} should only contain a-zA-Z")

    def validate_config(self):
        self.validate_latin(self.get("URL", "base_url"))
        self.validate_latin(self.get(CONFIG_FILTER_KEY, "city"))
        self.validate_alpha(self.get(CONFIG_FILTER_KEY, "state"))
        self.validate_number(self.get(CONFIG_FILTER_KEY, "min_donation"))
        self.set(CONFIG_FILTER_KEY, "min_donation", float(self.get(CONFIG_FILTER_KEY, "min_donation")) if self.get(CONFIG_FILTER_KEY, "min_donation") else 0)
        self.validate_number(self.get(CONFIG_FILTER_KEY, "max_donation"))
        self.set(CONFIG_FILTER_KEY, "max_donation", float(self.get(CONFIG_FILTER_KEY, "max_donation")) if self.get(CONFIG_FILTER_KEY, "max_donation") else 1e15)
        self.validate_date(self.get(CONFIG_FILTER_KEY, "from_date"))
        self.set(CONFIG_FILTER_KEY, "from_date", datetime.date.fromisoformat(self.get(CONFIG_FILTER_KEY, "from_date")) if self.get(CONFIG_FILTER_KEY, "from_date") else datetime.date.fromisoformat("1970-01-01"))
        self.validate_date(self.get(CONFIG_FILTER_KEY, "until_date"))
        self.set(CONFIG_FILTER_KEY, "until_date", datetime.date.fromisoformat(self.get(CONFIG_FILTER_KEY, "until_date")) if self.get(CONFIG_FILTER_KEY, "until_date") else datetime.date.today())

        if self.get(CONFIG_FILTER_KEY, "min_donation") > self.get(CONFIG_FILTER_KEY, "max_donation"):
            raise ValueError("min_donation should be less than max_donation")

        if self.get(CONFIG_FILTER_KEY, "from_date") > self.get(CONFIG_FILTER_KEY, "until_date"):
            raise ValueError("from_date should be less than until_date")

        logger.info("Configuration validated")