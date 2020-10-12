from multiprocessing import Pool
import socket
global BACK, BLOCK, INTTOLETTR, LETTERTOINT
BACK = 2
BLOCK = 0
LETTERTOINT = {"l": 0, "r": 1, "u": 2, "d": 3}
INTTOLETTR = {0: "l", 1: "r", 2: "u", 3: "d"}


class Ma:
    def __init__(self, x, y, sock):
        self.x = x
        self.y = y
        self.setpsCounter = 0
        self.solutions = []  # optional places to teasure.
        self.prev = []  # arr of corrent path in maze
        self.s = sock
        self.lastStep = 0
        resp = str(self.s.recv(1024))
        print(resp)
        self.LookAround()

    def UpdatePrev(self):
        '''
        Mark return way for countinue after block with BACK.
        '''
        if self.lastStep == 1 or self.lastStep == 3:
            self.prev[-1][self.lastStep - 1] = BACK
        else:
            self.prev[-1][self.lastStep + 1] = BACK

    def BlockPrev(self):
        '''
        Mark block way with BACK.
        '''
        if self.lastStep == 1 or self.lastStep == 3:
            self.prev[-1][self.lastStep - 1] = BLOCK
        else:
            self.prev[-1][self.lastStep + 1] = BLOCK

    def LookAround(self):
        '''
        Request to recive open ways,  
        '''
        self.s.send("i".encode())
        resp = str(self.s.recv(1024))
        while "What " in resp:
            resp = str(self.s.recv(1024))
        m = resp.replace("/", "").replace("'", "").replace("\\",
                                                           "").replace("n", "").replace(", ", "=").split("=")[1::2]
        self.prev += [m]
        resp = self.s.recv(1024)

    def GoStep(self, where):
        '''
        where (str) - l,r,u,d
        '''
        self.lastStep = LETTERTOINT[where]
        self.s.send(where.encode())
        resp = self.s.recv(1024)
        resp = self.s.recv(1024)
        self.x, self.y = self.clacNewPlace(where)
        if self.setpsCounter != -1:
            self.setpsCounter += 1
        else:
            self.setpsCounter = 0
        if self.setpsCounter % 10 == 0:
            self.clacTrease()
            
        self.LookAround()
        self.UpdatePrev()

    def clacTrease(self,i):
        '''
        We get the distance diagonally when we are close enough. 
        We can narrow the search to 4 points on the map.
        '''
        self.s.send("g".encode())
        res = self.s.recv(1024)
        print(self.x, self.y, res)
        self.s.recv(1024)
        if "Your distance from the treasure is" in res.decode():
            self.setpsCounter = -1 # Get distance in the next step as well
            des = int(res.decode().split(" ")[-1][:-1])
            print(self.x, self.y, des)
            res = [(y, i) for y in range(100)
                   for i in range(100) if i**2 + y**2 == des]
            if len(res) == 2:
                disA,disB = res[0]
                tempSol = []
                tempSol += [(self.x-disA, self.y-disB)]
                tempSol += [(self.x+disA, self.y-disB)]
                tempSol += [(self.x-disA, self.y+disB)]
                tempSol += [(self.x+disA, self.y+disB)]
                tempSol += [item[::-1] for item in tempSol] # and maybe the oposite
                print(tempSol)
                if len(self.solutions) == 0:
                    self.solutions += tempSol
                else:
                    self.solutions = list(set(self.solutions) & set(tempSol))
                    print(self.solutions)
            if len(self.solutions) == 1: # we found it! 
                self.s.send("s".encode())
                print(self.s.recv(1024))
                x,y = self.solutions[0]
                self.s.send(
                    ("("+str(x)+","+str(y)+")").encode())
                print(
                    ("("+str(x)+","+str(y)+")"))
                print(self.s.recv(1024))
                print("_flag!_"*20)
                print(self.x, self.y)
                self.s.close()

    def GoBack(self):
        self.lastStep = [u for u, v in enumerate(self.prev[-1]) if v == BACK][0]
        where = INTTOLETTR[self.lastStep]
        self.x, self.y = self.clacNewPlace(where)
        del self.prev[-1]
        self.BlockPrev()
        self.s.send(where.encode())
        resp = (self.s.recv(100), self.s.recv(100))

    def clacNewPlace(self, where):
        x, y = self.x, self.y
        if where == "l":
            x -= 1
        elif where == "r":
            x += 1
        elif where == "u":
            y += 1
        elif where == "d":
            y -= 1
        return (x, y)


def Independentgame(num):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((URL_TO_CHELLANGE, 80))
    s.send("hi\n\n".encode())
    q = [s.recv(1024) for i in range(12)]
    x = str(q[10]).split("(")[1].split(")")[0].split(",")
    game = Ma(int(x[0]), int(x[1]), s)
    i = 0
    try:
        while len(game.prev) > 0 and i < 300:
            i += 1
            if all([i != "1" for i in game.prev[-1]]):
                game.GoBack()
                continue

            for direct in [0,2,1,3]:
                if game.prev[-1][direct] == "1":
                    game.GoStep(INTTOLETTR[direct])
                    break

    except:
        print("except", game.prev)
        pass
    return game

if __name__ == "__main__": 
    pool = Pool(processes=100)              # Start a worker processes.
    with pool:
        res = pool.map(Independentgame, list(range(100)))
