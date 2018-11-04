from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db

migrate = Migrate(app, db, compare_type=True)
# migrate.init_app(app)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
