import subprocess
import urllib.parse

def search_in_browser(query):
    # 將中文進行URL編碼
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.google.com/search?q={encoded_query}"
    #瀏覽器執行檔位址
    edge_path = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    #使用subprocess執行瀏覽器並搜尋URL
    subprocess.run([edge_path, url])

if __name__ == "__main__":
    while True:
        # 輸入要搜尋的資訊
        query = input("輸入想搜尋的資訊: ")
        search_in_browser(query)
