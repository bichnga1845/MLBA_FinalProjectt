import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image


# ============================================================
# 1) HÀM LOAD MODEL
# ============================================================
def load_fruit_model(model_filename: str):
    """
    Load mô hình trái cây từ thư mục train_ml_result.
    model_filename: tên file .h5
    """
    model_path = os.path.join("..", "train_ml_result", model_filename)

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"❌ Không tìm thấy model: {model_path}")

    print(f"Loading model from: {model_path}")
    model = tf.keras.models.load_model(model_path, compile=False)
    print("✅ Model loaded successfully!")
    return model


# ============================================================
# 2) HÀM PREDICT ẢNH
# ============================================================
def predict_fruit(model, img_path, class_indices, img_size=(224, 224)):
    """
    Dự đoán class trái cây + chất lượng.
    Trả về: (predicted_class, confidence)
    """

    if not os.path.exists(img_path):
        raise FileNotFoundError(f"Không tìm thấy ảnh: {img_path}")

    # Load ảnh
    img = image.load_img(img_path, target_size=img_size, color_mode="rgb")
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0

    # Predict
    pred = model.predict(img_array)[0]
    pred_index = np.argmax(pred)

    # Lấy đúng tên class theo index
    if isinstance(class_indices, dict):
        labels = list(class_indices.keys())
    else:
        labels = class_indices

    pred_class = labels[pred_index]
    confidence = float(np.max(pred))

    return pred_class, confidence, img


# ============================================================
# 3) HÀM HIỂN THỊ ẢNH + KẾT QUẢ
# ============================================================
def show_prediction(img, pred_class, confidence):
    plt.imshow(img)
    plt.axis("off")
    plt.title(f"Prediction: {pred_class}\nConfidence: {confidence:.2%}")
    plt.show()


# ============================================================
# 4) CHƯƠNG TRÌNH CHÍNH
# ============================================================
if __name__ == "__main__":

    # Danh sách class theo index
    class_indices = {
        'Apple_Bad': 0, 'Apple_Good': 1,
        'Banana_Bad': 2, 'Banana_Good': 3,
        'Guava_Bad': 4, 'Guava_Good': 5,
        'Lime_Bad': 6, 'Lime_Good': 7,
        'Orange_Bad': 8, 'Orange_Good': 9,
        'Pomegranate_Bad': 10, 'Pomegranate_Good': 11
    }

    # --- 1) Load model ---
    model = load_fruit_model("b0_best_fruit_type_quality_model.h5")

    # --- 2) Đường dẫn ảnh test ---
    img_path = os.path.join("..", "final_ml", "uploads", "orange.jpg")

    # --- 3) Predict ---
    pred_class, confidence, img = predict_fruit(model, img_path, class_indices)

    # --- 4) Print result ---
    if "_" in pred_class:
        fruit, quality = pred_class.split("_")
        print(f"Fruit: {fruit}")
        print(f"Quality: {quality}")
        print(f"Confidence: {confidence:.2%}")
    else:
        print(f"Prediction: {pred_class} ({confidence:.2%})")

    # --- 5) Hiển thị ảnh ---
    show_prediction(img, pred_class, confidence)
