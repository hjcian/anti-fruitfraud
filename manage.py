from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
import sys
from app import app, db

migrate = Migrate(app, db, compare_type=True)
# migrate.init_app(app)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    if "--debug" in sys.argv:
        manager.add_command("runserver", Server(use_debugger=True))
    manager.run()
