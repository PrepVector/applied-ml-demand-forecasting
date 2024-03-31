from statsmodels.tsa.seasonal import seasonal_decompose
from src.logger import ProjectLogger


class SeasonalDecomposer:
    def __init__(self, frequency):
        self.frequency = frequency
        self.logger = ProjectLogger().get_logger()

    def decompose(self, df, model="additive"):
        """
        Decompose the time-series data using seasonal_decompose.

        Parameters:
        - df (DataFrame): DataFrame containing the time-series data with a datetime index.
        - model (str, optional): Type of seasonal decomposition. Default is 'additive'.

        Returns:
        - decomposed (DecomposeResult): Result of seasonal decomposition.
        """
        try:
            series = df[["demand_in_MW"]]
            decomposed = seasonal_decompose(series, model=model, period=self.frequency)
            return decomposed
        except Exception as e:
            self.logger.exception("Error while doing seasonal decomposition")
