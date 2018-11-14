from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()


<<<<<<< HEAD
@app.route('/jinhaoLab3')
def jinhaoLab3():
	return 'This is Jinhao Liu lab3'
