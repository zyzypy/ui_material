# =========== flask =============
FLASK_CONFIG = {
    'SECRET_KEY': 'flask_secret_key'     # flask中 session cookie等必须
}



# ############ mysql database ###########
import  pymysql.cursors
DB_CONFIG = {
      'host': '127.0.0.1',
      'port': 3306,
      'user': 'root',
      'password': '56canaan',
      'db': 'ui',
      'charset': 'utf8mb4',
      'cursorclass': pymysql.cursors.DictCursor
}


# ============== 七牛 ==============
QINIU_CONFIG = {
    'ACCESS_KEY': 'HImCU5E1C4eWG_mf8fTlDZ6YJPCdb8lYKqczjUq5',
    'SECRET_KEY': 'N3YZ7ZaTmU19Oscanaansss63bXiTI8Uyyf6hsJ1',
    'DOMAIN_FLASK_CDN': 'qiniu.1owo.com',
    'BUCKET_MATERIAL': 'flask',
    'DOMAIN_TEST_FLASK': 'o83ozpt7u.bkt.clouddn.com',
    'BUCKET_BLOG': '',
    'BUCKET_TEST': 'test',
}
