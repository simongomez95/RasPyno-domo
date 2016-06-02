import datetime
from flask import Flask, render_template
from time import sleep
from nanpy import(ArduinoApi, SerialManager)


app = Flask(__name__)

led = 13
swch = 12
ledState = False
swchState = 0

try:
    connection = SerialManager()
    ard = ArduinoApi(connection)

    # pinMode setup for arduino
    ard.pinMode(led, ard.OUTPUT)
    ard.pinMode(swch, ard.INPUT)
except:
    print("Failed To Connect to Arduino")




def toggle_light():
    try:
        if ard.digitalRead(led):
            ard.digitalWrite(led, 0)
        else:
            ard.digitalWrite(led, 1)

    except:
        print("Failed to turn light on")
    return "Luz"


app.jinja_env.globals.update(toggle_light=toggle_light)

@app.route('/')
def home():

    estadoLuz = True
    time = datetime.datetime.now()
    timeStr = time.strftime("%Y-%m-%d %H:%M")
    if estadoLuz==True:
        estadoLuz='ON'
    else:
        estadoLuz='OFF'

    return render_template("home.html", estadoLuz=estadoLuz, timeStr=timeStr)


@app.route('/lights/')
def luces():
    return render_template("Lights.html")


@app.route('/temp/')
def temp():
    temperatura = 200
    return render_template("temperature.html", temperatura=temperatura)


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
    app.run()
