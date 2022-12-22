from flask import Flask, render_template, request


messanger = ['whatsapp', 'viber', 'telegram']
hat = ['главная', 'каталог', 'ДС', 'выйти', 'войти', 'пользователь',
       'корзина', 'регистрация']


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', messanger=messanger, hat=hat)


@app.route('/enter', methods=['POST', 'GET'])
def enter():
    if request.method == 'POST':
        print('post')
        print(request.form)
    else:
        print('get')
    return render_template('enter.html')


if __name__ == '__main__':
    app.run(debug=True)
