from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_cors import CORS

from models import db, Message

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods =['GET', 'POST']) 
def messages():
    if request.method =='GET':
        messages = Message.query.order_by('created_at').all()
        # flask does jsonify for us? 
        response = [ message.to_dict() for message in messages] 
        # response = make_response(
        #     jsonify([ message.to_dict() for message in messages]) #map from each message in messages to object 
        #     # js messages.map(message => message.to_dict())
        # )
        # return 'this is where messages will go'
    elif request.method == 'POST':
        data = request.get_json()
        # get from model Message
        message = Message(
            body = data['body'],
            username = data['username']
        )
        # do something with message
        db.session.add(message)
        db.session.commit()
        response = make_response(
            jsonify(message.to_dict()), 201
            # 201 http code created
        )
    return response
    # messages = Message.query.all()
    # serialized_messages=[]
    # for message in messages:
    #     serialized_messages = {
    #         'id': message.id,
    #         'body': message.body,
    #         'username': message.username,
    #         'created_at': message.created_at.strftime('%Y-%m-%dT%H:%M:%S'),
    #     }
    #     serialized_messages.append(serialized_messages)
    # return jsonify(serialized_messages)
    

@app.route('/messages/<int:id>', methods =['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()

    if request.method == 'PATCH':
        newMessageData = request.get_json()
        for key in newMessageData:
            setattr(message, key, newMessageData[key])
        db.session.add(message)
        db.session.commit()

        response = make_response(jsonify(message.to_dict()))
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        response = jsonify({'message': f'deleted message {id}'})
    return response

    # return f'this is where we get message by id info {id}'
    message = Message.query.get_or_404(id)

    serialized_message ={
        'id': message.id,
        'body': message.body,
        'username': message.username,
        'created_at': message.created_at.strftime('%Y-%m-%dT%H:%M:%S'),
    }
    return jsonify(serialized_message)

if __name__ == '__main__':
    app.run(port=4000)
