# =========== 素材库 ================
from flask import Blueprint, redirect, render_template, request, g, url_for, flash,abort
import pymysql
from database import multi_params
from config import DB_CONFIG, QINIU_CONFIG
from material.subtitle import subtitles
from random import randint
from math import ceil


# #### BLUEPRINT ######
# folder路径是跟在蓝图名文件夹后的，比如template_folder='templates'会在material/templates下寻找。不存在则用项目根目录下的static和templates文件夹。
material = Blueprint('material', __name__, static_folder='static', template_folder='templates', url_prefix='/material')


# ==== rout
@material.route('/masonry', defaults={'category': 'mobile_interface', 'current_page_number': 1, 'page_size': 20})
@material.route('/masonry/<category>', defaults={'current_page_number': 1, 'page_size': 20})
@material.route('/masonry/<category>/<int:current_page_number>', defaults={'page_size': 20})
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
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            # 素材表 过滤条件：素材为主图。
            sql_params = multi_params(category, True, pagination['sql_limit_start'], pagination['page_size'])
            sql = "select * from ( select * from material where category=%s and main_img_flag=%s order by downloads desc,views desc ) as t  limit %s,%s;" % sql_params   # limit 0,10 限制10条数据 占位符后必须跟元组
            # print(sql)
            cursor.execute(sql)
            material_list = cursor.fetchall()   # [{col,col,col},{col,col,col}]
            # print(material_dict)

            # 分页查询总页数
            sql_params2 = multi_params(category, True)
            sql2 = "select count(id) from material where category =%s and main_img_flag=%s;" % sql_params2
            # print(sql2)
            cursor.execute(sql2)
            material_list_amount = cursor.fetchall()[0]['count(id)']     # [{'count(id)': 938}]
            if len(material_list) == 0:
                flash('查询结果空')
            else:
                pagination['page_amount'] = ceil(material_list_amount/page_size)    # ceil(4.0)=4   ceil(4.5)=5  int(amount/size)+1整除时会导致多一页
                # print('page_amount' + str(pagination['page_amount']))
    except Exception as sql_error:
        print('sql_error ' + str(sql_error))
        return '模块material.masonry 内部错误，请联系管理员'
    finally:
        connection.close()

    # ===== 注意配置测试或加速域名 =======
    # url加工，这部分经常变化所以从数据库取出后再处理，详见七牛api图片处理  缩放到指定宽度'?imageMogr2/thumbnail/400x'  等比例缩至30%'?imageMogr2/thumbnail/!30p'
    for material in material_list:
            material['url'] = 'http://' + QINIU_CONFIG['DOMAIN_FLASK_CDN'] + '/' + material['qiniu_key'] + '?imageMogr2/thumbnail/400x'
    subtitle = subtitles[randint(0, len(subtitles)-1)]
    return render_template('masonry.html', material_list=material_list, subtitle=subtitle, pagination=pagination)
    # return render_template('beian_masonry.html', material_list=material_list, subtitle=subtitle, pagination=pagination)     # 备案假页面

@material.route('/detail/<folder>')
def detail(folder):
    """
    素材详情页，由masonry预览页进入。 浏览量+1.
    :param folder:作品目录
    :return:作品目录下的所有文件 包含预览图和源文件
    """
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            # 取一个作品目录下的数据
            sql_params = multi_params(folder)
            sql = 'select * from material where folder=%s' % sql_params
            cursor.execute(sql)
            material_list = cursor.fetchall()

            # 浏览量views加1    写入是主图的那条记录
            sql_params2 = multi_params(1, folder, True)
            sql2 = 'update material set views=views+%s where folder=%s and main_img_flag=%s' % sql_params2
            cursor.execute(sql2)
            connection.commit()
    except Exception as sql_error:
        print('sql_error ' + str(sql_error))
        return '模块material.detail 内部错误，请联系管理员'
    finally:
        connection.close()

    # 拼url，不进行图像缩放，判断资源是源文件还是图片。
    views = 0
    downloads = 0
    if len(material_list) == 0:     # 爬虫有时请求 /detail/index.html 或url错误导致没有查询结果
        abort(404)
    else:
        for material in material_list:      # 拼接url，区分预览图和源文件
            material['url'] = 'http://' + QINIU_CONFIG['DOMAIN_FLASK_CDN'] + '/' + material['qiniu_key']
            if material['postfix'] in ('psd', 'ai', 'eps', 'rar', 'zip', 'ppt', 'pptx', 'psb', 'sketch'):
                material['flag'] = 'source_file'
                downloads = material['downloads'] if material['downloads'] >= downloads else downloads  # 几个源文件可能下载次数不同，取最多次的
            elif material['postfix'] in ('jpg', 'jpeg', 'png', 'gif'):
                material['flag'] = 'preview_img'
                if material['main_img_flag']:
                    views = material['views']

        return render_template('detail.html', material_list=material_list, downloads=downloads, views=views)


@material.route('/detail/<folder>/<pager>')
def detail_pager(folder, pager):
    """ 作品详细页上的翻页，转到上一个或下一个作品详细
    :param folder:
    :param pager:
    :return: folder ，重定向到 detail()
    """
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            sql = 'select DISTINCT %s from material' % 'folder'
            cursor.execute(sql)
            folder_results = cursor.fetchall()     # [{'folder':'按钮 50个 酷黑'}，{ }，{ }]
    except Exception as sql_error:
        print('sql_error ' + str(sql_error))
        return '模块material.detail_pager 内部错误，请联系管理员'
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

    return redirect(url_for('material.detail', folder=folder))


@material.route('/download_single/<id>')
def download_single(id):
    """
    点下载按钮，重定向到下载链接。
    下载量加1。
    判断用户下载权限
    :param folder:
    :param url:
    :return:
    """
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            # 取一个作品下一个文件的url
            sql_params = multi_params(id)
            sql = 'select qiniu_key from material where id=%s' % sql_params
            cursor.execute(sql)
            qiniu_key = cursor.fetchone()      # {'col':'value'}
            # 一个作品下一个文件的下载量加1
            sql2 = 'update material set downloads=downloads+1 where id=%s' % sql_params
            cursor.execute(sql2)
            connection.commit()
    except Exception as sql_error:
        print('sql_error ' + str(sql_error))
        return '模块material.download_single 内部错误，请联系管理员'
    finally:
        connection.close()

    url = 'http://' + QINIU_CONFIG['DOMAIN_FLASK_CDN'] + '/' + qiniu_key['qiniu_key']
    return redirect(url)



@material.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('material.masonry'))