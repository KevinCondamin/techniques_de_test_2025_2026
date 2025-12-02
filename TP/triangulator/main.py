from flask import Flask

def init():
    app = Flask(__name__)
    return app

app = init()

@app.route('/triangulation/<pointSetId>', methods=['GET'])
def triangulation(pointSetId):
    pass

init()