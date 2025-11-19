import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image


# ============================================================
# 1) HÀM LOAD MODEL
# ============================================================
def load_fruit_model(model_filename: str):
    """Load model từ thư mục train_ml_result."""
    model_path = os.path.join("..", "train_ml_result", model_filename)

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"❌ Không tìm thấy model: {model_path}")

    print(f"Loading model from: {model_path}")
    model = tf.keras.models.load_model(model_path, compile=False)
    print("✅ Model loaded successfully!")
    return model


# ============================================================
# 2) HÀM DỰ ĐOÁN (TYPE hoặc QUALITY)
# ============================================================
def predict_fruit(model, img_path, class_indices, img_size=(160, 160)):
    """Dự đoán chung cho mọi model."""
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"❌ Không tìm thấy ảnh: {img_path}")

    # Load & preprocess
    img = image.load_img(img_path, target_size=img_size, color_mode="rgb")
    img_array = np.expand_dims(image.img_to_array(img), axis=0) / 255.0

    pred = model.predict(img_array)[0]
    pred_index = np.argmax(pred)

    labels = list(class_indices.keys())
    label = labels[pred_index]
    confidence = float(np.max(pred))

    return label, confidence, img


# ============================================================
# 3) HIỂN THỊ HÌNH + KẾT QUẢ
# ============================================================
def show_full_prediction(img, fruit_type, type_conf, quality_label, quality_conf):
    plt.imshow(img)
    plt.axis("off")
    plt.title(
        f"Fruit Type: {fruit_type} ({type_conf:.2%})\n"
        f"Quality: {quality_label} ({quality_conf:.2%})"
    )
    plt.show()


# ============================================================
# 4) CHƯƠNG TRÌNH CHÍNH (GỘP TYPE + QUALITY)
# ============================================================
if __name__ == "__main__":

    # --- CLASS MAPPING ---
    type_indices = {
        "Apple": 0,
        "Banana": 1,
        "Guava": 2,
        "Lime": 3,
        "Orange": 4,
        "Pomegranate": 5
    }

    quality_indices = {
        "Bad": 0,
        "Good": 1
    }

    # --- LOAD 2 MODEL ---
    fruit_type_model = load_fruit_model("v2_best_fruit_type_model.h5")
    fruit_quality_model = load_fruit_model("v2_best_fruit_quality_model.h5")

    # --- CHỌN ẢNH ---
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(BASE_DIR, "..", "final_ml", "uploads", "apple.jpg")
    img_path = os.path.normpath(img_path)

    # --- PREDICT TYPE ---
    fruit_type, type_conf, img = predict_fruit(
        fruit_type_model, img_path, type_indices
    )

    # --- PREDICT QUALITY ---
    quality_label, quality_conf, _ = predict_fruit(
        fruit_quality_model, img_path, quality_indices
    )

    # --- PRINT RESULT ---
    print("\n===== RESULT =====")
    print(f"🍎 Fruit Type: {fruit_type} ({type_conf:.2%})")
    print(f"✨ Quality   : {quality_label} ({quality_conf:.2%})")

    # --- HIỂN THỊ ẢNH ---
    show_full_prediction(img, fruit_type, type_conf, quality_label, quality_conf)
