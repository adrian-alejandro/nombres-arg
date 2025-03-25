from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from .utils import pull_data_from_url, clean_column
from .config import (NAMES_DATA, LASTNAMES_DATA, NAMES_COLUMN, LASTNAMES_COLUMN,
                        NAMES_EXPORT, LASTNAMES_EXPORT, MAX_WORKERS, NAMES_RAW, 
                        LASTNAMES_RAW, NAMES_INTER, LASTNAMES_INTER)
from .logging_config import logger
import pandas as pd

class NameDataProcessor:
    def __init__(self):
        self.names_data = None
        self.lastnames_data = None
        self.unique_names = None
        self.unique_lastnames = None
        self.names_processed_data = None
        self.lastnames_processed_data = None

    def pull_data(self):
        logger.info("Fetching data from sources...")
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_names = executor.submit(pull_data_from_url, NAMES_DATA, usecols=[NAMES_COLUMN])
            future_lastnames = executor.submit(pull_data_from_url, LASTNAMES_DATA, usecols=[LASTNAMES_COLUMN])

            self.names_data = future_names.result()
            self.lastnames_data = future_lastnames.result()

        logger.info(f"Data successfully retrieved: {self.names_data.shape[0]} names, {self.lastnames_data.shape[0]} lastnames.")

    def process_data(self):
        logger.info("Processing data in parallel...")

        with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {
                executor.submit(clean_column, self.names_data.copy(deep=True), NAMES_COLUMN, True): "names",
                executor.submit(clean_column, self.lastnames_data.copy(deep=True), LASTNAMES_COLUMN, False): "lastnames"
            }

            for future in as_completed(futures):
                result_type = futures[future]
                try:
                    result, data = future.result()
                    if result_type == "names":
                        self.unique_names, self.names_processed_data = pd.Series(result, dtype=str), data
                    else:
                        self.unique_lastnames, self.lastnames_processed_data = pd.Series(result, dtype=str), data
                    logger.info(f"Finished processing {result_type}.")
                except Exception as e:
                    logger.error(f"Error processing {result_type}: {e}")

    def export_data(self, save_raw=False, save_intermediate=False):
        if save_raw:
            logger.info("Exporting raw data...")
            self.names_data.to_csv(NAMES_RAW, index=False)
            self.lastnames_data.to_csv(LASTNAMES_RAW, index=False)
            
        if save_intermediate:
            logger.info("Exporting intermediate results...")
            self.names_processed_data.to_csv(NAMES_INTER, index=False)
            self.lastnames_processed_data.to_csv(LASTNAMES_INTER, index=False)
        
        logger.info("Exporting processed data...")
        # The export is just a pandas Series, so no need for index or header
        self.unique_names.to_csv(NAMES_EXPORT, index=False, header=None)
        self.unique_lastnames.to_csv(LASTNAMES_EXPORT, index=False, header=None)
        
        logger.info("Data successfully exported.")

    def run(self, save_raw=False, save_intermediate=False):
        try:
            self.pull_data()
            self.process_data()
            self.export_data(save_raw=save_raw, save_intermediate=save_intermediate)
            logger.info("Preprocessing completed successfully.")
        except Exception as e:
            logger.error(f"An error occurred: {e}", exc_info=True)
