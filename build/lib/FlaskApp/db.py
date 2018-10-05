import sqlite3 as sql

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    """
    Returns database connection
    """

    # g is a special object that is unique for each db request
    # used to store data made by multiple function calls.
    if 'db' not in g:
        g.db = sql.connect(
            current_app.config['DATABASE'],
            detect_types=sql.PARSE_DECLTYPES
        )
        g.db.row_factory = sql.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


# this creates a command line command that initializes
# the database and displays a message upon success.
@click.command('init-db')
@with_appcontext
def init_db_command():
    "Clear existing data and create new tables."

    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
