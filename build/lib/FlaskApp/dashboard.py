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

    # insert dummy data.
    db.execute('INSERT INTO job (job_title, job_desc, author_id)'
                ' VALUES (?, ?, ?)',
                ("Title", "description", 1)
            )
    jobs = db.execute(
        'SELECT j.id, job_title, job_desc, created, author_id, username'
        ' FROM job j JOIN user u ON j.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    return render_template('dashboard/index.html', jobs=jobs)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['job_title']
        body = request.form['job_desc']
        error = None

        if not title:
            error = 'Job title is required.'
        elif not body:
            error = 'Job description is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO job (job_title, job_desc, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('dashboard.index'))

    return render_template('dashboard/create.html')


def get_job(id, check_author=True):
    job = get_db().execute(
        'SELECT j.id, job_title, job_desc, created, author_id, username'
        ' FROM job j JOIN user u ON j.author_id = u.id'
        ' WHERE j.id = ?',
        (id,)
    ).fetchone()

    if job is None:
        abort(404, "Job id {0} doesn't exist.".format(id))

    if check_author and job['author_id'] != g.user['id']:
        # 403 Error means Forbidden
        abort(403)

    return job


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    job = get_job(id)

    if request.method == 'POST':
        title = request.form['job_title']
        body = request.form['job_desc']
        error = None

        if not title:
            error = 'Job title is required.'
        elif not body:
            error = 'Job description is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE job SET job_title = ?, job_desc = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('dashboard.index'))

    return render_template('dashboard/update.html', job=job)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_job(id)
    db = get_db()
    db.execute('DELETE FROM job WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('dashboard.index'))
