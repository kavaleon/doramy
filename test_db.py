from flask import Flask
import os
from models import *

BASE_DIR = os.getcwd()
DB_PATH = os.path.join(BASE_DIR, 'db', 'db_quiz.db')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SECRET_KEY'] = 'edvldsfs'

db.init_app(app)


with app.app_context():
    create_data()
    users = User.query.all()
    print(users)
    #quizes = Quiz.query.all()
    #quiz = Quiz.query.filter_by(id=1).all()[0]        # если не существует- выдает пустой список
    #quiz = Quiz.query.filter_by(id=1).one()         #одна запись
    #quiz = Quiz.query.get(2)        #если нет - выдает ошибку
    #print(quizes)
    #print(len(quiz.question))
    #quiz = Quiz.query.filter_by(id=1).delete()    - удалить
    '''for quiz in quizes:
        print(quiz.name)
        for question in quiz.question:
            print(question)

    quiz = Quiz.query.get(quiz_id)
    question = Question.query.get(quest_id)
    quiz.question.append(question)      # добавление связи для вопроса и квиза по айди
    commit
    Question.query.filter(question.id.in_([1,2,3])).all()
    quiz.question.remove(Question.query.get(3))      #удаление вопроса из списка в квизе'''