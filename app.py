from flask import *
import redis   # 导入redis 模块
import json
import time
import sys,os
r = redis.Redis(host='localhost', port=6379, decode_responses=True)  

app = Flask(__name__)

class ReverseProxied(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        scheme = environ.get('HTTP_X_FORWARDED_PROTO')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)

app.wsgi_app = ReverseProxied(app.wsgi_app)
app.secret_key = 'dev'


name = 'Grey Li'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':  # 判断是否是 POST 请求
		# 获取表单数据
		title = request.form.get('title')  # 传入表单对应输入字段的 name 值
		year = request.form.get('year')
		# 验证数据
		if not title or not year or len(year) > 4 or len(title) > 60:
			flash('Invalid input.')  # 显示错误提示
			return redirect(url_for('index'))  # 重定向回主页
		# 保存表单数据到数据库
		movies.append({'title':title, 'year':year})  # 创建记录
		flash('Item Created.')
		#return redirect(url_for('index'))  # 重定向回主页

	return render_template('index.html', name=name, movies=movies)
	
	
@app.route('/model/<id>')
def show_model(id):
	js = r.get('P'+id)  # 取出键 id 对应的值
	j = json.loads(js)
	return render_template('model.html', pics=j['pic'], title=j['title'])

@app.route('/mm/')
def show_mm():
	shows = []
	for i in range(20):
		js = r.get(r.randomkey())  
		j = json.loads(js)
		shows.append(j)
	return render_template('mm.html', albums=shows)
	
	
	
	
@app.route('/user/<name>')
def user_page(name):
    return url_for("index") + '<br> User: %s' % escape(name)
	
	
@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    #user = User.query.first()
    return render_template('404.html', user='jay'), 404  # 返回模板和状态码
