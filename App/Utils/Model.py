
import tensorflow as tf
import numpy as np
from pathlib import Path
from typing import List, Dict, Union

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = "/Skin-Diagnosis-ML-API/App/Model"


class Model:
    """A wrapper class for a TensorFlow model used for making predictions."""

    def __init__(self) -> None:
        """Initializes the model by loading it from the saved directory."""
        try:
            self.model = tf.saved_model.load(MODEL_PATH).signatures["serving_default"]
        except (OSError, ValueError) as e:
            raise RuntimeError(f"Error loading model from {MODEL_PATH}: {e}")

    def make_prediction(self, data: tf.Tensor) -> List[Dict[str, Union[float, Dict[str, float]]]]:
        """Makes a prediction using the loaded model.
        
        Args:
            data (tf.Tensor): Input data for the model.
        
        Returns:
            List[Dict[str, Union[float, Dict[str, float]]]]: A list of dictionaries containing class probabilities.
        
        Raises:
            ValueError: If the input data is not a valid tensor.
        """
        if not isinstance(data, tf.Tensor):
            raise ValueError("Input data must be a TensorFlow tensor.")
        
        data = tf.cast(data, tf.float32)  # Convert input to float32
        predictions = self.model(data)
        
        if "output_0" not in predictions:
            raise KeyError("Expected key 'output_0' not found in model output.")
        
        predictions = predictions["output_0"].numpy()  # Convert TensorFlow tensor to NumPy array
        
        if predictions.ndim != 2:
            raise ValueError("Unexpected output shape from model.")
        
        if predictions.shape[1] == 1:
            # Binary classification
            classes = ["Malignant", "Benign"]
            predictions = predictions.flatten()
            result = [{classes[0]: float(1 - prob), classes[1]: float(prob)} for prob in predictions]

        else:
            # Multi-class classification
            classes = [
                "Actinic keratoses", "Basal cell carcinoma", "Benign keratosis-like lesions",
                "Dermatofibroma", "Melanocytic nevi", "Melanoma", "Vascular lesions"
            ]
            if predictions.shape[1] != len(classes):
                raise ValueError("Mismatch between model output size and expected class labels.")
            
            result = [
                {classes[i]: float(prob) for i, prob in enumerate(pred)}
                for pred in predictions
            ]
        
        return result

    def __call__(self, images: tf.Tensor) -> List[Dict[str, Union[float, Dict[str, float]]]]:
        """Makes a prediction when the instance is called.
        
        Args:
            images (tf.Tensor): Input tensor of images.
        
        Returns:
            List[Dict[str, Union[float, Dict[str, float]]]]: A list of predictions.
        """
        return self.make_prediction(images)
