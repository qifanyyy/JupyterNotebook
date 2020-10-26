'''
Evolutionary selection of a strategy for the coin clairvoyance game.

'Game' class plays the coin clairvoyance game with M pairs of opponents
for K rounds, where each player possesses initially 'bank' dollars.
At the beginning of each round there's 'pot' dollars in the pot,
and player 1 can bet 'bet' dollars.

'GeneSelect' inherits 'Game' class, which allows it to calculate the
strategies scores basing on the performance of the players using those
strategies.
'''

import numpy as np
import time
import matplotlib.pyplot as plt

            
class Game:
    
    def __init__(self,pot,bet,bank,M,K):
        '''
        pot -- size of the pot originally on the table.
        
        bet -- size of the bet.
        
        M -- number of player pairs in the population. Players are divided
        into two groups, each of size M. Players from group 1 look at the
        coin, players from group 2 don't look at the coin.
        
        bankroll -- bankroll of players from groups 1 and 2.
        
        N -- size of gene vectors for players from groups 1 and 2. Genes
        encode the probabilities for an action at each particular game
        situation. For player 1 we have size-2 gene, where the first 
        component encodes the probability of value bet, and the second
        component encodes the probability of bluff. For player 2 we have
        size-1 gene, with the component encoding the probability of call.
        
        genotype -- genotypes for players from groups 1 and 2.
        Initialized randomly.
        
        K -- number of rounds to play the game for each genotype, in order
        to evaluate the fit function.
        '''
        self.pot=pot
        self.bet=bet       
        self.M=M      
        self.bankroll={1:[bank for _ in range(self.M)],\
                       2:[bank for _ in range(self.M)]}
        self.N={1:2,2:1}
        G1=np.random.random(size=(self.M,self.N[1]))
        G1=np.array([[int(1000*x)/1000.0 for x in r] for r in G1])
        G2=np.random.random(size=(self.M,self.N[2]))
        G2=np.array([[int(1000*x)/1000.0 for x in r] for r in G2])
        self.genotype={1:G1,2:G2}
        self.K=K   
        
    def game_round(self):
        '''
        Plays one round of the game.
        Starts by matching up opponents from group 2 for players from group 1.
        '''
        opponents=np.random.choice(range(self.M),self.M,replace=False)
        for a1 in range(self.M):
            '''
            flip=0 --> heads.
            flip=1 --> tails.
            '''
            flip=np.random.randint(2)
            '''
            bet1  -- if Player 1 bets.
            call2 -- if Player 2 checks/calls.
            '''
            bet1=False
            call2=False
            '''
            Select an opponent for player a1 from group 1..
            '''
            a2=opponents[a1]
            '''
            Whether Player 1 bets with heads.
            '''
            if flip==0:
                r=np.random.random()
                if r<=self.genotype[1][a1][0]:
                    bet1=True
                else:
                    bet1=False
            '''
            Whether Player 1 bets with tails (bluffs).
            '''
            if flip==1:
                r=np.random.random()
                if r<=self.genotype[1][a1][1]:
                    bet1=True
                else:
                    bet1=False
            '''
            Player 2 calls (checks) all the checks from Player 1 or
            the bets from Player 1 if its strategy tells it to call.
            '''
            r=np.random.random()
            if bet1==False or (bet1==True and r<=self.genotype[2][a2][0]):
                call2=True
            else:
                call2=False
            if flip==0:
                if not bet1:
                    self.bankroll[1][a1]+=self.pot
                else:
                    if call2:
                        self.bankroll[1][a1]+=(self.pot+self.bet)
                        self.bankroll[2][a2]-=self.bet
                    else:
                        self.bankroll[1][a1]+=self.pot
            if flip==1:
                if not bet1:
                    self.bankroll[2][a2]+=self.pot
                else:
                    if call2:
                        self.bankroll[1][a1]-=self.bet
                        self.bankroll[2][a2]+=(self.pot+self.bet)
                    else:
                        self.bankroll[1][a1]+=self.pot
    
    def clear_bankroll(self):
        '''
        Restore the bankrolls to their default values.
        '''
        self.bankroll={1:[self.bank for _ in range(self.M)],\
                       2:[self.bank for _ in range(self.M)]} 
    def play(self):
        '''
        Play K rounds of the game. We will use the resulting final bankrolls
        as the fit function for the strategies.
        '''
        for r in range(self.K):
           self.game_round() 
           
class GeneSelect(Game):
    
    def __init__(self,pot,bet,bank,M,K,propagate,selection_rate):
        '''
        pot, bet, bank, M, K -- attributes of Game.
        
        propagate -- probability of having no mutation.
        
        selection_rate -- fraction of top performers taken to breed.
        
        fit_scores -- fit scores for strategies; will be derived from 
        bankrolls of players exercising those strategies.
        '''
        self.pot=pot
        self.bet=bet
        self.bank=bank
        self.M=M
        self.K=K
        Game.__init__(self,self.pot,self.bet,self.bank,self.M,self.K)
        self.propagate=propagate        
        self.selection_rate=selection_rate
        self.fit_scores={1:[1e-10 for _ in range(self.M)],\
                         2:[1e-10 for _ in range(self.M)]}
        np.random.seed(int(time.time()))  
        
    def update_fit_scores(self):
        '''
        Calculates fits of currently exisitng genotypes.
        Starts by resetting old bankroll records, plays the game to generate
        new resulting bankrolls, and normalizes the bankrolls to obtain the
        fit scores.
        '''
        self.clear_bankroll()
        self.play()
        sum1=np.sum(self.bankroll[1])+0.0
        sum2=np.sum(self.bankroll[2])+0.0
        for k in range(self.M):
            self.fit_scores[1][k]=self.bankroll[1][k]/sum1
            self.fit_scores[2][k]=self.bankroll[2][k]/sum2
            
    def offspring(self,i,j,group):
        '''
        Generates an offspring for parents 'i' and 'j' from the 'group'.
        We iterate over positions 'k' in the chromosome of size 'N[group]'.
        Each entry 'offspring[k]' of the offspring is obtained as a weighted
        average of the corresponding entries of the parents. The weights
        are chosen to be the fit scores of the parents. With probability
        '1-self.propagate' an additional mutation will be added. The mutation
        will decrease the value of the gene half of the time, shifting it
        by some uniformly picked number towards zero, and increase the value
        of the gene half of the time, shifting it by some uniformly picked
        number towards one.
        '''
        if i==j:
            raise ValueError("Select different parents for reproduction")
        offspring=[]
        for k in range(self.N[group]):
            gik=self.genotype[group][i,k]
            gjk=self.genotype[group][j,k]
            fi=self.fit_scores[group][i]
            fj=self.fit_scores[group][j]
            weighted_mean=(fi*gik+fj*gjk)/(fi+fj)
            r=np.random.random()
            if r<=1-self.propagate:
                sgn=np.random.random()
                if sgn<=0.5:
                    interval=weighted_mean
                    mutate=interval*np.random.random()
                    weighted_mean-=mutate
                else:
                    interval=1-weighted_mean
                    mutate=interval*np.random.random()
                    weighted_mean+=mutate
            offspring+=[weighted_mean]
        offspring=np.array(offspring)
        return offspring
    
    def new_generation(self):
        '''
        Updates generation of players basing on their fit scores.
        Agents are ranked and sorted by their scores. Top 'select_rate'
        are selected for reproduction. The rest, 'fill', will be filled
        by the offsprings of the selected players. The players are
        selected for breeding with probabilities proportional to their
        fit scores, so we normalize those, 'select_scores', to add up to
        one. We also keep track of the indices 'discard_indexes' of the
        players which we discarded, so that we can fill those with 
        offsprings of the selected players.
        '''
        all_scores={1:[],2:[]}
        for i in range(self.M):
            all_scores[1]+=[[i,self.fit_scores[1][i]]]
            all_scores[2]+=[[i,self.fit_scores[2][i]]]
        all_scores[1].sort(key=lambda x:x[1],reverse=True) 
        all_scores[2].sort(key=lambda x:x[1],reverse=True) 
        select=int(self.selection_rate*self.M)
        fill=self.M-select
        selected={1:np.array(all_scores[1][:select]),\
                  2:np.array(all_scores[2][:select])}
        select_indexes={1:selected[1][:,0],2:selected[2][:,0]}
        select_scores={1:selected[1][:,1]+1e-10,2:selected[1][:,1]+1e-10}
        select_scores[1]/=np.sum(select_scores[1])
        select_scores[2]/=np.sum(select_scores[2])
        select_scores[1][-1]=1-np.sum(select_scores[1][:-1])
        select_scores[2][-1]=1-np.sum(select_scores[2][:-1])
        discard_indexes={1:list(set(range(self.M))-set(select_indexes[1])),\
                         2:list(set(range(self.M))-set(select_indexes[2]))}
        ct=0
        while ct<fill:
            i,j=np.random.choice(select_indexes[1],2,p=select_scores[1],\
                                 replace=False)
            offspring=self.offspring(int(i),int(j),1)
            self.genotype[1][discard_indexes[1][ct]]=offspring
            i,j=np.random.choice(select_indexes[2],2,p=select_scores[2],\
                                 replace=False)
            offspring=self.offspring(int(i),int(j),2)
            self.genotype[2][discard_indexes[2][ct]]=offspring
            ct+=1        
    def evolve(self,generations):
        '''
        Run evolution for 'generations' number of generations.
        At each evolution run we produce the new generation using the
        new_generation() method, and update the fit scores for the
        produced generation.
        '''
        for _ in range(generations):
            self.new_generation()
            self.update_fit_scores()
  
game1=GeneSelect(pot=2,bet=3,bank=10000,M=1000,K=100,\
                 propagate=0.98,selection_rate=0.5)
    
game1.evolve(2000)

value_bet_rate_1_1=game1.genotype[1][:,0]
bluff_rate_1_1=game1.genotype[1][:,1]
call_rate_2_1=game1.genotype[2]

f=plt.figure(figsize=(10,6),dpi=100)
plt.hist(value_bet_rate_1_1,bins=200)
mn,std=value_bet_rate_1_1.mean(),value_bet_rate_1_1.std()
mn=int(100*mn)/100.0
std=int(100*std)/100.0
plt.title("Value bets rate for Player 1, mean={}, std={}".\
          format(mn,std))
plt.show()
f.savefig("value_bet_rate_1_1.pdf" ,dpi=100, facecolor='w', edgecolor='w',\
           orientation='portrait', papertype=None, format=None,\
           transparent=False, bbox_inches=None, pad_inches=0.1,frameon=None)

f=plt.figure(figsize=(10,6),dpi=100)
plt.hist(bluff_rate_1_1,bins=200)
mn,std=bluff_rate_1_1.mean(),bluff_rate_1_1.std()
mn=int(100*mn)/100.0
std=int(100*std)/100.0
plt.title("Bluff rate for Player 1, mean={}, std={}".\
          format(mn,std))
plt.show()
f.savefig("bluff_rate_1_1.pdf" ,dpi=100, facecolor='w', edgecolor='w',\
           orientation='portrait', papertype=None, format=None,\
           transparent=False, bbox_inches=None, pad_inches=0.1,frameon=None)

f=plt.figure(figsize=(10,6),dpi=100)
plt.hist(call_rate_2_1,bins=200)
mn,std=call_rate_2_1.mean(),call_rate_2_1.std()
mn=int(100*mn)/100.0
std=int(100*std)/100.0
plt.title("Call rate for Player 2, mean={}, std={}".\
          format(mn,std))
plt.show()
f.savefig("call_rate_2_1.pdf" ,dpi=100, facecolor='w', edgecolor='w',\
           orientation='portrait', papertype=None, format=None,\
           transparent=False, bbox_inches=None, pad_inches=0.1,frameon=None)

game2=GeneSelect(pot=1,bet=1,bank=10000,M=1000,K=100,\
                 propagate=0.98,selection_rate=0.5)
    
game2.evolve(2000)

value_bet_rate_1_2=game2.genotype[1][:,0]
bluff_rate_1_2=game2.genotype[1][:,1]
call_rate_2_2=game2.genotype[2]

f=plt.figure(figsize=(10,6),dpi=100)
plt.hist(value_bet_rate_1_2,bins=200)
mn,std=value_bet_rate_1_2.mean(),value_bet_rate_1_2.std()
mn=int(100*mn)/100.0
std=int(100*std)/100.0
plt.title("Value bets rate for Player 1, mean={}, std={}".\
          format(mn,std))
plt.show()
f.savefig("value_bet_rate_1_2.pdf" ,dpi=100, facecolor='w', edgecolor='w',\
           orientation='portrait', papertype=None, format=None,\
           transparent=False, bbox_inches=None, pad_inches=0.1,frameon=None)

f=plt.figure(figsize=(10,6),dpi=100)
plt.hist(bluff_rate_1_2,bins=200)
mn,std=bluff_rate_1_2.mean(),bluff_rate_1_2.std()
mn=int(100*mn)/100.0
std=int(100*std)/100.0
plt.title("Bluff rate for Player 1, mean={}, std={}".\
          format(mn,std))
plt.show()
f.savefig("bluff_rate_1_2.pdf" ,dpi=100, facecolor='w', edgecolor='w',\
           orientation='portrait', papertype=None, format=None,\
           transparent=False, bbox_inches=None, pad_inches=0.1,frameon=None)

f=plt.figure(figsize=(10,6),dpi=100)
plt.hist(call_rate_2_2,bins=200)
mn,std=call_rate_2_2.mean(),call_rate_2_2.std()
mn=int(100*mn)/100.0
std=int(100*std)/100.0
plt.title("Call rate for Player 2, mean={}, std={}".\
          format(mn,std))
plt.show()
f.savefig("call_rate_2_2.pdf" ,dpi=100, facecolor='w', edgecolor='w',\
           orientation='portrait', papertype=None, format=None,\
           transparent=False, bbox_inches=None, pad_inches=0.1,frameon=None)

game3=GeneSelect(pot=1,bet=3,bank=10000,M=1000,K=100,\
                 propagate=0.995,selection_rate=0.5)
    
game3.evolve(2000)

value_bet_rate_1_3=game3.genotype[1][:,0]
bluff_rate_1_3=game3.genotype[1][:,1]
call_rate_2_3=game3.genotype[2]

f=plt.figure(figsize=(10,6),dpi=100)
plt.hist(value_bet_rate_1_3,bins=200)
mn,std=value_bet_rate_1_3.mean(),value_bet_rate_1_3.std()
mn=int(100*mn)/100.0
std=int(100*std)/100.0
plt.title("Value bets rate for Player 1, mean={}, std={}".\
          format(mn,std))
plt.show()
f.savefig("value_bet_rate_1_3.pdf" ,dpi=100, facecolor='w', edgecolor='w',\
           orientation='portrait', papertype=None, format=None,\
           transparent=False, bbox_inches=None, pad_inches=0.1,frameon=None)

f=plt.figure(figsize=(10,6),dpi=100)
plt.hist(bluff_rate_1_3,bins=200)
mn,std=bluff_rate_1_3.mean(),bluff_rate_1_3.std()
mn=int(100*mn)/100.0
std=int(100*std)/100.0
plt.title("Bluff rate for Player 1, mean={}, std={}".\
          format(mn,std))
plt.show()
f.savefig("bluff_rate_1_3.pdf" ,dpi=100, facecolor='w', edgecolor='w',\
           orientation='portrait', papertype=None, format=None,\
           transparent=False, bbox_inches=None, pad_inches=0.1,frameon=None)

f=plt.figure(figsize=(10,6),dpi=100)
plt.hist(call_rate_2_3,bins=200)
mn,std=call_rate_2_3.mean(),call_rate_2_3.std()
mn=int(100*mn)/100.0
std=int(100*std)/100.0
plt.title("Call rate for Player 2, mean={}, std={}".\
          format(mn,std))
plt.show()
f.savefig("call_rate_2_3.pdf" ,dpi=100, facecolor='w', edgecolor='w',\
           orientation='portrait', papertype=None, format=None,\
           transparent=False, bbox_inches=None, pad_inches=0.1,frameon=None)

game4=GeneSelect(pot=2,bet=1,bank=10000,M=1000,K=100,\
                 propagate=0.98,selection_rate=0.5)
    
game4.evolve(2000)

value_bet_rate_1_4=game4.genotype[1][:,0]
bluff_rate_1_4=game4.genotype[1][:,1]
call_rate_2_4=game4.genotype[2]

f=plt.figure(figsize=(10,6),dpi=100)
plt.hist(value_bet_rate_1_4,bins=2000)
mn,std=value_bet_rate_1_4.mean(),value_bet_rate_1_4.std()
mn=int(100*mn)/100.0
std=int(100*std)/100.0
plt.title("Value bets rate for Player 1, mean={}, std={}".\
          format(mn,std))
plt.show()
f.savefig("value_bet_rate_1_4.pdf" ,dpi=100, facecolor='w', edgecolor='w',\
           orientation='portrait', papertype=None, format=None,\
           transparent=False, bbox_inches=None, pad_inches=0.1,frameon=None)

f=plt.figure(figsize=(10,6),dpi=100)
plt.hist(bluff_rate_1_4,bins=200)
mn,std=bluff_rate_1_4.mean(),bluff_rate_1_4.std()
mn=int(100*mn)/100.0
std=int(100*std)/100.0
plt.title("Bluff rate for Player 1, mean={}, std={}".\
          format(mn,std))
plt.show()
f.savefig("bluff_rate_1_4.pdf" ,dpi=100, facecolor='w', edgecolor='w',\
           orientation='portrait', papertype=None, format=None,\
           transparent=False, bbox_inches=None, pad_inches=0.1,frameon=None)

f=plt.figure(figsize=(10,6),dpi=100)
plt.hist(call_rate_2_4,bins=200)
mn,std=call_rate_2_4.mean(),call_rate_2_4.std()
mn=int(100*mn)/100.0
std=int(100*std)/100.0
plt.title("Call rate for Player 2, mean={}, std={}".\
          format(mn,std))
plt.show()
f.savefig("call_rate_2_4.pdf" ,dpi=100, facecolor='w', edgecolor='w',\
           orientation='portrait', papertype=None, format=None,\
           transparent=False, bbox_inches=None, pad_inches=0.1,frameon=None)
