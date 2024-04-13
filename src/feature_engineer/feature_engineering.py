import pandas as pd
from src.logger import ProjectLogger


class FeatureEngineering:
    def __init__(self, data):
        self.logger = ProjectLogger().get_logger()
        self.data = data

    def add_time_features(self):
        """
        Add time-related features to the DataFrame.

        Returns:
            pd.DataFrame or None: DataFrame with added time features if successful, otherwise None.
        """
        if self.data is not None:
            try:
                # Add time-related features
                self.data["dow"] = self.data.index.dayofweek
                self.data["doy"] = self.data.index.dayofyear
                self.data["year"] = self.data.index.year
                self.data["month"] = self.data.index.month
                self.data["quarter"] = self.data.index.quarter
                self.data["hour"] = self.data.index.hour
                self.data["weekday"] = self.data.index.weekday
                self.data["woy"] = self.data.index.isocalendar().week
                self.data["dom"] = self.data.index.day
                self.data["date"] = self.data.index.date

                # Add the season number
                self.data["season"] = self.data["month"].apply(
                    lambda month_number: (month_number % 12 + 3) // 3
                )

                return self.data
            except Exception as e:
                self.logger.exception(f"Error adding time features: {e}")
                return None
        else:
            self.logger.warning("No data provided.")
            return None

    # this is a sample function, where you can code your own features
    def customized_features(self):
        pass
