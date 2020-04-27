from config import  DB_CONFIG
import  pymysql
# 取本地数据库
material_items = []
connection = pymysql.connect(**DB_CONFIG)
try:
    with connection.cursor() as cursor:
        sql = "select %s,%s,%s from material" % ('id', 'title', 'hash')
        cursor.execute(sql)
        material_items = cursor.fetchall()      # [{'id': 1, 'hash': 'wer24234', 'title': 'r'}, {'id': 2, 'hash': '32wersdf', 'title': 'r'}]
        # print(material_items)
        # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
        # connection.commit()
finally:
    connection.close()
# 本地结果集的hash列， 后面用来比较
print('本地已有条目数' + str(len(material_items)))
print(material_items[1800])
