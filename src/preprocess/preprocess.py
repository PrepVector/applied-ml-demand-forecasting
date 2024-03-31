import pandas as pd
from src.logger import ProjectLogger


class DataPreprocessor:
    logger = ProjectLogger().get_logger()

    def __init__(self, data):
        self.data = data

    @staticmethod
    def remove_duplicates(data, subset):
        """
        Remove duplicates from the DataFrame based on the specified subset.

        Args:
            data (pd.DataFrame): Input DataFrame.
            subset (list): List of column names to consider for duplicate removal.

        Returns:
            pd.DataFrame: DataFrame with duplicates removed.
        """
        try:
            # Deduplicate, only keeping the last measurement per datetime
            data.drop_duplicates(subset=subset, keep="last", inplace=True)

            DataPreprocessor.logger.info("Removed duplicates")

            return data
        except Exception as e:
            DataPreprocessor.logger.exception(f"Error removing duplicates: {e}")
            return None

    @staticmethod
    def remove_outliers(data, column, threshold=3):
        """
        Remove outliers from the DataFrame based on the specified column.

        Args:
            data (pd.DataFrame): Input DataFrame.
            column (str): Column name to consider for outlier removal.
            threshold (float): Z-score threshold for identifying outliers.

        Returns:
            pd.DataFrame: DataFrame with outliers removed.
        """
        try:
            z_scores = (data[column] - data[column].mean()) / data[column].std()
            data_no_outliers = data[abs(z_scores) < threshold].copy()

            DataPreprocessor.logger.info("Removed Outliers")

            return data_no_outliers
        except Exception as e:
            DataPreprocessor.logger.exception(f"Error removing outliers: {e}")
            return None

    def preprocess_data(self):
        """
        Preprocess the loaded data:
        - Convert 'Datetime' column to datetime format.
        - Sort the DataFrame by 'Datetime' in ascending order.
        - Rename the target variable column to 'demand_in_MW'.

        Returns:
            pd.DataFrame or None: Processed DataFrame if successful, otherwise None.
        """
        if self.data is not None:
            try:
                # Convert 'Datetime' column to datetime format
                self.data["Datetime"] = pd.to_datetime(self.data["Datetime"])

                # Sort the DataFrame by 'Datetime' in ascending order
                self.data.sort_values(
                    by=["Datetime"], axis=0, ascending=True, inplace=True
                )
                self.data.reset_index(inplace=True, drop=True)

                # Rename the target variable column to 'demand_in_MW'
                self.data.rename(columns={"PJME_MW": "demand_in_MW"}, inplace=True)

                DataPreprocessor.logger.info("Data Preprocessing is done")

                return self.data
            except Exception as e:
                DataPreprocessor.logger.exception(f"Error preprocessing data: {e}")
                return None
        else:
            DataPreprocessor.logger.warning(
                "No data loaded. Use the load_file method first."
            )
            return None
