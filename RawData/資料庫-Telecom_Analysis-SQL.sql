/* 建立新的資料庫"telecom_analysis" */
CREATE DATABASE telecom_analysis; 

/* 建立新的資料表"base_station--df1" */
CREATE TABLE base_station(
telecom CHAR(10) NOT NULL,
city CHAR(10)NOT NULL,
city_area CHAR(10) NOT NULL,
bs_type CHAR(10),
bs_qty  INT NOT NULL,
data_date CHAR(10) NOT NULL,
data_time DATE NOT NULL);

/* 建立新的資料表"population--df1_1" */
CREATE TABLE population(
city CHAR(10) NOT NULL,
city_area CHAR(10) NOT NULL,
population INT not NULL);

/* 建立新的資料表"user_qty--df2" */
CREATE TABLE user_qty(
telecom CHAR(10) NOT NULL,
total_user INT NOT NULL,
total_4G INT NOT NULL,
monthly_4G INT,
prepaidcard_4G INT,
total_5G INT NOT NULL,
monthly_5G INT,
prepaidcard_5G INT,
data_date CHAR(10) NOT NULL,
data_time DATE NOT NULL); 

/* 建立新的資料表"store_qty--df3" */
CREATE TABLE store_qty(
telecom CHAR(10) NOT NULL,
city CHAR(10)NOT NULL,
city_area CHAR(10) NOT NULL,
store_name CHAR(30) NOT NULL,
store_addr CHAR(100) NOT NULL); 

