from flask import Flask, render_template
from flask_socketio import SocketIO, emit,send
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



app = Flask(__name__,template_folder='templates')
socketio = SocketIO(app, cors_allowed_origins="*")
# socketio = SocketIO(app, async_mode='gevent_uwsgi')
# socketio = SocketIO(app, async_mode='threading')
app.debug = True



app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
