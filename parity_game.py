#!/usr/bin/python3


# code for parity game


from random import seed, randint, sample
from copy import deepcopy
import numpy as np


inf = float("inf")

players=['EVEN/MAX','ODD/MIN '] # player 0 is Eve (wants even), player 1 is Adam (wants odd)


def smaller(x,y):
    return (x==[] and y==[]) or x[0]<y[0] or (x[0]==y[0] and smaller(x[1:],y[1:]))

class state:

    def __init__(self, nb, player, next_states, val):
        self.nb = nb
        self.player = player
        self.next_states = next_states
        self.val = val

    def print(self, end=''):
        print("State",self.nb, "player:",self.player,players[self.player],"next_states:",self.next_states,"val:",self.val, end=end)
        

# class for parity and payoff games 
        
class game:   
    
    def __init__(self, nb_states, nb_actions, nb_priorities): # init a random parity game

        self.states = [ state( i, #  state number,
                               randint(0,1),   # random player
                               [randint(0, nb_states-1) for a in range(nb_actions)],  # random next states
                               randint(1,nb_priorities) )   #  priority
                        for i in range(nb_states) ]

    def print(self):
        
        for state in self.states:
            state.print(end="\n")


    # ZIELONKA ALGORITHM (reference algorithm)

    def attractor(self, i, U): #  computes the attractor of set U for player i 
        
        oldattr = set()
        attr = U.copy()

        while( attr != oldattr ):

            oldattr = attr.copy()
            
            for state in self.states:
                if state.player==i:
                    for j in state.next_states:
                        if j in attr:
                            attr.add(state.nb)
                            break
                else: # opponent
                    test = map( lambda j: j in attr, state.next_states )
                    if False not in test:
                        attr.add(state.nb)
                        
        return attr


    def copy_and_remove(self, A):  # remove nodes of the set A
        
        g = deepcopy(self)
        
        oldB = set()
        B = A.copy()

        while (B != oldB):

            oldB = B.copy()
            
            for state in g.states.copy():  # (copy is important)
                if state in g.states and state.nb in B:
                    g.states.remove(state)
                else:
                    for j in B:
                        if j in state.next_states:
                            state.next_states.remove(j)
                    if state.next_states == []:
                        B.add(state.nb)      # if no more successor, add node for removal

        return g
    
        
    def solve_zielonka(self):  # Zielonka's algorithm
        
        all_priorities = set ( [ state.val for state in self.states ] )
        all_states = set( [ state.nb for state in self.states ] )
        
        p = max(all_priorities)
        i = p%2
        
        if p==min( [state.val for state in self.states  ] ):

            W = [ set(), set() ]
            W[i] = all_states
            return W

        U = set ( [ state.nb  for state in self.states if state.val==p ] )
        A = self.attractor(i, U)
        if A==all_states:
            W = [ set(), set() ]
            W[i] = all_states
            return W

        g2 = self.copy_and_remove(A)
        W2 = g2.solve_zielonka()

        if W2[1-i] == set():

            W = [ set(), set() ]
            W[i] = all_states
            return W

        B = self.attractor(1-i, W2[1-i])
        if B==all_states:
            W = [ set(), set() ]
            W[1-i] = all_states
            return W

        g3 = self.copy_and_remove(B)
        W3 = g3.solve_zielonka() 

        W = [ set(), set() ]
        W[i] = W3[i]
        W[1-i] = W3[1-i].union(B)
        return W



    # ALGORITHM

    def value_iteration(self, verbose=False):  

        if verbose:
            print("Running Value Iteration")
            
        all_states = [ state.nb for state in self.states ]
        nb_states = len(all_states)
        mp = max ( [ state.val for state in self.states ] )
        
        v=dict()
        
        for i in all_states:
            v[i]=[0]*(mp+1)
            
            
        for t in range(nb_states*nb_states):

            w = deepcopy(v)
            w0 = deepcopy(v0)
            
            for state in self.states:
                
                if state.player==0: # Even/Max
                    q = [ -inf ]*(mp+1)
                    for y2 in state.next_states:
                        q2 = deepcopy(w[y2])
                        i = state.val%2
                        z = 1-2*i
                        q2[mp-state.val] += z
                        if smaller2(q,q2, nb_states):
                            q = q2
                else: # Odd/Min
                    q = [ inf ]*(mp+1)
                    for y2 in state.next_states:
                        q2 = deepcopy(w[y2])
                        i = state.val%2
                        z = 1-2*i
                        q2[mp-state.val] += z
                        if smaller2(q2,q, nb_states):
                            q = q2

                v[state.nb]=q

            if verbose:
                print(t,"v=",v)

        for i in all_states:
            v[i] = [ abs(x) for x in v[i] ]
                
        return(v)

            
    def solve(self, verbose=False):

        all_states = set( [ state.nb for state in self.states ] )
        nb_states = len(all_states)
        mp = max ( [ state.val for state in self.states ] )
        
        v = self.value_iteration(verbose)
        print("v=",v)

        w=dict()
        for i in all_states:
            for k in range(mp+1):
                if v[i][k] > 0:
                    if v[i][k] >= nb_states:
                        w[i]=(mp-k)*(1-2*((mp-k)%2))
                    else:
                        w[i]=0
                    break

        print("w=",w)

        
        for t in range(nb_states):

            w2 = deepcopy(w)
            
            for state in self.states:
                
                if state.player==0: # Even/Max
                    q = -inf
                    for y2 in state.next_states:
                        q = max(q, w2[y2])
                else: # Odd/Min
                    q = inf
                    for y2 in state.next_states:
                        q = min(q, w2[y2])

                w[state.nb]=q

            if verbose:
                print(t,"w=",w)

        W = [set(),set()]
        for i in all_states:
            if w[i]>0:
                W[0].add(i)
            elif w[i]<0:
                W[1].add(i)

        
                
        return(W)

        



    
# Main: test the algorithm vs Zielonka

n=4
a=2
d=n


for i in range(0,10000):

    seed(i)
    g = game(n,a,d)
    
    print("* Seed=",i)    
    g.print()
    
    W = g.solve_zielonka()
    print("Solution (Zielonka):",W,"\n")
    
    W2 = g.solve(verbose=True)
    print("Solution:",W2,"\n\n")
    
    if W!=W2:
        print("STOP")
        exit(1)
