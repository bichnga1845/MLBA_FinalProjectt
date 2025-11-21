"""
Quick test script for the MobileNetV2 fruit-type model stored in train_ml_result/.
Works with TensorFlow/Keras 2.15 (legacy) by providing a compatible InputLayer.
"""

import os
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing import image
from tensorflow.keras.mixed_precision import Policy as MPPolicy

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from final_ml.ui.ui_resultExt import ui_resultExt  # noqa: E402


@keras.utils.register_keras_serializable(name="LegacyInputLayer")
class LegacyInputLayer(keras.layers.InputLayer):
    """InputLayer that ignores batch_shape keys produced by older TF versions."""

    def __init__(self, *args, **kwargs):
        kwargs.pop("batch_shape", None)
        kwargs.pop("batch_input_shape", None)
        super().__init__(*args, **kwargs)


keras.utils.get_custom_objects()["InputLayer"] = LegacyInputLayer
keras.utils.get_custom_objects()["DTypePolicy"] = MPPolicy

MODEL_PATH = BASE_DIR / "train_ml_result" / "v2_best_fruit_type_model.h5"
DEFAULT_IMAGE = BASE_DIR / "final_ml" / "uploads" / "banana.jpg"


def predict_fruit_type(model, img_path, class_indices, img_size=(160, 160)):
    """Load image, run inference and show result."""
    img = image.load_img(img_path, target_size=img_size, color_mode="rgb")
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0

    pred = model.predict(img_array, verbose=0)[0]
    pred_index = int(np.argmax(pred))
    labels = list(class_indices.keys()) if isinstance(class_indices, dict) else class_indices

    pred_class = labels[pred_index]
    confidence = float(np.max(pred))

    plt.imshow(img)
    plt.axis("off")
    plt.title(f"Prediction: {pred_class}\nConfidence: {confidence:.2%}")
    plt.show()
    return pred_class, confidence


if __name__ == "__main__":
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

    loader = ui_resultExt({}, "", None)
    model = loader.safe_load_model(str(MODEL_PATH))
    if model is None:
        raise RuntimeError("Failed to load model via safe loader.")

    CLASS_INDICES = {
        "Apple": 0,
        "Banana": 1,
        "Guava": 2,
        "Lime": 3,
        "Orange": 4,
        "Pomegranate": 5,
    }

    image_path = str(DEFAULT_IMAGE)
    pred_class, confidence = predict_fruit_type(model, image_path, CLASS_INDICES)
    print(f"Fruit: {pred_class}, Confidence: {confidence:.2%}")
