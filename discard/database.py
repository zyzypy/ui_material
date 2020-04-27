# 驱动 pymysql 支持py3，用法跟mysqldb一致
import pymysql.cursors


# insert update 拼sql给参数加括号和双引号
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


# select 占位符后接多参数用
def multi_params(*params):
    ret = []
    # 根据不同值类型分别进行sql语法拼装，拼sql给字符串加双引号
    for param in params:
        if isinstance(param, (int, float, bool)):
            ret.append(str(param))  # '1'通过占位符并入到str类型的sql语句中就没单引号了
        elif isinstance(param, (str,)):
            ret.append('"' + param + '"')
        else:
            print('unsupport value: %s ' % param)
    return tuple(ret)        # （True, '"str"', 0 ）

#
# # config
# config = {
#           'host': '127.0.0.1',
#           'port': 3306,
#           'user': 'root',
#           'password': '56tyghbn',
#           'db': 'ui',
#           'charset': 'utf8mb4',
#           'cursorclass': pymysql.cursors.DictCursor,
#           }
#
#
# # 创建连接
# connection = pymysql.connect(**config)
#
#
#
# # 执行sql语句
# try:
#     with connection.cursor() as cursor:
#         # 执行sql语句，插入记录
#         sql = "insert into test (`name`, `email`) values (%s, %s)"
#         cursor.execute(sql, ('Tom', 'tom@qq.com'))
#         rs = cursor.fetchall()
#         print(rs)
#     # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
#     connection.commit()
#
# finally:
#     connection.close()