import os
import numpy as np
import librosa
import tensorflow as tf
import joblib
from sklearn.preprocessing import LabelEncoder
import subprocess
import urllib.parse

# 提取特徵函數
def extract_features(file_path, max_len=40):
    y, sr = librosa.load(file_path, sr=None)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=128)
    # 填充或截斷到固定長度
    if mfcc.shape[1] > max_len:
        mfcc = mfcc[:, :max_len]
    else:
        mfcc = np.pad(mfcc, ((0, 0), (0, max_len - mfcc.shape[1])), mode='constant')
    return mfcc

# 識別語音文件中的標籤
def recognize_speech_from_file(file_path, model, label_encoder, max_len=40):
    feature = extract_features(file_path, max_len)
    feature = np.expand_dims(feature, axis=0)  # 增加批次維度
    prediction = model.predict(feature)
    predicted_label = np.argmax(prediction, axis=1)
    return label_encoder.inverse_transform(predicted_label)[0]

# 加載上面保存的模型
model_path = 'saved_model/my_modelatoz'        # 加載上面保存的模型----------------加載上面保存的模型---------------加載上面保存的模型----------------加載上面保存的模型--------------加載上面保存的模型------
loaded_model = tf.keras.models.load_model(model_path)

# 加載標籤編碼器
label_encoder = joblib.load('label_encoder.pkl')

# 顯示加載後的模型結構
loaded_model.summary()

# 預測多個音頻文件並組合成單詞
def predict_word_from_audio_files(audio_files, model, label_encoder):
    predicted_word = ''
    for file_path in audio_files:
        predicted_label = recognize_speech_from_file(file_path, model, label_encoder)
        predicted_word += predicted_label
    return predicted_word
def search_in_browser(query):
    # 將中文進行URL編碼
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.google.com/search?q={encoded_query}"
    #瀏覽器執行檔位址
    edge_path = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    #使用subprocess執行瀏覽器並搜尋URL
    subprocess.run([edge_path, url])


# 測試識別
audio_files = [
    r"C:\Users\s0978\OneDrive\桌面\sound\atoz\A\A_1.wav",  # 放測試的音檔路徑----------放測試字母音檔路徑-----------放測試字母音檔路徑---------放測試字母音檔路徑------------------放測試字母音檔路徑
    r"C:\Users\s0978\OneDrive\桌面\sound\atoz\R\R_3.wav",  # 放測試的音檔路徑----------放測試字母音檔路徑-----------放測試字母音檔路徑---------放測試字母音檔路徑------------------放測試字母音檔路徑
    r"C:/Users/s0978/OneDrive/桌面/sound/atoz/R/R_7.wav",  # 放測試的音檔路徑----------放測試字母音檔路徑-----------放測試字母音檔路徑---------放測試字母音檔路徑------------------放測試字母音檔路徑
    r"C:\Users\s0978\OneDrive\桌面\sound\atoz\A\A_8.wav",  # 放測試的音檔路徑----------放測試字母音檔路徑-----------放測試字母音檔路徑---------放測試字母音檔路徑------------------放測試字母音檔路徑
    r"C:\Users\s0978\OneDrive\桌面\sound\atoz\Y\Y_7.wav",  # 放測試的音檔路徑----------放測試字母音檔路徑-----------放測試字母音檔路徑---------放測試字母音檔路徑------------------放測試字母音檔路徑
  

]

predicted_word = predict_word_from_audio_files(audio_files, loaded_model, label_encoder)
print(f"Predicted word: {predicted_word}")

# 輸入要搜尋的資訊
query = predicted_word
search_in_browser(query)
