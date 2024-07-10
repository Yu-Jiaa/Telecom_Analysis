# 載入套件、讀取檔案
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import Data_SQL  # 載入Data_SQL.py

data_path = os.getcwd() + "\RawData\\"
df1 = pd.read_csv(data_path + "1.行動通信業務基地臺統計數.csv")
df1_1 = pd.read_excel(data_path + "鄉鎮戶數及人口數-113年4月.xls")
df2 = pd.read_csv(data_path + "2.行動寬頻服務用戶數統計.csv")
df3 = pd.read_csv(data_path + "3.門市店點資料.csv", encoding="UTF-16", sep="\t")


# 資料整理+分析

# =============================================================================
# -------------------df1-基地臺------------------
# =============================================================================
# 刪除["業者名稱"]的空格及多餘文字
# [統計期]欄位：整數轉為文字，只抓前5字str[:5]，如:11303、11302
# 取前(民國年)3位，轉成西元+1911，+月份，合併年月，為新欄位[日期]
# 刪除欄位

df1["業者名稱"] = df1["業者名稱"].str.strip().str.replace("股份有限公司", "")
df1["統計期"] = df1["統計期"].astype(str).str[:5]
df1["Year"] = df1["統計期"].str[:3].astype(int) + 1911
df1["Month"] = df1["統計期"].str[3:]
df1["統計期"] = df1["Year"].astype(str) + "-" + df1["Month"]
df1["日期"] = pd.to_datetime(df1["統計期"], format='%Y-%m')
df1.drop(columns=["Year", "Month"], inplace=True)


# 判斷縣市區域、新增[區域]欄位
n_li = ["臺北市", "新北市", "基隆市", "新竹市", "桃園市", "新竹縣", "宜蘭縣"]
c_li = ["臺中市", "苗栗縣", "彰化縣", "南投縣", "雲林縣"]
s_li = ["高雄市", "臺南市", "嘉義市", "嘉義縣", "屏東縣"]
e_li = ["花蓮縣", "臺東縣"]
i_li = ["澎湖縣", "金門縣", "連江縣"]

def area(city):
    if city in n_li:
        return "北部"
    elif city in c_li:
        return "中部"
    elif city in s_li:
        return "南部"
    elif city in e_li:
        return "東部"
    elif city in i_li:
        return "離島"
    
df1["區域"] = df1["縣市"].apply(area)
df1 = df1.reindex(columns=["業者名稱", "縣市", "區域", "類別", "基地臺", "統計期", "日期"])

# -------------------df1_1-人口數------------------
# 只抓取第1、3欄資料(縣市、人口數)
# 2個欄位重新命名(縣市、人口數)
# 刪除["縣市"]的字串空格
# 抓取有在(n_li+c_li+...)中的資料(=排除小計資料)
# 判斷縣市區域、新增[區域]欄位

df1_1 = df1_1[[df1_1.columns[0], df1_1.columns[2]]]
df1_1.rename(columns={df1_1.columns[0]: "縣市",
             df1_1.columns[1]: "人口數"}, inplace=True)
df1_1["縣市"] = df1_1["縣市"].str.replace(" ", "")
df1_1 = df1_1[df1_1["縣市"].isin(
    n_li+c_li+s_li+e_li+i_li)].reset_index(drop=True)
df1_1["區域"] = df1_1["縣市"].apply(area)
df1_1 = df1_1.reindex(columns=["縣市", "區域", "人口數"])


# -------------------df1分析-------------------
# (1-2)2024年各家電信-基地台數量(各區域)
# (3)近2年各家電信的基地台數量趨勢
# (4)基地臺與人口數比較

bs = df1[df1["日期"] == max(df1["日期"])]
bs1 = bs.groupby("業者名稱")["基地臺"].sum().reset_index()
bs2 = bs.groupby(["業者名稱", "區域"])["基地臺"].sum().reset_index()
bs3 = df1.groupby(["業者名稱", "日期"])["基地臺"].sum().reset_index()
bs3 = bs3.groupby(["業者名稱", pd.Grouper(key="日期", freq="1YS")])[
    "基地臺"].max().reset_index()
# 1YS:以1年為區間
# .sort_values("日期",ascending=False)

telecom = ["中華電信", "台灣大哥大", "遠傳電信", "台灣之星", "亞太電信"]
bs3_dict = {}
for i in telecom:
    bs3_dict[i] = bs3[bs3["業者名稱"].str.contains(i)]
    # str.contains包含

# -------------------df1_1分析-------------------

ps = df1_1.groupby("區域")["人口數"].sum().to_frame()
ps = ps.join(bs2.groupby("區域")["基地臺"].sum().to_frame(), on="區域")
ps = ps.reindex(["北部", "中部", "南部", "東部", "離島"])


# =============================================================================
# -------------------df2資料-用戶數------------------
# =============================================================================

# 刪除["業者名稱"]的空白及多餘文字
# [統計期]欄位：整數轉為文字，只抓前5字str[:5]，如:11303、11302
# 取前(民國年)3位，轉成西元+1911，+月份，合併年月，為新欄位[日期]
# 刪除欄位

# df2.info()
df2["業者名稱"] = df2["業者名稱"].str.strip().str.replace("股份有限公司", "")
df2["統計期"] = df2["統計期"].astype(str)
df2["Year"] = df2["統計期"].str[:3].astype(int) + 1911
df2["Month"] = df2["統計期"].str[3:]
df2["統計期"] = df2["Year"].astype(str) + "-" + df2["Month"]
df2["日期"] = pd.to_datetime(df2["統計期"], format='%Y-%m')
df2.fillna(0, inplace=True) # 缺失補0
df2.drop(columns=["Year", "Month"], inplace=True)
df2 = df2.reindex(columns=["業者名稱", "行動寬頻總用戶數", "4G用戶數小計", "4G月租型",
                  "4G預付卡型",  "5G用戶數小計", "5G月租型", "5G預付卡型", "統計期", "日期"])


# -------------------df2分析-------------------
# (1)us1--2024年各家電信-用戶數(4G、5G)
# (2)us2--2024年各家電信-用戶類別(4G月租、4G預付卡、5G月租、5G預付卡)
# (3)us3--2015-2024年各家電信的用戶數趨勢(5家)
# (4)us4--2024年用戶數與基地台的比較(bs1)

us = df2[df2["日期"] == max(df2["日期"])]
us1 = us.groupby("業者名稱")[["行動寬頻總用戶數", "4G用戶數小計",
                          "5G用戶數小計"]].sum().reset_index()
us2 = us.groupby("業者名稱")[["4G月租型", "4G預付卡型", "5G月租型",
                          "5G預付卡型"]].sum()
us3 = df2.groupby(["業者名稱", "日期"])["行動寬頻總用戶數"].sum().reset_index()
us3 = us3.groupby(["業者名稱", pd.Grouper(key="日期", freq="1YS")])[
    "行動寬頻總用戶數"].max().reset_index()
# 1YS:以1年為區間
us3_1 = df2.groupby(["業者名稱", "日期"])[["4G用戶數小計", "5G用戶數小計"]].sum().reset_index()
us3_1 = us3_1.groupby(["業者名稱", pd.Grouper(key="日期", freq="1YS")])[
    ["4G用戶數小計", "5G用戶數小計"]].max().reset_index()

telecom = ["中華電信", "台灣大哥大", "遠傳電信", "台灣之星", "亞太電信"]
us3_dict, us3_1_dict = {}, {}
for i in telecom:
    us3_dict[i] = us3[us3["業者名稱"].str.contains(i)]
    us3_1_dict[i] = us3_1[us3_1["業者名稱"].str.contains(i)] 
    # str.contains包含 

# 抓取總用戶數資料並更名
# 將用戶數資料及基地台資料結合
us4 = us1[["業者名稱", "行動寬頻總用戶數"]].rename(columns={"行動寬頻總用戶數": "用戶數"})
us4 = pd.concat([us4, bs1.drop(columns=['業者名稱'])], axis=1).set_index("業者名稱")


# =============================================================================
# -------------------df3資料-門市點------------------
# =============================================================================
# 刪除["業者名稱"]的空白
# 判斷縣市區域、新增[區域]欄位

# df3.info()
df3["業者名稱"] = df3["業者名稱"].str.strip().str.replace("股份有限公司", "")
df3["區域"] = df3["縣市"].apply(area)
df3 = df3.reindex(columns=["業者名稱", "縣市", "區域", "門市", "地址"])


# -------------------df3分析-------------------
# (1)2024年各家電信-門市數量
# (2)2024年各區域-各家電信-門市數量
# (3)門市與用戶數的比較(us4)

st = df3.groupby(["業者名稱"])["門市"].nunique().reset_index()
st1 = df3.groupby(["業者名稱", "區域"])["門市"].nunique().reset_index()

# 將門市數量資料及用戶數資料結合並更名
st2 = pd.concat([st, us1["行動寬頻總用戶數"]], axis=1).set_index("業者名稱")\
    .rename(columns={"行動寬頻總用戶數": "用戶數"})


Data_SQL.data_sql(df1, df1_1, df2, df3) # 資料存入資料庫


# %% 繪製圖表

def draw_charts():

    # 設定y軸為千分位
    def y_thousand(x, pos):
        return f'{int(x):,}'
    
    # =============================================================================
    # -------------------df1圖表-------------------
    # =============================================================================
    
    
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 設置中文字體
    plt.rcParams['axes.unicode_minus'] = False  # 解決座標軸負號顯示問題
    
    # bs1 最新一期-各家電信-基地台數量 (總量+各區域)
    # fig, ax = plt.subplots(figsize=(8,6))
    # # bar_color=["#87b6d7","#ffd897","#f4988f"]
    # bs_2024=ax.bar(bs1["業者名稱"], bs1["基地臺"], width=0.5)
    # ax.bar_label(bs_2024,fontsize=11, color="#2d3047", padding=10)
    # plt.show()
    
    
    # bs2 最新一期-各家電信-基地台數量-各區域---------------------
    fig, ax = plt.subplots(figsize=(8, 6))
    bs_area = bs2.pivot(index='業者名稱', columns='區域', values='基地臺')[
        ["北部", "中部", "東部", "南部", "離島"]]  # 轉換透視表、變更順序
    area_colors = ["#bb8588", "#d8a48f", "#efebce", "#d6ce93", "#a3a380"]
    bs_area.plot(kind='bar', stacked=True, ax=ax, color=area_colors, width=0.6)
    
    def add_y_text(data, total):  # 加數字標籤
        for i in range(len(data.index)):
            ax.text(i, max(total)*1.05,
                    f"({total[i]:,})", va="center", ha="center", color="#2d3047", fontsize=10)
            y_offset = 0
            for j in data.columns:
                y = data.loc[data.index[i], j]  # 例如: bs_area.loc["中華電信","北部"]
                ax.text(i, y_offset + y/2, f"{j} - {y:,}", va="center",
                        ha="center", fontsize=10, color="#282828")
                y_offset += y
    add_y_text(bs_area, bs1['基地臺'])  # 加數字標籤
    
    ax.get_legend().remove()  # 移除圖例
    ax.set_ylim(0, 38000)  # 設定y軸數字上限
    ax.yaxis.set_major_formatter(FuncFormatter(y_thousand))  # 設定y軸千分位
    ax.set_xlabel("")  # 移除x軸index的文字
    
    plt.xticks(rotation=0)  # x軸的文字方向
    plt.title(f"{bs['統計期'][0]}-基地臺數量(總量+各區域)", fontsize=15, fontweight="bold", y=1.01)  # 標題    
    plt.show()
    # plt.savefig(r".\PIC\bs1.png", transparent=True) # 儲存圖片，背景透明
    
    
    # bs1_1 各區域-基地臺數量與人口數之比較---------------------
    fig, ax = plt.subplots(figsize=(8, 6))
    bar_color = ["#87b6d7", "#feb793", "#f4988f", "#c890b6", "#bddd98"]
    ax.bar(ps.index, ps["基地臺"], color=bar_color, label="基地臺")
    
    # 數字標籤
    for i in range(0, len(ps.index)):
        ax.text(i, ps.iloc[i]["基地臺"]+500, f'{ps.iloc[i]["基地臺"]:,}', ha='center')
    
    ax.set_ylim(0, 40000)  # 設定y軸數字上限
    ax.yaxis.set_major_formatter(FuncFormatter(y_thousand))  # 設定y軸千分位
    ax.text(-0.9, 41500, "基地臺", rotation=0)
    
    ax2 = ax.twinx()  # 新增右邊的Y軸
    ax2.plot(ps.index, ps["人口數"], "--", color="#696969", label="人口數", marker='o')
    ax2.set_ylim(0, 12000000)  # 設定y軸數字上限
    ax2.yaxis.set_major_formatter(FuncFormatter(y_thousand))  # 設定y軸千分位
    ax2.text(4.5, 12500000, "人口數", rotation=0)
    
    for i, v in zip(ps.index, ps["人口數"]):
        ax2.text(i, v, f"{v:,}", fontsize=9)
    
    # 增加標籤 (人口數//基地臺)
    for i in range(0, len(ps.index)):
        t = ax.text(i, 12000, f' {ps.iloc[i]["人口數"]//ps.iloc[i]["基地臺"]}人 / \n基地台 ', ha='center')
        
        t.set_bbox(dict(facecolor="w", alpha=0.6, edgecolor="r", boxstyle="round"))
    
    fig.legend(loc="upper right", ncol=2, bbox_to_anchor=(0.85, 0.88))  # 圖例
    plt.title(f"{bs['統計期'][0]}-各區域-基地臺數量與人口數之比較", fontsize=15, fontweight="bold", y=1.01)  # 標題
    plt.subplots_adjust(right=0.88)  # 調整圖表位置
    plt.show()
    # plt.savefig(r".\PIC\bs2.png", transparent=True) # 儲存圖片，背景透明
    
    
    # bs3 2014-2024年基地台數量趨勢---------------------
    fig, ax = plt.subplots(figsize=(8, 6))
    # plot_colors=["#3da5d9","#ffc09f","#ef476f","#8e7dbe","#8cb369"]
    plot_colors = ["#0064a8", "#ffad21", "#e72410",
                   "#c890b6", "#bddd98"]  # B60376、7EC42D
    line_style = ["-", "-", "-", "--", "--"]
    for [(key, value), plot_color, line_style] in zip(bs3_dict.items(), plot_colors, line_style):
        ax.plot(value["日期"], value["基地臺"], line_style, marker='o',
                linewidth=2, color=plot_color, label=key)
    
    min_y, max_y = str(min(bs3['日期'])), str(max(bs3['日期']))
    ax.set_ylim(-2000, 38000)  # 設定y軸數字上限
    ax.legend(loc="lower right", fontsize=10)  # 圖例
    ax.yaxis.set_major_formatter(FuncFormatter(y_thousand))  # 設定y軸千分位
    # plt.xticks(fontsize=9,rotation=0)
    plt.title(f"{min_y[:4]} ~ {max_y[:4]}年-基地台數量趨勢", fontsize=15, fontweight="bold", y=1.01)  # 標題
    plt.grid(color="#f0efeb")  # 網格
    plt.show()
    # plt.savefig(r".\PIC\bs3.png", transparent=True) # 儲存圖片，背景透明
    
    
    
    # =============================================================================
    # -------------------df2圖表-------------------
    # =============================================================================
    
    # us1 最新一期-各家電信-用戶數量 (總量+各類別)
    # fig, ax = plt.subplots(figsize=(8,6))
    # us_2024=ax.bar(us1["業者名稱"], us1["行動寬頻總用戶數"], width=0.6)
    # ax.bar_label(us_2024,labels=[f'{int(bar.get_height()):,}' for bar in us_2024],
    #              fontsize=11, color="#2d3047",padding=3)
    
    # us1
    fig, ax = plt.subplots(figsize=(8, 6))
    us_type = us1.drop(columns="行動寬頻總用戶數")\
        .rename(columns={"4G用戶數小計": "4G", "5G用戶數小計": "5G"})
    us_type.set_index("業者名稱", inplace=True)
    bar_colors = ["#d8a48f", "#efebce"]
    us_type.plot(kind='bar', stacked=True, ax=ax, color=bar_colors, width=0.6)
    
    add_y_text(us_type, us1["行動寬頻總用戶數"])  # 加數字標籤
    ax.set_ylim(0, 13000000)  # 設定y軸數字上限
    ax.yaxis.set_major_formatter(FuncFormatter(y_thousand))  # 設定y軸千分位
    
    ax.set_xlabel("")  # 移除x軸index的文字
    ax.get_legend().remove()  # 移除圖例
    plt.xticks(rotation=0)  # x軸的文字方向
    plt.title(f"{max(us['統計期'])}-用戶數量(總量+各類別)", fontsize=15, fontweight="bold", y=1.01)  # 標題
    plt.show()
    # plt.savefig(r".\PIC\us1.png", transparent=True) # 儲存圖片，背景透明
    # ax.legend(ncol=2,fontsize=10) # 圖例，2欄
    
    
    # us2 2024年用戶類別---------------------
    
    fig, ax = plt.subplots(1, 3, figsize=(12, 4))
    
    def func(s, d):
        t = int(round(s/100.*sum(d)))     # 透過百分比反推原本的數值
        return f'{s:.1f}%\n({int(t):,})'     # 使用文字格式化的方式，顯示內容
    
    
    pie_color = ["#87b6d7", "#feb793", "#bddd98", "#f4988f", "#c890b6"]
    for i in range(3):
        ax[i].set_title(us2.index[i], loc="center", fontsize=13)  # 小標題
        ax[i].pie(us2.iloc[i], radius=1.2, labels=us2.columns, colors=pie_color,
                  autopct=lambda x: func(x, us2.iloc[i]), textprops={"color": "black", "size": 10},
                  startangle=30)
    
    fig.suptitle(f"{max(us['統計期'])}-用戶類別占比", fontsize=15, fontweight="bold")  # 大標題
    plt.tight_layout()  # 自動保持合適的間距
    # fig.delaxes(ax[1, 1]) # 隱藏[1, 1]的區塊
    plt.show()
    # plt.savefig(r".\PIC\us2.png", transparent=True) # 儲存圖片，背景透明
    
    
    # us3 2015-2024年用戶數量趨勢---------------------
    fig, ax = plt.subplots(1, 2, figsize=(14, 6))
    plot_colors = ["#0064a8", "#ffad21", "#e72410",
                   "#c890b6", "#bddd98"]  # B60376、7EC42D
    line_style = ["-", "-", "-", "--", "--"]
    
    # 總用戶數量
    for [(key, value), plot_color, line_style] in zip(us3_dict.items(), plot_colors, line_style):
        ax[0].plot(value["日期"], value["行動寬頻總用戶數"], line_style,
                marker='o', linewidth=2, color=plot_color, label=key)
    ax[0].legend(fontsize=10)  # 圖例
    ax[0].grid(color="#f0efeb")  # 網格
    ax[0].yaxis.set_major_formatter(FuncFormatter(y_thousand))  # 設定y軸為千分位
    ax[0].set_title("總用戶數量")  # 小標題
    ax[0].set_ylim(-500000,12000000)  # 設定y軸數字上限
    
    # 4G & 5G-用戶數量
    for [(key, value), plot_color] in zip(us3_1_dict.items(), plot_colors):
        ax[1].plot(value["日期"], value["4G用戶數小計"], "-",
                marker='o', linewidth=2, color=plot_color, label=f"{key}-4G")
    for [(key, value), plot_color] in zip(us3_1_dict.items(), plot_colors):
        ax[1].plot(value["日期"], value["5G用戶數小計"], ":",
                marker='o', linewidth=2, color=plot_color, label="-5G")
    ax[1].legend(fontsize=10, ncol=2)  # 圖例
    ax[1].grid(color="#f0efeb")  # 網格
    ax[1].yaxis.set_major_formatter(FuncFormatter(y_thousand))  # 設定y軸為千分位
    ax[1].set_title("4G & 5G-用戶數量")  # 小標題
    ax[1].set_ylim(-500000,12000000)  # 設定y軸數字上限
    ax[1].tick_params(axis='y', labelsize=0)
    
    min_y, max_y = str(min(us3['日期'])), str(max(us3['日期']))
    fig.suptitle(f"{min_y[:4]} ~ {max_y[:4]}年-用戶數量趨勢", fontsize=15, fontweight="bold", y=0.97)  # 大標題
    plt.tight_layout()  # 自動保持合適的間距
    plt.show()
    # plt.savefig(r".\PIC\us3.png", transparent=True) # 儲存圖片，背景透明
    
    
    # us4 2024年用戶數與基地台之比較---------------------
    fig, ax = plt.subplots(figsize=(8, 6))
    bar_color = ["#87b6d7", "#feb793", "#f4988f", "#c890b6", "#bddd98"]
    ax.bar(us4.index, us4["用戶數"], color=bar_color, label="用戶數", width=0.6)
    
    # 數字標籤
    for i in range(0, len(us4.index)):
        ax.text(i, us4.iloc[i]["用戶數"]*1.022, f'{us4.iloc[i]["用戶數"]:,}', ha='center')
        
    ax.set_ylim(0, 13000000)  # 設定y軸數字上限
    ax.yaxis.set_major_formatter(FuncFormatter(y_thousand))  # 設定y軸為千分位
    ax.text(-0.65, 13000000, "用戶數", rotation=0)
    
    ax2 = ax.twinx()  # 新增右邊的Y軸
    ax2.plot(us4.index, us4["基地臺"], "--", color="#696969", label="基地臺", marker='o')
    ax2.set_ylim(27000, 37000)  # 設定y軸數字上限
    ax2.yaxis.set_major_formatter(FuncFormatter(y_thousand))  # 設定y軸為千分位
    ax2.text(2.4, 37300, "基地臺", rotation=0)
    
    for i, v in zip(us4.index, us4["基地臺"]):  # 加數字標籤
        ax2.text(i, v*1.003, f"{v:,}", fontsize=9)
    
    # 增加標籤 (用戶數//基地臺)
    for i in range(0, len(us4.index)):
        t = ax.text(
            i, 3000000, f'{us4.iloc[i]["用戶數"] // us4.iloc[i]["基地臺"]:,}人 /\n基地台', ha='center')
        
        t.set_bbox(dict(facecolor="w", alpha=0.6, edgecolor="r", boxstyle="round"))
    
    fig.legend(loc="upper right", ncol=2, bbox_to_anchor=(0.9, 0.88))  # 圖例
    plt.title(f"{max(us['統計期'])}-用戶數與基地台之比較", fontsize=15, fontweight="bold", y=1.01)  # 標題
    plt.show()
    # plt.savefig(r".\PIC\us4.png", transparent=True) # 儲存圖片，背景透明
    
    
    # =============================================================================
    # -------------------df3圖表-------------------
    # =============================================================================
    
    # st1 2024年各區域-各家電信-門市數量---------------------
    fig, ax = plt.subplots(figsize=(8, 6))
    st_area = st1.pivot(index='業者名稱', columns='區域', values='門市')[
        ["北部", "中部", "東部", "南部", "離島"]]  # 轉換透視表、變更順序
    st_area.plot(kind='barh', stacked=True, ax=ax, color=area_colors, width=0.6)
    
    
    def add_st1_text():  # 加數字標籤
        for i in range(len(st_area.index)):
            ax.text(750, i, f"({st['門市'][i]})", va="center", ha="center")  # 總計
            x_offset = 0
            for j in st_area.columns:
                # 例如: st_area.loc["中華電信","北部"]
                x = st_area.loc[st_area.index[i], j]
                ax.text(x_offset + x/2, i, f"{j}-{x}", va="center", ha="center")
                x_offset += x
    
    
    add_st1_text()  # 加數字標籤
    
    ax.set_xlim(0, 780)  # 設定x軸數字上限
    ax.xaxis.set_major_formatter(FuncFormatter(y_thousand))  # 設定x軸千分位
    ax.set_ylabel("")  # 移除y軸index的文字
    ax.invert_yaxis()  # 設定y軸刻度反轉
    
    
    def set_st1_y():  # y軸字串改垂直
        li = []
        for i in st_area.index:
            text = "\n"
            for j in i:
                text += j+"\n"
            li.append(text)
        return li
    
    
    ax.set_yticklabels(set_st1_y())  # 設定y軸標籤內容
    
    ax.get_legend().remove()  # 移除圖例
    plt.title("2024年-各家電信-門市數量(總量+各區域)", fontsize=15, fontweight="bold", y=1.01)  # 標題
    plt.show()
    # plt.savefig(r".\PIC\st1.png", transparent=True) # 儲存圖片，背景透明
    
    
    # st2 門市數量與用戶數之比較---------------------
    fig, ax = plt.subplots(figsize=(8, 6))
    bar_color = ["#87b6d7", "#feb793", "#f4988f", "#c890b6", "#bddd98"]
    st2_bar = ax.bar(st2.index, st2["門市"],
                     color=bar_color, label="門市數量", width=0.6)
    ax.bar_label(st2_bar, padding=3)  # 加數字標籤
    ax.set_ylim(0, 800)  # 設定y軸數字上限
    ax.text(-0.65, 800*1.05, "門市數量", rotation=0)
    
    ax2 = ax.twinx()  # 新增右邊的Y軸
    ax2.plot(st2.index, st2["用戶數"], "--", color="#696969", label="用戶數", marker='o')
    ax2.text(2.4, 13000000*1.03, "用戶數", rotation=0)
    
    for i, v in zip(st2.index, st2["用戶數"]):  # 加數字標籤
        ax2.text(i, v*1.015, f"{v:,}", fontsize=9)
    
    ax2.yaxis.set_major_formatter(FuncFormatter(y_thousand))  # 設定x軸千分位
    ax2.set_ylim(5000000, 13000000)  # 設定y軸數字上限
    
    # 增加標籤 (用戶數//門市數量)
    for i in range(0, len(st2.index)):
        t = ax.text(
            i, 250, f'{st2.iloc[i]["用戶數"] // st2.iloc[i]["門市"]:,}人 /\n門市', ha='center')
        
        t.set_bbox(dict(facecolor="w", alpha=0.6, edgecolor="r", boxstyle="round"))
    
    fig.legend(loc="upper right", ncol=2, bbox_to_anchor=(0.85, 0.88))  # 圖例
    plt.title("2024年-門市數量與用戶數之比較", fontsize=15, fontweight="bold", y=1.01)  # 標題
    plt.subplots_adjust(right=0.88)  # 調整圖表位置
    plt.show()
    # plt.savefig(r".\PIC\st2.png", transparent=True) # 儲存圖片，背景透明


draw_charts() # 繪圖



