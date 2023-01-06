from flask import Flask, render_template, session,redirect,request
from flask_socketio import SocketIO, emit,send
from settings import app,socketio
from models import*
import secrets

app.secret_key = secrets.token_hex(16)


@app.route('/')
def index():
    return render_template('base.html')



@app.route('/signup',methods = ['POST', 'GET'])
def signup():
    if request.method=='POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if User.query.filter_by(username=username).first()==username:
            return ("username not avalibale")
        if user:
            return("Email already in used")
        if password != request.form['Conform_password']:
            return('Worng Password')
        user = User(username=username,email=email,password=password )
        db.session.add(user)
        db.session.commit()
        print("Signup Succcessfull")
        return redirect('login')
    return render_template('signup.html')

# @socketio.on('signup', namespace='/signup')
# def handle_signup(data):
#     print('DATA is ',data)
#     emit('check_signup', data, broadcast=True)

# @socketio.on('check_signup', namespace='/signup')
# def handle_check_signup(data):
#     print("data received")
#     email = data['email']
#     client = User.query.filter_by(email=email).first()
#     if client:
#         emit('signup_failure', broadcast=True)
#     else:
#         name = data['name']
#         password = data['password']
#         new_client = User(name=name, email=email, password=password)
#         db.session.add(new_client)
#         db.session.commit()
        # emit('signup_success', {'id': new_client.id}, broadcast=True)











# @socketio.on('message')
# def handleMessage(msg):
# 	print('Message: ' + msg)
# 	message=Message(text=msg)
# 	db.session.add(message)
# 	db.session.commit()
# 	send(msg, broadcast=True)


@app.route('/login',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            if user.email==email and user.password==password:
                session['user_id'] = user.id
                print('Logged in successfully.')

                return redirect('friends')
            else:
                return("Wrong Password")
        else:
            return("Wrong Email or Password")
    
    return render_template('login.html')

# @socketio.on('login',namespace='/login')
# def handle_login(data):
#     print("login data :",data)
#     emit('check_login', data, broadcast=True)


# @socketio.on('check_login',namespace='/login')
# def handle_login(data):
#     email = data['email']
#     password = data['password']

#     user = User.query.filter_by(email=email).first()
#     user.set_password(password)
#     if user and user.check_password(password):
#         session['user_id'] = user.id
#         print("User logdin",session['user_id'])
#         emit('login_success', {'user_id': user.id}, broadcast=True)
#     else:
#         emit('login_failure', broadcast=True)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')



@socketio.on('addfriend', namespace='/addfrinds')
def add_friend(friend_id):
    if 'user_id' in session:
        user=User.query.get(session['user_id'])
        # user = User.query.get(user_id)
        friend = User.query.get(friend_id)
        user.friends.append(friend)
        db.session.commit()



@app.route('/friends')
def get_friend():
    if 'user_id' in session:
        # user = User.query.get(user_id)
        # user=User.query.get(session['user_id'])
        # friends = user.friends.all()

        return render_template('friends.html',msd="hello msg")
    return render_template('friends.html')

def send_msg(current_user,friend,message_text):
    if 'user_id' in session:
        user=User.query.get(session['user_id'])
        new_message = Message(sender=user, recipient=friend, message_text=message_text)
        db.session.add(new_message)
        db.session.commit()


def get_msg():
    if 'user_id' in session:
        user=User.query.get(session['user_id'])
        messages = Message.query.filter_by(sender_id=user, receiver_id=2).all()


# @app.route('/friends')
# def friends():
#     if 'user_id' in session:
#         user=User.query.get(session['user_id'])
#         # user_id = request.args.get('user_id')
#         user = User.query.filter_by(id=user.id).first()
#         friends = user.friends if user else []
#         return render_template('friends.html', friends=friends)


# @app.route('/friends')
# def friends():
#     return render_template('friends.html')


if __name__ == '__main__':
    with app.app_context():
        socketio.run(app)