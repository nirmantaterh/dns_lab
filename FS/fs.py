from http import client
from flask import Flask, abort, request, Response
from socket import *
app = Flask(__name__)


@app.route('/')
def hint():
    return 'Please refer to each pages according to the given formats.'

@app.route('/register', methods=['PUT'])
def register():
    req = request.get_json()
    hName = req["hostname"]
    ip = req["ip"]
    asIp = req["as_ip"]
    asPort = req["as_port"]

    # Send UDP message to the authoritative server.
    clientSock = socket(AF_INET, SOCK_DGRAM)
    udpMsg = 'TYPE=A\nNAME='+hName+'\nVALUE='+ip+'\nTTL=10'
    print(udpMsg)
    udpMsg = udpMsg.encode()
    clientSock.sendto(udpMsg, (asIp, 53533))
    # Wait for reply from the authoritative server.
    replyMsg, serverAddr = clientSock.recvfrom(2048)
    clientSock.close()

    # Registration successful.
    # Returns 201.
    return Response('HTTP response 201:\n'+'Hostname: '+hName+',\nIP: '+ip+',\nas IP: '+asIp+',\nas port: '+asPort, status=201)

@app.route('/fibonacci')
def fibFunc():
    baseNum = request.args.get('number')
    # Only takes non-negative integers as input.
    if not baseNum.isdecimal():
        abort(400)
    else:
        # Fibonacci calculations.
        baseNum = int(baseNum)
        fibPre = 0
        fibCur = 1
        if baseNum > 0:
            for i in range(baseNum):
                temp = fibPre
                fibPre = fibCur
                fibCur = temp + fibCur
        # Fibonacci number generated.
        # Returns 200.
        return Response('Fibonacci number generated.\n'+'The result is: '+str(fibPre), status = 200)

app.run(host='0.0.0.0',
        port=9090,
        debug=True)