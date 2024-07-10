import pymysql


# 檢查資料庫及資料表
def check_database():
    try:
        print("檢查資料庫及資料表...")
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="12345678",
            port=3306)
        conn.autocommit(True)  # 自動commit()
        cursor = conn.cursor()  # 使用cursor()方法操作資料庫

        # 檢查資料庫是否存在，若不存在則建立
        cursor.execute("SHOW DATABASES LIKE 'telecom_analysis'")
        result = cursor.fetchone()
        if not result:
            cursor.execute("CREATE DATABASE telecom_analysis")
            print("資料庫 telecom_analysis 建立完成")
        else:
            print("資料庫 telecom_analysis...OK")

        # 使用 telecom_analysis 資料庫
        conn.select_db('telecom_analysis')

        # 檢查資料表 base_station 是否存在，若不存在則建立
        cursor.execute("SHOW TABLES LIKE 'base_station'")
        result = cursor.fetchone()
        if not result:
            cursor.execute("""  CREATE TABLE base_station(
                    telecom CHAR(10) NOT NULL,
                    city CHAR(10) NOT NULL,
                    city_area CHAR(10) NOT NULL,
                    bs_type CHAR(10),
                    bs_qty INT NOT NULL,
                    data_date CHAR(10) NOT NULL,
                    data_time DATE NOT NULL)  """)
            print("資料表 base_station 建立完成")
        else:
            print("資料表 base_station...OK")

        # 檢查資料表 population 是否存在，若不存在則建立
        cursor.execute("SHOW TABLES LIKE 'population'")
        result = cursor.fetchone()
        if not result:
            cursor.execute("""  CREATE TABLE population(
                    city CHAR(10) NOT NULL,
                    city_area CHAR(10) NOT NULL,
                    population INT NOT NULL)  """)
            print("資料表 population 建立完成")
        else:
            print("資料表 population...OK")

        # 檢查資料表 user_qty 是否存在，若不存在則創建
        cursor.execute("SHOW TABLES LIKE 'user_qty'")
        result = cursor.fetchone()
        if not result:
            cursor.execute("""  CREATE TABLE user_qty(
                    telecom CHAR(10) NOT NULL,
                    total_user INT NOT NULL,
                    total_4G INT NOT NULL,
                    monthly_4G INT,
                    prepaidcard_4G INT,
                    total_5G INT NOT NULL,
                    monthly_5G INT,
                    prepaidcard_5G INT,
                    data_date CHAR(10) NOT NULL,
                    data_time DATE NOT NULL )  """)
            print("資料表 user_qty 建立完成")
        else:
            print("資料表 user_qty...OK")

        # 檢查資料表 store_qty 是否存在，若不存在則創建
        cursor.execute("SHOW TABLES LIKE 'store_qty'")
        result = cursor.fetchone()
        if not result:
            cursor.execute("""  CREATE TABLE store_qty(
                    telecom CHAR(10) NOT NULL,
                    city CHAR(10) NOT NULL,
                    city_area CHAR(10) NOT NULL,
                    store_name CHAR(30) NOT NULL,
                    store_addr CHAR(100) NOT NULL )  """)
            print("資料表 store_qty 建立成功")
        else:
            print("資料表 store_qty...OK")

    except Exception as e:
        print("資料庫連接或操作失敗：", e)

    finally:
        cursor.close()
        conn.close()
        # print("資料庫連線結束")


# 資料寫入資料庫(df1、df1_1、df2、df3)
def data_sql(df1, df1_1, df2, df3):
    check_database()  # 先檢查資料庫及資料表是否存在
    print("\n開始寫入資料...")

    try:  # 開啟資料庫連接
        conn = pymysql.connect(host="localhost",     # 主機名稱
                               user="root",         # 帳號
                               password="12345678",  # 密碼
                               database="telecom_analysis",  # 資料庫
                               port=3306)           # port
        conn.autocommit(True)  # 自動commit()
        cursor = conn.cursor()  # 使用cursor()方法操作資料庫

    # 將資料df1寫到資料庫中
        try:
            # 刪除base_station表中所有資料
            cursor.execute("DELETE FROM base_station")
            print("base_station...資料清空完成")

            col_len = "%s, " * (len(df1.columns)-1) + "%s"
            for i in range(len(df1)):
                sql = f"INSERT INTO base_station VALUES ({col_len})"
                var = (df1.iloc[i, 0], df1.iloc[i, 1], df1.iloc[i, 2],
                       df1.iloc[i, 3], df1.iloc[i, 4], df1.iloc[i, 5], df1.iloc[i, 6].strftime('%Y-%m-%d %H:%M:%S'))
                cursor.execute(sql, var)

            print("df1...資料寫入完成")
        except Exception as e:
            print("df1...資料寫入錯誤訊息：", e)

    # 將資料df1_1寫到資料庫中
        try:
            # 刪除population表中所有資料
            cursor.execute("DELETE FROM population")
            print("population...資料清空完成")

            col_len = "%s, " * (len(df1_1.columns)-1) + "%s"
            for i in range(len(df1_1)):
                sql = f"INSERT INTO population VALUES ({col_len})"
                var = (df1_1.iloc[i, 0], df1_1.iloc[i, 1], df1_1.iloc[i, 2])
                cursor.execute(sql, var)

            print("df1_1...資料寫入完成")
        except Exception as e:
            print("df1_1...資料寫入錯誤訊息：", e)

    # 將資料df2寫到資料庫中
        try:
            # 刪除user_qty表中所有資料
            cursor.execute("DELETE FROM user_qty")
            print("user_qty...資料清空完成")

            col_len = "%s, " * (len(df2.columns)-1) + "%s"
            for i in range(len(df2)):
                sql = f"INSERT INTO user_qty VALUES ({col_len})"
                var = (df2.iloc[i, 0], df2.iloc[i, 1], df2.iloc[i, 2], df2.iloc[i, 3], df2.iloc[i, 4], df2.iloc[i, 5],
                       df2.iloc[i, 6], df2.iloc[i, 7], df2.iloc[i, 8], df2.iloc[i, 9].strftime('%Y-%m-%d %H:%M:%S'))
                cursor.execute(sql, var)

            print("df2...資料寫入完成")
        except Exception as e:
            print("df2...資料寫入錯誤訊息：", e)

    # 將資料df3寫到資料庫中
        try:
            # 刪除store_qty表中所有資料
            cursor.execute("DELETE FROM store_qty")
            print("store_qty...資料清空完成")

            col_len = "%s, " * (len(df3.columns)-1) + "%s"
            for i in range(len(df3)):
                sql = f"INSERT INTO store_qty VALUES ({col_len})"
                var = (df3.iloc[i, 0], df3.iloc[i, 1], df3.iloc[i, 2], df3.iloc[i, 3], df3.iloc[i, 4])
                cursor.execute(sql, var)

            print("df3...資料寫入完成")
        except Exception as e:
            print("df3...資料寫入錯誤訊息：", e)

    except Exception as e:
        print("資料庫連接失敗：", e)

    finally:
        cursor.close()
        conn.close()
        print("\n資料庫連線結束...")
