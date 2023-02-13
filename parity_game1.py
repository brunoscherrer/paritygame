#!/usr/bin/python3


# code for parity game


from random import seed, randint, sample
from copy import deepcopy
import numpy as np

players=['EVEN/MAX','ODD/MIN '] # player 0 is Eve (wants even), player 1 is Adam (wants odd)


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
                               randint(0,nb_priorities-1) )   #  priority
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
    
    def value_iteration(self, T, v, no_update=[], verbose=False):  # (standard) Value Iteration (for a payoff game) for T steps from 0

        if verbose:
            print("Running Value Iteration")
            
        for t in range(T):

            w = deepcopy(v)
            
            for state in self.states:

                if state.nb not in no_update:
                
                    if state.player==0: # Even/Max
                        y = state.next_states[0]
                        q = float("-inf")
                        for y2 in state.next_states:
                            q2 = state.val + w[y2]
                            if q2 >= q:
                                y = y2
                                q = q2
                    else: # Odd/Min
                        y = state.next_states[0]
                        q = float("inf")
                        for y2 in state.next_states:
                            q2 = state.val + w[y2]
                            if q2 <= q:
                                y = y2
                                q = q2

                    v[state.nb]=q

            if verbose:
                print(t,"v=",v)

        return(v)

    
    def find_winning_region(self, verbose=False):

        if verbose:
            print("Let's find a winning region for the game")
            self.print()

        A = set( [ state.nb for state in self.states ] )
        g = deepcopy(self)

        while(True):

            nb_states = len(A)
            all_priorities = set ( [ state.val for state in g.states ] )
            
            p = max(all_priorities)
            i = p%2
            
            # build the payoff game
            g2 = deepcopy(g) 
            for state in g2.states:
                if state.val==p:
                    state.val=[1,-1][i]
                else:
                    state.val=0

            if verbose:
                print("One considers the following payoff game")
                g2.print()

            # run nb_states steps of value iteration from v=0
            v = dict()
            for state in g2.states:
                v[state.nb]=0
            v = g2.value_iteration(nb_states*(nb_states+1),v,[],verbose)

            if verbose:
                print("T^(n^2+n) 0 =",v)

            B = set( [ state.nb for state in g2.states if v[state.nb]==0 ] )
            C = set( [ state.nb for state in g2.states if abs(v[state.nb])>=nb_states ] )
            
            if verbose:
                print("B=",B)
                print("C=",C)

            if C!=set():  
                return C,i,p
                
            # If C is empty, then B is necessarily not empty    #################################
            #if B==set():   # Player i wins (with parity p) on A  #################################
            #    return A,i,p    #################################

            if verbose:
                print(players[i],"cannot win on any subset of",A,"with priority",p,"by being forced to go to",B)

            g = g.copy_and_remove(A - B) # restrict the game to B
            A=B

        

        
    def solve(self, verbose=False):

        all_states = set( [ state.nb for state in self.states ] )
        nb_states = len(all_states)
        
        # initialize v
        v = dict()
        for i in all_states:
            v[i]=0

        while True:

            # 1) Propagate non-zero values
            
            g = deepcopy(self)   
            for state in g.states:
                state.val=0
            w = g.value_iteration(nb_states,v,[x for x in all_states if v[x]!=0],verbose)
            
            A = set( [ i for i in all_states if w[i]==0 ] )

            if verbose:
                print("w=",w)
                print("A=",A)

            if A==set():
                
                W = [ set(), set() ]
                for i in all_states:
                    if w[i]<0:
                        W[1].add(i)
                    else:
                        W[0].add(i)

                if verbose:
                    print ("It is over: W=",W)

                return(W)

            # 2) Look for a winning region
            
            g2 = self.copy_and_remove(all_states-A) # g2 = game restricted to A
            
            A2,j,p = g2.find_winning_region(verbose)

            for i in A2:   # update v consequently
                v[i]=[1,-1][j]
                
            if verbose:
                print("* Region A2=",A2,"is won by",players[j])
                print("v=",v)
        
         



    
# Main: test the algorithm vs Zielonka

n=4
a=2
d=n


for i in range(571,10000):

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
