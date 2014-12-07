#!/usr/bin/python
# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()
from SmartClinicServ import create_app
from flask.ext.socketio import SocketIO, join_room, leave_room, emit
from flask.ext.mail import Mail

import sys
reload(sys)

sys.setdefaultencoding("utf-8")

numRooms = 0
roomCount = {}
application = create_app()
socketio = SocketIO(application)

@socketio.on('asdmessage')
def handle_message(message):
    print('received message: ' + message)
    socketio.emit("response ", "socket com test")

@socketio.on('message')
def exchange_message(message, room):
    print room
    socketio.emit('message', message, room=room)

# @socketio.on('random create or join')
# def handle_random_room(room):
#     if(room == '') {
#             client.hkeys("rooms key", function (err, replies) {
#                 console.log("replies num " + replies.length);
#                 if(replies.length > 1) {
#                     room = replies[1];
#                     client.hdel("rooms key", room);
#                     console.log("delete room ", room);
#                 }
#                 else {
#                     room = uuid();
#                     client.hset("rooms key", room, 'for global or gender option ', redis.print);
#                 }
#             });
#         }
#
#         var numClients = io.sockets.clients(room).length; //clients in room
#
#         log('RandomRoom ' + room + ' has ' + numClients + ' client(s)');
#         log('Request to create or join room', room);
#
#         if (numClients == 0){
#             socket.join(room);
#             socket.emit('created', room);
#
#         } else if (numClients == 1) {
#             io.sockets.in(room).emit('join', room);
#             socket.join(room);
#             socket.emit('joined', room);
#         } else {
#             socket.emit('full', room);
#         }

@socketio.on('create or join')
def handle_spec_room(room):
    numClients = 0
    print roomCount.get(room)
    if roomCount.get(room) == None:
        roomCount[room] = 0
        numClients = 0
    else:
        numClients = roomCount.get(room)

    print 'test'

    if numClients == 0:
        join_room(room)
        socketio.emit('created', room)
        print 'created room'
        roomCount[room] = 1

    elif numClients == 1:
        socketio.emit('join', room)
        print 'join room'
        emit('joined', 'testfile')
        join_room(room)
        print 'joined room'
        roomCount[room] = 2
    else:
        socketio.emit('full', room)


if __name__ == '__main__':
     #application.run(host='0.0.0.0', port=5000, debug=True)
    socketio.run(application, host='0.0.0.0', port=5000)

