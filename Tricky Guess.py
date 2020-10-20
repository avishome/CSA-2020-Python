import socket,string
ar = []
word = words
a = string.ascii_lowercase
sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM)
sock.connect(("tricky-guess.csa-challenge.com",2222))
msg = sock.recv(1024).decode()
while "GO !" not in msg:
  msg = sock.recv(1024).decode()
for i in range(5):
  sock.send(ens[i][0][0].encode())
  fi = res = int(sock.recv(100).decode()[:-1])
  print(ens[i][0][0],res)
  sock.send(ens[i][0][1].encode())
  se = res = int(sock.recv(100).decode()[:-1])
  print(ens[i][0][1],res)
  th = set(a) - (set(ens[i][0][1]) | set(ens[i][0][0]))
  #print(set(a) - (set(mashlim[0]) | set(words[0])),set(mashlim[0]) & set(words[0]))
  word = [n for n in word if len(set(n) & set(ens[i][0][0]))==fi]
  word = [n for n in word if len(set(n) & set(ens[i][0][1]))==se]
  word = [n for n in word if len(set(n) & set(th))==12-fi-se]
if len(word) == 1:
  sock.send(word[0].encode())
  print(sock.recv(2000).decode())
