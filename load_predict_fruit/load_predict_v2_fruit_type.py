import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image


# ============================================================
# 1) HÀM LOAD MODEL
# ============================================================
def load_fruit_type_model(model_filename: str):
    """
    Load mô hình phân loại loại trái cây từ thư mục train_ml_result.
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
# 2) HÀM PREDICT LOẠI TRÁI CÂY
# ============================================================
def predict_fruit_type(model, img_path, class_indices, img_size=(160, 160)):
    """
    Dự đoán loại quả (Apple, Banana, ...).
    Trả về: (predicted_class, confidence, img)
    """

    if not os.path.exists(img_path):
        raise FileNotFoundError(f"❌ Không tìm thấy ảnh: {img_path}")

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
# 3) HÀM HIỂN THỊ KẾT QUẢ DỰ ĐOÁN
# ============================================================
def show_prediction_type(img, pred_class, confidence):
    plt.imshow(img)
    plt.axis("off")
    plt.title(f"Fruit Type: {pred_class}\nConfidence: {confidence:.2%}")
    plt.show()


# ============================================================
# 4) CHƯƠNG TRÌNH CHÍNH
# ============================================================
if __name__ == "__main__":

    # MAPPING CLASS TYPE (không có Good/Bad)
    class_indices = {
        "Apple": 0,
        "Banana": 1,
        "Guava": 2,
        "Lime": 3,
        "Orange": 4,
        "Pomegranate": 5
    }

    # --- 1) Load model ---
    model = load_fruit_type_model("v2_best_fruit_type_model.h5")

    # --- 2) Đường dẫn ảnh test ---
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(BASE_DIR, "..", "final_ml", "uploads", "apple.jpg")
    img_path = os.path.normpath(img_path)

    # --- 3) Predict ---
    pred_class, confidence, img = predict_fruit_type(model, img_path, class_indices)

    # --- 4) Print result ---
    print("\n===== RESULT =====")
    print(f"🍎 Fruit Type: {pred_class}")
    print(f"🔍 Confidence: {confidence:.2%}")

    # --- 5) Hiển thị ảnh ---
    show_prediction_type(img, pred_class, confidence)
