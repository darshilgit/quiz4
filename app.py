from flask import Flask, render_template, request
import pyodbc as db
import redis
import pygal

app = Flask(__name__)
conn = db.connect("Driver={ODBC Driver 17 for SQL Server};Server=tcp:cloud3dbserver.database.windows.net,1433;Database=cloud3db;Uid=dbuser@cloud3dbserver;Pwd={Mypassword!};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
# redis_connect_dict = {}
# redis_connect_dict['host'] = 'cloud3redis.redis.cache.windows.net'
# redis_connect_dict['port'] = 6380
# redis_connect_dict['db'] = 0
# redis_connect_dict['password'] = 'iMB7hsBunvCnYzZPekiBk+ZAX3TzDKzDplY+Pc8Y2+s='
#
# r = redis.StrictRedis(redis_connect_dict['host'],
#                       redis_connect_dict['port'],
#                       redis_connect_dict['db'],
#                       redis_connect_dict['password'],
#                       ssl=True)
#
# bar_chart = pygal.Bar(width=1000, height=500)
# bar_chart.add('a', [1, 2,3,4,5,6,7,8,9])
# bar_chart.add('b', [1, 3,7,8,9,12,10,1])
# bar_chart.add('c', [1, 3,7,8,9,12,10,1])
# bar_chart.add('d', [1, 2,3,4,5,6,7,8,9])

# line = pygal.Bar(width=1000, height=500)
# line.add('a', [1, 2,3,4,5,6,7,8,9])
# line.add('b', [1, 3,7,8,9,12,10,1])

@app.route('/')
def hello_world():
    return render_template('common.html',)

@app.route('/question1', )
def question1():
    return render_template('question1.html')

@app.route('/question1_execute',  methods=['GET'])
def question1_execute():
    bar_chart = pygal.Bar(width=1000, height=500)
    sql = "select * from population where State = 'Alabama' or State = 'Alaska' or State = 'California' or State = 'Florida'"
    print(sql)
    cursor = conn.cursor()
    result = cursor.execute(sql).fetchall()
    #population_values = []
    for r in result:
        state = r[0]
        population_values = []
        for year in range(1,len(r)):
            string_val = r[year]
            string_val = string_val.replace(",", "")
            int_val = int(string_val)
            population_values.append(int_val)
        bar_chart.add(state, population_values)
    return render_template('question1.html', chart=bar_chart.render_data_uri())


@app.route('/question2', )
def question2():
    return render_template('question2.html')

@app.route('/question2_execute',  methods=['GET'])
def question2_execute():
    cursor = conn.cursor()
    sql = "select * from population where State = 'Alabama' or State = 'Florida'"
    print(sql)
    result = cursor.execute(sql).fetchall()
    xy_chart = pygal.XY(stroke=False, height=300)
    xy_chart.title = 'Correlation'
    for r in result:
        db_years = [None, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]
        state = ""
        scatterplot_data = []
        for i in range(1, len(r)):
            state = r[0]
            print(r[0])
            population_val = r[i]
            print(r[i])
            population_val = population_val.replace(",", "")
            int_val = int(population_val)
            tuple = (db_years[i], int_val)
            scatterplot_data.append(tuple)
        xy_chart.add(state, scatterplot_data)
    xy_chart.render()
    return render_template('question2.html', chart=xy_chart.render_data_uri())
    #return render_template('question2.html', result=result, chart=bar_chart.render_data_uri(), line =line.render_data_uri() )

@app.route('/question3', )
def question3():
    return render_template('question3.html')


@app.route('/question3_execute',  methods=['GET'])
def question3_execute():
    pie_chart = pygal.Pie(height=300)
    pie_chart.title = 'Browser usage in February 2012 (in %)'
    pie_chart.add('IE', 19.5)
    pie_chart.add('Firefox', 36.6)
    pie_chart.add('Chrome', 36.3)
    pie_chart.add('Safari', 4.5)
    pie_chart.add('Opera', 2.3)
    pie_chart.render()
    return render_template('question3.html', chart=pie_chart.render_data_uri())


@app.route('/question4', )
def question4():
    return render_template('question4.html')
@app.route('/question4_execute',  methods=['GET'])
def question4_execute():
    cursor = conn.cursor()
    line_chart = pygal.Line()
    line_chart.title = 'BL (in %)'
    line_chart.x_labels = map(str, range(1970, 2015, 5))
    codes = ["IND","AFG"]
    for code in codes:
        sql = "select entity, BLPercent from educationshare where Code = " + "'" + code + "'"
        print(sql)
        result = cursor.execute(sql).fetchall()
        print(result)
        bp_values = []
        country = ""
        for r in result:
            country = r[0]
            bp_values.append(r[1])
        line_chart.add(country, bp_values)
    return render_template('question4.html', chart=line_chart.render_data_uri())


@app.route('/question7', )
def question7():
    return render_template('question7.html')

@app.route('/question7_execute',  methods=['GET'])
def question7_execute():
    bar_chart = pygal.Bar(width=1000, height=500)
    year = str(request.args.get('year'))
    year = 'y_'+year
    lrange1 = request.args.get('lrange1')
    hrange1 = request.args.get('hrange1')
    lrange2 = request.args.get('lrange2')
    hrange2 = request.args.get('hrange2')
    lrange3 = request.args.get('lrange3')
    hrange3 = request.args.get('hrange3')
    range = [lrange1 +'-' + hrange1, lrange2 +'-' + hrange2, lrange3 +'-' + hrange3]
    print(range)
    cursor = conn.cursor()
    sql = "select count(State) from population where " + year + " between " + "'" + lrange1 + "'" + " and " + "'" + hrange1 + "'"
    sql1 = "select count(State) from population where " + year + " between " + "'" + lrange2 + "'" + " and " + "'" + hrange2 + "'"
    sql2 = "select count(State) from population where " + year + " between " + "'" + lrange3 + "'" + " and " + "'" + hrange3 + "'"
    print(sql)
    result = cursor.execute(sql).fetchall()
    print(result)
    answers = []
    answers.append(result[0][0])
    result = cursor.execute(sql1).fetchall()
    answers.append(result[0][0])
    result = cursor.execute(sql2).fetchall()
    answers.append(result[0][0])
    bar_chart.add(range[0], answers[0])
    bar_chart.add(range[1], answers[1])
    bar_chart.add(range[2], answers[2])
    return render_template('question7.html', chart=bar_chart.render_data_uri())


if __name__ == '__main__':
    app.run()
