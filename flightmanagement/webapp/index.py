from flask import render_template, request, redirect
from webapp import app, login, admin
from flask_login import login_user, logout_user, current_user
import dao
from decorators import loggedin


@app.route('/')
def index():
    flights = dao.load_flights()
    tickets = dao.load_tickets()
    start_dates = dao.load_start_dates()
    return render_template('index.html', flights=flights, tickets=tickets, start_dates=start_dates)


@app.route("/admin-login", methods=['post'])
def process_admin_login():
    username = request.form.get('username')
    password = request.form.get('password')
    u = dao.auth_user(username=username, password=password)
    if u:
        login_user(user=u)

    return redirect('/admin')


@app.route('/login', methods=['get', 'post'])
@loggedin
def process_user_login():
    err_msg = None
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.auth_user(username, password)
        if user:
            login_user(user)

            next = request.args.get('next')
            return redirect(next if next else '/')
        else:
            err_msg = 'Tên đăng nhập hoặc mật khẩu không hợp lệ!'

    return render_template('login.html', err_msg=err_msg)


@app.route('/logout', methods=['get'])
def logout_my_user():
    logout_user()
    return redirect('/')


@app.route('/book_ticket')
def flight_search():
    airports = dao.load_airports()
    return render_template('book_ticket.html', airports=airports)


@app.route('/logout')
def my_user_logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['get', 'post'])
@loggedin
def process_user_register():
    err_msg = None
    if request.method.__eq__('POST'):
        try:
            password = request.form['password']
            confirm = request.form['confirm']

            if password.__eq__(confirm):
                try:
                    dao.add_user(username=request.form['username'],
                                 password=password,
                                 name=request.form['name'])
                    return redirect('/login')
                except:
                    err_msg = 'Hệ thống đang bảo trì! Vui lòng quay lại sau!'
            else:
                err_msg = 'Mật khẩu không khớp'
        except:
            err_msg = 'Dữ liệu không hợp lệ'

    return render_template('register.html', err_msg=err_msg)


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
