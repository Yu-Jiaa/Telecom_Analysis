# 資料下載

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep,time
import pandas as pd
import threading
import requests
import re
import os


# NCC、人口資料下載
def fileDownload():
    
    # NCC資料下載
    try:    
        # 網頁網址
        ur="https://www.ncc.gov.tw/chinese/opendata_item.aspx?menu_function_sn="
        url = ["208","16769"]
        
        for i in range(len(url)):
            res = requests.get(ur+url[i])
            soup = BeautifulSoup(res.text, 'html.parser')
            file_name = soup.find(id="_ctl0_CPH_Caption_lblTitle").string  # 抓檔名
            file_link = soup.find('a', id='csv_link').get("href")  # 連結
            
            download_url="https://www.ncc.gov.tw/chinese/"+file_link  # 下載完整連結
            filename = save_path + f'\{i+1}.{file_name}.csv'  # 完整檔名
            file_resp = requests.get(download_url)
            
            # 寫入檔案
            with open(filename, 'wb') as f:
                f.write(file_resp.content)  
                
        print("NCC資料下載成功\^0^/")

    except:
        print("NCC資料下載失敗<T.T>..")
    
    
    # 人口資料下載
    try: 
        # 設定下載選項
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("prefs", 
                {"download.default_directory": save_path}) #設定檔案下載位置

        ps_driver=webdriver.Chrome(options=chrome_options)
        ps_driver.get("https://www.ris.gov.tw/app/portal/346")
        sleep(5)
        
        ps_driver.switch_to.frame("content-frame")  
        sleep(1)  #進入框架
        
        ps_driver.find_element(By.CSS_SELECTOR, '[data-title="鄉鎮戶數及人口數(9701)"]').click()  
        sleep(1)  # 點選檔案選項
        
        ps_driver.find_element(By.CLASS_NAME, "btn.btn-primary.btn-action").click()  
        sleep(1)  # 點選下載
        
        print("人口資料下載成功\^0^/")
        
    except:
        print("人口資料下載失敗<T.T>..")
        

# 中華電信
def cht():
    url='https://my.cht.com.tw/ServiceCenter'
    cht_driver=webdriver.Chrome()
    cht_driver.get(url)

    cht_store=cht_driver.find_elements(By.CLASS_NAME,"text-black.font-16")
    cht_store[1].click()  # 點選第2項-門市查詢及預約
    cht_driver.find_element(By.CLASS_NAME,"btn.btn_select").click()  # 點選縣市列表下拉
    cht_city=cht_driver.find_elements(By.CLASS_NAME,"dialog-selector")  # 獲取縣市清單

    cht_city_li=[]
    for i in cht_city:
        cht_city_li.append(i.text)  # 存入縣市列表

    sleep(1)
    cht_city[0].click()
    cht_driver.find_element(By.CLASS_NAME,"btn.btn-200.btn-outline-black-999").click()  # 清除

    for i in range(len(cht_city)): #len(cht_city)
        cht_store_name = ""
        cht_store_addr = ""
        sleep(1)
        cht_driver.find_element(By.CLASS_NAME,"btn.btn_select").click()  # 點選縣市列表
        sleep(0.3)
        cht_driver.find_elements(By.CLASS_NAME,"font-14")[i].click()  # 點縣市選項
        cht_driver.find_element(By.CLASS_NAME,"btn.btn-200.btn-primary").click()  # 搜尋
        WebDriverWait(cht_driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME,"font-16")))  # 等待資料載入
        
        # 資料抓取(門市&地址)-------------------------#
        cht_soup = BeautifulSoup(cht_driver.page_source,'html.parser')
        cht_store_name = cht_soup.select("div.space-between > div")  # 門市店名
        cht_store_addr = cht_soup.select("span.text-black.pointer")  # 地址
        
        # 店名、地址存入列表
        for j, k in zip(cht_store_name, cht_store_addr):
            cht_com_li.append("中華電信")
            cht_store_city_li.append(cht_city_li[i])
            cht_store_name_li.append(j.text)
            cht_store_addr_li.append(k.text[5:])  # 排除前5碼郵遞區號
            
        cht_driver.find_element(By.CLASS_NAME,"text-black-666.icon.arrow-back").click() #回上一頁

    cht_driver.quit()  # 結束關閉


# 台灣大哥大   
def twm():
    url='https://www.taiwanmobile.com/mobile/storelbs/lbs.html'
    twm_driver=webdriver.Chrome()
    twm_driver.get(url)

    twm_driver.find_element(By.CLASS_NAME,"v2-o-footer__cookie-button").click()  # 同意cookie
    sleep(1)
    twm_sel = twm_driver.find_element(By.CLASS_NAME,"v2-a-form-select")  # 點縣市下拉選項
    twm_city = twm_sel.find_elements(By.TAG_NAME,"option")  # 獲取縣市清單

    twm_city_li=[]
    for i in twm_city:
        twm_city_li.append(i.text)  # 存入縣市列表

    for i in range(1,len(twm_city)-1):
        twm_store_name = ""
        twm_store_addr = ""
        twm_sel.click() #點選項
        twm_city[i].click() #點縣市
        twm_driver.find_element(By.CLASS_NAME,"v2-page-store__result-filter-function-button").click() #搜尋

        #資料抓取(門市&地址)-------------------------#
        sleep(2)
        twm_soup = BeautifulSoup(twm_driver.page_source,'html.parser')
        twm_store_name = twm_soup.select("p.v2-m-store-card__topic-title")  # 門市店名
        twm_store_addr = twm_soup.select("p.v2-m-store-card__content-value")  # 地址
        
        # 店名存入列表
        for j in twm_store_name:
            twm_com_li.append("台灣大哥大")
            twm_store_city_li.append(twm_city_li[i])
            twm_store_name_li.append(j.text)
        
        # 地址資料處理：判斷是否為地址（地址一般不包含"週|營業|(0?)|(0??)")
        for j in twm_store_addr:     
            if not re.search(r'週|營業|\(0.\)|\(0..\)', j.text):
                twm_store_addr_li.append(j.text)  # 地址存入列表
            
    twm_driver.quit()   # 結束關閉


# 遠傳電信
def fet():
    url='https://ecare.fetnet.net/DigService/help-center/store'
    fet_driver=webdriver.Chrome()
    fet_driver.get(url)
    
    WebDriverWait(fet_driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME,"fui-dropdown-item")))  # 等待資料載入
    fet_driver.find_element(By.CLASS_NAME,"fui-dropdown-item").click()  # 點選項(方式)
    
    WebDriverWait(fet_driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME,"fui-item  ")))  # 等待資料載入
    fet_driver.find_element(By.CLASS_NAME,"fui-item  ").click()  # 點選項(選縣市方式)
    
    fet_sel = fet_driver.find_elements(By.CLASS_NAME,"fui-dropdown-item")  # 點縣市列表
    fet_city = fet_driver.find_elements(By.CSS_SELECTOR,"div.menu-wrapper span.content")  # 獲取縣市清單
    
    for i in range(2, len(fet_city)): 
        fet_store_name = ""
        fet_store_addr = ""
        sleep(0.5)
        fet_sel[1].click()  # 點縣市列表
        sleep(0.3)
        fet_cities=fet_city[i].text  # 縣市名稱
        fet_city[i].click()  # 點縣市
        
        sleep(0.5)
        WebDriverWait(fet_driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.list h4")))  # 等待資料載入
        
        # if i in [4,6,7]: sleep(3)  # 部分縣市資料載入較慢
        # else: sleep(1.2) # 已改寫成until
        

        #資料抓取(門市&地址)-------------------------#
        sleep(1.5)
        fet_soup = BeautifulSoup(fet_driver.page_source,'html.parser')
        fet_store_name = fet_soup.select("div.list h4")  # 門市店名
        fet_store_addr = fet_soup.select("div.d-flex.justify-between.flex-align-center p")  # 地址
        
        # 店名、地址存入列表
        for j, k in zip(fet_store_name,fet_store_addr):
            fet_com_li.append("遠傳電信")
            fet_store_city_li.append(fet_cities)
            fet_store_name_li.append(j.text)
            fet_store_addr_li.append(k.text)
    fet_driver.quit()  # 結束關閉


#-----------------------------------------------

# 檔案下載路徑
# 路徑資料夾是否存在，如果不存在則建立
save_path = os.getcwd() + r"\RawData"
if not os.path.exists(save_path):
    os.makedirs(save_path)

try:
    start_time=time()  #紀錄開始時間
    fileDownload() # NCC、人口資料下載
    
    # 建立列表
    cht_com_li=[]
    cht_store_city_li=[]
    cht_store_name_li=[]
    cht_store_addr_li=[]   
    twm_com_li=[]
    twm_store_city_li=[]
    twm_store_name_li=[]
    twm_store_addr_li=[] 
    fet_com_li=[]
    fet_store_city_li=[]
    fet_store_name_li=[]
    fet_store_addr_li=[]
    
    # 多執行緒
    fet_thread = threading.Thread(target=fet)
    fet_thread.start()  # 開始跑‌「遠傳」門市網站
    sleep(10)
    cht_thread = threading.Thread(target=cht)
    cht_thread.start()  # 開始跑‌「中華」門市網站
    sleep(10)
    twm_thread = threading.Thread(target=twm)
    twm_thread.start()  # 開始跑‌「台哥大」門市網站
    
    fet_thread.join()  # 等待「遠傳」結束
    cht_thread.join()  # 等待「中華」結束
    twm_thread.join()  # 等待「台哥大」結束
    print("門市資料抓取完成\^0^/")
    
    # 3家門市資料結合、存入.csv
    data = {"業者名稱": cht_com_li + twm_com_li + fet_com_li,
            "縣市": cht_store_city_li + twm_store_city_li + fet_store_city_li,
            "門市": cht_store_name_li + twm_store_name_li + fet_store_name_li,
            "地址": cht_store_addr_li + twm_store_addr_li + fet_store_addr_li}
    
    # 地址移除空格及開頭數字
    data["地址"] = [re.sub(r'^\d+', '', str(i).strip()) for i in data["地址"]]
    # 將"縣市、地址"的「台」更改為「臺」
    data["縣市"] = [re.sub("台", "臺", i) for i in data["縣市"]]
    data["地址"] = [re.sub("台", "臺", i) for i in data["地址"]] 
    
    pd.DataFrame(data).to_csv(save_path + r"\3.門市店點資料.csv", encoding="UTF-16", index=False, sep='\t')
    print("門市資料儲存成功\^0^/")
    print(f"路徑:{save_path}")
    
    end_time=time()  # 結束時間
    run_time=f"{int((end_time-start_time)//60)}分{int((end_time-start_time)%60)}秒"
    print(f"資料抓取共花費 {run_time}...")
    
except:
    print("資料下載失敗..\n人生不會總是一帆風順，再試一次吧~")
        
