#!/usr/bin/env python
try:
    import matplotlib.pyplot as plt
except:
    raise
import sys
import networkx as nx

class Person:
	def __init__(self, pid, rankings):
		self.pid = pid
		self._rankings = rankings
		self._proposedTo = dict([(k,False) for k in rankings])
		self._engagedTo = None

	def _breakOffWith(self, p):
		assert(p == self._engagedTo and p != None)
		self._engagedTo = None
		p._engagedTo = None

	def nextHighestUnproposed(self):
		for r in self._rankings:
			if not self._proposedTo[r]: return r
		return None

	def breakOff(self):
		p = self._engagedTo
		self._breakOffWith(p)

	def getFiancee(self):
		return self._engagedTo

	def engageTo(self, p):
		if self.getFiancee():
			self.breakOff()
		self._engagedTo = p
		if p.getFiancee():
			p.breakOff()
		p._engagedTo = self

	def isFree(self):
		return not self._engagedTo

	def prefers(self, m1, m2):
		return self._rankings.index(m1.pid) < self._rankings.index(m2.pid)

	def proposedTo(self, p):
		self._proposedTo[p.pid] = True

	def canPropose(self):
		return not all(self._proposedTo.values())
                
        # Returns list of PIDs? of women who a man has proposed to.
        def namesProposedTo(self):
                return [PID for PID, mybool in self._proposedTo.items() if mybool == True]

men_rankings = {'MA': ['WA','WB','WC','WD'], 'MB': ['WB','WD','WC','WA'],
			    'MC': ['WC','WB','WA','WD'], 'MD': ['WB','WA','WD','WC']}
women_rankings = {'WA': ['MC','MD','MA','MB'], 'WB': ['MA','MD','MB','MC'],
				  'WC': ['MC','MB','MA','MD'], 'WD': ['MB','MC','MD','MA']}
#men_rankings = {'MA': ['WA','WB','WC'], 'MB': ['WB','WA','WC'], 'MC': ['WB','WA','WC']}
#women_rankings = {'WA': ['MA','MC','MB'], 'WB': ['MA','MB','MC'], 'WC': ['MB','MC','MA']}
men = {k: Person(k,ranks) for (k,ranks) in men_rankings.items()}
women = {k: Person(k,ranks) for (k,ranks) in women_rankings.items()}

def freeMan(ms):
	for m in ms.values():
		if m.isFree() and m.canPropose(): return m
	return None

def foo(n, men, women, proposer, proposed, stage_num, myFilename):
    # I should note that the PIDs serve as the label of the nodes.
    # myFilename is a string containing the filename to save the picture in.
    B=nx.Graph()
    # Add nodes corresponding to men, women
    B.add_nodes_from(men.keys())
    B.add_nodes_from(women.keys())
    # Add edges. Can probably be made clean with filter.
    for m in men:
        matched = men[m].getFiancee()
        if matched is not None:
            B.add_edges_from([(m, matched.pid)])
    # Map men and women to positions
    # First, we convert from dict to list, and sort by ID.
    men_list = sorted(men.items(), reverse=True)
    women_list = sorted(women.items(), reverse=True)
    pos = {}
    for i in range(len(men_list)):
        # We set up the positions
        man_ID = men_list[i][0]
        woman_ID = women_list[i][0]
        pos[man_ID] = (0,i)
        pos[woman_ID] = (1,i)

    if stage_num == 1:
        stage1(B, pos, proposer, proposed)
    elif stage_num == 2:
        stage2(B, pos, proposer, proposed)
    elif stage_num == 3:
        stage3(B, pos, proposer, proposed)
    else:
        raise
    # Draw all edges and labels
    nx.draw_networkx_labels(B, pos)
    nx.draw_networkx_edges(B, pos)
    plt.axis('off')
    plt.savefig(myFilename)
    #plt.show()

# Next, we divide it up between three stages, each having different node colors.

# Stage 1: A man is proposing to a woman.
def stage1(B, pos, proposer, proposed):
    # Draw proposed.
    nx.draw_networkx_nodes(B, pos,
                           nodelist=[proposer.pid],
                           node_color='y',
                           label="proposer",
                           node_size=500)
    # Draw rest of the men
    rest_men_pids = [key for key in men.keys() if key not in [proposer.pid]]
    nx.draw_networkx_nodes(B, pos,
                          nodelist=rest_men_pids,
                          node_size=500)
    # Draw women that rejected him
    rejectors = proposer.namesProposedTo()
    nx.draw_networkx_nodes(B, pos,
                          nodelist=rejectors,
                          node_color="black",
                          node_size=500)
    # Draw rest of the women
    rest_women_pids = [x for x in men_rankings[proposer.pid] if x not in rejectors]
    nx.draw_networkx_nodes(B, pos,
                          nodelist=rest_women_pids,
                          node_color=range(len(rest_women_pids)),
                          cmap=plt.cm.Greens,
                          node_size=500)

# Stage 2: A woman is comparing her option(s).
def stage2(B, pos, proposer, proposed):
    # Draw proposed.
    nx.draw_networkx_nodes(B, pos,
                           nodelist=[proposed.pid],
                           node_color='y',
                           node_size=500)
    # Draw rest of the women.
    rest_women_pids = [key for key in women.keys() if key not in [proposed.pid]]
    nx.draw_networkx_nodes(B, pos,
                           nodelist=rest_women_pids,
                           node_size=500)
    # Draw current suitors.
    if proposed.isFree():
        suitors = [proposer.pid]
    else:
	fiance = proposed.getFiancee()
	if proposed.prefers(proposer, fiance):
		suitors = [proposer.pid, fiance.pid]
	else:
	        suitors = [fiance.pid, proposer.pid]
    nx.draw_networkx_nodes(B, pos,
                           nodelist=suitors,
                           node_color=range(len(suitors)),
                           cmap=plt.cm.Greens,
                           node_size=500)
    # Draw rest of the men
    rest_men_pids = [x for x in women_rankings[proposed.pid] if x not in suitors]
    nx.draw_networkx_nodes(B, pos,
                           nodelist=list(rest_men_pids),
                           node_color="black",
                           node_size=500)

# Stage 3: Resolution.
def stage3(B, pos, proposer, proposed):
    # Draw all men
    nx.draw_networkx_nodes(B, pos,
                          nodelist=list(reversed(men.keys())),
                          node_size=500)
    # Draw all women
    nx.draw_networkx_nodes(B, pos,
                          nodelist=list(reversed(women.keys())),
                          node_size=500)    

#################################
######## Begin algorithm ########
#################################

# Generates a string given an int.
def genFilename(counter):
    return "gs_pic" + str(counter).zfill(3) + ".png"

m = freeMan(men)
counter = 6 # First six images are for the legend.
while m:
	wid = m.nextHighestUnproposed()
	w = women[wid]
        foo(4, men, women, m, w, 1, genFilename(counter))
        counter += 1
        foo(4, men, women, m, w, 2, genFilename(counter))
        counter += 1
	if w.isFree():
		m.engageTo(w)
	else:
		m2 = w.getFiancee()
		if w.prefers(m, m2):
			w.engageTo(m)
	m.proposedTo(w)
        foo(4, men, women, m, w, 3, genFilename(counter))
        counter += 1
	m = freeMan(men)

# Jank way to generate a pause at the end of the gif/animation.
for i in range(3):
    foo(4, men, women, m, w, 3, genFilename(counter))
    counter += 1

for m in sorted(men.values(), key=lambda m: m.pid):
	w = m.getFiancee()
	print "%s <==> %s" % (m.pid, w.pid if w else "NONE")
