import pandas as pd
from src.logger import ProjectLogger


class DataLoader:
    def __init__(self, file_name):
        self.file_name = file_name
        self.logger = ProjectLogger().get_logger()

    def get_extension(self):
        """
        Get the file extension from the provided file name.

        Returns:
            str: File extension.
        """
        try:
            name_split = self.file_name.split(".")
            return name_split[-1]
        except Exception as e:
            self.logger.exception("Error while getting file extension")

    def load_file(self):
        """
        Load data from a CSV or Excel file based on the file extension.

        Returns:
            pd.DataFrame or None: Loaded DataFrame if successful, otherwise None.
        """

        extension = self.get_extension()
        if extension == "csv":
            try:
                data = pd.read_csv(self.file_name)
                return data
            except Exception as e:
                self.logger.exception(f"Error loading CSV file: {e}")
        elif extension == "xlsx":
            try:
                data = pd.read_excel(self.file_name)
                return data
            except Exception as e:
                self.logger.exception(f"Error loading Excel file: {e}")
        else:
            self.logger.exception(
                "Unsupported file format. Please provide a CSV or Excel file."
            )
