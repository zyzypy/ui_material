"""
重要维护：获取七牛list，加工存入本地数据库

目录维护：prefix_list

基本只新增，修改删除未写方法，手动去七牛和数据库修改
"""
import datetime
import pymysql
from config import DB_CONFIG, QINIU_CONFIG
from sevencow import Cow


# 返回可用于multiple rows的sql拼装值
def multipleRows(*params):
    ret = []
    # 根据不同值类型分别进行sql语法拼装
    for param in params:
        if isinstance(param, (int, float, bool)):
            ret.append(str(param))
        elif isinstance(param, (str,)):
            ret.append('"' + param + '"')
        else:
            print('unsupport value: %s ' % param)
    return '(' + ','.join(ret) + ')'


# 执行py文件时才执行下面代码
if __name__ == '__main__':

    print('七牛数据同步到本地数据库，开始')


    # 取七牛数据
    print('七牛bucket:' + QINIU_CONFIG['BUCKET_MATERIAL'])
    # #########注意维护prefix_list #########
    prefix_list = [
        'background',   #背景素材图片质量控制不好，暂不获取
        'button',
        'icon',
        'mobile_interface',
        'mobile_kit',
        'mockup',
        'office',
        'ppt',
        'logo',
        'vi',
        'website',

    ]
    print('连接到七牛')
    cow = Cow(access_key=QINIU_CONFIG['ACCESS_KEY'], secret_key=QINIU_CONFIG['SECRET_KEY'])
    b = cow.get_bucket(QINIU_CONFIG['BUCKET_MATERIAL'])  # BUCKET_DESIGN=‘flask’

    qiniu_items = []
    for prefix in prefix_list:
        # 根据前缀（一级目录）循环 取七牛bucket中所有数据，七牛 list（）每次最多取一千条数据 所以分前缀循环取。
        rs = b.list_files(prefix=prefix, limit=1000)
        prefix_items = rs['items']
        print('prefix-%s amount-%d' % (prefix, len(prefix_items)))
        qiniu_items.extend(prefix_items)
    print('七牛数据条目数 %d' % len(qiniu_items))


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
    material_items_hash = []
    for material_item in material_items:
        material_items_hash.append(material_item['hash'])



    # 比较新增数据，存本地前加工七牛数据
    connection = pymysql.connect(**DB_CONFIG)
    cursor = connection.cursor()
    batch_list = []
    # 比较 出七牛有但本地没有
    for qiniu_item in qiniu_items:
        if qiniu_item['hash'] not in material_items_hash:
            # 处理数据
            qiniu_key = qiniu_item['key']      # http域名+key才是访问路径
            main_img_flag = True if str(qiniu_item['key']).split('/')[-1].find('预览')!=-1 else False     # str.find()找不到会返回-1
            category = str(qiniu_item['key']).split('/')[0]       # key = button/一个按钮/1.psd
            folder = str(qiniu_item['key']).split('/')[1]
            title = str(qiniu_item['key']).split('/')[-1].split('.')[0]
            postfix = str(qiniu_item['key']).split('/')[-1].split('.')[-1]
            size = round(qiniu_item['fsize']/1024/1024, 2)
            views = 0
            downloads = 0
            hash = qiniu_item['hash']
            create_time = datetime.datetime.now().__str__()

            batch_list.append(multipleRows(qiniu_key, main_img_flag, category, folder, title, postfix, size, views, downloads, hash, create_time))
    print('比较出的新增数据条目数：' + str(len(batch_list)))
    print('比较出的新增数据&加工后：' + str(batch_list))
    # 批量插入 https://github.com/TsaiZehua/PyMySQL
    sql = 'insert into material (qiniu_key, main_img_flag, category, folder, title, postfix, size, views, downloads , hash, create_time ) VALUES %s' \
          % ','.join(batch_list)
    # print('\n\n' + sql)
    rs = cursor.execute(sql)
    connection.commit()
    connection.close()
    print('sql插入条目数' + str(rs))






# # 七牛中新增数据同步到本地数据库
# # 取本地数据
# print('get local data hash column')
# material_items_hash = []
# for item_hash in Material.objects.values('hash'):
#     material_items_hash.append(item_hash['hash'])
# print(material_items_hash)
#
# print('get qiniu data')
# cow = Cow(access_key=SEVEN_COW['ACCESS_KEY'], secret_key=SEVEN_COW['SECRET_KEY'])
# b = cow.get_bucket(SEVEN_COW['BUCKET_DESIGN'])  # BUCKET_DESIGN=‘flask’
# print('from bucket： %s' % SEVEN_COW['BUCKET_DESIGN'])
# # 注意维护prefix_list。素材都存在一个七牛bucket中，七牛bucket list方法一次最多1000条数据,所以根据prefix分次取。
# prefix_list = [
#     # 'background',
#     'button',
#     'icon',
#     'mobile_interface',
#     'mobile_kit',
#     'mockup',
#     'office',
#     'ppt',
#     'logo',
#     'website',
# ]
# # 取七牛原始数据
# qiniu_items = []
# items_to_insert = []
# for prefix in prefix_list:
#     # 根据一级目录循环 取七牛bucket中所有数据
#     rs = b.list_files(prefix=prefix, limit=1000)
#     prefix_items = rs['items']
#     print('prefix-%s amount-%d' % (prefix, len(prefix_items)))
#     qiniu_items.extend(prefix_items)
# print('七牛数据条目数 %d' % len(qiniu_items))
#
# print('比对hash')
# print('新增条目：')
# for qiniu_item in qiniu_items:
#         # 如果七牛有但本地没有
#         if qiniu_item['hash'] not in material_items_hash:
#             # 处理数据
#             url = 'http://' + SEVEN_COW['DOMAIN_FLASK_CDN'] + '/' + qiniu_item['key']      # 域名/key
#             main_img_flag = True if str(qiniu_item['key']).split('/')[-1].find('预览')!=-1 else False     # str.find()找不到会返回-1
#             category = str(qiniu_item['key']).split('/')[0]       # key = button/一个按钮/1.psd
#             folder = str(qiniu_item['key']).split('/')[1]
#             title = str(qiniu_item['key']).split('.')[0]
#             postfix = str(qiniu_item['key']).split('/')[-1].split('.')[-1]
#             size = round(qiniu_item['fsize']/1024/1024, 2)
#             # views = default
#             # downloads = default
#             hash = qiniu_item['hash']
#
#             material = Material(url=url, main_img_flag=main_img_flag, category=category, folder=folder, title=title,
#                                 postfix=postfix, size=size, hash=hash)
#             print(qiniu_item['key']+',')
#             items_to_insert.append(material)
#
#
# print('比对新增条目数：' + str(len(items_to_insert)) )
#
# # 处理好的数据插入到本地数据库
# rs = Material.objects.bulk_create(items_to_insert)
# print('插入完成。条目数：%d' % len(rs))



# 返回格式
# 七牛api list。 http://developer.qiniu.com/code/v6/api/kodo-api/rs/list.html
# {
#     "marker": "<marker string>",
#     "commonPrefixes": [
#         "xxx",
#         "yyy"
#     ],
#     "items": [
#         {
#             "key"：     "<key           string>",
#             "putTime":   <filePutTime   int64>,
#             "hash":     "<fileETag      string>",
#             "fsize":     <fileSize      int64>,
#             "mimeType": "<mimeType      string>",
#             "customer": "<endUserId     string>"
#         },
#         ...
#     ]
# }