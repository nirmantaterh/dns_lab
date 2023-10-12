from socket import *

print('====================================')
print('Hello from the authoritative server.')
print('====================================')
print()


dnsTable = []
serverPort = 53533
serverSock = socket(AF_INET, SOCK_DGRAM)
serverSock.bind(("", serverPort))
while True:
    reqMsg, clientAddr = serverSock.recvfrom(2048)
    reqInfo = reqMsg.decode().split('\n')
    # Length=4 means this message is sent by a fibonacci server for registration.
    if len(reqInfo) == 4:
        # Generate DNS record and save it into the DNS table.
        dnsRec = ['', '', '', '']
        dnsRec[0] = (reqInfo[0].split('='))[1]
        dnsRec[1] = (reqInfo[1].split('='))[1]
        dnsRec[2] = (reqInfo[2].split('='))[1]
        dnsRec[3] = (reqInfo[3].split('='))[1]
        dnsTable.append(dnsRec)
        print('DNS table\'s content updated. Current content is:')
        print(dnsTable)
        print()
        # Send a reply back to the requesting fibonacci server.
        replyMsg = 'DNS registration successful!'
        replyMsg = replyMsg.encode()
        serverSock.sendto(replyMsg, clientAddr)
    # Length=2 means this message is sent by a user server for DNS query.
    if len(reqInfo) == 2:
        # Extract host name from this message and search for its corresponding record.
        hName = (reqInfo[1].split('='))[1]
        replyMsg = 'DNS not found.'
        for dnsRec in dnsTable:
            if dnsRec[1] == hName:
                replyMsg = 'TYPE='+dnsRec[0]+'\nNAME='+dnsRec[1]+'\nVALUE='+dnsRec[2]+'\nTTL='+dnsRec[3]
        # Send a reply back to the requesting user server.
        replyMsg = replyMsg.encode()
        serverSock.sendto(replyMsg, clientAddr)