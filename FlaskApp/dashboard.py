from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from FlaskApp.auth import login_required
from FlaskApp.db import get_db

bp = Blueprint('dashboard', __name__)

# the dashboard will display all available jobs from the jobs database

@bp.route('/')
def index():
    db = get_db()

    # jobs = db.execute(
    #     'SELECT j.id, job_title, job_desc, created, author_id, username'
    #     ' FROM job j JOIN user u ON j.author_id = u.id'
    #     ' ORDER BY created DESC'
    # ).fetchall()

    jobs = db.execute(
        'SELECT * FROM Job j'
        ' ORDER BY created DESC'
    ).fetchall()

    return render_template('dashboard/index.html', jobs=jobs)


@bp.route('/manager_dashboard')
def manager_dashboard():
    db = get_db()

    jobs = db.execute(
        'SELECT * FROM Job j'
        ' ORDER BY created DESC'
    ).fetchall()

    return render_template('dashboard/manager_dashboard.html', jobs=jobs)


# @bp.route('/<int:id>/profile')
@bp.route('/profile')
@login_required
def user_profile():
    return render_template('dashboard/profile.html')


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['job_title']
        body = request.form['job_desc']
        job_credentials = request['job_credentials']
        begin_date = request.form['job_date_beg']
        end_date = request.form['job_date_beg']
        begin_time = request.form['job_time_beg']
        end_time = request.form['job_time_end']
        job_city = request.form['job_city']
        job_state = request.form['job_state']
        job_zip = request.form['job_zip']

        error = None

        if not title:
            error = 'Job title is required.'
        elif not body:
            error = 'Job description is required.'
        elif not begin_date or not end_date:
            error = "Both Job Begin and End Date are required."
        elif not begin_time or not end_time:
            error = "Both Job Begin Time and Job End time are required."
        elif not job_city or not job_state or not job_zip:
            error = " A city, state and zip code are required for all jobs. "

        if error is not None:
            flash(error)
        else:
            db = get_db()
            # g.user['u_id']
            db.execute(
                'INSERT INTO Job (job_title, job_desc, job_credentials, job_date_beg, job_date_end, job_time_beg, job_time_end, job_city, job_state, job_zip, m_id)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (title, body, job_credentials, begin_date, end_date, begin_time, end_time, job_city, job_state, job_zip, 1)
            )
            print(title, body, begin_date, end_date, begin_time, end_time, job_city, job_state, job_zip, 1)
            db.commit()
            
            return redirect(url_for('dashboard.index'))

    return render_template('dashboard/create.html')


def get_job(id, check_author=True):
    job = get_db().execute(
        'SELECT job_id, job_title, job_desc, created, m_id'
        ' FROM Job WHERE job_id = ?',
        (id,)
    ).fetchone()

    if job is None:
        abort(404, "Job id {0} doesn't exist.".format(id))

    # if check_author and job['m_id'] != g.user['u_id']:
        # 403 Error means Forbidden
        # abort(403)

    return job


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    job = get_job(id)

    if request.method == 'POST':
        title = request.form['job_title']
        body = request.form['job_desc']
        qualifications = request.form['job_credentials']
        begin_date = request.form['job_date_beg']
        end_date = request.form['job_date_beg']
        begin_time = request.form['job_time_beg']
        end_time = request.form['job_time_end']
        job_city = request.form['job_city']
        job_state = request.form['job_state']
        job_zip = request.form['job_zip']
        error = None

        if not title:
            error = 'Job title is required.'
        elif not body:
            error = 'Job description is required.'
        elif not begin_date or not end_date:
            error = "Both Job Begin and End Date are required."
        elif not begin_time or not end_time:
            error = "Both Job Begin Time and Job End time are required."
        elif not job_city or not job_state or not job_zip:
            error = " A city, state and zip code are required for all jobs. "

        if error is not None:
            flash(error)
        else:
            db = get_db()

            db.execute(
                'UPDATE Job SET job_title = ?, job_desc = ?, job_credentials = ?, job_date_beg = ?, job_date_end = ?, job_time_beg = ?, job_time_beg = ?, job_city = ?, job_state = ?, job_zip = ?, m_id = ?'
                ' WHERE job_id = ?',
                (title, body, qualifications, begin_date, end_date, begin_time, end_time, job_city, job_state, job_zip, 1, id)
            )
            db.commit()
            return redirect(url_for('dashboard.index'))

    return render_template('dashboard/update.html', job=job)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_job(id)
    db = get_db()
    db.execute('DELETE FROM job WHERE job_id = ?', (id,))
    db.commit()
    return redirect(url_for('dashboard.index'))
