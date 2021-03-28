'''this is the flask svc and we use this to initialize any api or server in the flask'''

from app import AppFactory  # importing the api factory

app = AppFactory.create_app()  # we are initializing the factory ap
