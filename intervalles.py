#!/usr/bin/python

n=5

g=[0]
for i in range(1,n+1):
    g.append( -pow(-(n+1),i-1) )

print(g)
print()

for i in range(1,n+1):
    x = g[i]+(n-1)*g[i-1]
    y = n*g[i]
    print(i, min(x,y),max(x,y))
