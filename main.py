from flask import Flask, render_template, session,redirect,request
from flask_socketio import SocketIO, emit,send
from settings import app,socketio
from models import*
import secrets

app.secret_key = secrets.token_hex(16)


@app.route('/')
def index():
    return render_template('base.html')



# @app.route('/signup',methods = ['POST','GET'])
@app.route('/signup',methods = ['POST', 'GET'])
def signup():
    if request.method=='POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if User.query.filter_by(name=username).first()==username:
            return ("username not avalibale")
        if user:
            return("Email already in used")
        if password != request.form['Conform_password']:
            return('Worng Password')
        user = User(name=username,email=email,password=password )
        db.session.add(user)
        db.session.commit()
        print("Signup Succcessfull")
        return redirect('login')
    return render_template('signup.html')



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



@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')



# @socketio.on('addfriend', namespace='/addfrinds')
@app.route('/add_friends/<friend_id>')
def add_friend(friend_id):
    if 'user_id' in session:
        user=User.query.get(session['user_id'])
        # user = User.query.get(user_id)
        friend = User.query.get(friend_id)
        user.friends.append(friend)
        db.session.commit()
        return render_template('add_friends.html')
    return redirect("login")



@app.route('/search', methods=['POST','GET'])
def search_user():
    if 'user_id' in session:
        user_neme= User.query.get(session['user_id'])
        if request.method == 'POST':
            search_query = request.form['search']
            data = User.query.filter(User.name.contains(search_query)).all()
            if data:
                print("USER DATA FOR FRIENDS:",data)
                return render_template('add_friends.html',user_neme=user_neme,data=data)
            else:
                return("User Not found")
        return render_template('add_friends.html',user_neme=user_neme)
    return redirect('login')


@app.route('/friends',methods = ['POST', 'GET'])
def get_friend():
    if 'user_id' in session:
        # user = User.query.get(user_id)
        user=User.query.get(session['user_id'])
        friends = user.friends.all()

        return render_template('friends.html',user=user,friends=friends)
    return redirect ('login')



@app.route('/messages/<friend_id>')
def message(friend_id):
    if 'user_id' in session:
        friend=User.query.get(friend_id)
        print("session['user_id'] : ",(session['user_id']))
        print("Frind id : ",(friend.id))

        messages = Message.query.filter(((Message.sender_id == session['user_id']) & (Message.recipient_id == friend_id)) | ((Message.sender_id == friend_id) & (Message.recipient_id == session['user_id']))).all()

        print('message' ,messages)


        return render_template("message.html",friend=friend,messages=messages)
    return redirect('login')





@socketio.on('send_message',)
def handle_send_message(data):
    # Save the message to the database
    print("DATA IS ",data)
    # user_id = data['user_id']
    friend_id = data['friend_id']
    message = data['message']
    new_message = Message(sender_id=session['user_id'], recipient_id=friend_id, message_text=message)
    db.session.add(new_message)
    db.session.commit()

    # Send the new message to all connected clients
    socketio.emit('new_message', {'message': message}, broadcast=True)





if __name__ == '__main__':
    with app.app_context():
        # socketio.run(app)
        socketio.run(app, host='192.168.29.71', port=5000)