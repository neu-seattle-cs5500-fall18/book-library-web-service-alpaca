from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()

@app.route('/zheLab3')
def zheLab3():
	return 'This is Zhe Song lab3'

