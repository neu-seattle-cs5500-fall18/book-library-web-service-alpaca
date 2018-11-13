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
=======
@app.route('/anranLab3')
def anranLab3():
	return 'This is Anran Su lab3'
>>>>>>> d34f2b6a0d993a6e2d989107eb206785d0220d8e
