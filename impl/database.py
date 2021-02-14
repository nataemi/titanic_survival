import mysql.connector


class DataBaseConnector:
    def __init__(self):
        self.mydb = mysql.connector.connect(
          host="localhost",
          user="root",
          password="password",
          database="titanic",
          autocommit=True
        )

    def get_cursor(self):
        return self.mydb.cursor()

    def select_all_data(self):
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM USER_INPUT_DATA")
        result = cursor.fetchall()
        cursor.close()
        for x in result:
          print(x)
        return result

    def insert_data(self, userinput):
        cursor = self.get_cursor()
        sql = "INSERT INTO USER_INPUT_DATA(pclass,age,sex,sibsp,parch,survival) VALUES(%s,%s,%s,%s,%s,%s)"
        val = (userinput.pclass,userinput.age, userinput.sex, userinput.sibsp, userinput.parch, userinput.survival)
        cursor.execute(sql, val)
        print(cursor.rowcount, "record inserted.")
        cursor.close()



