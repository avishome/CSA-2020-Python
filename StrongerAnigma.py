import socket
import string
LEN_PREIOD = 26
conf_from_0 = [[] for _ in range(LEN_PREIOD)]
to_send = """
HELLO FIELD AGENT!
COMMANDS:
    SEND-SECRET-DATA
    GET-SECRET-DATA
    GOODBYE
    """
to_send = "".join([u for u in to_send if u in string.ascii_uppercase])
LEN_OF_INTRO = len(to_send)
REST_AFTRE_INTRO = LEN_PREIOD - (LEN_OF_INTRO%LEN_PREIOD)
count = 0
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("18.156.68.123", 80))
s.recv(58)
m1 = s.recv(88)
s.send(("A"*(REST_AFTRE_INTRO)+"\n").encode())
s.recv(23)
m2 = s.recv(88)
if m1 == m2:
  m2 = "".join([u for u in m2.decode() if u in string.ascii_uppercase])
  print(m2)
  for i,uv in enumerate(zip(to_send,m2)):
    conf_from_0[i%LEN_PREIOD] += [(uv[0],uv[1])]
else:
  print("Error in cycle length")
count += LEN_OF_INTRO

for it in range(0,30):
  s.send(("AA" + "\n").encode())
  count += 2
  s.recv(23)
  m2 = s.recv(88)
  m2 = "".join([u for u in m2.decode() if u in string.ascii_uppercase])
  for i,uv in enumerate(zip(to_send,m2),start = count):
    conf_from_0[i%LEN_PREIOD] += [(uv[0],uv[1])]
  count += LEN_OF_INTRO
  print(count,end = " ")

msgA = [[z[1] for z in v if z[0] == u] if u in string.ascii_uppercase else [u] for u,v in zip("GETSECRETDATA",(conf_from_0*2)[count%LEN_PREIOD:])]
msg_in_zero = "".join([i[0] for i in msgA if len(i)])
msg_in_zero = msg_in_zero[:3]+"-"+msg_in_zero[3:9]+"-"+msg_in_zero[9:]
s.send((msg_in_zero+"\n").encode())
count += len("GETSECRETDATA")
msg_of_GETSECRETDATA = s.recv(1000).decode()
s.close()

msg_of_GETSECRETDATA = msg_of_GETSECRETDATA[:-2]
msg_of_GETSECRETDATA2 = "".join(msg_of_GETSECRETDATA.replace("{","").split("_"))
msgA = [[z[0] for z in v if z[1]==u] if any([z[1]==u for z in v]) else ["?"] for u,v in zip(msg_of_GETSECRETDATA2,(conf_from_0*5)[count%LEN_PREIOD:])]

m = [i[0] for i in msgA if len(i)]
m.insert(msg_of_GETSECRETDATA.find("{",0),"{")
p =msg_of_GETSECRETDATA.find("_",0)
while p != -1:
  m.insert(p,"_")
  p = msg_of_GETSECRETDATA.find("_",p+1)
m.insert(msg_of_GETSECRETDATA.find("}",p+1),"}")
print("\n","".join(m)[:-1])
