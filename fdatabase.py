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

