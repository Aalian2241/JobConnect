from market import app
from flask_session import Session

#Checks if the run.py file has executed directly and not imported
if __name__ == '__main__':
    
    app.run(debug='True')