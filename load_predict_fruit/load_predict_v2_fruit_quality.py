import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image


# ============================================================
# 1) HÀM LOAD MODEL
# ============================================================
def load_fruit_quality_model(model_filename: str):
    """
    Load mô hình phân loại chất lượng trái cây (Good / Bad).
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
# 2) HÀM PREDICT CHẤT LƯỢNG (GOOD / BAD)
# ============================================================
def predict_fruit_quality(model, img_path, class_indices, img_size=(160, 160)):
    """
    Dự đoán chất lượng trái cây (Good / Bad).
    Trả về: (quality_label, confidence, img)
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

    # Lấy tên label
    labels = list(class_indices.keys())
    quality_label = labels[pred_index]
    confidence = float(np.max(pred))

    return quality_label, confidence, img


# ============================================================
# 3) HÀM HIỂN THỊ KẾT QUẢ
# ============================================================
def show_prediction_quality(img, quality_label, confidence):
    plt.imshow(img)
    plt.axis("off")
    plt.title(f"Quality: {quality_label}\nConfidence: {confidence:.2%}")
    plt.show()


# ============================================================
# 4) CHƯƠNG TRÌNH CHÍNH
# ============================================================
if __name__ == "__main__":

    # Chỉ có 2 class
    class_indices = {
        "Bad": 0,
        "Good": 1
    }

    # --- 1) Load model ---
    model = load_fruit_quality_model("v2_best_fruit_quality_model.h5")

    # --- 2) Đường dẫn ảnh test ---
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(BASE_DIR, "..", "final_ml", "uploads", "banana.jpg")
    img_path = os.path.normpath(img_path)

    # --- 3) Predict ---
    quality_label, confidence, img = predict_fruit_quality(model, img_path, class_indices)

    # --- 4) Print kết quả ---
    print("\n===== RESULT =====")
    print(f"✨ Quality: {quality_label}")
    print(f"🔍 Confidence: {confidence:.2%}")

    # --- 5) Hiển thị ảnh ---
    show_prediction_quality(img, quality_label, confidence)
