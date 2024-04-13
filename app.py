import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from src.utils.load_file import DataLoader
from src.utils.seasonal_decompose import SeasonalDecomposer
from src.utils.visualization import Visualizer
from src.model.load_model import ModelLoader
from src.model.inference import ModelInference
from src.logger import ProjectLogger

# getting logger
logger = ProjectLogger().get_logger()

logger.info("Application Started")

# Set page configuration
st.set_page_config(
    page_title="Demand Forecasting",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)

# CSS style for title
title_style = """
            <style>
            .title {
                text-align: center;
                color:#faa356;
            }
            .steps-heading {
                color:#a2d2fb;
            }
            </style>
        """
st.markdown(title_style, unsafe_allow_html=True)


# Page heading
st.markdown(
    "<h1 class='title'>Demand Forecasting<span style='color:#b3cee5'>&#x1F4C8;</span></h1>",
    unsafe_allow_html=True,
)

# Problem Statement
problem_statement = """
        <h2 style="color:#a2d2fb">Problem Statement</h2>

        > Energy demand forecasting is crucial for effective resource planning and management in the power sector. 
        This Streamlit app aims to provide a user-friendly interface for energy demand forecasting, allowing users to 
        input relevant features and obtain forecasted electricity demand. """
st.markdown(problem_statement, unsafe_allow_html=True)

# adding vertical space between section to section
add_vertical_space(2)


# Steps to Solve
steps_to_solve = """
        <h2 class='steps-heading'>Steps to Solve</h2>

        <ol>
            <li><strong style="color:#4caf50">Data Preprocessing:</strong> Prepare the dataset for analysis by handling missing values, encoding categorical variables, and scaling numerical features.</li>
            <li><strong style="color:#4caf50">Exploratory Data Analysis (EDA):</strong> Explore the dataset to gain insights into the distribution of features, identify patterns, and detect anomalies.</li>
            <li><strong style="color:#4caf50">Feature Engineering:</strong> Create new features or transform existing ones to enhance the predictive power of the model. This may include generating lag features, extracting temporal information, or combining features.</li>
            <li><strong style="color:#4caf50">Model Selection and Training:</strong> Choose an appropriate machine learning model for forecasting electricity demand, such as linear regression, decision trees, or time series models. Train the selected model on the preprocessed dataset.</li>
            <li><strong style="color:#4caf50">Model Evaluation:</strong> Evaluate the performance of the trained model using appropriate metrics such as mean absolute error (MAE), mean squared error (MSE), or root mean squared error (RMSE). This step helps assess the accuracy and reliability of the forecasting model.</li>
            <li><strong style="color:#4caf50">Forecasting:</strong> Once the model is evaluated and deemed satisfactory, use it to generate forecasts of electricity demand. Provide users with the ability to input relevant features such as date, time, day of the week, etc., and obtain forecasted demand values.</li>
        </ol>
        """
st.markdown(steps_to_solve, unsafe_allow_html=True)

add_vertical_space(2)

# Data Exploration
data_exploration = """ <h2 style="color:#a2d2fb">Data Exploration</h2> """
st.markdown(data_exploration, unsafe_allow_html=True)
add_vertical_space(2)


def get_data(file_name):
    logger.info(f"Trying to load data in {file_name}")
    # getting the loaded data
    data_obj = DataLoader(file_name)
    data = data_obj.load_file()

    if "Unnamed: 0" in data.columns:
        data.set_index(["Unnamed: 0"], inplace=True)
        # data.drop(columns=["Unnamed: 0"],axis=1,inplace=True)

    return data


# dividing screen into two half to show raw data

raw_data_col, final_data_col = st.columns(2)

raw_data = None
final_data = None

with raw_data_col:
    with st.spinner("Loading Raw Data..!!!"):
        st.write("Raw Data")
        raw_data = get_data("data/raw_data/PJME_hourly.csv")
        st.dataframe(raw_data)

with final_data_col:
    with st.spinner("Loading Final Data...!!"):
        st.write("Final Data :")
        final_data = get_data("data/processed/final_data.csv")
        st.dataframe(final_data)


# Visualizations
data_exploration = """ <h2 style="color:#a2d2fb">Seasonal Decomposition of Data</h2> """
st.markdown(data_exploration, unsafe_allow_html=True)

# adding vertical spaces
add_vertical_space(2)


# function to get decomposed values
def get_decomposed_values(data, frequecny):
    logger.info("Trying to decompose data.")
    decomposer = SeasonalDecomposer(frequency=frequecny)
    decomposed_data = decomposer.decompose(data)
    return decomposed_data


# we've hourly data, so we'll be taking 24hrs per day into 365 days in a year
decomposed_data = get_decomposed_values(final_data, frequecny=24 * 365)


def get_visualizer():
    visualizer_obj = Visualizer()
    return visualizer_obj


visualizer = get_visualizer()

if decomposed_data != None:
    trend_col, seasonal_col = st.columns(2)

    residual_plot, _ = st.columns(2)

    with trend_col:
        with st.spinner("Visualizing Trend...!!!"):
            trend_plot = visualizer.line_plot(
                decomposed_data.trend, y_column="trend", title="Trend Plot", height=300
            )
            st.plotly_chart(trend_plot)

    with seasonal_col:
        with st.spinner("Visualizing Seasonality...!!!"):
            seasonal_plot = visualizer.line_plot(
                decomposed_data.seasonal,
                y_column="seasonal",
                title="Seasonal Plot",
                height=300,
            )
            st.plotly_chart(seasonal_plot)

    with residual_plot:
        with st.spinner("Visualizing Residuals...!!!"):
            residual_plot = visualizer.line_plot(
                decomposed_data.resid,
                y_column="resid",
                title="Residual Plot",
                height=300,
            )
            st.plotly_chart(residual_plot)


# energy Forecast
energy_forecast = """ <h2 style="color:#a2d2fb">Energy Demand Forecasting</h2> """
st.markdown(energy_forecast, unsafe_allow_html=True)

# model location
holt_winter_model_path = "models/holt_winter_model.pkl"
prophet_model_path = 'models/prophet_model.pkl'

# adding dropdown to select model
drop_down_col, _ = st.columns(2)

with drop_down_col:
    model_name= st.selectbox("Select Model",["Holt-Winter","Prophet"],index=0)


if model_name == "Prophet":
    # model obj
    model = ModelLoader().load_model(prophet_model_path)
else:
    model = ModelLoader().load_model(holt_winter_model_path)



# inferecning obj
inference_obj = ModelInference(model)

# loading test_data & plotting forecasting for test data
test_data = get_data("data/processed/test_data.csv")
test_data_pred = inference_obj.test_data_prediction(test_data,model_name)


test_pred_plot = visualizer.test_prediction_plot(
    test_data, test_data_pred, "demand_in_MW"
)

# test data Forecasting
add_vertical_space(2)
test_data_forecasting = """ <h4>Energy Demand Forecasting For Test Data</h4> """
st.markdown(test_data_forecasting, unsafe_allow_html=True)

_, plot_col, _ = st.columns([1, 3, 1])
with plot_col:
    st.plotly_chart(test_pred_plot)


add_vertical_space(2)

hourly_forecasting = """ <h4>Forecasting With Confidence Intervals</h4> """
st.markdown(hourly_forecasting, unsafe_allow_html=True)

add_vertical_space(2)

# dividing columns for plot & slider
slider_col, plot_col = st.columns([1, 3])


no_of_hours = 24
with slider_col:
    days = st.slider("No of days", min_value=1, max_value=100, value=2)
    if days:
        no_of_hours *= days

# forecasting for users input
if model_name=="Holt-Winter":
    forecast_values = inference_obj.HoltWinterForecast_with_intervals(
        no_of_hours, confidence_level=0.95
    )
else:
    forecast_values = inference_obj.ProphetForecast_with_intervals(
        no_of_hours
    )
forecast_plot = visualizer.forecast_with_confidence(forecast_values,model_name)
with plot_col:
    with st.spinner("Loading...!!!"):
        st.plotly_chart(forecast_plot)