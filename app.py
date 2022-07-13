from peewee import *
import datetime

from flask import Flask, redirect, url_for
from flask import render_template
from flask_bcrypt import Bcrypt
from forms import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'
bcrypt = Bcrypt(app)


db = SqliteDatabase('blog.db')


class BaseClass(Model):
    class Meta:
        database = db

#unique=true для предостаращения дублирования email


class User(BaseClass):
    email = CharField(unique=True)
    password = CharField()
    register_date = DateTimeField(default=datetime.datetime.now)

    def __str__(self) -> str:
        return f'User: {self.email} / {self.register_date}'


class Post(BaseClass):
    title = CharField()
    content = TextField()
    publish_date = DateTimeField(null=True)
    views = IntegerField(default=0)
    author = ForeignKeyField(User, backref='posts', lazy_load=False)


class Comment(BaseClass):
    date = DateTimeField(default=datetime.datetime.now)
    content = TextField()
    user = ForeignKeyField(User, backref='comments', lazy_load=False)
    post = ForeignKeyField(Post, backref='comments', lazy_load=False)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/posts')
def posts():
    fixtures = [
        {
            "title": "Ozbekistondagi dastulash boyicha oquv markazlari",
            "post_date": "2022 Fev 3 22:05:00",
            "views": 15,
            "content": "Ma'lumki, so'ngi vaqtlarda O'zbekistonda axborot texnologiyalari - IT ga e'tibor ancha oshib bormoqda. Albatta bunda o'quv markazlarinign roli juda katta. Quyida O'zbekistondagi dasturlashni o'rgatadigan o'quv markazlar, akademiyalar yoki maklablari ro'yxati(internetdan ma'lumot mavjudlari), umumiy 120 ta, balkim bu to'liq emasdir, balkim ro'yxatdagi qaysilaridir yopilib ketgandir yoki tushib qolgandir.",
        },
        {
            "title": "Ozbekistondagi dastulash boyicha oquv markazlari",
            "post_date": "2022 Fev 3 22:05:00",
            "views": 15,
            "content": "Ma'lumki, so'ngi vaqtlarda O'zbekistonda axborot texnologiyalari - IT ga e'tibor ancha oshib bormoqda. Albatta bunda o'quv markazlarinign roli juda katta. Quyida O'zbekistondagi dasturlashni o'rgatadigan o'quv markazlar, akademiyalar yoki maklablari ro'yxati(internetdan ma'lumot mavjudlari), umumiy 120 ta, balkim bu to'liq emasdir, balkim ro'yxatdagi qaysilaridir yopilib ketgandir yoki tushib qolgandir.",
        },
        {
            "title": "Ozbekistondagi dastulash boyicha oquv markazlari",
            "post_date": "2022 Fev 3 22:05:00",
            "views": 15,
            "content": "Ma'lumki, so'ngi vaqtlarda O'zbekistonda axborot texnologiyalari - IT ga e'tibor ancha oshib bormoqda. Albatta bunda o'quv markazlarinign roli juda katta. Quyida O'zbekistondagi dasturlashni o'rgatadigan o'quv markazlar, akademiyalar yoki maklablari ro'yxati(internetdan ma'lumot mavjudlari), umumiy 120 ta, balkim bu to'liq emasdir, balkim ro'yxatdagi qaysilaridir yopilib ketgandir yoki tushib qolgandir.",
        },
        {
            "title": "Ozbekistondagi dastulash boyicha oquv markazlari",
            "post_date": "2022 Fev 3 22:05:00",
            "views": 15,
            "content": "Ma'lumki, so'ngi vaqtlarda O'zbekistonda axborot texnologiyalari - IT ga e'tibor ancha oshib bormoqda. Albatta bunda o'quv markazlarinign roli juda katta. Quyida O'zbekistondagi dasturlashni o'rgatadigan o'quv markazlar, akademiyalar yoki maklablari ro'yxati(internetdan ma'lumot mavjudlari), umumiy 120 ta, balkim bu to'liq emasdir, balkim ro'yxatdagi qaysilaridir yopilib ketgandir yoki tushib qolgandir.",
        },
        {
            "title": "Ozbekistondagi dastulash boyicha oquv markazlari",
            "post_date": "2022 Fev 3 22:05:00",
            "views": 15,
            "content": "Ma'lumki, so'ngi vaqtlarda O'zbekistonda axborot texnologiyalari - IT ga e'tibor ancha oshib bormoqda. Albatta bunda o'quv markazlarinign roli juda katta. Quyida O'zbekistondagi dasturlashni o'rgatadigan o'quv markazlar, akademiyalar yoki maklablari ro'yxati(internetdan ma'lumot mavjudlari), umumiy 120 ta, balkim bu to'liq emasdir, balkim ro'yxatdagi qaysilaridir yopilib ketgandir yoki tushib qolgandir.",
        },
        {
            "title": "Ozbekistondagi dastulash boyicha oquv markazlari",
            "post_date": "2022 Fev 3 22:05:00",
            "views": 15,
            "content": "Ma'lumki, so'ngi vaqtlarda O'zbekistonda axborot texnologiyalari - IT ga e'tibor ancha oshib bormoqda. Albatta bunda o'quv markazlarinign roli juda katta. Quyida O'zbekistondagi dasturlashni o'rgatadigan o'quv markazlar, akademiyalar yoki maklablari ro'yxati(internetdan ma'lumot mavjudlari), umumiy 120 ta, balkim bu to'liq emasdir, balkim ro'yxatdagi qaysilaridir yopilib ketgandir yoki tushib qolgandir.",
        },
    ]
    return render_template('posts.html', posts=fixtures)

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data

        user = User.get_or_none(User.email == email)

        if not user:
            return 'User not found'

        if bcrypt.check_password_hash(user.password, password):
            # session write needle information
            # redirect
            return 'Login success'
        else:
            return 'Password incorrect'

    return render_template('login.html', form=login_form)

def logout():
    return redirect(url_for('home'))

# Authentication vs Authorization
# flask: forms, bcrypt, peewee select

if __name__ == '__main__':
    app.run(port=8080, debug=True)
