from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    #__tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    surname = db.Column(db.String(25))
    email = db.Column(db.String(30))
    password = db.Column(db.String(20))
    age = db.Column(db.Integer)
    admin = db.Column(db.Boolean)
    quizes = db.relationship('Quiz', backref='user')


    def __init__(self, name, surname, email, password, age, admin=False):
        super().__init__()
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password
        self.age = age
        self.admin = admin


quiz_question = db.Table('quiz_question',
                         db.Column('quiz_id', db.Integer, db.ForeignKey('quiz.id'), primary_key=True),
                         db.Column('question_id', db.Integer, db.ForeignKey('question.id'), primary_key=True))

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30))
    icon = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, user:User, icon=''):
        super().__init__()
        self.user = user
        self.name = name
        self.icon = icon

    def __repr__(self):
        return self.name

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quest = db.Column(db.String(100))
    answer1 = db.Column(db.String())
    answer2 = db.Column(db.String())
    answer3 = db.Column(db.String())
    answer_r = db.Column(db.String())


    quiz = db.relationship('Quiz', secondary=quiz_question, backref='question')

    def __init__(self, quest, answer1, answer2, answer3, answer_r):
        super().__init__()
        self.quest = quest
        self.answer1 = answer1
        self.answer2 = answer2
        self.answer3 = answer3
        self.answer_r = answer_r




class Statistic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    quiz_id = db.Column(db.Integer)
    quiz_name = db.Column(db.String(100))
    quiz_time = db.Column(db.String(50))
    right = db.Column(db.Integer)
    total = db.Column(db.Integer)


    def __init__(self, user_id, quiz_id, quiz_name, quiz_time, right, total):
        super().__init__()
        self.user_id = user_id
        self.quiz_name = quiz_name
        self.quiz_id = quiz_id
        self.quiz_time = quiz_time
        self.right = right
        self.total = total


def create_data():
    db.drop_all()
    db.create_all()
    users = [User(name='Ulyan', surname='surname1', email='email1@tt.ru', password='1111', age=23, admin=True),
             User(name='Admin', surname='surname2', email='email2@tt.ru', password='2222', age=25),
             User(name='Igor', surname='surname3', email='email3@tt.ru', password='3333', age=27),
             User(name='Andrew', surname='surname4', email='email4@tt.ru', password='4444', age=23),
             User(name='John', surname='surname5', email='email5@tt.ru', password='5555', age=21)]

    quizes = [Quiz('quiz1', users[0]),
              Quiz('quiz2', users[1]),
              Quiz('quiz3', users[2]),
              Quiz('quiz4', users[0]),
              Quiz('quiz5', users[3])]

    questions = [Question('Почему секретарь Ким решила уйти с работы? ("Что случилось с секретарем Ким?") ',  'Она нашла более высокооплачиваемую работу',  'её оскорбила семья президента',  'Она решила поступить в университет ',  'Она выплатила долги отца и хотела найти себя'),
                Question('Как До Бон Сун получила свою силу? ("Силачка До Бон Сун")',  'Её ударила молния',  'На неё наложила проклятие старая ведьма',  'Ей вкололи экспериментальное лекартсво, которое превратило её в силачку',  'Она передалась ей от матери'),
                Question('Кто был врагом девятихвостого лиса Ли Ена в дораме "История девятихвостого лиса"?',  'Хатхэ',  'Невеста Улитка',  'Пульгасари',  'Имуги'),
                Question('Кто привел Ким Бок-Джу в спортивный зал? ("Фея тяжелой атлетики")',  'Мать',  'Брат',  'Сосед',  'Отец'),
                Question('Где капитан армии Ю Си-Джин впервые встретил свою будущую возлюбленную, врача Кан Мо-Ен? ("Потомки солнца")',  'В Афганистане, во время выполнения военной операции',  'На улице, капитан вышел на прогулку',  'В городе Урук, во время землетрясения',  'В больнице, где она работала врачом'),
                Question('Почему одноклассники издевались над Им Джу Ген, героиней дорамы "Истинная красота"?',  'Её отец работал уборщиком в школе',  'Из-за болезни матери',  'Она была очень популярной ',  'Из-за её внешности'),
                Question('Сколько личностей умещается в главном герое дорамы "Убей меня, исцели меня"?',  'Три',  'Две',  'Десять ',  'Семь'),
                Question('Почему люди стали терять контроль и превращаться в странных существ в дораме "Счастье"?',  'Из-за ядерного оружия',  'Из-за испытаний, которые проводили военные',  'Из-за мистических событий',  'Из-за вируса'),
                Question('Почему придворные дамы носят красные манжеты? ("Красная манжета")',  'Потому что выполняют тяжелую работу',  'Красный цвет- символ преданности и любви ',  'Потому что когда-то придворные дамы выполняли военные обязанности и защищали короля',  'В знак того, что они навсегда принадлежат королю'),
                Question('Кто является постояльцами необычного отеля "Дель Луна"? ("Отель Дель Луна")',  'Люди',  'Животные',  'Вампиры',  'Призраки'),
                Question('Кан Джи Вон и Ю Джи Хек умерли, но получили ещё один шанс прожить жизнь. Как они поняли, что оба вернулись в прошлое? ("Выйди замуж за моего мужа")',  'Ю Джи Хек сам рассказал об этом Кан Джи Вон',  'Они встретили умершего отца Кан Джи Вон',  'У них были вещи из будующего',  'Они назвали песни группы BTS, которые на тот момент ещё не вышли'),
                Question('Как девушка из бедной семьи Кым Чан Ди попала в элитную школу "Шинхва"? ("Мальчики краше цветов")',  'Её устроил туда парень',  'Она поступила туда, потому что очень хорошо училась',  'Её пристроил туда богатый дядя, который внезапно объявился ',  'Она спасла мальчика и её пригласили в школу'),
                Question('Как называется жанр аниме, в котором в центре внимания музыкальные исполнители и шоу-бизнес?',  'Добуцу',  'Кайто',  'Моэ',  'Идолы'),
                Question('Как называется жанр аниме, в котором главная героиня - девочка, обладающая волшебными способностями?',  'Моэ',  'Токусацу',  'Кайто',  'Махо-сёдзё'),
                Question('Какое самое продолжительное аниме в жанре махо-сёдзё?',  'Девочка-волшебница Мадока',  'Сакура - собирательница карт',  'Ван-Пис',  'Сейлор Мун'),
                Question('В каком аниме владыка темных сил отправлет своего ребенка на воспитание хулигану-старшекласснику?',  'Код Гиас',  'Ванпачмен',  'Повелитель',  'Вельзевул'),
                Question('Как зовут кота с крыльями главного героя Нацу из аниме "Хвост Феи"',  'Фрогги',  'Лили',  'Майл',  'Хэппи'),
                Question('Как называется королевство, где находится штаб гильдии "Хвост Феи"?',  'Боско',  'Син',  'Лиан',  'Фиор'),
                Question('Какой силой обладает маг Грей Фуллбастер из аниме "Хвост Феи"?',  'Магия воды',  'Магия ветра',  'Магия огня',  'Магия льда'),
                Question('Как зовут ученика Сайтамы из аниме "Ванпачмен"?',  'Фубуки',  'Стингер',  'Планко',  'Генос'),
                Question('Какой герой S-класса из аниме "Ванпачмен" в действительности не обладает никакой силой?',  'Бофой',  'Бэнг',  'Рой',  'Кинг'),
                Question('Какой силой обладает девочка с зелеными волосами Тацумаки из аниме "Ванпачмен"?',  'Управление водой',  'Телепатия',  'Управление огнем',  'Телекинез'),
                Question('В каком кафе работает по вечерам главная героиня аниме "Президент студсовета - горничная"?',  'Котокафе',  'Анти-кафе',  'Обычное кафе',  'Косплей-кафе'),
                Question('Как зовут полковника армии Аместриса и огненного алхимика из аниме "Стальной алхимик"?',  'Эдвард Элрик',  'Кинг Бредли',  'Лили Штэнфорд',  'Рой Мустанг'),
                Question('Назовите имя старосты класса 1 - А из аниме "Моя геройская академия"?',  'Шоко Тодорки',  'Момо Яойорозу',  'Роко Кагияма',  'Тенья Иида'),
                Question('Кто из профессиональных героев "Моя геройская академия" может увеличиваться за мгновение?',  'Мируко',  'Рюккю',  'Никто',  'Леди Гора'),
                Question('В каком из аниме демон - родная сестра главного героя?',  'Выжившие среди демонов',  'Кровавая луна',  'Убийца Акаме',  'Клинок, рассекающий демонов'),
                Question('Как называется параллельный мир, в который попадает главный герой аниме "Восхождение героя щита"?',  'Голдшир',  'Ритвек',  'Нитрон',  'Мелромарк'),
                Question('В каком году вышла первая серия Ван-Пис?',  '1996',  '2006',  '1990',  '1999'),
                Question('Какое прозвище у главного героя "Ван Пис" Луффи?',  'Глаз со шрамом',  'Красная жилетка',  'Коротышка',  'Соломенная шляпа'),
                Question('В каком из аниме главный герой постоянно издевается над девушкой, в которую влюблен?',  'Радужные дни',  'Дорога юности',  'Бездомный бог',  'Волчица и Черный принц')]

    statistics = [Statistic( user_id=2, quiz_id=1,quiz_name='quiz1', quiz_time='15', right=2, total=4),
                  Statistic(user_id=1, quiz_id=1, quiz_name='quiz2', quiz_time='15', right=1, total=4),
                  Statistic(user_id=3, quiz_id=3, quiz_name='quiz3', quiz_time='16', right=2, total=4),
                  Statistic(user_id=1, quiz_id=2, quiz_name='quiz1', quiz_time='12', right=4, total=4),
                  Statistic(user_id=3, quiz_id=2, quiz_name='quiz2', quiz_time='15', right=3, total=4)]


    quizes[1].question.append(questions[15])
    quizes[0].question.append(questions[12])
    quizes[2].question.append(questions[23])
    quizes[1].question.append(questions[26])
    quizes[0].question.append(questions[28])
    quizes[2].question.append(questions[21])
    quizes[1].question.append(questions[28])
    quizes[3].question.append(questions[20])
    quizes[4].question.append(questions[7])
    quizes[3].question.append(questions[10])

    db.session.add_all(statistics)
    db.session.add_all(questions)
    db.session.add_all(quizes)
    db.session.commit()

