from flask_script import Manager
from app import create_app


app = create_app()
manager = Manager(app)


from app.services import KNNService


@manager.command
def train_model():
    KNNService.train_classifier('app/ml_models/knn.sav')


if __name__ == '__main__':
    manager.run()
