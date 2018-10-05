
## Advanced HCI Fedex Project 
=============================
Make sure you have anaconda installed.

Create an new environment in anaconda 
    > conda create --name adv-hci python=3.6`

Activate environment:
    > `source activate flask-test`

Make sure you are in the correct directory.
from directory : ../HCI_FedEx

Run setup to install dependencies: 
    > `python setup.py install`

Verify flask and other dependencies were installed
    > `conda list`

To run app: 
    `export FLASK_APP=FlaskApp`
    `export FLASK_ENV=development`

Initialize the database:
    > `flask init-db`

Run on local host and open in browser:
    > `flask run`