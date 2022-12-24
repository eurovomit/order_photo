import sqlite3


class FDatabase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def insert_ds(self, name, city):
        try:
            self.__cur.execute("""INSERT INTO kindergarten 
                                  VALUES (NULL, ?, ?)""", (name, city))
            self.__db.commit()
        except sqlite3.Error as e:
            print('ошибка добавления детского сада' + str(e))
            return False
        return True

    def show_orders(self):
        try:
            self.__cur.execute("""SELECT order_id, user_login, user_phone, status_name, price
                                  FROM orders
                                  JOIN user u on orders.order_user = u.user_id
                                  JOIN status s on orders.order_status = s.status_id;""")
            res = self.__cur.fetchall()
            return res
        except sqlite3.Error as e:
            print(str(e))

    def show_order(self, order_id):
        try:
            self.__cur.execute("""SELECT photo_name, type_size, count, count * t.type_price AS cost
                                  FROM order_photo
                                  JOIN photo p on order_photo.photo_id = p.photo_id
                                  JOIN type t on order_photo.type_id = t.type_id
                                  WHERE order_id = ?;""", (order_id))
            res = self.__cur.fetchall()
            return res
        except sqlite3.Error as e:
            print(str(e))
