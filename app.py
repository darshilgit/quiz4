from flask import Flask, render_template, request
import pyodbc as db
import redis
import pygal

app = Flask(__name__)
conn = db.connect("Driver={ODBC Driver 17 for SQL Server};Server=tcp:cloud3dbserver.database.windows.net,1433;Database=cloud3db;Uid=dbuser@cloud3dbserver;Pwd={Mypassword!};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
redis_connect_dict = {}
redis_connect_dict['host'] = 'cloud3redis.redis.cache.windows.net'
redis_connect_dict['port'] = 6380
redis_connect_dict['db'] = 0
redis_connect_dict['password'] = 'iMB7hsBunvCnYzZPekiBk+ZAX3TzDKzDplY+Pc8Y2+s='

r = redis.StrictRedis(redis_connect_dict['host'],
                      redis_connect_dict['port'],
                      redis_connect_dict['db'],
                      redis_connect_dict['password'],
                      ssl=True)

bar_chart = pygal.Bar(width=1000, height=500)
bar_chart.add('a', [1, 2,3,4,5,6,7,8,9])
bar_chart.add('b', [1, 3,7,8,9,12,10,1])
bar_chart.add('c', [1, 3,7,8,9,12,10,1])
bar_chart.add('d', [1, 2,3,4,5,6,7,8,9])

line = pygal.Bar(width=1000, height=500)
line.add('a', [1, 2,3,4,5,6,7,8,9])
line.add('b', [1, 3,7,8,9,12,10,1])

@app.route('/')
def hello_world():
    return render_template('common.html',)

@app.route('/question1', )
def question1():
    return render_template('question1.html')

@app.route('/question1_execute',  methods=['GET'])
def question1_execute():
    sql = "select * from counties"
    print(sql)
    cursor = conn.cursor()
    result = cursor.execute(sql).fetchall()
    return render_template('question1.html', result=result, chart=bar_chart.render_data_uri(), line =line.render_data_uri() )

if __name__ == '__main__':
    app.run()
