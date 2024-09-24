import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Создаем приложение Flask
app = Flask(__name__)

# Получаем переменные окружения
db_name = os.getenv('db_name')
db_user = os.getenv('db_user')
db_pass = os.getenv('db_pass')
db_host = os.getenv('db_host')
db_port = os.getenv('db_port')

# Формируем строку подключения к базе данных
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{
    db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Создаем объект базы данных
db = SQLAlchemy(app)


# Определяем модель для хранения данных
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<User {self.name}>"


# Инициализируем базу данных (создаем таблицы)
with app.app_context():
    db.create_all()


# Определяем маршрут для добавления пользователя
@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.json.get('name')
    if name:
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User added successfully!'}), 201
    return jsonify({'message': 'Name is required'}), 400


# Определяем маршрут для получения списка всех пользователей
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [{'id': user.id, 'name': user.name} for user in users]
    return jsonify(users_list)


# Главная страница
@app.route('/')
def hello_world():
    return 'Hello, Andrii! Welcome to your Flask Web App with PostgreSQL and .env variables!'


# Запускаем приложение
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
