from flask import Flask, render_template, request, redirect, jsonify
import requests
import pymysql

app = Flask(__name__)

# app.config['KEY'] = '758b8aeba9ee4aecb775bc6d2a04d633'
app.config['KEY'] = '966410e2ecfb9c91340fb765bedfc8c2'


def git_adcode(name):
    conn1 = pymysql.connect(host="localhost", port=3306, user="root",
                            password="mysql", database="Utils_data",charset="utf8")


    #数据库操作：读取句子：
    cs = conn1.cursor()
    # sql = "select adcode from ChinaArea_data where name like '%s\%';"%name  #TypeError: not enough arguments for format string
    # #会被注入
    #拼接字符串  引号 %
    # name = "'"+name+"'"
    name = "'%"+name+"%'"  #某些地名会搜两个不同的adcode
    sql = "select adcode from ChinaArea_data where name like %s;" %name
    # sql = "select *from tb_aphorism where id=2;"
    cs.execute(sql)
    data = cs.fetchall()  # 是一个元组
    # data1 = cs.fetchone()
    cs.close()
    conn1.close()

    #返回句子
    return data[0][0] #某些地名会搜两个不同的adcode,取第一个



@app.route('/')
def index():
    return render_template('index.html')


'''
URL:https://restapi.amap.com/v3/weather/weatherInfo?parameters

请求方式GET
https://restapi.amap.com/v3/weather/weatherInfo?city=110101&key=<用户key>
'''
@app.route('/get_weather', methods=['POST'])
def get_weather():
    city = request.form.get('city')
    print('city:%s'%city)
    city_adcode =git_adcode(city)

    return redirect('/show_weather?' + '&city_adcode=' + city_adcode)

@app.route('/show_weather')
def show_weather():
    city_adcode = request.args.get('city_adcode')
    weather_url = 'https://restapi.amap.com/v3/weather/weatherInfo?city=' + city_adcode + '&key=' + app.config['KEY']
    # return jsonify(weather_url=weather_url)
    # return render_template('map_test02.html', weather_url=weather_url)
    response = requests.get(weather_url)
    json_data = response.json()
    return jsonify(weather_data=json_data)  #注意转码
'''
{"weather_data":{"count":"1","info":"OK","infocode":"10000","lives":[{"adcode":"440607","city":"\u4e09\u6c34\u533a",
"humidity":"83","province":"\u5e7f\u4e1c","reporttime":"2019-07-20 19:46:02","temperature":"27","weather":"\u9634",
"winddirection":"\u897f\u5357","windpower":"\u22643"}],"status":"1"}}
'''


@app.route('/get_form', methods=['POST'])
def get_data():
    province = request.form.get('province')
    city = request.form.get('city')
    area = request.form.get('area')
    detail = request.form.get('detail')
    return redirect('/show_map?'+'&province='+ province + '&city=' + city + '&area=' + area + '&detail=' + detail)

@app.route('/show_map')
def show_map():
    province = request.args.get('province')
    city = request.args.get('city')
    area = request.args.get('area')
    detail = request.args.get('detail')
    address = 'address=' + province + city + area + detail
    #获取城市编码
    url = 'https://restapi.amap.com/v3/geocode/geo?' + address + '&key=' + app.config['KEY']
    response = requests.get(url)
    json_data = response.json()
    location = json_data['geocodes'][0]['location']
    # print(location)
    map_url = 'https://restapi.amap.com/v3/staticmap?zoom=13&size=750*750&markers=mid,,A:' + location + '&location=' + location + '&key=' + app.config['KEY']

    return render_template('map_test02.html', map_url=map_url)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

