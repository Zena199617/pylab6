from flask import Flask
import sqlite3
from flask import g

app = Flask(__name__)

DATABASE = 'db.sqlite'
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def root():
    body = """<html>
    <head><title>Lab6</title></head>
    <body>
        <table>
            <tr>
                <th>Имя</th>
                <th>Подарок</th>
                <th>Стоимость</th>
                <th>Статус</th>
            </tr>    
"""

    for le in get_db().execute('SELECT * FROM lab6'):
        bought = "Куплен" if le[3] else "Не куплен"
        body += """
            <tr>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
            </tr>""".format(le[0], le[1], le[2],bought)

    body += """
            </table>
        </body>
    </html>
    """

    return body


if __name__ == '__main__':
    app.run()
