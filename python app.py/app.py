"""
LUNG CANCER DETECTION - COMPLETE DEPLOYMENT SCRIPT
This script automatically organizes your data and deploys the project
Run: python deploy_lung_cancer.py
"""

import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

# Configuration
SOURCE_DATA_PATH = r"C:\Users\dhara\Downloads\archive (10)"
PROJECT_NAME = "LungCancerDetection"
BASE_PATH = os.path.join(os.path.expanduser("~"), "Desktop", PROJECT_NAME)

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_step(message):
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}➡️  {message}{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

def create_project_structure():
    """Create all necessary folders"""
    print_step("Creating project structure")
    
    folders = [
        "dataset/CT_Scan/adenocarcinoma",
        "dataset/CT_Scan/normal",
        "dataset/CT_Scan/squamous_cell_carcinoma",
        "dataset/Histopathology/adenocarcinoma",
        "dataset/Histopathology/benign",
        "dataset/Histopathology/squamous_cell_carcinoma",
        "models",
        "static/css",
        "static/uploads",
        "templates",
        "logs",
        "notebooks"
    ]
    
    for folder in folders:
        path = os.path.join(BASE_PATH, folder)
        os.makedirs(path, exist_ok=True)
        print(f"  Created: {folder}")
    
    print_success("Project structure created")

def organize_dataset():
    """Automatically organize your dataset"""
    print_step("Organizing your dataset")
    
    if not os.path.exists(SOURCE_DATA_PATH):
        print_error(f"Source data path not found: {SOURCE_DATA_PATH}")
        print("Please check if the path is correct")
        return False
    
    print(f"Source path: {SOURCE_DATA_PATH}")
    
    # List contents of source directory
    print("\nContents of source directory:")
    try:
        for item in os.listdir(SOURCE_DATA_PATH):
            print(f"  - {item}")
    except:
        print("  Could not list directory contents")
    
    # Look for the actual dataset folders
    found_ct = False
    found_histo = False
    
    # Check for Lung CT Dataset
    ct_source = os.path.join(SOURCE_DATA_PATH, "Lung CT Dataset")
    if os.path.exists(ct_source):
        found_ct = True
        print(f"\n  Found CT dataset at: {ct_source}")
        
        # Copy CT scan images
        for class_name in ['adenocarcinoma', 'normal', 'squamous_cell_carcinoma']:
            src = os.path.join(ct_source, class_name)
            dst = os.path.join(BASE_PATH, "dataset/CT_Scan", class_name)
            
            if os.path.exists(src):
                files = [f for f in os.listdir(src) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                print(f"    Found {len(files)} {class_name} images")
                
                # Copy all images
                for file in files:
                    try:
                        shutil.copy2(os.path.join(src, file), os.path.join(dst, file))
                    except:
                        print_warning(f"      Failed to copy {file}")
                
                print_success(f"      Copied {len(files)} {class_name} images")
            else:
                print_warning(f"      {class_name} folder not found in CT dataset")
    
    # Check for Histopathological Images
    histo_source = os.path.join(SOURCE_DATA_PATH, "Histopathological Images")
    if os.path.exists(histo_source):
        found_histo = True
        print(f"\n  Found Histopathology dataset at: {histo_source}")
        
        # Copy histopathology images
        for class_name in ['adenocarcinoma', 'benign', 'squamous_cell_carcinoma']:
            src = os.path.join(histo_source, class_name)
            dst = os.path.join(BASE_PATH, "dataset/Histopathology", class_name)
            
            if os.path.exists(src):
                files = [f for f in os.listdir(src) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                print(f"    Found {len(files)} {class_name} images")
                
                # Copy all images
                for file in files:
                    try:
                        shutil.copy2(os.path.join(src, file), os.path.join(dst, file))
                    except:
                        print_warning(f"      Failed to copy {file}")
                
                print_success(f"      Copied {len(files)} {class_name} images")
            else:
                print_warning(f"      {class_name} folder not found in histopathology dataset")
    
    # If folders not found with exact names, try alternative names
    if not found_ct:
        # Look for any folder containing 'CT' or 'Lung'
        for item in os.listdir(SOURCE_DATA_PATH):
            if 'CT' in item.upper() or 'LUNG' in item.upper():
                ct_source = os.path.join(SOURCE_DATA_PATH, item)
                if os.path.isdir(ct_source):
                    found_ct = True
                    print(f"\n  Found possible CT dataset at: {ct_source}")
                    # Try to organize from this folder
                    for class_name in ['adenocarcinoma', 'normal', 'squamous_cell_carcinoma']:
                        # Look for class folders inside
                        for subitem in os.listdir(ct_source):
                            if class_name.lower() in subitem.lower():
                                src = os.path.join(ct_source, subitem)
                                dst = os.path.join(BASE_PATH, "dataset/CT_Scan", class_name)
                                if os.path.isdir(src):
                                    files = [f for f in os.listdir(src) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                                    for file in files:
                                        shutil.copy2(os.path.join(src, file), os.path.join(dst, file))
                                    print_success(f"      Copied {len(files)} {class_name} images")
                    break
    
    if not found_histo:
        # Look for any folder containing 'Histo' or 'Pathology'
        for item in os.listdir(SOURCE_DATA_PATH):
            if 'HISTO' in item.upper() or 'PATH' in item.upper():
                histo_source = os.path.join(SOURCE_DATA_PATH, item)
                if os.path.isdir(histo_source):
                    found_histo = True
                    print(f"\n  Found possible Histopathology dataset at: {histo_source}")
                    # Try to organize from this folder
                    for class_name in ['adenocarcinoma', 'benign', 'squamous_cell_carcinoma']:
                        for subitem in os.listdir(histo_source):
                            if class_name.lower() in subitem.lower():
                                src = os.path.join(histo_source, subitem)
                                dst = os.path.join(BASE_PATH, "dataset/Histopathology", class_name)
                                if os.path.isdir(src):
                                    files = [f for f in os.listdir(src) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                                    for file in files:
                                        shutil.copy2(os.path.join(src, file), os.path.join(dst, file))
                                    print_success(f"      Copied {len(files)} {class_name} images")
                    break
    
    if not found_ct and not found_histo:
        print_error("No dataset folders found!")
        print("\nExpected folders:")
        print("  - Lung CT Dataset/")
        print("  - Histopathological Images/")
        print("\nOr folders containing:")
        print("  - adenocarcinoma/")
        print("  - normal/")
        print("  - benign/")
        print("  - squamous_cell_carcinoma/")
        return False
    
    print_success("Dataset organization completed")
    return True

def create_requirements_file():
    """Create requirements.txt"""
    print_step("Creating requirements.txt")
    
    requirements = """# Core ML
tensorflow==2.13.0
keras==2.13.1
numpy==1.24.3
pandas==2.0.3
scikit-learn==1.3.0

# Visualization
matplotlib==3.7.2
seaborn==0.12.2
plotly==5.15.0

# Image Processing
Pillow==10.0.0
opencv-python==4.8.0.74

# Web Framework
flask==2.3.2
werkzeug==2.3.6
gunicorn==21.2.0

# Utilities
tqdm==4.65.0
joblib==1.3.1
python-dotenv==1.0.0
"""
    
    with open(os.path.join(BASE_PATH, "requirements.txt"), 'w') as f:
        f.write(requirements)
    
    print_success("requirements.txt created")

def create_app_file():
    """Create the Flask application file"""
    print_step("Creating Flask application")
    
    app_code = '''"""
LUNG CANCER DETECTION - FLASK WEB APPLICATION
"""

import os
import pickle
import numpy as np
from flask import Flask, render_template, request, jsonify, url_for
from werkzeug.utils import secure_filename
import tensorflow as tf
from tensorflow.keras.models import load_model
import datetime
import base64
from io import BytesIO
import matplotlib.pyplot as plt

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global variables
ct_model = None
histo_model = None
ct_class_indices = None
histo_class_indices = None

def load_models():
    """Load trained models"""
    global ct_model, histo_model, ct_class_indices, histo_class_indices
    
    print("Loading models...")
    
    # CT Model
    if os.path.exists('models/ct_model_final.h5'):
        ct_model = load_model('models/ct_model_final.h5')
        with open('models/ct_class_indices.pkl', 'rb') as f:
            ct_class_indices = pickle.load(f)
        print("✓ CT model loaded")
    
    # Histopathology Model
    if os.path.exists('models/histo_model_final.h5'):
        histo_model = load_model('models/histo_model_final.h5')
        with open('models/histo_class_indices.pkl', 'rb') as f:
            histo_class_indices = pickle.load(f)
        print("✓ Histopathology model loaded")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(img_path):
    """Preprocess image for prediction"""
    from tensorflow.keras.preprocessing import image
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array

def predict_image(model, img_path, class_indices):
    """Make prediction on single image"""
    img_array = preprocess_image(img_path)
    predictions = model.predict(img_array, verbose=0)[0]
    pred_class_idx = np.argmax(predictions)
    confidence = np.max(predictions)
    
    idx_to_class = {v: k for k, v in class_indices.items()}
    pred_class = idx_to_class[pred_class_idx]
    
    return pred_class, confidence, predictions

def create_probability_plot(probabilities, class_names):
    """Create probability plot as base64"""
    plt.figure(figsize=(8, 4))
    bars = plt.bar(class_names, probabilities, color=['#2ecc71', '#3498db', '#e74c3c'])
    plt.title('Class Probabilities', fontsize=14, fontweight='bold')
    plt.xlabel('Classes')
    plt.ylabel('Probability')
    plt.ylim([0, 1])
    
    for bar, prob in zip(bars, probabilities):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                f'{prob:.2%}', ha='center', va='bottom')
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ct-scan')
def ct_scan():
    return render_template('ct_scan.html')

@app.route('/histopathology')
def histopathology():
    return render_template('histopathology.html')

@app.route('/ensemble')
def ensemble():
    return render_template('ensemble.html')

@app.route('/predict/ct', methods=['POST'])
def predict_ct():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        if ct_model is None:
            return jsonify({'error': 'Model not loaded. Please train first.'}), 500
        
        pred_class, confidence, probs = predict_image(ct_model, filepath, ct_class_indices)
        plot_data = create_probability_plot(probs, list(ct_class_indices.keys()))
        
        return jsonify({
            'success': True,
            'prediction': pred_class,
            'confidence': float(confidence),
            'probabilities': probs.tolist(),
            'image_path': url_for('static', filename=f'uploads/{filename}'),
            'plot': plot_data
        })
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/predict/histo', methods=['POST'])
def predict_histo():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        if histo_model is None:
            return jsonify({'error': 'Model not loaded. Please train first.'}), 500
        
        pred_class, confidence, probs = predict_image(histo_model, filepath, histo_class_indices)
        plot_data = create_probability_plot(probs, list(histo_class_indices.keys()))
        
        return jsonify({
            'success': True,
            'prediction': pred_class,
            'confidence': float(confidence),
            'probabilities': probs.tolist(),
            'image_path': url_for('static', filename=f'uploads/{filename}'),
            'plot': plot_data
        })
    
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    print("="*60)
    print("LUNG CANCER DETECTION SYSTEM")
    print("="*60)
    load_models()
    print(f"\nServer starting at: http://localhost:5000")
    print("Press Ctrl+C to stop")
    app.run(debug=True, host='0.0.0.0', port=5000)
'''
    
    with open(os.path.join(BASE_PATH, "app.py"), 'w', encoding='utf-8') as f:
        f.write(app_code)
    
    print_success("app.py created")

def create_training_scripts():
    """Create training scripts for both models"""
    print_step("Creating training scripts")
    
    # CT Model training script
    train_ct_code = '''"""
CT SCAN MODEL TRAINING
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import VGG16
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
import matplotlib.pyplot as plt
import pickle

# Configuration
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 20  # Reduced for quick testing
NUM_CLASSES = 3
CLASS_NAMES = ['adenocarcinoma', 'normal', 'squamous_cell_carcinoma']
DATASET_PATH = "dataset/CT_Scan"

os.makedirs('models', exist_ok=True)

def train_ct_model():
    print("="*50)
    print("Starting CT model training...")
    print("="*50)
    
    # Check if dataset exists
    if not os.path.exists(DATASET_PATH):
        print(f"Error: Dataset path {DATASET_PATH} not found!")
        return None, None
    
    # Data generators
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        validation_split=0.2
    )
    
    print("\nLoading training data...")
    train_gen = train_datagen.flow_from_directory(
        DATASET_PATH,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training',
        shuffle=True
    )
    
    print("Loading validation data...")
    val_gen = train_datagen.flow_from_directory(
        DATASET_PATH,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation',
        shuffle=False
    )
    
    print(f"\nClasses: {train_gen.class_indices}")
    print(f"Training samples: {train_gen.samples}")
    print(f"Validation samples: {val_gen.samples}")
    
    # Model
    print("\nBuilding model...")
    base_model = VGG16(weights='imagenet', include_top=False, input_shape=(IMG_SIZE, IMG_SIZE, 3))
    base_model.trainable = False
    
    model = keras.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(NUM_CLASSES, activation='softmax')
    ])
    
    model.compile(optimizer=Adam(learning_rate=0.0001),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    
    model.summary()
    
    # Train
    print("\nStarting training...")
    history = model.fit(
        train_gen,
        epochs=EPOCHS,
        validation_data=val_gen,
        callbacks=[
            EarlyStopping(patience=5, restore_best_weights=True),
            ModelCheckpoint('models/best_ct_model.h5', save_best_only=True)
        ]
    )
    
    # Save
    print("\nSaving model...")
    model.save('models/ct_model_final.h5')
    with open('models/ct_class_indices.pkl', 'wb') as f:
        pickle.dump(train_gen.class_indices, f)
    
    # Plot training history
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Train')
    plt.plot(history.history['val_accuracy'], label='Validation')
    plt.title('Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Train')
    plt.plot(history.history['val_loss'], label='Validation')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('models/ct_training_history.png')
    plt.show()
    
    print("\n✅ CT model training completed!")
    return model, history

if __name__ == "__main__":
    train_ct_model()
'''
    
    with open(os.path.join(BASE_PATH, "train_ct.py"), 'w') as f:
        f.write(train_ct_code)
    
    # Histopathology model training script
    train_histo_code = '''"""
HISTOPATHOLOGY MODEL TRAINING
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
import matplotlib.pyplot as plt
import pickle

# Configuration
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 20  # Reduced for quick testing
NUM_CLASSES = 3
CLASS_NAMES = ['adenocarcinoma', 'benign', 'squamous_cell_carcinoma']
DATASET_PATH = "dataset/Histopathology"

os.makedirs('models', exist_ok=True)

def train_histo_model():
    print("="*50)
    print("Starting Histopathology model training...")
    print("="*50)
    
    # Check if dataset exists
    if not os.path.exists(DATASET_PATH):
        print(f"Error: Dataset path {DATASET_PATH} not found!")
        return None, None
    
    # Data generators
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        vertical_flip=True,
        validation_split=0.2
    )
    
    print("\nLoading training data...")
    train_gen = train_datagen.flow_from_directory(
        DATASET_PATH,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training',
        shuffle=True
    )
    
    print("Loading validation data...")
    val_gen = train_datagen.flow_from_directory(
        DATASET_PATH,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation',
        shuffle=False
    )
    
    print(f"\nClasses: {train_gen.class_indices}")
    print(f"Training samples: {train_gen.samples}")
    print(f"Validation samples: {val_gen.samples}")
    
    # Model
    print("\nBuilding model...")
    base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(IMG_SIZE, IMG_SIZE, 3))
    base_model.trainable = False
    
    model = keras.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(NUM_CLASSES, activation='softmax')
    ])
    
    model.compile(optimizer=Adam(learning_rate=0.0001),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    
    model.summary()
    
    # Train
    print("\nStarting training...")
    history = model.fit(
        train_gen,
        epochs=EPOCHS,
        validation_data=val_gen,
        callbacks=[
            EarlyStopping(patience=5, restore_best_weights=True),
            ModelCheckpoint('models/best_histo_model.h5', save_best_only=True)
        ]
    )
    
    # Save
    print("\nSaving model...")
    model.save('models/histo_model_final.h5')
    with open('models/histo_class_indices.pkl', 'wb') as f:
        pickle.dump(train_gen.class_indices, f)
    
    # Plot training history
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Train')
    plt.plot(history.history['val_accuracy'], label='Validation')
    plt.title('Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Train')
    plt.plot(history.history['val_loss'], label='Validation')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('models/histo_training_history.png')
    plt.show()
    
    print("\n✅ Histopathology model training completed!")
    return model, history

if __name__ == "__main__":
    train_histo_model()
'''
    
    with open(os.path.join(BASE_PATH, "train_histopathology.py"), 'w') as f:
        f.write(train_histo_code)
    
    print_success("Training scripts created")

def create_html_templates():
    """Create HTML templates"""
    print_step("Creating HTML templates")
    
    # Base.html
    base_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lung Cancer Detection - {% block title %}{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .navbar {
            background: #2c3e50 !important;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .navbar-brand {
            color: white !important;
            font-weight: bold;
        }
        .nav-link {
            color: rgba(255,255,255,0.8) !important;
        }
        .nav-link:hover {
            color: white !important;
        }
        .main-container {
            padding: 2rem;
            margin-top: 60px;
        }
        .card {
            border: none;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            background: rgba(255,255,255,0.95);
            margin-bottom: 20px;
        }
        .card-header {
            background: linear-gradient(135deg, #3498db, #2c3e50);
            color: white;
            border-radius: 15px 15px 0 0 !important;
            font-weight: bold;
            padding: 15px 20px;
        }
        .btn-primary {
            background: linear-gradient(135deg, #3498db, #2c3e50);
            border: none;
            border-radius: 25px;
            padding: 10px 30px;
            transition: all 0.3s;
        }
        .btn-primary:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(52,152,219,0.4);
        }
        .btn-success {
            background: linear-gradient(135deg, #27ae60, #229954);
            border: none;
            border-radius: 25px;
            padding: 10px 30px;
        }
        .upload-area {
            border: 3px dashed #3498db;
            border-radius: 10px;
            padding: 3rem;
            text-align: center;
            cursor: pointer;
            background: rgba(52,152,219,0.05);
            transition: all 0.3s;
        }
        .upload-area:hover {
            background: rgba(52,152,219,0.1);
            transform: scale(1.02);
        }
        .upload-area i {
            font-size: 3rem;
            color: #3498db;
            margin-bottom: 1rem;
        }
        .preview-image {
            max-width: 100%;
            max-height: 300px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .loading-spinner {
            display: none;
            text-align: center;
            padding: 2rem;
        }
        .prediction-box {
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            text-align: center;
            color: white;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.02); }
            100% { transform: scale(1); }
        }
        .prediction-high { background: linear-gradient(135deg, #27ae60, #2ecc71); }
        .prediction-medium { background: linear-gradient(135deg, #f39c12, #e67e22); }
        .prediction-low { background: linear-gradient(135deg, #e74c3c, #c0392b); }
        .footer {
            background: #2c3e50;
            color: white;
            padding: 1.5rem;
            text-align: center;
            margin-top: 2rem;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark fixed-top">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-lungs"></i> LungCancer AI
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/ct-scan">CT Scan</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/histopathology">Histopathology</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/ensemble">Ensemble</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="main-container">
        <div class="container">
            {% block content %}{% endblock %}
        </div>
    </div>

    <footer class="footer">
        <div class="container">
            <p class="mb-0">Lung Cancer Detection System | Powered by Deep Learning</p>
            <p class="mb-0"><small>For Research & Educational Purposes Only</small></p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>"""
    
    with open(os.path.join(BASE_PATH, "templates", "base.html"), 'w', encoding='utf-8') as f:
        f.write(base_html)
    
    # Index.html
    index_html = """{% extends "base.html" %}

{% block title %}Home{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-10">
        <div class="card">
            <div class="card-body text-center p-5">
                <i class="fas fa-lungs" style="font-size: 5rem; color: #3498db;"></i>
                <h1 class="display-4 mt-4">Lung Cancer Detection System</h1>
                <p class="lead">Using Deep Learning (CNN) on CT Scans and Histopathology Images</p>
                <hr class="my-4">
                <p>Upload medical images for instant AI-powered analysis and classification</p>
                
                <div class="row mt-5">
                    <div class="col-md-4">
                        <div class="card h-100">
                            <div class="card-body">
                                <i class="fas fa-ct-scan fa-3x text-primary"></i>
                                <h4 class="mt-3">CT Scan Analysis</h4>
                                <p>Analyze chest CT scans for lung nodule detection and classification</p>
                                <a href="/ct-scan" class="btn btn-primary">Try Now</a>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card h-100">
                            <div class="card-body">
                                <i class="fas fa-microscope fa-3x text-success"></i>
                                <h4 class="mt-3">Histopathology</h4>
                                <p>Analyze tissue samples for cancer type classification</p>
                                <a href="/histopathology" class="btn btn-success">Try Now</a>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card h-100">
                            <div class="card-body">
                                <i class="fas fa-brain fa-3x text-info"></i>
                                <h4 class="mt-3">Ensemble Analysis</h4>
                                <p>Combine both methods for comprehensive diagnosis</p>
                                <a href="/ensemble" class="btn btn-info text-white">Try Now</a>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="alert alert-info mt-5">
                    <i class="fas fa-info-circle"></i>
                    <strong>Note:</strong> This system is for research and educational purposes only.
                    Always consult with healthcare professionals for medical diagnosis.
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}"""
    
    with open(os.path.join(BASE_PATH, "templates", "index.html"), 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    # ct_scan.html
    ct_scan_html = """{% extends "base.html" %}

{% block title %}CT Scan Analysis{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <div class="card">
            <div class="card-header">
                <i class="fas fa-ct-scan"></i> CT Scan Analysis
            </div>
            <div class="card-body">
                <div class="upload-area" id="uploadArea">
                    <i class="fas fa-cloud-upload-alt"></i>
                    <h4>Drag & Drop or Click to Upload</h4>
                    <p class="text-muted">Supported formats: JPG, PNG, JPEG</p>
                    <input type="file" id="fileInput" accept=".jpg,.jpeg,.png" style="display: none;">
                </div>
                
                <div id="preview" style="display: none;" class="mt-4 text-center">
                    <img id="previewImage" class="preview-image">
                </div>
                
                <div class="loading-spinner" id="loadingSpinner">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <p class="mt-2">Analyzing image...</p>
                </div>
                
                <div id="result" style="display: none;" class="mt-4">
                    <h4 class="text-center">Analysis Results</h4>
                    <div class="prediction-box" id="predictionBox">
                        <h5 id="predictionClass"></h5>
                        <h2 id="confidenceScore"></h2>
                    </div>
                    <div class="text-center">
                        <img id="resultPlot" class="img-fluid mt-3" style="max-width: 100%;">
                    </div>
                    <div class="text-center mt-4">
                        <button class="btn btn-primary" onclick="resetUpload()">
                            <i class="fas fa-redo"></i> Analyze Another Image
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
$(document).ready(function() {
    $('#uploadArea').click(function() {
        $('#fileInput').click();
    });
    
    $('#uploadArea').on('dragover', function(e) {
        e.preventDefault();
        $(this).css('border-color', '#2c3e50');
    });
    
    $('#uploadArea').on('dragleave', function(e) {
        e.preventDefault();
        $(this).css('border-color', '#3498db');
    });
    
    $('#uploadArea').on('drop', function(e) {
        e.preventDefault();
        $(this).css('border-color', '#3498db');
        const files = e.originalEvent.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });
    
    $('#fileInput').change(function(e) {
        if (this.files.length > 0) {
            handleFile(this.files[0]);
        }
    });
    
    function handleFile(file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            $('#previewImage').attr('src', e.target.result);
            $('#preview').show();
            $('#uploadArea').hide();
            uploadAndPredict(file);
        };
        reader.readAsDataURL(file);
    }
    
    function uploadAndPredict(file) {
        const formData = new FormData();
        formData.append('file', file);
        
        $('#loadingSpinner').show();
        $('#result').hide();
        
        $.ajax({
            url: '/predict/ct',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                $('#loadingSpinner').hide();
                
                if (response.success) {
                    const confidence = response.confidence * 100;
                    $('#predictionClass').text('Prediction: ' + response.prediction.replace(/_/g, ' '));
                    $('#confidenceScore').text(confidence.toFixed(2) + '% Confidence');
                    
                    // Set prediction box color
                    const box = $('#predictionBox');
                    box.removeClass('prediction-high prediction-medium prediction-low');
                    if (confidence >= 80) {
                        box.addClass('prediction-high');
                    } else if (confidence >= 60) {
                        box.addClass('prediction-medium');
                    } else {
                        box.addClass('prediction-low');
                    }
                    
                    $('#resultPlot').attr('src', 'data:image/png;base64,' + response.plot);
                    $('#result').show();
                } else {
                    alert('Error: ' + response.error);
                    resetUpload();
                }
            },
            error: function(xhr, status, error) {
                $('#loadingSpinner').hide();
                alert('Error during prediction: ' + error);
                resetUpload();
            }
        });
    }
});

function resetUpload() {
    $('#uploadArea').show();
    $('#preview').hide();
    $('#result').hide();
    $('#fileInput').val('');
}
</script>
{% endblock %}"""
    
    with open(os.path.join(BASE_PATH, "templates", "ct_scan.html"), 'w', encoding='utf-8') as f:
        f.write(ct_scan_html)
    
    # histopathology.html
    histo_html = """{% extends "base.html" %}

{% block title %}Histopathology Analysis{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <div class="card">
            <div class="card-header">
                <i class="fas fa-microscope"></i> Histopathology Analysis
            </div>
            <div class="card-body">
                <div class="upload-area" id="uploadArea">
                    <i class="fas fa-cloud-upload-alt"></i>
                    <h4>Drag & Drop or Click to Upload</h4>
                    <p class="text-muted">Supported formats: JPG, PNG, JPEG</p>
                    <input type="file" id="fileInput" accept=".jpg,.jpeg,.png" style="display: none;">
                </div>
                
                <div id="preview" style="display: none;" class="mt-4 text-center">
                    <img id="previewImage" class="preview-image">
                </div>
                
                <div class="loading-spinner" id="loadingSpinner">
                    <div class="spinner-border text-success" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <p class="mt-2">Analyzing tissue sample...</p>
                </div>
                
                <div id="result" style="display: none;" class="mt-4">
                    <h4 class="text-center">Analysis Results</h4>
                    <div class="prediction-box" id="predictionBox">
                        <h5 id="predictionClass"></h5>
                        <h2 id="confidenceScore"></h2>
                    </div>
                    <div class="text-center">
                        <img id="resultPlot" class="img-fluid mt-3" style="max-width: 100%;">
                    </div>
                    <div class="text-center mt-4">
                        <button class="btn btn-success" onclick="resetUpload()">
                            <i class="fas fa-redo"></i> Analyze Another Image
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
$(document).ready(function() {
    $('#uploadArea').click(function() {
        $('#fileInput').click();
    });
    
    $('#uploadArea').on('dragover', function(e) {
        e.preventDefault();
        $(this).css('border-color', '#27ae60');
    });
    
    $('#uploadArea').on('dragleave', function(e) {
        e.preventDefault();
        $(this).css('border-color', '#3498db');
    });
    
    $('#uploadArea').on('drop', function(e) {
        e.preventDefault();
        $(this).css('border-color', '#3498db');
        const files = e.originalEvent.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });
    
    $('#fileInput').change(function(e) {
        if (this.files.length > 0) {
            handleFile(this.files[0]);
        }
    });
    
    function handleFile(file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            $('#previewImage').attr('src', e.target.result);
            $('#preview').show();
            $('#uploadArea').hide();
            uploadAndPredict(file);
        };
        reader.readAsDataURL(file);
    }
    
    function uploadAndPredict(file) {
        const formData = new FormData();
        formData.append('file', file);
        
        $('#loadingSpinner').show();
        $('#result').hide();
        
        $.ajax({
            url: '/predict/histo',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                $('#loadingSpinner').hide();
                
                if (response.success) {
                    const confidence = response.confidence * 100;
                    $('#predictionClass').text('Prediction: ' + response.prediction.replace(/_/g, ' '));
                    $('#confidenceScore').text(confidence.toFixed(2) + '% Confidence');
                    
                    // Set prediction box color
                    const box = $('#predictionBox');
                    box.removeClass('prediction-high prediction-medium prediction-low');
                    if (confidence >= 80) {
                        box.addClass('prediction-high');
                    } else if (confidence >= 60) {
                        box.addClass('prediction-medium');
                    } else {
                        box.addClass('prediction-low');
                    }
                    
                    $('#resultPlot').attr('src', 'data:image/png;base64,' + response.plot);
                    $('#result').show();
                } else {
                    alert('Error: ' + response.error);
                    resetUpload();
                }
            },
            error: function(xhr, status, error) {
                $('#loadingSpinner').hide();
                alert('Error during prediction: ' + error);
                resetUpload();
            }
        });
    }
});

function resetUpload() {
    $('#uploadArea').show();
    $('#preview').hide();
    $('#result').hide();
    $('#fileInput').val('');
}
</script>
{% endblock %}"""
    
    with open(os.path.join(BASE_PATH, "templates", "histopathology.html"), 'w', encoding='utf-8') as f:
        f.write(histo_html)
    
    # ensemble.html
    ensemble_html = """{% extends "base.html" %}

{% block title %}Ensemble Analysis{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-10">
        <div class="card">
            <div class="card-header">
                <i class="fas fa-brain"></i> Ensemble Analysis (CT + Histopathology)
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <h5 class="text-center">CT Scan</h5>
                        <div class="upload-area" id="ctUploadArea">
                            <i class="fas fa-cloud-upload-alt"></i>
                            <p>Upload CT Scan</p>
                            <input type="file" id="ctFileInput" accept=".jpg,.jpeg,.png" style="display: none;">
                        </div>
                        <div id="ctPreview" style="display: none;" class="mt-3 text-center">
                            <img id="ctPreviewImage" class="preview-image" style="max-height: 200px;">
                        </div>
                    </div>
                    <div class="col-md-6">
                        <h5 class="text-center">Histopathology</h5>
                        <div class="upload-area" id="histoUploadArea">
                            <i class="fas fa-cloud-upload-alt"></i>
                            <p>Upload Histopathology Image</p>
                            <input type="file" id="histoFileInput" accept=".jpg,.jpeg,.png" style="display: none;">
                        </div>
                        <div id="histoPreview" style="display: none;" class="mt-3 text-center">
                            <img id="histoPreviewImage" class="preview-image" style="max-height: 200px;">
                        </div>
                    </div>
                </div>
                
                <div class="text-center mt-4">
                    <button class="btn btn-primary btn-lg" id="analyzeBtn" disabled>
                        <i class="fas fa-analytics"></i> Analyze Both
                    </button>
                </div>
                
                <div class="loading-spinner" id="loadingSpinner">
                    <div class="spinner-border text-primary" role="status"></div>
                    <p class="mt-2">Analyzing images...</p>
                </div>
                
                <div id="result" style="display: none;" class="mt-4">
                    <h4 class="text-center">Ensemble Results</h4>
                    <div class="row mt-4">
                        <div class="col-md-4">
                            <div class="card">
                                <div class="card-body text-center">
                                    <h5>CT Scan</h5>
                                    <h3 id="ctPrediction"></h3>
                                    <p id="ctConfidence" class="text-muted"></p>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="card">
                                <div class="card-body text-center">
                                    <h5>Histopathology</h5>
                                    <h3 id="histoPrediction"></h3>
                                    <p id="histoConfidence" class="text-muted"></p>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="card">
                                <div class="card-body text-center">
                                    <h5>Ensemble</h5>
                                    <h3 id="ensemblePrediction"></h3>
                                    <p id="ensembleConfidence" class="text-muted"></p>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="text-center mt-4">
                        <button class="btn btn-primary" onclick="resetAll()">
                            <i class="fas fa-redo"></i> Analyze New Images
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
let ctFile = null;
let histoFile = null;

$(document).ready(function() {
    // CT Scan upload
    $('#ctUploadArea').click(function() {
        $('#ctFileInput').click();
    });
    
    $('#ctFileInput').change(function(e) {
        if (this.files.length > 0) {
            ctFile = this.files[0];
            const reader = new FileReader();
            reader.onload = function(e) {
                $('#ctPreviewImage').attr('src', e.target.result);
                $('#ctPreview').show();
                $('#ctUploadArea').hide();
                checkFiles();
            };
            reader.readAsDataURL(ctFile);
        }
    });
    
    // Histopathology upload
    $('#histoUploadArea').click(function() {
        $('#histoFileInput').click();
    });
    
    $('#histoFileInput').change(function(e) {
        if (this.files.length > 0) {
            histoFile = this.files[0];
            const reader = new FileReader();
            reader.onload = function(e) {
                $('#histoPreviewImage').attr('src', e.target.result);
                $('#histoPreview').show();
                $('#histoUploadArea').hide();
                checkFiles();
            };
            reader.readAsDataURL(histoFile);
        }
    });
    
    $('#analyzeBtn').click(function() {
        analyzeEnsemble();
    });
});

function checkFiles() {
    if (ctFile && histoFile) {
        $('#analyzeBtn').prop('disabled', false);
    }
}

function analyzeEnsemble() {
    const formData = new FormData();
    formData.append('ct_file', ctFile);
    formData.append('histo_file', histoFile);
    
    $('#loadingSpinner').show();
    $('#result').hide();
    $('#analyzeBtn').prop('disabled', true);
    
    $.ajax({
        url: '/predict/ensemble',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            $('#loadingSpinner').hide();
            
            if (response.success) {
                $('#ctPrediction').text(response.ct_scan.prediction.replace(/_/g, ' '));
                $('#ctConfidence').text((response.ct_scan.confidence * 100).toFixed(2) + '% confidence');
                
                $('#histoPrediction').text(response.histopathology.prediction.replace(/_/g, ' '));
                $('#histoConfidence').text((response.histopathology.confidence * 100).toFixed(2) + '% confidence');
                
                $('#ensemblePrediction').text(response.ensemble.prediction.replace(/_/g, ' '));
                $('#ensembleConfidence').text((response.ensemble.confidence * 100).toFixed(2) + '% confidence');
                
                $('#result').show();
            }
        },
        error: function() {
            $('#loadingSpinner').hide();
            alert('Error during analysis');
            resetAll();
        }
    });
}

function resetAll() {
    ctFile = null;
    histoFile = null;
    
    $('#ctUploadArea').show();
    $('#ctPreview').hide();
    $('#histoUploadArea').show();
    $('#histoPreview').hide();
    $('#result').hide();
    $('#analyzeBtn').prop('disabled', true);
    $('#ctFileInput').val('');
    $('#histoFileInput').val('');
}
</script>
{% endblock %}"""
    
    with open(os.path.join(BASE_PATH, "templates", "ensemble.html"), 'w', encoding='utf-8') as f:
        f.write(ensemble_html)
    
    print_success("HTML templates created")

def create_run_script():
    """Create run script for easy execution"""
    print_step("Creating run scripts")
    
    # Windows batch file - FIXED the escape sequence issue
    run_bat = '''@echo off
title Lung Cancer Detection System
color 0A

echo ========================================
echo    LUNG CANCER DETECTION SYSTEM
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b
)

REM Create virtual environment if not exists
if not exist "venv" (
    echo [1/5] Creating virtual environment...
    python -m venv venv
) else (
    echo [1/5] Virtual environment already exists
)

REM Activate virtual environment - FIXED: using CALL with proper escaping
call venv\\Scripts\\activate >nul 2>&1

REM Install requirements
echo [2/5] Installing requirements (this may take a few minutes)...
pip install -q --upgrade pip
pip install -q -r requirements.txt

REM Check if models exist
if not exist "models\\ct_model_final.h5" (
    echo.
    echo [3/5] Models not found. Training required.
    echo.
    echo Choose training option:
    echo   1. Train CT model only (quick - 20 epochs)
    echo   2. Train both models (full - 20 epochs each)
    echo   3. Skip training (use existing models)
    echo.
    set /p choice="Enter choice (1-3): "
    
    if "!choice!"=="1" (
        echo Training CT model...
        python train_ct.py
    )
    if "!choice!"=="2" (
        echo Training CT model...
        python train_ct.py
        echo.
        echo Training Histopathology model...
        python train_histopathology.py
    )
) else (
    echo [3/5] Models found
)

REM Run the app
echo.
echo [4/5] Starting web application...
echo [5/5] Opening browser...
echo.
echo ========================================
echo    APPLICATION IS RUNNING!
echo ========================================
echo.
echo Open your browser and go to: http://localhost:5000
echo Press Ctrl+C to stop the application
echo.

start http://localhost:5000
python app.py

pause'''
    
    with open(os.path.join(BASE_PATH, "run.bat"), 'w', newline='\r\n') as f:
        f.write(run_bat)
    
    # Quick start guide - FIXED: using regular string instead of f-string with the path
    quick_start = """QUICK START GUIDE
=================

Your Lung Cancer Detection project has been set up successfully!

📁 PROJECT LOCATION:
%s

🚀 TO RUN THE APPLICATION:
-------------------------
1. Double-click 'run.bat' in this folder
   OR open Command Prompt and type: python app.py

2. Open your browser and go to: http://localhost:5000

📊 DATASET ORGANIZATION:
-----------------------
Your data has been organized into:
- dataset/CT_Scan/ (CT scan images)
- dataset/Histopathology/ (Histopathology images)

🎯 AVAILABLE FEATURES:
--------------------
✅ CT Scan Analysis - Upload and analyze chest CT scans
✅ Histopathology Analysis - Analyze tissue samples
✅ Ensemble Analysis - Combine both for comprehensive diagnosis
✅ Real-time predictions with confidence scores
✅ Probability visualization charts

⚙️ TRAINING OPTIONS:
------------------
Quick training (20 epochs): python train_ct.py
Full training (50+ epochs): Modify EPOCHS in training scripts

📝 NOTES:
--------
- First run will install dependencies (may take 5-10 minutes)
- Models need to be trained before making predictions
- For research and educational purposes only

Need help? Check README.md for detailed documentation
""" % SOURCE_DATA_PATH
    
    with open(os.path.join(BASE_PATH, "QUICK_START.txt"), 'w') as f:
        f.write(quick_start)
    
    print_success("Run scripts created")

def create_readme():
    """Create README file - FIXED: properly terminated f-string"""
    print_step("Creating README")
    
   