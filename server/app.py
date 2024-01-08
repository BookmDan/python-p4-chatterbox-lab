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

@app.route('/messages') #, methods =['GET']
def messages():
    return 'this is where messages will go'
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
    

@app.route('/messages/<int:id>', methods =['GET'])
def messages_by_id(id):
    message = Message.query.get_or_404(id)

    serialized_message ={
        'id': message.id,
        'body': message.body,
        'username': message.username,
        'created_at': message.created_at.strftime('%Y-%m-%dT%H:%M:%S'),
    }
    return jsonify(serialized_message)

if __name__ == '__main__':
    app.run(port=5555)
