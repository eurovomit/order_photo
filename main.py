from flask import Flask, render_template, request, flash, session, redirect, url_for, abort

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
    # если переменная userLogged с логином и паролем в сессии
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['phone'] == '+79814600001' and request.form['password'] == 'A1h9v9s0':
        session['userLogged'] = request.form['phone']
        return redirect(url_for('profile', username=session['userLogged']))


    # if request.method == 'POST':
    #     if len(request.form['phone']) > 5:
    #         flash(message='вход в аккаунт', category='succes')
    #     else:
    #         flash(message='неправильные данные', category='error')
    return render_template('enter.html')


@app.route('/profile/<username>')
def profile(username):
    # если эта переменная не в сессии, или логин не совпадает
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return f'profile {username}'


# обработка ненайденной страницы
@app.errorhandler(404)
def pageNotFound(error):
    return render_template('error.html', title='неверный адрес страницы',
                           messanger=messanger, hat=hat), 404

if __name__ == '__main__':
    app.run(debug=True)
