from flask import Flask, render_template, url_for, session, request, redirect
import os
from models import *
from sqlalchemy import select
from flask import jsonify
def check_info(info, errors_2):
    errors = []
    if not info['age']:
        errors.append(errors_2['age'][0])
    if not info['email']:
        errors.append(errors_2['email'])
    if not info['password']:
        errors.append(errors_2['password'])
    if info['password'] != info['ch_password']:
        errors.append(errors_2['ch_password'])
    return errors

def form_quiz_quest_work():
    first_form = request.form.getlist('first_form')
    second_form = request.form.getlist('second_form')
    for quiz in first_form:
        quiz = quiz.split('%%%')
        quiz_id = quiz[0]
        what_to_do = quiz[1]

        if what_to_do == 'add':
            if second_form:
                for question in second_form:
                    quize = Quiz.query.filter_by(id=quiz_id).one()
                    quest = Question.query.filter_by(id=question).one()
                    quize.question.append(quest)
                    db.session.commit()
            else:
                print('Вопросы не добавлены, т.к. они не выбраны')
        else:
            if what_to_do:
                quiz = Quiz.query.get(quiz_id)
                for question in quiz.question:
                    if question.id == int(what_to_do):
                        question = Question.query.filter_by(id=int(what_to_do)).one()
                        quiz.question.remove(question)
                        db.session.commit()
            else:
                pass

def form_edit_question_work():
    edit_question_id = request.form.get("edit_question_id")
    question = Question.query.get(edit_question_id)
    question.quest = request.form.get('edit_question')
    question.answer1 = request.form.get('edit_answer1')
    question.answer2 = request.form.get('edit_answer2')
    question.answer3 = request.form.get('edit_answer3')
    question.answer_r = request.form.get('edit_answer_r')
    db.session.commit()

def form_edit_quize_work():
    edit_URL = request.form.get('edit_URL')
    if not edit_URL:
        edit_URL = None
    quiz = Quiz.query.get(request.form.get("edit_quize_id"))
    quiz.name = request.form.get('edit_quize_name')
    quiz.icon = edit_URL
    db.session.commit()

def form_add_question_work():
    question = request.form.get('question')
    answer1 = request.form.get('answer1')
    answer2 = request.form.get('answer2')
    answer3 = request.form.get('answer3')
    answer_r = request.form.get('answer_r')
    question_full = Question(question, answer1, answer2, answer3, answer_r)
    db.session.add(question_full)

def form_add_quiz_work():
    name = request.form.get('name')
    url = request.form.get('url')
    if not url:
        url = ''
    quiz = Quiz(name=name, user=User.query.get(1), icon=url)
    db.session.add(quiz)


work_dir = os.getcwd()
DB_PATH = os.path.join(work_dir, 'db', 'db_quiz.db')

app = Flask(__name__,
                static_folder=os.path.join(work_dir, 'static'),
                template_folder=os.path.join(work_dir, 'templates'))

app.config['SECRET_KEY'] = 'ABRACADABRA' # обязательно для работы в сессии
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['JSON_AS_ASCII'] = False
errors_2 = {'name': 'Неверный ввод', 'surname': 'Неверный ввод',
                'age': ['Возраст не указан', 'Возраст от 10 до 90 лет'], 'email': 'Нет email', 'password': 'Нет пароля',
                'ch_password': 'Пароли не совпадают'}

db.init_app(app)
with (app.app_context()):
    create_data()
    @app.route('/', methods=['POST', 'GET'])
    def index():
        if session.get('login_ok'):
            return redirect(url_for('quizes'))

        if request.method == 'POST':
            email_u = request.form.get('email')
            password_u = request.form.get('password')
            try:
                user = User.query.filter_by(email=email_u).one()
                session['user_admin'] = user.admin
                if user:
                    if user.password == password_u:
                        session['user_name'] = user.name
                        session['login_ok'] = True
                        return redirect(url_for('quizes'))
                    else:
                        error = 'Пароль ввведен неверно'
                        return render_template('login.html', error=error)
            except:
                error = 'Пользователя с таким e-mail не существует'
                return render_template('login.html', error=error)


        if request.method == "GET":
            session['login_ok'] = False
            return render_template('login.html')

        return render_template('login.html')


    @app.route('/logout/')
    def logout():
        session['login_ok'] = False
        return redirect(url_for('index'))

    @app.route('/registration/', methods=['POST', 'GET'])
    def registration():
        global all_quizes

        values = []
        if request.method == 'POST':
            name = request.form.get('name')
            surname = request.form.get('surname')
            age = request.form.get('age')
            email = request.form.get('email')
            password = request.form.get('password')
            ch_password = request.form.get('ch_password')
            info = {'name': name, 'surname': surname, 'age': age, 'email': email,
                    'password': password, 'ch_password': ch_password}
            values = [name, surname, age, email]
            errors = check_info(info, errors_2)

            if not errors:
                user = User(name, surname, email, password, age)
                users = User.query.all()
                users.append(user)
                print(users)
                session['login_ok'] = True
                return redirect(url_for('quizes')) # записать вбазу --- перенаправить на главную
            else:
                return render_template('registration.html', errors=errors, values=values)

        if request.method == 'GET':
            print('work this')
            session['login_ok'] = False
            return render_template('registration.html', values=values)


    @app.route('/quizes/') # список квизов, если get - показываем квизы post - направляем на квиз
    def quizes():
        all_quizes = Quiz.query.all()
        session['quiz_id'] = 0
        if not session.get('login_ok'):
            return render_template('login.html')
        return render_template('quizes.html', all_quizes=all_quizes, name=session['user_name'], admin=session['user_admin'])


    @app.route('/test/', methods=['POST', 'GET']) # прохождение теста
    def test():
        if request.method == "GET":
            session['quiz'] = request.args.get('quiz')

            if session['quiz']:
                quiz_with_question = Quiz.query.filter_by(id=int(session['quiz'])).one()
                session['question_id'] = 0
                session['right_answer'] = 0
                session['total'] = len(quiz_with_question.question)
                session['number_of_question'] = 1
                info = quiz_with_question.question[session['question_id']]
                return render_template('test.html', values=info)
            else:
                return render_template('quizes.html', all_quizes=all_quizes)

        elif request.method == 'POST':
            quiz_with_question = Quiz.query.filter_by(id=int(session['quiz'])).one()

            answer = request.form.get('answer')
            if quiz_with_question.question[session['question_id']].answer_r == answer:
                session['right_answer'] += 1

            session["question_id"] += 1
            session["number_of_question"] += 1


            if session["number_of_question"] == len(quiz_with_question.question) + 1:
                return redirect(url_for('result'))


            info = quiz_with_question.question[session['question_id']]
            print(info)
            return render_template('test.html', values=info)

    @app.route('/result/')
    def result():
        return render_template('result.html', total=session['total'], answer=session['right_answer'])

    @app.route('/reda/', methods=['POST', 'GET'])
    def reda():
        if session['user_admin']:
            if request.method == 'GET':
                questions = Question.query.all()
                quizes = Quiz.query.all()
                return render_template('reda.html', quizes=quizes, questions=questions, len=len)

            elif request.method == 'POST':

                quize_to_delete = request.form.get('quize_to_delete')
                question_to_delete = request.form.get('question_to_delete')

                form_quiz_quest = request.form.get('form_quiz_question')
                form_edit_question = request.form.get('form_edit_question')
                form_edit_quize = request.form.get('form_edit_quize')
                form_add_question = request.form.get('form_add_question')
                form_add_quiz = request.form.get('form_add_quiz')

                if form_quiz_quest:
                    form_quiz_quest_work()

                if form_edit_question:
                    form_edit_question_work()

                if form_edit_quize:
                    form_edit_quize_work()

                if form_add_question:
                    form_add_question_work()

                if form_add_quiz:
                    form_add_quiz_work()


                if quize_to_delete:
                    Quiz.query.filter(Quiz.name == quize_to_delete).delete()

                if question_to_delete:
                    Question.query.filter(Question.quest == question_to_delete).delete()


                questions = Question.query.all()
                quizes = Quiz.query.all()
                db.session.commit()
                return render_template('reda.html', quizes=quizes, questions=questions, len=len)


    @app.route('/quiz_question/', methods=['POST', 'GET'])
    def quiz_question():
        quizes = Quiz.query.all()
        questions = Question.query.all()
        return render_template('quiz_question.html', quizes=quizes, questions=questions)

    @app.route('/edit_quize/<int:id>/', methods=['POST', 'GET'])
    def edit_quize(id):
        quize = Quiz.query.get(id)
        return render_template('edit_quize.html', id=id, values=quize)

    @app.route('/edit_question/<int:id>/', methods=['POST', 'GET'])
    def edit_question(id):
        question = Question.query.get(id)
        return render_template('edit_question.html', id=id, values=question)

    @app.route('/statistic/', methods=['POST', 'GET'])
    def statistic():
        info = Statistic.query.all()
        print(info)
        return render_template('statistic.html', values=info)

    @app.route('/api/quizes/', methods=['GET'])
    def return_json_quizes():
        quizes_json = []
        quizes = Quiz.query.all()
        for quiz in quizes:
            quizes_json.append({"quiz_name": quiz.name})
        print(quizes_json)

        return jsonify(quizes_json)

    @app.route('/api/questions/', methods=['GET'])
    def return_json_questions():
        questions_json = []
        questions = Question.query.all()
        for question in questions:
            questions_json.append({"question_name": question.quest})
        print(questions_json)

        return jsonify(questions_json)


    @app.route('/api/quiz/<int:id>/', methods=['GET'])
    def return_json_quiz(id):
        quiz = Quiz.query.get(id)
        quiz_json = {'id': quiz.id,
                         'quiz_name': quiz.name,
                         'quiz_icon': quiz.icon,
                         'quiz_user_id': quiz.user_id,
                     }
        print(quiz_json)

        return jsonify(quiz_json)

    @app.route('/api/question/<int:id>/', methods=['GET'])
    def return_json_question(id):
        question = Question.query.get(id)
        question_json = {'id': question.id,
                         'question_name': question.quest,
                         'question_answer1': question.answer1,
                         'question_answer2': question.answer2,
                         'question_answer3': question.answer3,
                         'question_answer_r': question.answer_r}
        print(question_json)

        return jsonify(question_json)

app.run(debug=True, port=5500, host='127.0.0.1')

