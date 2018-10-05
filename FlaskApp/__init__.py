from flask import Flask
import os

# [Documentation] : http://flask.pocoo.org/docs/1.0/tutorial/factory/

# application factory function
def create_app(test_config=None):
    # creates  flask instance and configures app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY="hci_dev",
            DATABASE=os.path.join(app.instance_path, 'FlaskApp.sqlite')
        )


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        #load the test config if passed
        app.config.from_mapping(test_config)

    #ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import dashboard
    app.register_blueprint(dashboard.bp)
    app.add_url_rule('/', endpoint='index')

    return app


# ***************************************************#
# ##### ---- CONFIGURATION ---- #####
# ***************************************************#
# app = Flask(__name__)
# app.secret_key = 'some_super_long_secret_key'


# ***************************************************#
# ##### ---- WEB PAGE ROUTES ---- #####
# ***************************************************#
# @app.route('/')
# @app.route('/home')
# def hello_world():
#     return redirect('main.html')


# @app.route('/login')
# def user_login():
#     return redirect('user_login.html')




# ***************************************************#
# #### ---- ERROR HANDLING ---- #####
# ***************************************************#
# @app.route('/robots.txt/')
# def robots():
#     return("User-agent: *\nDisallow: /register/\nDisallow: /login/\n")



# 404 - page  ot found error
# @app.errorhandler(404)
# def page_not_found(error):
#     try:
#         return render_template("405.html")
#     except Exception as e:
#         raise e


# Handle 405 method not allowed
# @app.errorhandler(405)
# def method_not_found(error):
#     try:
#         return render_template("404.html")
#     except Exception as e:
#         raise e


# # 500 error is an unknown internal server error.
# @app.errorhandler(500)
# def method_not_found(error):
#     try:
#         return render_template("500.html")
#     except Exception as e:
#         raise e

# if __name__ == "__main__":
#     app =  create_app()
