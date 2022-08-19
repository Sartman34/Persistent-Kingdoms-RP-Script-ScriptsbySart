from scapy.all import IP, TCP, send, sendp, sr1, RandShort
import socket
import sys
import time

ping_message = "\
GET /handlerservers.ashx?type=ping&keys&hidden=false HTTP/1.1\r\n\
Connection: Keep-Alive\r\n\
User-Agent: Mount Blade HTTP\r\n\
Host: warbandmain.taleworlds.com\r\n\
\r\n\
"

##def sr1(*args, **kwargs):
##    old_stdout = sys.stdout
##    old_stderr = sys.stderr
##    sys.stdout = sys.__stdout__
##    sys.stderr = sys.__stderr__
##
##    scapy.all.sr1(*args, **kwargs)
##
##    sys.stdout = old_stdout
##    sys.stderr = old_stderr
    
def logging_print(*string, end = "\n", sep = " "):
    print(*string, end = end, sep = sep)
    
    file = open("_pyshark logs.txt", "a")
    old_stdout = sys.stdout
    sys.stdout = file
    print(*string, end = end, sep = sep)
    sys.stdout = old_stdout
    file.close()

def calTSN(tgt):
    port = RandShort()
    seqNum = 0
    preNum = 0
    diffSeq = 0
    for x in range(1, 5):
##        if preNum != 0:
        preNum = seqNum
        pkt = tgt / TCP(sport = port, dport = 80)
        ans = sr1(pkt, verbose=0)
        seqNum = ans.getlayer(TCP).seq
        diffSeq = seqNum - preNum
        print ('[+] TCP Seq Difference: ' + str(diffSeq))
##        return seqNum + diffSeq

##ip=IP(src="2.3.4.5", dst="1.2.3.4")
##TCP_SYN=TCP(sport=1500, dport=80, flags="S", seq=100)
##TCP_SYNACK=sr1(ip/TCP_SYN)
##
##my_ack = TCP_SYNACK.seq + 1
##TCP_ACK=TCP(sport=1500, dport=80, flags="A", seq=101, ack=my_ack)
##send(TCP_ACK/ip)
##
##my_payload="space for rent!"
##TCP_PUSH=TCP(sport=1500, dport=80, flags="PA", seq=102, ack=my_ack)
##sendp(ip/TCP_PUSH/my_payload)

port = RandShort()
ip_address = IP(dst = socket.gethostbyname("warbandmain.taleworlds.com"))

calTSN(ip_address)

##while True:
##    send(ip_address / TCP(sport = port, dport = 80, flags = "S", seq = 0))
##    time.sleep(0.1)
##send(ip_address / TCP(sport = port, dport = 80, flags = "A", seq = 1, ack = 1))
##send(ip_address / TCP(sport = port, dport = 80, flags = "A", seq = 1, ack = 1) / ping_message)
##sendp(ip_address / TCP(sport = port, dport = 80, flags = "PA", seq = 1, ack = 1) / "hi")
input()

