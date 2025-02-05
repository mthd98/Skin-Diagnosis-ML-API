
import tensorflow as tf
import numpy as np
from pathlib import Path
from typing import List, Dict, Union

BASE_DIR = Path(__file__).resolve().parent

image_pre_processor_fn = tf.keras.applications.efficientnet_v2.preprocess_input


class PreprocessImages:
    """Class for preprocessing images before passing them to a model."""

    def __init__(self) -> None:
        """Initializes the preprocessing class with the appropriate function."""
        self.image_pre_processor_fn = image_pre_processor_fn

    def get_image_tensor(self, image: tf.Tensor, image_size: tuple) -> tf.Tensor:
        """Converts an image file path to a preprocessed tensor.

        Args:
            image (tf.Tensor): Raw image tensor.
            image_size (tuple): Target size for resizing the image.

        Returns:
            tf.Tensor: Preprocessed image tensor.
        """
        if not isinstance(image, tf.Tensor):
            raise ValueError("Input image must be a TensorFlow tensor.")

        image = tf.image.decode_jpeg(image, channels=3)
        image = tf.image.resize(image, image_size, method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
        return image

    def image_preprocessing(self, image: tf.Tensor) -> tf.Tensor:
        """Applies preprocessing transformations to an image tensor.

        Args:
            image (tf.Tensor): Input image tensor.

        Returns:
            tf.Tensor: Preprocessed image tensor.
        """
        if self.image_pre_processor_fn:
            image = self.image_pre_processor_fn(image)
        else:
            image = image / 255.0
        return image

    def preprocess_image(self, image: tf.Tensor, image_size: tuple) -> tf.Tensor:
        """Preprocesses a single image.

        Args:
            image (tf.Tensor): Input image tensor.
            image_size (tuple): Target size for resizing the image.

        Returns:
            tf.Tensor: Preprocessed image tensor.
        """
        image = self.get_image_tensor(image, image_size)
        return self.image_preprocessing(image)

    def preprocess_image_batch(self, images: List, image_size: tuple) -> tf.Tensor:
        """Preprocesses a batch of images.

        Args:
            images (List[file]): List of files.
            image_size (tuple): Target size for resizing the images.

        Returns:
            tf.Tensor: Batch of preprocessed images.
        """
        if not all(isinstance(image, bytes) for image in images):
            raise ValueError("All elements in images must be files.")
        
        image_batch = [self.preprocess_image(image, image_size) for image in images]
        return tf.stack(image_batch)