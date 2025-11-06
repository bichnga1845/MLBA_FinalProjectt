"""
Test Script for MobileNetV2 Fruit Quality Classification Model
Supports: Single image prediction, batch testing, and confusion matrix visualization
Optimized for Final_Project structure
"""

import os
import sys
import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from pathlib import Path

# ==================== CONFIGURATION ====================
# Get project root directory (Final_Project/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define paths based on actual structure
MODEL_DIR = os.path.join(BASE_DIR, 'Model')
MODEL_PATH = os.path.join(MODEL_DIR, 'mobilenetv2_model.keras')
BEST_MODEL_PATH = os.path.join(MODEL_DIR, 'best_model.h5')
CLASS_INDICES_PATH = os.path.join(MODEL_DIR, 'class_indices.npy')
DATASET_DIR = os.path.join(BASE_DIR, 'Dataset')
TEST_DIR = os.path.join(BASE_DIR, 'Test')
SINGLE_IMAGE_TEST_DIR = os.path.join(TEST_DIR, 'Single_Image_Test')

IMG_SIZE = (160, 160)
BATCH_SIZE = 32

# GPU configuration
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print(f"✓ GPU detected: {len(gpus)} device(s)")
    except RuntimeError as e:
        print(f"GPU configuration error: {e}")
else:
    print("⚠ No GPU detected, using CPU")

# ==================== MODEL LOADING ====================
def load_model_and_classes():
    """Load trained model and class indices"""

    print("\n" + "=" * 60)
    print("LOADING MODEL")
    print("=" * 60)

    model = None

    # Try loading different model formats in priority order
    # Priority: .keras > SavedModel > .h5 (h5 has compatibility issues with Keras 3)

    if os.path.exists(MODEL_PATH):
        print(f"Loading model from: {MODEL_PATH}")
        try:
            model = keras.models.load_model(MODEL_PATH)
            print("✓ Keras model (.keras) loaded successfully")
        except Exception as e:
            print(f"✗ Failed to load .keras model: {e}")

    if model is None:
        # Try SavedModel format
        saved_model_path = os.path.join(MODEL_DIR, 'saved_model')
        if os.path.exists(saved_model_path):
            print(f"Loading SavedModel from: {saved_model_path}")
            try:
                model = keras.models.load_model(saved_model_path)
                print("✓ SavedModel loaded successfully")
            except Exception as e:
                print(f"✗ Failed to load SavedModel: {e}")

    if model is None and os.path.exists(BEST_MODEL_PATH):
        # Last resort: try .h5 with custom objects
        print(f"Attempting to load .h5 model from: {BEST_MODEL_PATH}")
        print("⚠ Note: .h5 format may have compatibility issues with Keras 3")
        try:
            # Try with compile=False to avoid optimizer issues
            model = keras.models.load_model(BEST_MODEL_PATH, compile=False)
            print("✓ H5 model loaded (without compilation)")

            # Recompile the model
            model.compile(
                optimizer=keras.optimizers.Adam(learning_rate=0.001),
                loss='categorical_crossentropy',
                metrics=['accuracy']
            )
            print("✓ Model recompiled successfully")
        except Exception as e:
            print(f"✗ Failed to load .h5 model: {e}")

    if model is None:
        print("\n✗ ERROR: No model could be loaded!")
        print(f"Searched locations:")
        print(f"  - {MODEL_PATH} (.keras format)")
        print(f"  - {os.path.join(MODEL_DIR, 'saved_model')} (SavedModel format)")
        print(f"  - {BEST_MODEL_PATH} (.h5 format)")
        print("\n💡 Suggestion: Make sure you have trained the model first using MobileNetV2.py")
        sys.exit(1)

    # Load class indices
    if not os.path.exists(CLASS_INDICES_PATH):
        print(f"✗ ERROR: Class indices not found at {CLASS_INDICES_PATH}")
        sys.exit(1)

    class_indices = np.load(CLASS_INDICES_PATH, allow_pickle=True).item()
    class_names = {v: k for k, v in class_indices.items()}

    print(f"\nClasses loaded: {list(class_names.values())}")
    print(f"Number of classes: {len(class_names)}")

    return model, class_names

# ==================== SINGLE IMAGE PREDICTION ====================
def predict_single_image(model, class_names, image_path, show_plot=True):
    """
    Predict quality of a single fruit image

    Args:
        model: Trained Keras model
        class_names: Dictionary mapping class indices to names
        image_path: Path to image file
        show_plot: Whether to display the image with prediction

    Returns:
        Predicted class, confidence, and all probabilities
    """

    if not os.path.exists(image_path):
        print(f"✗ ERROR: Image not found at {image_path}")
        return None, None, None

    try:
        # Load and preprocess image
        img = load_img(image_path, target_size=IMG_SIZE)
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)

        # Predict
        predictions = model.predict(img_array, verbose=0)
        predicted_class_idx = np.argmax(predictions[0])
        confidence = predictions[0][predicted_class_idx] * 100
        predicted_class = class_names[predicted_class_idx]

        # Display result
        if show_plot:
            plt.figure(figsize=(10, 7))
            plt.imshow(img)
            plt.axis('off')

            # Color code: green for Good, red for Bad
            color = 'green' if 'Good' in predicted_class else 'red'

            # Create title with all probabilities
            title_lines = [f"Predicted: {predicted_class}",
                          f"Confidence: {confidence:.2f}%",
                          f"File: {os.path.basename(image_path)}"]

            plt.title('\n'.join(title_lines),
                     fontsize=14, fontweight='bold', color=color, pad=20)

            # Add probability distribution
            prob_text = "All Probabilities:\n"
            for idx, prob in enumerate(predictions[0]):
                prob_text += f"{class_names[idx]}: {prob*100:.2f}%\n"

            plt.text(0.02, 0.98, prob_text, transform=plt.gca().transAxes,
                    fontsize=9, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

            plt.tight_layout()
            plt.show()

        return predicted_class, confidence, predictions[0]

    except Exception as e:
        print(f"✗ Error predicting image: {e}")
        return None, None, None

# ==================== BATCH TESTING ====================
def test_on_dataset(model, class_names, dataset_dir=DATASET_DIR, show_confusion_matrix=True):
    """
    Test model on Dataset directory (Bad/Good structure)

    Args:
        model: Trained Keras model
        class_names: Dictionary mapping class indices to names
        dataset_dir: Directory containing Bad/ and Good/ folders
        show_confusion_matrix: Whether to plot confusion matrix
    """

    print("\n" + "=" * 60)
    print("TESTING MODEL ON DATASET")
    print("=" * 60)
    print(f"Dataset directory: {dataset_dir}")

    if not os.path.exists(dataset_dir):
        print(f"✗ ERROR: Dataset directory not found at {dataset_dir}")
        return None, None, None

    # Create test data generator without preprocessing in ImageDataGenerator
    # since we'll apply MobileNetV2 preprocessing separately
    test_datagen = ImageDataGenerator(rescale=1./255)

    test_generator = test_datagen.flow_from_directory(
        dataset_dir,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False
    )

    print(f"\n✓ Test samples: {test_generator.samples}")
    print(f"✓ Classes found: {test_generator.class_indices}")
    print(f"✓ Batches: {len(test_generator)}")

    # Evaluate model
    print("\nEvaluating model...")
    results = model.evaluate(test_generator, verbose=1)

    print("\n" + "-" * 60)
    print("TEST RESULTS")
    print("-" * 60)
    print(f"Test Loss:      {results[0]:.4f}")
    print(f"Test Accuracy:  {results[1]:.4f} ({results[1]*100:.2f}%)")
    if len(results) > 2:
        print(f"Test Precision: {results[2]:.4f}")
    if len(results) > 3:
        print(f"Test Recall:    {results[3]:.4f}")

    # Get predictions for confusion matrix
    print("\nGenerating predictions for detailed analysis...")
    test_generator.reset()
    predictions = model.predict(test_generator, verbose=1)
    predicted_classes = np.argmax(predictions, axis=1)
    true_classes = test_generator.classes

    # Classification report
    print("\n" + "-" * 60)
    print("CLASSIFICATION REPORT")
    print("-" * 60)
    class_labels = list(test_generator.class_indices.keys())
    report = classification_report(
        true_classes,
        predicted_classes,
        target_names=class_labels,
        digits=4
    )
    print(report)

    # Confusion matrix
    if show_confusion_matrix:
        cm = confusion_matrix(true_classes, predicted_classes)
        plot_confusion_matrix(cm, class_labels)

    return results, predictions, true_classes

# ==================== VISUALIZATION ====================
def plot_confusion_matrix(cm, class_names):
    """Plot confusion matrix"""

    plt.figure(figsize=(10, 8))
    sns.heatmap(
        cm,
        annot=True,
        fmt='d',
        cmap='Blues',
        xticklabels=class_names,
        yticklabels=class_names,
        cbar_kws={'label': 'Count'},
        linewidths=0.5,
        linecolor='gray'
    )
    plt.title('Confusion Matrix - Fruit Quality Classification',
             fontsize=16, fontweight='bold', pad=20)
    plt.ylabel('True Label', fontsize=12, fontweight='bold')
    plt.xlabel('Predicted Label', fontsize=12, fontweight='bold')
    plt.tight_layout()

    # Save plot
    cm_path = os.path.join(MODEL_DIR, 'confusion_matrix.png')
    plt.savefig(cm_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Confusion matrix saved to: {cm_path}")
    plt.show()

def plot_sample_predictions(model, class_names, dataset_dir=DATASET_DIR, num_samples=9):
    """Display a grid of sample predictions"""

    print("\n" + "=" * 60)
    print("SAMPLE PREDICTIONS")
    print("=" * 60)

    # Create test data generator
    test_datagen = ImageDataGenerator(rescale=1./255)

    test_generator = test_datagen.flow_from_directory(
        dataset_dir,
        target_size=IMG_SIZE,
        batch_size=num_samples,
        class_mode='categorical',
        shuffle=True
    )

    # Get a batch of images
    images, labels = next(test_generator)

    # Apply MobileNetV2 preprocessing for prediction
    images_preprocessed = tf.keras.applications.mobilenet_v2.preprocess_input(images * 255)
    predictions = model.predict(images_preprocessed, verbose=0)

    # Plot
    rows = 3
    cols = 3
    fig, axes = plt.subplots(rows, cols, figsize=(15, 15))
    axes = axes.ravel()

    for i in range(min(num_samples, len(images))):
        # Use original rescaled image for display
        img = images[i]

        true_class_idx = np.argmax(labels[i])
        pred_class_idx = np.argmax(predictions[i])

        true_class = class_names[true_class_idx]
        pred_class = class_names[pred_class_idx]
        confidence = predictions[i][pred_class_idx] * 100

        # Display image
        axes[i].imshow(img)
        axes[i].axis('off')

        # Color code: green for correct, red for incorrect
        is_correct = true_class_idx == pred_class_idx
        color = 'green' if is_correct else 'red'
        status = '✓ CORRECT' if is_correct else '✗ WRONG'

        title = f"{status}\nTrue: {true_class}\nPred: {pred_class}\nConf: {confidence:.1f}%"
        axes[i].set_title(title, fontsize=11, fontweight='bold', color=color)

    plt.suptitle('Sample Predictions (Random from Dataset)',
                fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()

    # Save plot
    samples_path = os.path.join(MODEL_DIR, 'sample_predictions.png')
    plt.savefig(samples_path, dpi=300, bbox_inches='tight')
    print(f"✓ Sample predictions saved to: {samples_path}")
    plt.show()

# ==================== BATCH PREDICTION ON FOLDER ====================
def predict_folder(model, class_names, folder_path, output_csv=None):
    """
    Predict all images in a folder and optionally save results to CSV

    Args:
        model: Trained Keras model
        class_names: Dictionary mapping class indices to names
        folder_path: Path to folder containing images
        output_csv: Path to save results CSV (optional)
    """

    print("\n" + "=" * 60)
    print("BATCH PREDICTION ON FOLDER")
    print("=" * 60)
    print(f"Folder: {folder_path}")

    if not os.path.exists(folder_path):
        print(f"✗ ERROR: Folder not found at {folder_path}")
        return None

    # Supported image formats
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}

    # Get all image files
    image_files = [
        f for f in Path(folder_path).rglob('*')
        if f.suffix.lower() in image_extensions
    ]

    if not image_files:
        print("✗ No images found in folder!")
        return None

    print(f"✓ Found {len(image_files)} images\n")

    results = []
    print("-" * 60)

    for idx, img_path in enumerate(image_files, 1):
        try:
            predicted_class, confidence, probs = predict_single_image(
                model, class_names, str(img_path), show_plot=False
            )

            if predicted_class:
                results.append({
                    'filename': img_path.name,
                    'path': str(img_path),
                    'predicted_class': predicted_class,
                    'confidence': f"{confidence:.2f}%",
                    **{f'prob_{class_names[i]}': f"{probs[i]*100:.2f}%"
                       for i in range(len(probs))}
                })

                status = '✓' if confidence > 80 else '⚠' if confidence > 60 else '✗'
                print(f"{status} [{idx}/{len(image_files)}] {img_path.name:30s} → {predicted_class:15s} ({confidence:.2f}%)")

        except Exception as e:
            print(f"✗ [{idx}/{len(image_files)}] Error processing {img_path.name}: {e}")

    print("-" * 60)
    print(f"✓ Successfully predicted {len(results)}/{len(image_files)} images")

    # Save to CSV if requested
    if output_csv and results:
        import pandas as pd
        df = pd.DataFrame(results)
        df.to_csv(output_csv, index=False)
        print(f"✓ Results saved to: {output_csv}")

    return results

# ==================== TEST SINGLE IMAGE FOLDER ====================
def test_single_image_folder(model, class_names):
    """Test all images in Test/Single_Image_Test/ folder"""

    if not os.path.exists(SINGLE_IMAGE_TEST_DIR):
        print(f"✗ ERROR: Single_Image_Test folder not found at {SINGLE_IMAGE_TEST_DIR}")
        return

    print("\n" + "=" * 60)
    print("TESTING SINGLE IMAGE FOLDER")
    print("=" * 60)
    print(f"Location: {SINGLE_IMAGE_TEST_DIR}")

    # Get all images
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
    images = [f for f in Path(SINGLE_IMAGE_TEST_DIR).glob('*')
              if f.suffix.lower() in image_extensions]

    if not images:
        print("✗ No images found!")
        return

    print(f"✓ Found {len(images)} images\n")

    # Test each image with visualization
    for img_path in images:
        print(f"\nTesting: {img_path.name}")
        print("-" * 60)
        predicted_class, confidence, _ = predict_single_image(
            model, class_names, str(img_path), show_plot=True
        )
        if predicted_class:
            print(f"Result: {predicted_class} ({confidence:.2f}%)")

# ==================== MAIN EXECUTION ====================
def main():
    """Main testing function"""

    print("\n" + "=" * 70)
    print(" " * 10 + "MOBILENETV2 FRUIT QUALITY CLASSIFICATION - TEST")
    print("=" * 70)

    # Load model
    model, class_names = load_model_and_classes()

    print("\n" + "=" * 70)
    print(" " * 25 + "TEST OPTIONS")
    print("=" * 70)
    print("  1. Test single image (enter custom path)")
    print("  2. Test all images in Test/Single_Image_Test/ folder")
    print("  3. Test on entire Dataset (Bad/Good)")
    print("  4. Show sample predictions (9 random images)")
    print("  5. Predict all images in a custom folder")
    print("  6. Run comprehensive test (options 2, 3, 4)")
    print("  7. Exit")
    print("=" * 70)

    choice = input("\n👉 Enter your choice (1-7): ").strip()

    if choice == '1':
        # Single image prediction
        image_path = input("Enter image path: ").strip().strip('"\'')
        if os.path.exists(image_path):
            predicted_class, confidence, probs = predict_single_image(
                model, class_names, image_path
            )
            if predicted_class:
                print(f"\n{'='*60}")
                print(f"RESULT: {predicted_class}")
                print(f"Confidence: {confidence:.2f}%")
                print(f"{'='*60}")
        else:
            print(f"✗ Image not found at: {image_path}")

    elif choice == '2':
        # Test Single_Image_Test folder
        test_single_image_folder(model, class_names)

    elif choice == '3':
        # Test on dataset
        test_on_dataset(model, class_names)

    elif choice == '4':
        # Sample predictions
        plot_sample_predictions(model, class_names)

    elif choice == '5':
        # Folder prediction
        folder_path = input("Enter folder path: ").strip().strip('"\'')
        if os.path.exists(folder_path):
            save_csv = input("Save results to CSV? (y/n): ").strip().lower()
            output_csv = None
            if save_csv == 'y':
                output_csv = os.path.join(folder_path, 'predictions.csv')
            predict_folder(model, class_names, folder_path, output_csv)
        else:
            print(f"✗ Folder not found at: {folder_path}")

    elif choice == '6':
        # Run comprehensive test
        print("\n" + "🚀" * 35)
        print("RUNNING COMPREHENSIVE TEST SUITE")
        print("🚀" * 35)

        print("\n[TEST 1/3] Testing Single_Image_Test folder...")
        test_single_image_folder(model, class_names)

        print("\n[TEST 2/3] Testing on entire Dataset...")
        test_on_dataset(model, class_names)

        print("\n[TEST 3/3] Generating sample predictions...")
        plot_sample_predictions(model, class_names)

        print("\n" + "✓" * 35)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("✓" * 35)

    elif choice == '7':
        print("\n👋 Goodbye!")
        sys.exit(0)

    else:
        print("✗ Invalid choice! Please select 1-7")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Test interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)