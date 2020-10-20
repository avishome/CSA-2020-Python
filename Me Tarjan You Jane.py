import math
arr = open(r"tree.txt","rb").read()
pa = eval(open(r"pairs.txt","r").read())
def getFat(f):
  arr1 = []
  while f != 0:
    f = math.floor((f - 1)  / 2)
    arr1 += [f]
  return arr1

"".join([chr(arr[max(set(getFat(p[0])) & set(getFat(p[1])))]) for p in pa])
