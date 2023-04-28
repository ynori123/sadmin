from flask import *
import datetime
from datetime import timedelta 
from flask_login import *
from flask_sqlalchemy import *
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'c85ee8b6f2e44cc59358074faa51120f'
app.permanent_session_lifetime = timedelta(minutes=120) 

# ==============================================================
# SQL ALCHEMY
# ==============================================================

app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///shift.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO']=True
app.config['SECTRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)

class Shifts(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    mon = db.Column(db.String(10))
    tue = db.Column(db.String(10))
    wed = db.Column(db.String(10))
    thu = db.Column(db.String(10))
    fri = db.Column(db.String(10))
    sat = db.Column(db.String(10))
    sun = db.Column(db.String(10))

class Employee(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    wages = db.Column(db.Integer)

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Mon(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    time = db.Column(db.String(10), nullable=False)
    position = db.Column(db.String(10))

class Tue(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    time = db.Column(db.String(10), nullable=False)
    position = db.Column(db.String(10))

class Wed(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    time = db.Column(db.String(10), nullable=False)
    position = db.Column(db.String(10))

class Thu(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    time = db.Column(db.String(10), nullable=False)
    position = db.Column(db.String(10))

class Fri(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    time = db.Column(db.String(10), nullable=False)
    position = db.Column(db.String(10))

class Sat(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    time = db.Column(db.String(10), nullable=False)
    position = db.Column(db.String(10))

class Sun(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    time = db.Column(db.String(10), nullable=False)
    position = db.Column(db.String(10))


# ==============================================================
# INITIALIZE
# ==============================================================

# Python interactive shell
# >>>
# from app import app, db
# with app.app_context():
#   db.create_all()

today = datetime.date.today()

if __name__ == '__main__':
    app.run()


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))
# ==============================================================
# URL ROUTING
# ==============================================================

@app.cli.command('initdb')
def init_db():
    db.create_all()
    print('ok')
    
@app.route('/')
def index():
    return redirect('/shift')
@app.route('/createadminuser', methods=['POST','GET'])
def signup_admin():
    if request.method == 'POST' and request.form['develop'] == 'hirakegoma':
        username = request.form['username']
        password = request.form['password']

        admin = Admin(username=username, password=generate_password_hash(password, 'sha256'))

        db.session.add(admin)
        db.session.commit()
        return redirect('/loginadmin')
    else:
        return render_template('signup_admin.html')

@app.route('/loginadmin')
def login_admin():
    return render_template(
        'login_admin.html'
    )

@app.route('/loginadmin.register', methods=['POST','GET'])
def login_admin_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username).first()
        if check_password_hash(admin.password,password):
            login_user(admin)
            return redirect('admin')

        return redirect('/loginadmin')
    else:return redirect('/')

@app.route('/logoutadmin')
@login_required
def logout_admin():
    logout_user(admin)
    return redirect(url_for(login_admin))

@app.route('/form')
def form():
    return render_template(
        'submit_shift.html',
        start_day = get_next_target_date(today, '月'),
        end_day = get_next_target_date(today, '日')
    )

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['user']
    mon = request.form['mon']
    tue = request.form['tue']
    wed = request.form['wed']
    thu = request.form['thu']
    fri = request.form['fri']
    sat = request.form['sat']
    sun = request.form['sun']

    db.session.add(
        Shifts(
            username = username,
            mon = mon,
            tue = tue,
            wed = wed,
            thu = thu,
            fri = fri,
            sat = sat,
            sun = sun
        )
    )
    db.session.flush()
    db.session.commit()

    return redirect(url_for('submit_success'))
@app.route('/submit.success')
def submit_success():
    return(render_template('submit_shift.html'))

@app.route('/admin')
@login_required
def admin():
    db_users = db.session.query(Shifts).all()

    shift = []
    for row in db_users:
        shift.append(
            {
                'username' : row.username,
                'mon' : row.mon,
                'tue' : row.tue,
                'wed' : row.wed,
                'thu' : row.thu,
                'fri' : row.fri,
                'sat' : row.sat,
                'sun' : row.sun
            }
        )
    return render_template(
        'admin.html',
        shift=shift,
        week = ['月曜日','火曜日','水曜日','木曜日','金曜日','土曜日','日曜日']
    )

week_of_shift = []

@app.route('/checkshift', methods=['POST'])
@login_required
def check_shift():
    shift = request.form
    num = len(shift)
    all = []
    for i in range(int(num/8)):
        all.append(
            {
                'user' : request.form['user'+str(i)],
                'mon' : request.form['mon'+str(i)],
                'tue' : request.form['tue'+str(i)],
                'wed' : request.form['wed'+str(i)],
                'thu' : request.form['thu'+str(i)],
                'fri' : request.form['fri'+str(i)],
                'sat' : request.form['sat'+str(i)],
                'sun' : request.form['tue'+str(i)]
            }
        )
    mon = day_of_staff('Mon', all)[7]
    week_of_shift.append(day_of_staff('Mon', all)[0])
    tue = day_of_staff('Tue', all)[7]
    week_of_shift.append(day_of_staff('Tue', all)[1])
    wed = day_of_staff('Wed', all)[7]
    week_of_shift.append(day_of_staff('Wed', all)[2])
    thu = day_of_staff('Thu', all)[7]
    week_of_shift.append(day_of_staff('Thu', all)[3])
    fri = day_of_staff('Fri', all)[7]
    week_of_shift.append(day_of_staff('Fri', all)[4])
    sat = day_of_staff('Sat', all)[7]
    week_of_shift.append(day_of_staff('Sat', all)[5])
    sun = day_of_staff('Sun', all)[7]
    week_of_shift.append(day_of_staff('Sun', all)[6])
    
    week_of_staff = [
        mon,tue,wed,thu,fri,sat,sun
    ]

    return render_template(
        'checkshift.html',
        shift = shift,
        num = num,
        all=all,
        week_of_staff=week_of_staff,
        japanese_week = ['月曜日','火曜日','水曜日','木曜日','金曜日','土曜日','日曜日']
    )

@app.route('/shift', methods=['POST','GET'])
def publish():
    for data,position in request.form.items():
        username = data.split('_')[0]
        time = data.split('_')[1]
        dayofweek = int(data.split('_')[2])

        add_shift_db(username, time, position, dayofweek)

    shifts = []
    for dayofweek in range(7):
        shifts.append(get_shift(dayofweek))

    return render_template(
        'shift.html',
        shifts=shifts,
        week = ['月曜日','火曜日','水曜日','木曜日','金曜日','土曜日','日曜日']        
    )

@app.route('/checkdelete')
@login_required
def check_delete():
    return render_template(
        'checkdelete.html'
    )

@app.route('/collectshift/<msg>')
@login_required
def collect_shift(msg):
    if (msg == 'allow'):
        db.session.query(Shifts).delete()
        db.session.commit()

        return render_template(
            'collect_shift.html'
        )
    elif (msg == 'deny'):
        return redirect(url_for('admin'))

# ==============================================================
# FUNCTIONS
# ==============================================================
def add_shift_db(username,time,position,dayofweek):
    if dayofweek == 0:
        db.session.add(
            Mon(
                username = username,
                time = time,
                position = position
            )
        )
        db.session.commit()
    elif dayofweek == 1:
        db.session.add(
            Tue(
                username = username,
                time = time,
                position = position
            )
        )
        db.session.commit()
    elif dayofweek == 2:
        db.session.add(
            Wed(
                username = username,
                time = time,
                position = position
            )
        )
        db.session.commit()
    elif dayofweek == 3:
        db.session.add(
            Thu(
                username = username,
                time = time,
                position = position
            )
        )
        db.session.commit()
    elif dayofweek == 4:
        db.session.add(
            Fri(
                username = username,
                time = time,
                position = position
            )
        )
        db.session.commit()
    elif dayofweek == 5:
        db.session.add(
            Sat(
                username = username,
                time = time,
                position = position
            )
        )
        db.session.commit()
    elif dayofweek == 6:
        db.session.add(
            Sun(
                username = username,
                time = time,
                position = position
            )
        )
        db.session.commit()

def get_shift(dayofweek):
    if dayofweek == 0:
        return_data = Mon.query.order_by(Mon.position.asc()).all()
    elif dayofweek == 1:
        return_data = Tue.query.order_by(Tue.position.asc()).all()
    elif dayofweek == 2:
        return_data = Wed.query.order_by(Wed.position.asc()).all()
    elif dayofweek == 3:
        return_data = Thu.query.order_by(Thu.position.asc()).all()
    elif dayofweek == 4:
        return_data = Fri.query.order_by(Fri.position.asc()).all()
    elif dayofweek == 5:
        return_data = Sat.query.order_by(Sat.position.asc()).all()
    elif dayofweek == 6:
        return_data = Sun.query.order_by(Sun.position.asc()).all()
    return return_data

def day_of_staff(day, all):
    day_of_staff = []
    mon_dat = []
    tue_dat = []
    wed_dat = []
    thu_dat = []
    fri_dat = []
    sat_dat = []
    sun_dat = []

    for i in all:
        if (i[day.lower()] == 'x' or i[day.lower()] == '' or i[day.lower()] == 'X' or i[day.lower()] == '0'):
            # 削り
            continue
        elif (i[day.lower()] == 'not_in'):
            continue
        day_of_staff.append(
            {
                'user' : i['user'],
                'time' : i[day.lower()]
            }
        )

        db.session.query(Mon).delete()
        db.session.commit()
        db.session.query(Tue).delete()
        db.session.commit()
        db.session.query(Wed).delete()
        db.session.commit()
        db.session.query(Thu).delete()
        db.session.commit()
        db.session.query(Fri).delete()
        db.session.commit()
        db.session.query(Sat).delete()
        db.session.commit()
        db.session.query(Sun).delete()
        db.session.commit()

        if day == 'Mon':
            dat = Mon(
                username = i['user'],
                time = i[day.lower()]
            )
            mon_dat.append(dat)
        if day == 'Tue':
            dat = Tue(
                username = i['user'],
                time = i[day.lower()]
            )
            tue_dat.append(dat)
        if day == 'Wed':
            dat = Wed(
                username = i['user'],
                time = i[day.lower()]
            )
            wed_dat.append(dat)
        if day == 'Thu':
            dat = Thu(
                username = i['user'],
                time = i[day.lower()]
            )
            thu_dat.append(dat)
        if day == 'Fri':
            dat = Fri(
                username = i['user'],
                time = i[day.lower()]
            )
            fri_dat.append(dat)
        if day == 'Sat':
            dat = Sat(
                username = i['user'],
                time = i[day.lower()]
            )
            sat_dat.append(dat)
        if day == 'Sun':
            dat = Sun(
                username = i['user'],
                time = i[day.lower()]
            )
            sun_dat.append(dat)

    shift = [mon_dat, tue_dat, wed_dat, thu_dat, fri_dat, sat_dat, sun_dat, day_of_staff]        

    return shift

def get_next_target_date(date, target_week):
    week = ['月','火','水','木','金','土','日']

    # 曜日を数値型で取得
    weekday = date.weekday()
    # dateから指定した曜日までの加算日数を計算
    add_days = 7 - weekday + week.index(target_week)
    # dateに加算
    next_target_date = date + datetime.timedelta(days = add_days)

    return next_target_date




