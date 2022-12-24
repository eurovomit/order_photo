import sqlite3

from flask import Flask, render_template, request, session, redirect, url_for, abort, g, flash

from order_photo.fdatabase import FDatabase

messanger = ['whatsapp', 'viber', 'telegram']
hat = ['главная', 'каталог', 'ДС', 'выйти', 'войти', 'пользователь',
       'корзина', 'регистрация']

# конфигурация приложения
DATABASE = 'photodb.db'
DEBUG = True
SECRET_KEY = 'gfjjsdkjvjshg8798.>kjhg'

app = Flask(__name__)
app.config.from_object(__name__)


# функция соединения с БД
def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    # результаты запросов не в виде кортежей, а в виде словаря
    conn.row_factory = sqlite3.Row
    return conn


# функция которая проверяет есть ли соединение с бд, если нет, то создает его
def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


# делаем закрытие бд автоматически при закрытии страницы
@app.teardown_appcontext
def close_db(error):
    if error is not None:
        print(error)
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/')
def index():
    # делаем соединение с бд автоматически при открытии страницы
    db = get_db()
    return render_template('index.html', messanger=messanger, hat=hat)


@app.route('/enter', methods=['POST', 'GET'])
def enter():
    # если переменная userLogged с логином и паролем в сессии
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['phone'] == '+79814600001' \
            and request.form['password'] == 'A1h9v9s0':
        session['userLogged'] = request.form['phone']
        return redirect(url_for('profile', username=session['userLogged']))
    return render_template('enter.html')


@app.route('/profile/<username>')
def profile(username):
    # если эта переменная не в сессии, или логин не совпадает
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return f'profile {username}'

# админка детских садов
@app.route('/adminds', methods=['POST', 'GET'])
def adminds():
    db = get_db()
    if request.method == 'POST':
        res = FDatabase(db).insert_ds(request.form['ds'], request.form['city'])
        if not res:
            flash('ошибка добавления ДС', category='error')
        else:
            flash('ДС добавлен успешно', category='success')
    return render_template('adminds.html', messanger=messanger, hat=hat)

# админка заказов
@app.route('/adminorders')
def adminorders():
    db = get_db()
    res = FDatabase(db).show_orders()
    return render_template('adminorders.html', res=res, messanger=messanger, hat=hat)

# создаем страницу подробностей заказа
# сначала отображаем все заказы из БД
# потом создаем ссылку на номере заказа и передаем ее в адрес <order_id>
# по этому номеру делаем выборку фото из заказов
@app.route('/order/<order_id>')
def order_detail(order_id):
    db = get_db()
    res = FDatabase(db).show_order(order_id)
    if len(res) == 0:
        abort(404)
    return render_template('order.html', res=res, messanger=messanger, hat=hat)

# обработка не найденной страницы
@app.errorhandler(404)
def page_not_found(error):
    if error != '':
        print(error)
    return render_template('error.html', title='неверный адрес страницы',
                           messanger=messanger, hat=hat), 404


if __name__ == '__main__':
    app.run()
