# 2020-04
# 数据库初始化脚本。
# 素材已停止更新，素材已上传腾讯云对象存储，直接读取本地文件生成固定信息而不用请求对象存储的api了。
import os
import sqlite3

conn = sqlite3.connect('sqlite.db')
c = conn.cursor()

sql1 = """ DROP TABLE IF EXISTS material; """
c.execute(sql1)

# v1结构 mysql
# create table material (
#   id int not null auto_increment,
#   qiniu_key varchar(100) not null COMMENT '七牛key',        /buttons/一套按钮/xxx.jpg
#   main_img_flag BOOLEAN DEFAULT FALSE COMMENT '是否主图',     1
#   category VARCHAR(50) COMMENT '大分类',                     background
#   folder VARCHAR(50) COMMENT '文件夹名',                      背景 低多边形 几何 三角形 彩色
#   title VARCHAR(50) COMMENT '单文件名',                       1.jpg
#   postfix VARCHAR(10) COMMENT '文件后缀',                     jpg
#   size float UNSIGNED COMMENT '文件大小',                     30000（byte）
#   views INTEGER COMMENT '浏览数',
#   downloads INTEGER COMMENT '下载数',
#   hash VARCHAR(100) COMMENT '七牛文件hash值',
#   created_time datetime,
#
#   primary key (id)
# );

# v2 sqlite3
sql2 = """
CREATE TABLE material
(
    id            INTEGER
        PRIMARY KEY autoincrement,
    key           VARCHAR(100) NOT NULL,
    main_img_flag BOOLEAN DEFAULT FALSE,
    category      VARCHAR(50),
    folder        VARCHAR(50),
    title         VARCHAR(50),
    postfix       VARCHAR(10),
    size          FLOAT UNSIGNED DEFAULT 0.0,
    views         INTEGER DEFAULT 0,
    downloads     INTEGER DEFAULT 0,
    hash          VARCHAR(100) DEFAULT '',
    created_time  DATETIME DEFAULT (datetime())
);
"""
c.execute(sql2)
conn.commit()

batch_list = []
BUCKET_LOCAL_PATH = '/Volumes/TOSHIBA 3T/BUCKETS/ui'
for root, dirs, files in os.walk(BUCKET_LOCAL_PATH):
    # print(root, dirs, files)
    # /Volumes/TOSHIBA 3T/BUCKETS/ui ['background', 'button', 'icon', 'mobile_interface', 'mobile_kit', 'mockup', 'office', 'ppt', 'vi', 'website'] ['维护规则.txt']
    # /Volumes/TOSHIBA 3T/BUCKETS/ui/background ['背景 低多边形 几何 三角形 彩色', '背景 低多边形 几何 炫彩 长方形色卡', '背景 星空 梦幻 繁星 渐变', '背景 线型 图标平铺', '背景 黑色 白色 中式 花纹 纹理', '谷歌材料设计官方壁纸400多张 Material Design 壁纸 折纸 几何'] []
    # 筛选出来 /Volumes/TOSHIBA 3T/BUCKETS/ui/background/背景 低多边形 几何 三角形 彩色 [] ['1.jpg', '13.jpg', '15.jpg', '19.jpg', '21.jpg', '22.jpg', '23.jpg', '25.jpg', '3.jpg', '30.jpg', '41.jpg', '66.jpg', '67.jpg', '70.jpg', '【预览】.jpg', '背景 低多边形 几何 三角形 彩色.rar']
    if dirs:
        continue

    _, category, folder = root.replace(BUCKET_LOCAL_PATH, '').split('/')

    for f in files:
        title = f
        postfix = f.split('.')[-1]
        main_img_flag = True if f.startswith('【预览】') else False
        key = os.path.join('/', category, folder, title)
        size = os.path.getsize(os.path.join(root, title))

        batch_list.append(tuple((key, main_img_flag, category, folder, title, postfix, size)))


sql3 = """ INSERT INTO material 
        (key, main_img_flag, category, folder, title, postfix, size) 
        VALUES (?, ?, ?, ?, ?, ?, ?)"""
c.executemany(sql3, batch_list)

conn.commit()
conn.close()


