from flask import Flask, render_template


messanger = ['whatsapp', 'viber', 'telegram']
hat = ['главная', 'каталог', 'ДС', 'выйти', 'войти', 'пользователь',
       'корзина', 'регистрация']


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', messanger=messanger, hat=hat)


if __name__ == '__main__':
    app.run(debug=True)
