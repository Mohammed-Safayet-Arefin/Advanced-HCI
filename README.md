## Advanced-HCI


# Project Setup
Make sure you have anaconda installed.

1. Create an new environment in anaconda:
    > `conda create --name adv-hci python=3.6`


2. Activate environment:
    > `source activate adv-hci`

3. navigate to the correct directory:
    > from directory : ../HCI_FedEx


4 . Run setup to install dependencies: 
    > `python setup.py install`


5. Verify flask and other dependencies were installed
    > `conda list`


6. To run app: 
    > `export FLASK_APP=FlaskApp`
    >  `export FLASK_ENV=development`


7. Initialize the database:
    > `flask init-db`


8. Run on local host and open in browser:
    > `flask run`