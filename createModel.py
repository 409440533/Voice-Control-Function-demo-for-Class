import os
import numpy as np
import librosa
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# 1. 收集數據
def load_data(data_dir, max_len=40):
    features = []
    labels = []
    if not os.path.exists(data_dir):
        raise ValueError(f"The directory {data_dir} does not exist.")
    
    for item in os.listdir(data_dir):
        item_path = os.path.join(data_dir, item)
        if os.path.isdir(item_path):
            print(f"Processing directory: {item_path}")
            for file_name in os.listdir(item_path):
                if file_name.lower().endswith('.wav'):  # 確保是 WAV 文件
                    file_path = os.path.join(item_path, file_name)
                    print(f"Loading {file_path}")  # 打印正在加載的文件
                    try:
                        feature = extract_features(file_path, max_len)
                        features.append(feature)
                        labels.append(item)  # 使用文件夾名稱作為標籤
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")
        elif item.lower().endswith('.wav'):
            # 如果直接在根目录中找到 WAV 文件
            print(f"Loading {item_path}")
            try:
                feature = extract_features(item_path, max_len)
                features.append(feature)
                labels.append("unknown")  # 如果没有子文件夹，假设所有文件的标签都是 unknown
            except Exception as e:
                print(f"Error processing {item_path}: {e}")
    
    if not features:
        raise ValueError("No audio files found in the data directory.")
    return np.array(features), np.array(labels)

def extract_features(file_path, max_len):
    y, sr = librosa.load(file_path, sr=None)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=128)
    # 填充或截断到固定长度
    if mfcc.shape[1] > max_len:
        mfcc = mfcc[:, :max_len]
    else:
        mfcc = np.pad(mfcc, ((0, 0), (0, max_len - mfcc.shape[1])), mode='constant')
    return mfcc

# 2. 預處理數據
data_dir = r"C:\Users\s0978\OneDrive\桌面\sound\atoz"  # 放Dataset的路徑---------------------------放Dataset的路徑----------------------------放Dataset的路徑----------------------------------
try:
    X, y = load_data(data_dir)
    print(f"Loaded {len(X)} samples with labels {set(y)}")
    
    # 使用 LabelEncoder 将字符串标签转换为整数
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)
except ValueError as e:
    print(e)
    exit(1)

# 3. 設計模型
def create_model(input_shape, num_classes):
    model = tf.keras.Sequential([
        tf.keras.layers.InputLayer(input_shape=input_shape),
        tf.keras.layers.Reshape((input_shape[0], input_shape[1], 1)),
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(num_classes, activation='softmax')  # 使用 num_classes 作為輸出
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

# 4. 訓練模型
input_shape = (128, 40)  # 更新输入形状以匹配新的特征数量
num_classes = len(set(y))  # 使用标签的数量作为输出类别的数量
model = create_model(input_shape, num_classes)
model.fit(X_train, y_train, epochs=10, validation_data=(X_val, y_val))

# 保存模型
model.save('saved_model/my_modelatoz')

# 顯示模型結構
model.summary()

# 獲取模型權重
weights = model.get_weights()
for i, weight in enumerate(weights):
    print(f"Weight layer {i}: {weight.shape}")

# 5. 評估模型
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {accuracy}")

# 6. 加載模型
loaded_model = tf.keras.models.load_model('saved_model/my_modelatoz')

# 顯示加載後的模型結構
loaded_model.summary()

# 獲取加載後的模型權重
loaded_weights = loaded_model.get_weights()
for i, weight in enumerate(loaded_weights):
    print(f"Loaded Weight layer {i}: {weight.shape}")

# 7. 部署模型
def recognize_speech_from_file(file_path, model, label_encoder, max_len=40):
    feature = extract_features(file_path, max_len)
    feature = np.expand_dims(feature, axis=0)  # 增加批次维度
    prediction = model.predict(feature)
    predicted_label = np.argmax(prediction, axis=1)
    return label_encoder.inverse_transform(predicted_label)[0]

# 測試識別
test_file_path = r"C:\Users\s0978\OneDrive\桌面\sound\atoz\A\A_2.wav"  # 放測試字母音檔路徑---------------------放測試字母音檔路徑-------------------------放測試字母音檔路徑-------------------------
predicted_label = recognize_speech_from_file(test_file_path, loaded_model, label_encoder)
print(f"Predicted label: {predicted_label}")
