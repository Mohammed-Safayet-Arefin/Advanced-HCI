import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from FlaskApp.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        db = get_db()

        u_id = request.form['u_id']
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username or not password or not u_id:
            error = "Please provide valid information"
            flash(error)
        elif (db.execute('SELECT * FROM Manager WHERE m_username = ?', (username,)).fetchone()) is not error:
            error = "Username is already taken"
            flash(error)
        elif (db.execute('SELECT * FROM Employee WHERE e_username = ?', (username,)).fetchone()) is not error:
            error = "Username is already taken"
            flash(error)

        if error is None:
            db.execute(
                'INSERT INTO Employee (e_id, e_username, e_password) VALUES (?, ? , ?)',
                (u_id, username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        # check = None
        # if error is None:
        #     if (db.execute('SELECT * FROM Manager WHERE m_id = ?', (u_id,)).fetchone()) is not check:
        #         db.execute('''UPDATE Manager SET m_username = ?, m_password = ? WHERE m_id = ?''',
        #                    (username, generate_password_hash(password), u_id))

        #     else:
        #         db.execute('''UPDATE Employee SET e_username = ?, e_password = ? WHERE e_id = ?''',
        #                    (username, generate_password_hash(password), u_id))

        #     db.commit()
        #     return redirect(url_for('auth.login'))

    return render_template('register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        db = get_db()

        username = request.form['username']
        password = request.form['password']

        user_m_check = db.execute(
            'SELECT * FROM Manager WHERE m_username = ?', (username,)).fetchone()
        user_e_check = db.execute(
            'SELECT * FROM Employee WHERE e_username = ?', (username,)).fetchone()

        print("Manager: ", user_m_check)
        print("Employee: ",  user_e_check)

        error = None
        isManager = False
        u_id = None

        if user_m_check is not None:
            user = user_m_check
            u_id = user_m_check['m_id']
            isManager = True

        elif user_e_check is not None:
            user = user_e_check
            u_id = user_e_check['e_id']
            isManager = False

        elif user_m_check is None and user_e_check is None:
            error = 'Incorrect username.'

        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'


        # if user is None:
        #     error = 'Incorrect username.'
        # elif not check_password_hash(user['password'], password):
        #     error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['u_id'] = u_id
            session['username'] = username
            session['isManager'] = isManager
            print("isManager:", isManager)

            if isManager:
                return redirect(url_for('dashboard.manager_dashboard'))
            else:
                return redirect(url_for('dashboard.index'))

        flash(error)

    return render_template('login.html')


@bp.before_app_request
def load_logged_in_user():
    u_id = session.get('u_id')
    username = session.get('username')
    isManager = session.get('isManager')
    print("u_id: ", u_id)
    print("Username: ", username)
    print("Manager: ", isManager)

    if u_id is None:
        g.user = None

    elif isManager == False:
        g.user = get_db().execute(
            'SELECT * FROM Employee WHERE e_id = ?', (u_id,)
        ).fetchone()
        print("Employee: ", g.user)

    elif isManager == True:
        g.user = get_db().execute(
            'SELECT * FROM Manager WHERE m_id = ?', (u_id,)
        ).fetchone()
        print("Manager: ", g.user)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


def login_required(view):
    """
    Decorator Fuction wraps view and checks if a user is loaded otherwise
    the user gets retured to the main login page. Prevents unauthorized access.
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view






