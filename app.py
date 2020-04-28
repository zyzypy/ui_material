import os
import sqlite3
from random import randint
from math import ceil
from flask import Flask, redirect, url_for, render_template, flash, abort

from subtitle import subtitles

# 配置
CONFIG = {
    'SECRET_KEY': 'canaanyz',
    'DOMAIN_FLASK_CDN': 'https://ui.cdn.1owo.com',
    'DB_PATH': os.path.join(os.path.dirname(__file__), 'sqlite.db'),
    'UI_SOURCE_FILE_POSTFIX_LIST': ('psd', 'ai', 'eps', 'rar', 'zip', 'ppt', 'pptx', 'psb', 'sketch'),
    'UI_SOURCE_PREVIEW_POSTFIX_LIST': ('jpg', 'jpeg', 'png', 'gif')
}


# flask实例
app = Flask(__name__)
app.config.from_mapping(CONFIG)




# sqlite行工厂函数，cursor.fetchall()返回数据行为字典
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', defaults={'category': 'mobile_interface', 'current_page_number': 1, 'page_size': 20})
@app.route('/index', defaults={'category': 'mobile_interface', 'current_page_number': 1, 'page_size': 20})
@app.route('/index/<category>', defaults={'current_page_number': 1, 'page_size': 20})
@app.route('/index/<category>/<int:current_page_number>', defaults={'page_size': 20})
def masonry(category, current_page_number, page_size):
    """瀑布流masonry预览页面
    :param category:大分类 默认值维护在上面route中
    :param current_page_number:分页 页码
    :param page_size:分页 每页条目数
    :return:material_dict
    """
    # 处理分页参数  第一页limit 0,20 取到的为第1到第20组，第二页 limit 20,20
    pagination = dict()
    pagination['page_size'] = page_size
    pagination['current_page_number'] = current_page_number
    pagination['sql_limit_start'] = (current_page_number-1) * page_size
    # 连接数据库
    connection = sqlite3.connect(app.config['DB_PATH'])     # 必须绝对路径
    connection.row_factory = dict_factory
    try:
        cursor = connection.cursor()
        # 分页 limit 0,10 从第一行开始往后取10行
        # 素材material表，过滤条件 素材为主图。
        sql_params = tuple((category, True, pagination['sql_limit_start'], pagination['page_size']))
        sql = """ select * from
                 (select * from material where category=? and main_img_flag=? order by downloads desc,views desc )
                as t  limit ?, ?;
              """
        cursor.execute(sql, sql_params)
        material_list = cursor.fetchall()   # [{col,col,col},{col,col,col}]
        if not material_list:
            raise Exception('结果集material_list空')

        # 分页 查询总页数
        sql_params2 = tuple((category, True))
        sql2 = """select count(id) from material 
                  where category=? and main_img_flag=?;
               """
        cursor.execute(sql2, sql_params2)
        material_amount = cursor.fetchone()['count(id)']
        pagination['page_amount'] = ceil(material_amount/page_size)    # ceil(4.0)=4   ceil(4.5)=5  int(amount/size)+1整除时会导致多一页
    except Exception as sql_error:
        print('sql_error ' + str(sql_error))
        return 'masonry视图sql错误，请联系管理员'
    finally:
        connection.close()

    # ===== 注意配置测试或cdn域名 =======
    # url加工，这部分经常变化所以从数据库取出后再处理。上线后cdn有refer验证本地会404，请替换成你自己的路径。
    for material in material_list:
            material['url'] = app.config['DOMAIN_FLASK_CDN'] + material['key']
    subtitle = subtitles[randint(0, len(subtitles)-1)]
    return render_template('masonry.html', material_list=material_list, subtitle=subtitle, pagination=pagination)


@app.route('/detail/<folder>')
def detail(folder):
    """
    素材详情页，由masonry预览页进入。 浏览量+1.
    :param folder:作品目录
    :return:作品目录下的所有文件 包含预览图和源文件
    """
    connection = sqlite3.connect(app.config['DB_PATH'])
    connection.row_factory = dict_factory
    try:
        cursor = connection.cursor()
        # 取一个作品目录下的数据
        sql_params = tuple((folder,))
        sql = """select * from material where folder=?"""
        cursor.execute(sql, sql_params)
        # 命名有歧义，首页中material代表一个作品集，这里代表作品集下的一个源文件或预览图。为减少修改没有动。
        material_list = cursor.fetchall()

        if len(material_list) == 0:  # 爬虫有时请求 /detail/index.html 或url错误导致没有查询结果
            abort(404)

        # 浏览量views加1    写入是主图的那条记录
        sql_params2 = tuple((1, folder, True))
        sql2 = """update material set views=views+? where folder=? and main_img_flag=?"""
        cursor.execute(sql2, sql_params2)
        connection.commit()
    except Exception as sql_error:
        print('sql_error ' + str(sql_error))
        return 'detail() 内部错误，请联系管理员'
    finally:
        connection.close()

    # 拼url，不进行图像缩放，判断资源是源文件还是图片。
    views = 0
    downloads = 0

    for material in material_list:      # 拼接url，区分预览图和源文件
        material['url'] = app.config['DOMAIN_FLASK_CDN'] + material['key']
        material['size'] = round(material['size']/1024/1024, 2)
        # 源文件后缀
        if material['postfix'] in app.config['UI_SOURCE_FILE_POSTFIX_LIST']:
            material['flag'] = 'source_file'
            downloads = material['downloads'] if material['downloads'] >= downloads else downloads  # 几个源文件可能下载次数不同，取最多次的
        elif material['postfix'] in app.config['UI_SOURCE_PREVIEW_POSTFIX_LIST']:
            material['flag'] = 'preview_img'
            if material['main_img_flag']:
                views = material['views']

    return render_template('detail.html', material_list=material_list, downloads=downloads, views=views)


@app.route('/detail/<folder>/<pager>')
def detail_pager(folder, pager):
    """ 作品详细页上的翻页，转到上一个或下一个作品详细
    :param folder:
    :param pager:
    :return: folder ，重定向到 detail()
    """
    connection = sqlite3.connect(app.config['DB_PATH'])
    connection.row_factory = dict_factory
    cursor = connection.cursor()
    # 查所有作品集然后取上一个或下一个作品名，再携带参数重定向到detail作品详情页
    try:
        sql = """select DISTINCT folder from material"""
        cursor.execute(sql)
        folder_results = cursor.fetchall()     # [{'folder':'按钮 50个 酷黑'}，{ }，{ }]
    except Exception as sql_error:
        print('sql_error ' + str(sql_error))
        return '视图detail_pager 内部错误，请联系管理员'
    finally:
        connection.close()

    folder_list = []
    for folder_result in folder_results:
        folder_list.append(folder_result['folder'])
    # print(folder_list)        # ['按钮 50个 酷黑','xxx','xxx']

    if pager == 'previous':
        try:
            folder = folder_list[folder_list.index(folder) - 1]
        except IndexError:
            folder = folder_list[-1]
    elif pager == 'next':
        try:
            folder = folder_list[folder_list.index(folder) + 1]
        except IndexError:
            folder = folder_list[0]
    else:
        abort(404)
    # print(folder)

    return redirect(url_for('detail', folder=folder))


@app.route('/download_single/<id>')
def download_single(id):
    """
    点下载按钮，重定向到下载链接。
    下载量加1。
    判断用户下载权限
    :param folder:
    :param url:
    :return:
    """
    connection = sqlite3.connect(app.config['DB_PATH'])
    connection.row_factory = dict_factory
    cursor = connection.cursor()
    try:
        # 取一个作品下一个文件的url
        sql_params = tuple((id,))
        sql = """select key from material where id=?"""
        cursor.execute(sql, sql_params)
        key = cursor.fetchone()      # {'col':'value'}
        # 一个作品下一个文件的下载量加1
        sql2 = 'update material set downloads=downloads+1 where id=?'
        cursor.execute(sql2, sql_params)
        connection.commit()
    except Exception as sql_error:
        print('sql_error ' + str(sql_error))
        return '视图download_single 内部错误，请联系管理员'
    finally:
        connection.close()

    url = app.config['DOMAIN_FLASK_CDN'] + key['key']
    return redirect(url)



@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('masonry'))


# deploye
# from werkzeug.contrib.fixers import ProxyFix
# app.wsgi_app = ProxyFix(app.wsgi_app)


# 生产环境关闭debug
if __name__ == '__main__':
    # export FLASK_DEBUG = True
    app.run(host='0.0.0.0', port=8000)
