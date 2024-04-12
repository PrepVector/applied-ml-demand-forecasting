import pickle
from src.logger import ProjectLogger
from prophet import Prophet

class ModelLoader:
    logger = ProjectLogger().get_logger()

    @staticmethod
    def load_model(file_path):
        """
        Load a model from a pickle file.

        Parameters:
        - file_path (str): Path to the pickle file containing the model.

        Returns:
        - model: Loaded model object.
        """
        try:
            with open(file_path, "rb") as model_file:
                loaded_model = pickle.load(model_file)

            ModelLoader.logger.info("Model Loaded Successfully !!!")
            return loaded_model
        except Exception as e:
            ModelLoader.logger.exception(
                "Exception Occurred while loading the saved model"
            )
