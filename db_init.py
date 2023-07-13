# 数据库初始化脚本。
import os
import sqlite3

# 仅做取数据路径，不做静态文件访问路径
BUCKET_LOCAL_PATH = '/Users/yangzheng/Downloads/ui_material'

connection = sqlite3.connect('sqlite.db')
cursor = connection.cursor()

sql = """DROP TABLE IF EXISTS material;"""
cursor.execute(sql)

# sqlite3
sql = """
CREATE TABLE IF NOT EXISTS material
(
    id            INTEGER
        PRIMARY KEY autoincrement,
    key           TEXT NOT NULL,    -- 文件相对存储桶路径
    main_img_flag BOOLEAN DEFAULT FALSE,
    category      TEXT NOT NULL,    -- 所属目录
    folder        TEXT NOT NULL,    -- 作品名
    title         TEXT NOT NULL,    -- 文件名     todo这几个字段命名得有些歧义
    postfix       TEXT,
    size          REAL UNSIGNED DEFAULT 0.0,
    views         INTEGER DEFAULT 0,
    downloads     INTEGER DEFAULT 0,
    hash          TEXT DEFAULT '',
    created_time  TEXT DEFAULT (datetime())
);
"""

# mysql
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

connection.execute(sql)
connection.commit()

batch_list = []
for root, dirs, files in os.walk(BUCKET_LOCAL_PATH):
    # os.walk()返回值结构 /<BUCKET_LOCAL_PATH> 、['文件夹1', '文件夹2', 'icon','website']、 ['单个文件1']，然后递归进入更深层目录。
    # 递归到最内层时返回 /<BUCKET_LOCAL_PATH>/background/漂亮作品、['【预览】1.jpg', '']
    # 按'/'划分得到分类文件夹、标题、后缀
    # print(root, dirs, files)
    if dirs:
        continue

    _, category, folder = root.replace(BUCKET_LOCAL_PATH, '').split('/')

    for f in files:
        title = f
        postfix = f.split('.')[-1]
        main_img_flag = True if f.startswith('【预览】') else False
        # 访问路径, app.py中会跟基础路径拼接，根据本地还是远程考虑key开头是否有‘/’，os.path.join不能正确处理http url。
        key = os.path.join(category, folder, title)
        size = os.path.getsize(os.path.join(root, title))

        batch_list.append(tuple((key, main_img_flag, category, folder, title, postfix, size)))


sql3 = """ INSERT INTO material
        (key, main_img_flag, category, folder, title, postfix, size)
        VALUES (?, ?, ?, ?, ?, ?, ?)"""
cursor.executemany(sql3, batch_list)

connection.commit()
connection.close()


