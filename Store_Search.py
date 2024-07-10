import os
import pymysql
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import webbrowser
import datetime


def search_sql():
    sql=""
    try:  # 開啟資料庫連接
        conn = pymysql.connect(host="localhost",     # 主機名稱
                               user="root",         # 帳號
                               password="12345678",  # 密碼
                               database="telecom_analysis",  # 資料庫
                               port=3306)           # port
        conn.autocommit(True)  # 自動commit()
        cursor = conn.cursor()  # 使用cursor()方法操作資料庫
        sql = f"SELECT telecom, city, store_name, store_addr FROM store_qty \
            WHERE telecom='{tele_value.get()}' AND city='{city_value.get()}';" # ORDER BY store_addr
        cursor.execute(sql)

        globals()["data"] = cursor.fetchall()  # 取得所有資料

    except Exception as e:
        print("fail", e)

    finally:
        cursor.close()
        conn.close()
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(now_time, "查詢完成...")


def clear_list():
    showlist.delete(0, tk.END)  # 清空列表
    tele_value.set(tele[0])     # 將縣市下拉設為預設值
    city_value.set("請選擇")     # 將縣市下拉設為預設值
    count.set("")               # 清空顯示資料筆數的文字
    map_btn["state"] = "disabled"  # 禁用地圖按鈕
    canvas.delete("all")        # 清空圖片
    

def show_text():
    showlist.delete(0, "end")   # 清空列表
    
    if city_value.get() != "請選擇" or "":
        search_sql()
        show_img()
        for item in data:
            showlist.insert(tk.END, f"【{item[2]}】 {item[3]}")
            
        if showlist.size() != 0:
            map_btn["state"]="normal"  # 啟用地圖按鈕
            
        count.set(f">> {tele_value.get()} / {city_value.get()}，共 {len(data)} 筆資料")   # 顯示資料筆數
            
    else:
        messagebox.showinfo("提示", "請選擇「縣市」!")
        

def addr_text():
    selection = showlist.curselection()
    
    if selection:
        index = selection[0]
        # print(data[index][3])  # 印出選擇項目的地址
        webbrowser.open_new_tab(f"https://www.google.com/maps/place/{data[index][3]}") #打開地址連結
    else:
        messagebox.showinfo("提示", "請選擇「門市」！")


def show_img():
    canvas.delete("all")        # 清空圖片
    if tele_value.get() == tele[0]:
        img_path=".\Pic\Logo\CHT.png"
    elif tele_value.get() == tele[1]:
        img_path=os.getcwd() + r"\Pic\Logo\TWM.png"
    else:
        img_path=os.getcwd() + r"\Pic\Logo\FET.png"
    # 載入圖片
    img = Image.open(img_path)
    img = img.resize((150, 150))
    tk_img = ImageTk.PhotoImage(img) # 將圖片轉換為 Tkinter 的 PhotoImage 格式
    # 在畫布上顯示新圖片
    canvas.create_image(0, 0, anchor='nw', image=tk_img)
    canvas.tk_img = tk_img  # 保存參考以避免被垃圾回收
   

data=""   
root = tk.Tk()
root.title("門市查詢")  # 視窗標題
root.configure(bg="#fff")   # 設定背景色
root.iconbitmap(os.getcwd() + r"\Pic\Logo\ICON.ico")  # 設定icon(格式限定 .ico)

width, height = 800, 400
left = int((root.winfo_screenwidth() - width)/2)    # 取得螢幕寬度
top = int((root.winfo_screenheight() - height)/2)  # 取得螢幕高度
root.geometry(f"{width}x{height}+{left}+{top}")  # 視窗大小及位置
root.resizable(False, False)   # 設定 x 方向和 y 方向都不能縮放
# root.minsize(width, height)    # 設定視窗最小，最大maxsize

font_set = ("微軟正黑體", 11)

tele_label = ttk.Label(root, text="請選擇電信業者：", font=font_set, background="#fff")
tele_label.place(x=20, y=20)

tele = ["中華電信", "台灣大哥大", "遠傳電信"]
ttk.Style().configure('Custom.TRadiobutton', font=font_set,
                      background='#fff', fg='blue')  # 設定Radiobutton樣式
tele_value = tk.StringVar()
for i in range(len(tele)):  # 建立Radiobutton
    radio_btn = ttk.Radiobutton(
        root, text=tele[i], variable=tele_value, value=tele[i], style="Custom.TRadiobutton")
    radio_btn.place(x=20, y=50 + i*25)  # y=45、70、95
    if i == 0:  # 選擇第一個
        tele_value.set(tele[i])


n_li = ["臺北市", "新北市", "基隆市", "新竹市", "桃園市", "新竹縣", "宜蘭縣"]
c_li = ["臺中市", "苗栗縣", "彰化縣", "南投縣", "雲林縣"]
s_li = ["高雄市", "臺南市", "嘉義市", "嘉義縣", "屏東縣"]
e_li = ["花蓮縣", "臺東縣"]
i_li = ["澎湖縣", "金門縣", "連江縣"]

city_label = ttk.Label(root, text="請選擇縣市：", font=font_set, background="#fff")
city_label.place(x=20, y=140)

city_opt = n_li+c_li+s_li+e_li+i_li  # 選項
city_value = tk.StringVar() # 取值
city_value.set("請選擇")

# 建立下拉選單
menu = ttk.Combobox(root, textvariable=city_value, values=city_opt, font=font_set, state="readonly")
menu.place(x=20, y=170, width=120, height=25)


# 設定Button樣式、建立按鈕
ttk.Style().configure("Round.TButton", relief="flat", font=font_set, background="#fff")
search_btn = ttk.Button(root, text="查詢", style="Round.TButton", command=show_text)
search_btn.place(x=width/3-100, y=135, width=80, height=30)

clear_btn = ttk.Button(root, text="清除", style="Round.TButton", command=clear_list)
clear_btn.place(x=width/3-100, y=170, width=80, height=30)

map_btn = ttk.Button(root, text="地圖", style="Round.TButton", command=addr_text, state="disabled") #normal #disabled
map_btn.place(x=width-100, y=10, width=80, height=30)


# 加入框架
frame = ttk.Frame(root)        
frame.place(x=width/3, y=50, width=width*2/3-20 ,height=height-60)
    
# 在框架中建立x捲動條 & y捲動條
scrollbar_x = tk.Scrollbar(frame, width=20, orient="horizontal")
scrollbar_x.pack(side="bottom", fill="both")
scrollbar_y = tk.Scrollbar(frame, width=20)
scrollbar_y.pack(side="right", fill="both")

# 在框架中建立showlist
showlist = tk.Listbox(frame, width=300, font=font_set, background="#fff", relief="flat",
                      selectbackground="#B7DEE8", selectforeground="#000", 
                      yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

showlist.pack(side="left", fill="both") # 將 Listbox 放置在框架中
scrollbar_y.config(command=showlist.yview) # 設定捲動條的連動
scrollbar_x.config(command=showlist.xview)

count = tk.StringVar()  # 設定 a 為文字變數
count.set("")            # 設定 a 的內容
count_label = ttk.Label(root, textvariable=count, font=font_set, background="#fff")
count_label.place(x=width/3, y=20)


img_path=""
# 建立一個畫布小工具
canvas = tk.Canvas(root, width=150, height=150, bg='#fff', highlightthickness=0, bd=0)
canvas.place(x=width/3-210, y=height-175)


root.mainloop()  # 顯示視窗

