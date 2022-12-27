import sqlite3

from flask import Flask, render_template, request, session, redirect, url_for, abort, g, flash
from werkzeug.security import generate_password_hash, check_password_hash
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


 # перхват запроса для установления соединения при открытии любой страницы
dbase = None
@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDatabase(db)


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


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']
        password1 = request.form['password1']
        if password1 == password and dbase.uniquephone(phone):
            hash = generate_password_hash(password)
            res = dbase.adduser(phone, hash)
            if res:
                flash('Вы успешно зарегистрированы')
                return redirect(url_for('enter'))
            else:
                flash('ошибка при добавлении')
        else:
            flash('неверно заполнены поля')

    return render_template('register.html')


@app.route('/profile/<username>')
def profile(username):
    # если эта переменная не в сессии, или логин не совпадает
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return f'profile {username}'

# админка детских садов
@app.route('/adminds', methods=['POST', 'GET'])
def adminds():
    if request.method == 'POST':
        res = dbase.insert_ds(request.form['ds'], request.form['city'])
        if not res:
            flash('ошибка добавления ДС', category='error')
        else:
            flash('ДС добавлен успешно', category='success')
    return render_template('adminds.html', messanger=messanger, hat=hat)

# админка заказов
@app.route('/adminorders')
def adminorders():
    res = dbase.show_orders()
    return render_template('adminorders.html', res=res, messanger=messanger, hat=hat)

# создаем страницу подробностей заказа
# сначала отображаем все заказы из БД
# потом создаем ссылку на номере заказа и передаем ее в адрес <order_id>
# по этому номеру делаем выборку фото из заказов
@app.route('/order/<order_id>')
def order_detail(order_id):
    res = dbase.show_order(order_id)
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
