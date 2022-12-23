from flask import Flask, render_template, request, flash


messanger = ['whatsapp', 'viber', 'telegram']
hat = ['главная', 'каталог', 'ДС', 'выйти', 'войти', 'пользователь',
       'корзина', 'регистрация']


app = Flask(__name__)
app.config['SECRET_KEY'] = 'kjhgjhgddjhkgkljH76876587'


@app.route('/')
def index():
    return render_template('index.html', messanger=messanger, hat=hat)


@app.route('/enter', methods=['POST', 'GET'])
def enter():
    if request.method == 'POST':
        if len(request.form['phone']) > 5:
            flash(message='вход в аккаунт', category='succes')
        else:
            flash(message='неправильные данные', category='error')
    return render_template('enter.html')


if __name__ == '__main__':
    app.run(debug=True)
