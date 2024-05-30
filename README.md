# Voice-Control-Function-demo-for-Class
A small project for Machine Learning in class of TKUEE
![測試用學校圖片](http://www.ee.tku.edu.tw/wp-content/uploads/2017/03/%E6%B7%A1%E6%B1%9F%E5%A4%A7%E5%AD%B8%E9%9B%BB%E6%A9%9F-06.png)  
# 報告標題
語音辨識用以自動搜尋

### 動機
平常用的裝置使用上多半都會具備有鍵盤或是滑鼠等設備輸入，平常也是很少使用語音輸入的功能，  
因此在這次的期末project也想嘗試看看有關語音作為輸入的應用，便嘗試結合到上網搜尋的部分。
 - 最初預期目標:  
利用機器學習辨識語音輸入，透過不同的輸入進而達成操作個人電腦，
機器學習目標在於能夠辨識不同的語音輸入，  
轉換成電腦的操作，以期最終能夠透過語音輸入的方式來開啟瀏覽器，模擬完整的搜尋過程，  
甚至擴展應用可以在檔案總管中建置資料夾，修改文件名稱等等。  

### 實作方法
 - 原先方法困難點:  
思考如何訓練語音輸入的模型時，遇到不少的問題，要能夠建構出一個能辨識不同的中文句子，  
在不同語氣下都能精準的辨別且完整的語音辨識 (Common Voice)的模型，
其所需要的資料量非常龐大，加上訓練過程非常耗時，沒有足夠的設備難以在時間內趕上報告時間，
而這些情況都是沒有事先考慮到的，只好對原先設定的目標進行修正。

 - 後續調整:   
※**辨識不同中英文單字⮕辨識英文字母及數字**。  
相較於中英文單字的組成與發音非常複雜，英文字母與數字0\~9相對簡單很多，  
因此最終決定採用僅辨識26個英文字母，或是數字0\~9的單輸入作為語音辨識的標的(共36個字元)。  
此調整能大幅降低訓練所需要的資料量以及硬體設備資源，並且也能夠透過增加步驟完成整個搜尋功能的執行，因此作為妥協方案是能夠接受的。

 - 進行方式:  
搜尋相關dataset:  
https://robertmassaioli.bitbucket.io/alphabet-upload.html  
此dataset中的資料每筆都是一個由A到Z逐字唸出的連續音檔，再透過資料前處理後，分割成A~Z 26個字母分開的語音共10組，處理完後即為模型訓練所使用的資料集。  
使用了別人的source code:
https://github.com/KuanHaoHuang/tbrain-tomofun-audio-classification  
<T-brain 2021，Tomofun 狗音辨識 AI 百萬挑戰賽：Top 3% Solution>的source code。  

執行步驟說明:  

先執行creatModel.py
 1. 會將輸入的音檔轉成頻譜，並利用此dataset生成CNN模型  
 2. 給了輸入字母A的音檔，模型預測出結果為A  
 3. 保存模型

再利用searchPredictedWord.py  
 1. 寫一個能判斷多個音檔的程式，然後依次給輸入A、R、R、A、Y  
 2. 得到預測結果ARRAY，結合後半段的程式在網上搜尋ARRAY  
 

最後結果:  
一開始嘗試利用自己的聲音去錄製並進行結果的預測，但最終預測結果非常糟糕。  
應該是因為訓練的資料大約只有10*26筆並不足夠，因此判別的精準度非常低，所以測試時改用資料集有的音訊。  
而後有就其他資料量相對大一些的dataset(4000筆訓練資料)用相同的程式做模擬，但能改善的情況仍有限。  
### DEMO  
PowerPoint:  
https://tku365-my.sharepoint.com/:p:/g/personal/409440418_o365_tku_edu_tw/EYnUiugR2HBEvaS2NvbXD2gBHBg99uFb90Ache_nj6hU2w?e=jQr7na

video:  
[ARRAY搜尋.mp4](https://github.com/409440533/Voice-Control-Function-demo-for-Class/blob/main/ARRAY%E6%90%9C%E5%B0%8B.mp4)

---
## tool version and dataset
python: 3.11.0

dataset used:  
[https://robertmassaioli.bitbucket.io/alphabet-upload.html ​](https://robertmassaioli.bitbucket.io/alphabet-upload.html?)處理過後:https://github.com/409440533/Voice-Control-Function-demo-for-Class/releases/tag/dataset  
[wenya-chungyuan-jauhhsiang/Spoken-Digit-Recognizer (github.com) ](https://github.com/wenya-chungyuan-jauhhsiang/Spoken-Digit-Recognizer)

---
未使用到參考資料:  
語音生成(生成測試資料):  
https://github.com/nateshmbhat/pyttsx3

