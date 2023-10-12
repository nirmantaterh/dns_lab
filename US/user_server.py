from flask import Flask, abort, request
import requests
from socket import *
app = Flask(__name__)

@app.route('/')
def Hint():
    return 'Please refer to /fibonacci according to the right argument format.'

@app.route('/fibonacci')
def ResolvePath():
    hName = request.args.get('hostname')
    fsPort = request.args.get('fs_port')
    seqNum = request.args.get('number')
    asIp = request.args.get('as_ip')
    asPort = request.args.get('as_port')
    if hName == None or fsPort == None or seqNum == None or asIp == None or asPort == None:
        abort(400) # 400 Bad Request if any argument is not given.
    
    # Resolve path and send UDP message to authoritative server for DNS query.
    userSock = socket(AF_INET, SOCK_DGRAM)
    requestMsg = 'TYPE=A\nNAME='+hName
    requestMsg = requestMsg.encode()
    userSock.sendto(requestMsg, (asIp, 53533))

    # Receive query results from the authoritative server.
    replyMsg, serverAddr = userSock.recvfrom(2048)
    if replyMsg.decode() == 'DNS not found.':
        abort(400) # No DNS record also leads to 400 Bad Request.
    # Show the results from fibonacci server's /fibonacci path using the IP address received.
    replyInfo = replyMsg.decode().split('\n')
    fsIP = 'http://'+(replyInfo[2].split('='))[1]+':'+fsPort+'/fibonacci?number='+seqNum
    r = requests.get(fsIP)
    r.encoding = 'utf-8'
    return r.text


app.run(host='0.0.0.0',
        port=8080,
        debug=True)