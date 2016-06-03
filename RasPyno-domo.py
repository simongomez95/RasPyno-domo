import datetime
from flask import Flask, render_template, Blueprint, Response, request, json
from time import sleep
from nanpy import(ArduinoApi, SerialManager)


app = Flask(__name__)

led = 13
sensor = "A2"
swch = 12
ledState = False
swchState = 0

try:
    connection = SerialManager()
    ard = ArduinoApi(connection)

    # pinMode setup for arduino
    ard.pinMode(led, ard.OUTPUT)
    ard.pinMode(swch, ard.INPUT)
    ard.pinMode(sensor, ard.INPUT)
    temp = ard.analogRead(sensor)/9.31
    print(temp)
except:
    print("Failed To Connect to Arduino")



@app.route('/')
def home():

    try:
        estadoLuz = ard.digitalRead(led)
    except:
        estadoLuz = "Debugging"
        print("derp")
    time = datetime.datetime.now()
    timeStr = time.strftime("%Y-%m-%d %H:%M")
    if estadoLuz:
        estadoLuz='ON'
    else:
        estadoLuz='OFF'

    return render_template("home.html", estadoLuz=estadoLuz, timeStr=timeStr)


@app.route('/lights/')
def luces():
    try:
        estadoLuz = ard.digitalRead(led)
    except:
        estadoLuz = False
        print("derp")

    if estadoLuz:
        estadoLuz='ON'
    else:
        estadoLuz='OFF'
    return render_template("Lights.html", estadoLuz=estadoLuz)


@app.route('/temp/')
def temp():
    temperatura = (5.0 * ard.analogRead(sensor) * 100.0) / 1024
    return render_template("temperature.html", temperatura=temperatura)


@app.route('/toggle/')
def toggle_light():
    print("Eh")
    try:
        if ard.digitalRead(led):
            ard.digitalWrite(led, 0)
        else:
            ard.digitalWrite(led, 1)

    except:
        print("Failed to turn light on")
    return "Luz"


app.jinja_env.globals.update(toggle_light=toggle_light)

#@app.route("/hello/")
#def hello():
#        time = datetime.datetime.now()
#        timeStr = time.strftime("%Y-%m-%d %H:%M")
#        swchState = ard.digitalRead(swch)
#        print("Switch State: {}".format(swchState))
#        ard.digitalWrite(led,swchState)
#
#        templateData = {
#           'title' : 'HELLO!',
#           'time' : timeStr,
#           'status' : swchState
#        }
#        return render_template('main.html', **templateData)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 80, debug = True)
