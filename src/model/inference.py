import statsmodels.api as sm
import numpy as np
from scipy import stats
from src.logger import ProjectLogger


class ModelInference:
    """
    A class for performing model inference and generating forecasted values with confidence intervals.

    Attributes:
        model: Time series model used for inference.

    Methods:
        test_data_prediction: Generate forecasted values for test data.
        HoltWinterForecast_with_intervals: Generate forecasted values with confidence intervals using Holt-Winters method.
    """

    def __init__(self, model):
        """
        Initialize ModelInference class.

        Parameters:
            model: Time series model used for inference.
        """
        self.model = model
        self.logger = ProjectLogger().get_logger()

    def test_data_prediction(self, test_data):
        """
        Generate forecasted values for test data.

        Parameters:
            test_data (DataFrame): DataFrame containing the test data.

        Returns:
            forecast_with_intervals: Forecasted values with intervals.
        """
        try:
            # Generate forecasted values with intervals
            forecast_with_intervals = self.model.forecast(len(test_data))

            self.logger.info(f"Forecasted interval length is {len(test_data)}")

            return forecast_with_intervals
        except Exception as e:
            self.logger.exception("Error occurred while doing forecasting")

    def HoltWinterForecast_with_intervals(self, steps, confidence_level=0.95):
        """
        Generate forecasted values with confidence intervals using Holt-Winters method.

        Parameters:
            steps (int): Number of steps to forecast.
            confidence_level (float, optional): Confidence level for calculating confidence intervals. Default is 0.95.

        Returns:
            forecast_values (array-like): Forecasted values.
            lower_bound (array-like): Lower bound of confidence intervals.
            upper_bound (array-like): Upper bound of confidence intervals.
        """
        try:
            # Generate predictions with confidence intervals
            forecast_values = self.model.forecast(steps=steps)

            # Get residuals and calculate standard deviation
            residuals = self.model.resid
            std_residuals = np.std(residuals)

            # Calculate confidence intervals
            z_score = stats.norm.ppf((1 + confidence_level) / 2)
            lower_bound = forecast_values - z_score * std_residuals
            upper_bound = forecast_values + z_score * std_residuals

            self.logger.info("Forecasted demand with upper & lower bounds")

            return {
                "forecast": forecast_values,
                "lower_bound": lower_bound,
                "upper_bound": upper_bound,
            }

        except Exception as e:
            self.logger.exception(
                f"Exception occurred while forecasting with intervals {e}"
            )
