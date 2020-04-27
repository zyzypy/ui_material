from flask import Flask, redirect, url_for, render_template
from config import FLASK_CONFIG

# flask实例
app = Flask(__name__)
app.config.from_mapping(FLASK_CONFIG)

def register_blueprints():
    """ 插接蓝图模块 """
    from material.view import material
    app.register_blueprint(material)

register_blueprints()


@app.route('/')
@app.route('/index')
def index():
    # module.view
    return redirect(url_for('material.masonry'))

# deploye
from werkzeug.contrib.fixers import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)


# 生产环境关闭debug
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
