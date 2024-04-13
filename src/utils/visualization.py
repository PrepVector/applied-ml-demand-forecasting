import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from src.logger import ProjectLogger


class Visualizer:
    """
    A class for generating visualizations using Plotly Express and Plotly Graph Objects.

    Attributes:
        None

    Methods:
        line_plot: Generate and display a line plot using Plotly Express.
        test_prediction_plot: Generate and display a line plot for test data and predictions using Plotly Graph Objects.
        forecast_with_confidence: Generate and display a forecast plot with confidence intervals using Plotly Graph Objects.
    """

    def __init__(self):
        self.logger = ProjectLogger().get_logger()

    def line_plot(self, data, y_column, title="", height=300):
        """
        Generate and display a line plot using Plotly Express.

        Parameters:
            data (DataFrame): DataFrame containing the data to plot.
            y_column (str): Name of the column to plot on the y-axis.
            title (str, optional): Title of the plot. Default is an empty string.
            height (int, optional): Height of the plot in pixels. Default is 300.

        Returns:
            fig: Plotly figure object.
        """
        try:
            fig = px.line(data, y=y_column, title=title, height=height)

            # Adjust line width
            fig.update_traces(line=dict(width=2))

            # Change layout of axes and the figure's margins
            # to emulate tight_layout
            fig.update_layout(
                xaxis=dict(showticklabels=False, linewidth=1),
                yaxis=dict(title=""),
                margin=dict(l=40, r=40, b=0, t=40, pad=0),
            )

            return fig

        except Exception as e:
            self.logger.exception("Error while plotting line graph", e)

    def test_prediction_plot(self, test_data, test_pred, y_col):
        """
        Generate and display a line plot for test data and predictions using Plotly Graph Objects.

        Parameters:
            test_data (DataFrame): DataFrame containing the test data.
            test_pred (DataFrame): DataFrame containing the predicted values.
            y_col (str): Name of the column to plot on the y-axis.

        Returns:
            fig: Plotly figure object.
        """
        try:
            # Create figure
            fig = go.Figure()

            # Plot test data with blue color
            fig.add_trace(
                go.Scatter(
                    x=test_data.index,
                    y=test_data[y_col],
                    mode="lines",
                    name="Test - Ground Truth",
                    line=dict(color="blue"),
                )
            )

            # Plot forecasted values with orange color
            fig.add_trace(
                go.Scatter(
                    x=test_data.index,
                    y=test_pred,
                    mode="lines",
                    name="Test - Prediction",
                    line=dict(color="orange"),
                )
            )

            fig.update_traces(line=dict(width=0.5))

            # Adjust layout
            fig.update_layout(
                xaxis_title="Date & Time (yyyy/mm/dd hh:MM)",
                yaxis_title="Energy Demand [MW]",
            )

            return fig
        except Exception as e:
            self.logger.exception("Error while plotting prediction plot", e)

    def forecast_with_confidence(self, forecast_values,model_name):
        """
        Generate and display a forecast plot with confidence intervals using Plotly Graph Objects.

        Parameters:
            forecast_values (dict): Dictionary containing forecast values and confidence intervals.

        Returns:
            fig: Plotly figure object.
        """
        try:
            # Plot the predictions with confidence intervals using Plotly
            fig = go.Figure()

            # Add predicted values
            fig.add_trace(
                go.Scatter(
                    x=np.arange(1, len(forecast_values["forecast"]) + 1),
                    y=forecast_values["forecast"],
                    mode="lines",
                    name="Predicted",
                )
            )

            # Add confidence intervals
            fig.add_trace(
                go.Scatter(
                    x=np.arange(1, len(forecast_values["lower_bound"]) + 1),
                    y=forecast_values["lower_bound"],
                    mode="lines",
                    line=dict(color="rgba(0,0,255,0.2)"),
                    name="Lower Bound",
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=np.arange(1, len(forecast_values["upper_bound"]) + 1),
                    y=forecast_values["upper_bound"],
                    mode="lines",
                    fill="tonexty",
                    fillcolor="rgba(0,0,255,0.2)",
                    line=dict(color="rgba(0,0,255,0.2)"),
                    name="Upper Bound",
                )
            )

            # Update layout
            fig.update_layout(
                title=model_name+" Forecast with Confidence Intervals",
                xaxis_title="Hours",
                yaxis_title="Forecasted Value",
            )

            return fig

        except Exception as e:
            self.logger.exception(
                "Error while plotting forecasting plot with confidence intervals", e
            )
