# flask w/ model ML
from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np

app = Flask(__name__)

with open('models/roughness.pkl', 'rb') as f:
    model_roughness = pickle.load(f)
with open('models/fwhm.pkl', 'rb') as f:
    model_fwhm = pickle.load(f)
with open('models/Twinning.pkl', 'rb') as f:
    model_twinning = pickle.load(f)
with open('models/FE Intensity.pkl', 'rb') as f:
    model_fe_intensity = pickle.load(f)
with open('models/Thickness.pkl', 'rb') as f:
    model_thickness = pickle.load(f)

def get_prediction(lt_layer,as2_pressure,GT,AT,annealing_time,intended_thickness):
    x = np.array([lt_layer,as2_pressure,GT,AT,annealing_time,intended_thickness]).reshape(1,-1)
    roughness = model_roughness.predict(x)
    fwhm = model_fwhm.predict(x)
    twinning = model_twinning.predict(x)
    fe_intensity = model_fe_intensity.predict(x)
    thickness = model_thickness.predict(x)
    
    return dict(Roughness = roughness, Fwhm = fwhm, Twinning = twinning, Fe_intensity = fe_intensity, Thickness = thickness)

@app.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == 'POST':
        body = request.form
        
        layer_type = body['data1']
        intended_thickness = float(body['data2'])
        lt_thickness = float(body['data3'])
        as2_pressure = float(body['data4'])
        at= float(body['data5'])
        gt = float(body['data6'])
        annealing_time = float(body['data7'])
        # model prediction
        result = get_prediction(lt_thickness,as2_pressure,gt,at,annealing_time,intended_thickness)
        return render_template('home.html', result=result)
        # return render_template('result.html', body=body)
    return render_template('home.html')

@app.route('/predict', methods = ['GET', 'POST'])
def predict():
    if request.method == 'POST':
        body = request.json

        layer_type = body['data1']
        intended_thickness = body['data2']
        lt_thickness = body['data3']
        as2_pressure = body['data4']
        at= body['data5']
        gt = body['data6']
        annealing_time = body['data7']
     

        return jsonify({
            'hello'
        })
    elif request.method == 'GET':
        return jsonify({
            'status': 'Anda nge-GET'
        })
    else:
        return jsonify({
            'status': 'Anda tidak nge-POST & nge-GET'
        })

# @app.route('/predictform', methods = ['POST', 'GET'])
# def predictform():
    # if request.method == 'POST':
    #     body = request.form
        
    #     layer_type = body['data1']
    #     intended_thickness = float(body['data2'])
    #     lt_thickness = float(body['data3'])
    #     as2_pressure = float(body['data4'])
    #     at= float(body['data5'])
    #     gt = float(body['data6'])
    #     annealing_time = float(body['data7'])
    #     # model prediction
    #     result = get_prediction(lt_thickness,as2_pressure,gt,at,annealing_time,intended_thickness)
    #     return render_template('home.html', prediction_text='Predicted value of Roughness {}'.format(result['roughness']))
    #     # return render_template('result.html', body=body)


if __name__ == '__main__':
    app.run(host="localhost")