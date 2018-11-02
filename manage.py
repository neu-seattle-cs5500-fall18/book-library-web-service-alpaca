from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()


@app.route('/anranLab3')
def anranLab3():
	return 'This is Anran Su lab3'