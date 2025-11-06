import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image
import numpy as np
import tensorflow as tf


def predict_fruit_type(model, img_path, class_indices, img_size=(160,160)):
    """
    Dự đoán loại quả và hiển thị kết quả cùng hình ảnh.

    model: mô hình keras đã train
    img_path: đường dẫn tới ảnh
    class_indices: dict {class_name: index}, hoặc list class_name theo index
    img_size: kích thước ảnh dùng khi train
    """
    # --- Load và xử lý ảnh ---
    img = image.load_img(img_path, target_size=img_size, color_mode='rgb')
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # thêm batch dimension
    img_array /= 255.0  # scale giống train

    # --- Dự đoán ---
    pred = model.predict(img_array)[0]
    pred_index = np.argmax(pred)

    # Nếu class_indices là dict: chuyển sang list theo index
    if isinstance(class_indices, dict):
        labels = list(class_indices.keys())
    else:
        labels = class_indices

    pred_class = labels[pred_index]
    confidence = np.max(pred)

    # --- Hiển thị ảnh ---
    plt.imshow(img)
    plt.axis('off')
    plt.title(f"Prediction: {pred_class}\nConfidence: {confidence:.2%}")
    plt.show()

    return pred_class, confidence


# === Chạy ứng dụng ===
if __name__ == "__main__":
    # Load model và class_indices
    model = tf.keras.models.load_model("best_fruit_type_mobilenetv2.h5", compile=False)
    class_indices = {
        'Apple': 0,
        'Banana': 1,
        'Guava': 2,
        'Lime': 3,
        'Orange': 4,
        'Pomegranate': 5
    }

    img_path = "banana.jpg"
    pred_class, confidence = predict_fruit_type(model, img_path, class_indices)

    print(f"Fruit: {pred_class}, Confidence: {confidence:.2%}")

