from time import time
start=time()
q=0
for i in range(0,1000):
    q+=i
for i in range(2,930):
    q+=i
print(time()-start)
start=time()
q=0
for i in range(0,1000):
    if i>0:
        q+=i
    q+=i
print(time()-start)