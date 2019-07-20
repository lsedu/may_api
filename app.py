from flask import Flask, render_template, request, redirect
import requests
app = Flask(__name__)

# app.config['KEY'] = '758b8aeba9ee4aecb775bc6d2a04d633'
app.config['KEY'] = '966410e2ecfb9c91340fb765bedfc8c2'

@app.route('/map')
def map():
    return render_template('map_test01.html')

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

    url = 'https://restapi.amap.com/v3/geocode/geo?' + address + '&key=' + app.config['KEY']
    response = requests.get(url)
    json_data = response.json()
    location = json_data['geocodes'][0]['location']
    # print(location)
    map_url = 'https://restapi.amap.com/v3/staticmap?zoom=15&size=750*500&markers=mid,,A:' + location + '&location=' + location + '&key=' + app.config['KEY']

    return render_template('map_test02.html', map_url=map_url)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

