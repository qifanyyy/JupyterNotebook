import pandas as pd
import networkx as nx
import sys
import numpy as np
import time

PORTS = ['LAX','SFO','PHX','SEA','DEN','ATL','ORD','BOS','IAD','JFK']   #all nodes in graph
INTERMEDPORTS = ['SFO','PHX','SEA','DEN','ATL','ORD','BOS','IAD']       #all nodes other than source and destination
Sources = ['LAX']+INTERMEDPORTS                                         #all possible source nodes for directed flights
Destinations = INTERMEDPORTS+['JFK']                                    #all possible destination nodes for flights
AIRLINES = ['United Airlines','Delta Airlines','American Airlines']     #all airline names
SOURCE = 'LAX'                                                          #Source node
DEST = 'JFK'                                                            #Destination node



#define function to reset Graph node labels and current time
def reset_labels(G):
    for node in G.nodes:
        G.nodes[node]['label'] = 'none'
        G.nodes[node]['l'] = 'none'
    G.nodes[SOURCE]['label'] = 'start'
    G.nodes[SOURCE]['l'] = 'f'
    current_time = pd.to_datetime('12:00 AM').strftime('%H:%M')
    return G, current_time


#function takes node names (shortest node names) and checks if there are flights that satisfy time and flow constraints for
# the whole path, if yes returns it, if no returns False
def checknodes (G,minpath,current_time, keysdict):
    # while there are flights that satisfy this path (forward or backward), check them for augmenting flow (time and flow constraints), otherwise discard path from PATHS
    foundflights = True         #boolean to check whether all nodes in path have viable flights or not
    index=0                     #iterator over minimum path
    edges = []                  #stores viable edges of path
    while foundflights and index <len(minpath)-1:
        # get all possible flights between u and v
        found_possible_forward = True
        found_possible_backward = True
        u = minpath[index]
        v = minpath[index+1]
        try:
            possible_for_flights = G[u][v]
            # get keys of such flights
            #keys_for =[j for j in possible_for_flights]
            #keys_for = sorted(dict(possible_for_flights), key=lambda x: (dict(possible_for_flights)[x]['arr_time'],dict(possible_for_flights)[x]['flow']-dict(possible_for_flights)[x]['capacity']), reverse=False)
            if u+" to "+v in keysdict:
                keys_for = keysdict[u+" to "+v]
            else:
                keys_for = sorted(dict(possible_for_flights), key=lambda x: dict(possible_for_flights)[x]['arr_time'],
                                  reverse=False)
                keysdict[u+" to "+v] = keys_for

        except:
            #print('no flights exist from',u,'to',v)
            found_possible_forward = False
        try:
            possible_bak_flights = G[v][u]
            #keys_bak = [j for j in possible_bak_flights]
            #keys_bak = sorted(dict(possible_bak_flights), key=lambda x: (dict(possible_bak_flights)[x]['arr_time'],dict(possible_bak_flights)[x]['flow']-dict(possible_bak_flights)[x]['capacity']), reverse=False)
            if v+" to "+u in keysdict:
                keys_bak = keysdict[v+" to "+u]
            else:
                keys_bak = sorted(dict(possible_bak_flights), key=lambda x: dict(possible_bak_flights)[x]['arr_time'],reverse=False)
                keysdict[v+" to "+u] = keys_bak

        except:
            #print('no flights exist from',v,'to',u)
            found_possible_backward = False

        # set boolean to check whether there is a viable flight between u and v
        foundflight = False
        if found_possible_forward:       #found at least 1 forward flight (from u to v)
            j = 0

            while not foundflight and j < len(possible_for_flights):
                # store possible flight
                e = possible_for_flights[keys_for[j]]

                #if departure time of e is greater than current time and flow is less than capacity of e
                if e['dep_time'] >= current_time and e['capacity'] > e['flow'] and G.nodes[v]['label']=='none':

                    # label v with edge e's key (which is index of flight in mydata dataframe)
                    G.nodes[v]['label'] = e['mykey']
                    #print(G.nodes[v]['label'])

                    # label v with either forward labelling
                    G.nodes[v]['l'] = 'f'

                    #update current time to arrival time of this flight
                    current_time = e['arr_time']
                    #print('found flight', e, 'from node', u, 'to node', str(v) + '.', 'Now current time is', current_time)
                    foundflight = True

                    #append edge to list of edges
                    edges.append(e)
                j += 1

            if not foundflight:
                #print("Couldn't find possible augmenting forward flight from node",u,"to node",v,". Gonna check backward flights between these 2.")
                foundflights = False
            else:
                foundflights = True

        if found_possible_backward and not foundflight:           #found at least 1 backward flight (from v to u) on path u to v

            if u!=SOURCE:

                if G.nodes[u]['l'] == 'f':          #previous flight was forward (fb)
                    j = 0

                    while not foundflight and j < len(possible_bak_flights):
                        # store possible flight
                        e = possible_bak_flights[keys_bak[j]]

                        # if departure time of at least 1 flight out of the backward edge is greater than current time and flow is greater than 0 and v is unlabeled
                        if e['flow'] > 0 and G.nodes[v]['label'] == 'none':

                            if max([G[pe[0]][pe[1]][pe[2]]['dep_time'] for pe in e['prev_dep_edges']]) >= current_time:
                                # label v with edge e's key (which is index of flight in mydata dataframe)
                                G.nodes[v]['label'] = e['mykey']
                                # print(G.nodes[v]['label'])

                                # label v with either backward labelling
                                G.nodes[v]['l'] = 'b'

                                # update current time to be minimum arrival time of previous arrival edges to this backward edge e
                                current_time = min([G[pe[0]][pe[1]][pe[2]]['arr_time'] for pe in e['prev_arr_edges']])
                                #print('found flight', e, 'from node', u, 'to node', str(v) + '.', 'Now current time is',
                                #      current_time)
                                foundflight = True

                                # append edge to list of edges
                                edges.append(e)
                        j += 1

                elif G.nodes[u]['l'] == 'b':        #previous edge was b (bb)
                    j = 0

                    while not foundflight and j < len(possible_bak_flights):
                        # store possible flight
                        e = possible_bak_flights[keys_bak[j]]
                        # if flow is greater than 0 and v is unlabeled

                        if e['flow'] > 0 and G.nodes[v]['label'] == 'none':
                            # label v with edge e's key (which is index of flight in mydata dataframe)
                            G.nodes[v]['label'] = e['mykey']
                            # print(G.nodes[v]['label'])

                            # label v with either backward labelling
                            G.nodes[v]['l'] = 'b'

                            # update current time to be minimum arrival time of previous arrival edges to this backward edge e
                            current_time = min([G[pe[0]][pe[1]][pe[2]]['arr_time'] for pe in e['prev_arr_edges']])
                            #print('found flight', e, 'from node', u, 'to node', str(v) + '.', 'Now current time is',
                            #      current_time)
                            foundflight = True

                            # append edge to list of edges
                            edges.append(e)
                        j += 1

                else: #previous edge was neither forward nor backward
                    print("Previous edge of current backward edge was neither forward nor backward! ERROR!")
                    sys.exit()

            if not foundflight:  # if you can't find any flight in between the nodes of minpath
                #print("Couldn't find possible augmenting backward flight from node", v, "to node", u,
                #      ". This path cannot be used to augment flow.")
                foundflights = False
            else:
                foundflights = True

        if not found_possible_backward and not found_possible_forward:
            #found no flights between u and v
            #cannot happen since path must have either forward or backward between u and v to be considered
            print('Found no flights between',u,'and',v,'ERRORRR!')
            sys.exit()

        index += 1


    #check if path we found has a backward path
    #back = False
    #if foundflights:
    #    for node in G.nodes:
    #        if G.nodes[node]['l'] == 'b':
    #            back = True
    #if back:
    #    print('FOUND PATH WITH A BACKWARD PATH:',edges)
    #if not foundflights:
        #print("Couldn't find flights for path",minpath,".Edges found are:",edges)

    return G, edges, foundflights, current_time, keysdict


def calc_delta_of_path (G,minpath,edges,contrib):
    #define vector that will store delta values of every edge in path we found
    Deltas = np.full(len(edges),1000000,int)
    #define edges where transition happened from forward path to backward path
    transition_edges_fb = []

    #traverse the minpath by iterating over its edges
    for i in range(len(minpath)-1):
        j = i+1
        #store first and second nodes of edge
        u = minpath[i]
        v = minpath[j]
        # point to e in graph
        e = G[edges[i]['u']][edges[i]['v']][edges[i]['mykey']]

        #if current edge is forward
        if G.nodes[v]['l'] == 'f':
            #calculate delta of current edge
            Deltas[i] = e['capacity'] - e['flow']

            #if we are not at the source node
            if u!=SOURCE:
                prev_e = G[edges[i-1]['u']][edges[i-1]['v']][edges[i-1]['mykey']]

                #if previous edge was labelled backward, means we are currently at the end of a backward path
                if G.nodes[u]['l'] == 'b':
                    #get flow contributions to prev_e from its previous arrival edges that can be replaced by flow to e instead
                    flow_conts_of_arr_to_prev_e = [contrib[pe[2],prev_e['mykey']] for pe in prev_e['prev_arr_edges'] if G[pe[0]][pe[1]][pe[2]]['arr_time']<=e['dep_time']]
                    #sum them up
                    flowatoe = sum(flow_conts_of_arr_to_prev_e)

                    #beginning of backward path
                    b = transition_edges_fb.pop()
                    b = G[b['u']][b['v']][b['mykey']]
                    #forward edge right before backward path began
                    f = transition_edges_fb.pop()
                    f = G[f['u']][f['v']][f['mykey']]
                    # get flow contributions of b to its previous departure edges that can be replaced by flow from f instead
                    flow_conts_of_dep_from_b = [contrib[b['mykey'],pe[2]] for pe in b['prev_dep_edges'] if f['arr_time']<=G[pe[0]][pe[1]][pe[2]]['dep_time']]
                    #sum them up
                    flowdfromb = sum(flow_conts_of_dep_from_b)

                    #the minimum of these 2 flows is the delta of the whole backward path
                    delta = min(flowatoe,flowdfromb)

                    if delta == 0:
                        #This condition cannot happen!
                        print('delta of backward path was 0. EXITING!')
                        sys.exit()

                    #iterate over backward path edges and assign this delta to respective positions in Deltas vector
                    startofbpath = edges.index(b)
                    index = startofbpath
                    while edges[index]!=e:
                        Deltas[index] = delta
                        index += 1

        elif G.nodes[v]['l']=='b': #i.e. current edge e is backward
            if u!=SOURCE:
                prev_e = G[edges[i - 1]['u']][edges[i - 1]['v']][edges[i - 1]['mykey']]

                #if previous edge was forward
                if G.nodes[u]['l'] == 'f':
                    transition_edges_fb = [prev_e,e]
        else:
            #edge is neither backward nor forward! This should never happen!
            print('Edge was neither backward nor forward. Error during calculating delta!')
            sys.exit()
    return min(Deltas)


def augment_flow(G,delta,edges,contrib,minpath,netflow):
    # define edges where transition happened from forward path to backward path
    transition_edges_fb = []
    #Get the path's minimum delta value which we will augment it by
    netflow += delta

    for i in range(len(minpath)-1):
        j = i + 1
        # store first and second nodes of edge
        u = minpath[i]
        v = minpath[j]
        # point to e in graph
        e = G[edges[i]['u']][edges[i]['v']][edges[i]['mykey']]

        #if edge e is forward
        if G.nodes[v]['l'] == 'f':
            G[u][v][e['mykey']]['flow'] += delta

            #if we are not at the source node
            if u!=SOURCE:
                #point to previous edge in the path
                prev_e = G[edges[i - 1]['u']][edges[i - 1]['v']][edges[i - 1]['mykey']]

                #if previous edge was forward (ff)
                if G.nodes[u]['l'] == 'f':
                    #append edge e to prev_e's previous augmenting departure edges
                    if [e['u'],e['v'],e['mykey']] not in prev_e['prev_dep_edges']:
                        prev_e['prev_dep_edges'] += [[e['u'],e['v'],e['mykey']]]
                    # append edge prev_e to e's previous augmenting arrival edges
                    if [prev_e['u'],prev_e['v'],prev_e['mykey']] not in e['prev_arr_edges']:
                        e['prev_arr_edges'] += [[prev_e['u'],prev_e['v'],prev_e['mykey']]]
                    contrib[prev_e['mykey'],e['mykey']] += delta

                #else edge prev_e was backward (bf), which is the end of the backward path
                elif G.nodes[u]['l'] == 'b':
                    # beginning of backward path
                    b = transition_edges_fb.pop()
                    b = G[b['u']][b['v']][b['mykey']]
                    # forward edge right before backward path began
                    f = transition_edges_fb.pop()
                    f = G[f['u']][f['v']][f['mykey']]

                    # iterate over backward path edges, augment their flow, prev edges, and flow contributions
                    startofbpath = edges.index(b)
                    index = startofbpath
                    while edges[index] != e:
                        #point to that backward edge in the Graph
                        bedge = G[edges[index]['u']][edges[index]['v']][edges[index]['mykey']]
                        # decrease that backward edge's flow by delta
                        bedge['flow'] -= delta

                        #if flight is not used anymore, (0 people on it)
                        if bedge['flow'] == 0:

                            #if bedge is only edge in backward path
                            if startofbpath == index and bedge==prev_e:
                                # append flow contribution of forward edge (the one right before backward path starts) by the amount the backward edge (bedge) contributes to its departure edges
                                contrib[f['mykey'], [pe[2] for pe in bedge['prev_dep_edges']]] += contrib[
                                    bedge['mykey'], [pe[2] for pe in bedge['prev_dep_edges']]]
                                # set the flow contribution of bedge to all other edges 0
                                contrib[bedge['mykey'], :] = 0
                                # add all flow contributions to bedge to e instead
                                contrib[[pe[2] for pe in bedge['prev_arr_edges']], e['mykey']] += contrib[
                                    [pe[2] for pe in bedge['prev_arr_edges']], bedge['mykey']]
                                # remove all flow contributions to bedge
                                contrib[:, bedge['mykey']] = 0
                                # remove bedge's previous arrival augmented edges and remove bedge from them, and add them to e and e to them
                                for pe in bedge['prev_arr_edges']:
                                    G[pe[0]][pe[1]][pe[2]]['prev_dep_edges'].remove([bedge['u'],bedge['v'],bedge['mykey']])
                                    bedge['prev_arr_edges'].remove([pe[0],pe[1],pe[2]])
                                    if [pe[0],pe[1],pe[2]] not in e['prev_arr_edges']:
                                        e['prev_arr_edges'] += [[pe[0],pe[1],pe[2]]]
                                    if [e['u'],e['v'],e['mykey']] not in G[pe[0]][pe[1]][pe[2]]['prev_dep_edges']:
                                        G[pe[0]][pe[1]][pe[2]]['prev_dep_edges'] += [[e['u'],e['v'],e['mykey']]]
                                # remove bedge's previous departure augmented edges and remove bedge from them, and f to them and add them to f
                                for pe in bedge['prev_dep_edges']:
                                    G[pe[0]][pe[1]][pe[2]]['prev_arr_edges'].remove([bedge['u'],bedge['v'],bedge['mykey']])
                                    bedge['prev_dep_edges'].remove([pe[0],pe[1],pe[2]])
                                    if [f['u'],f['v'],f['mykey']] not in G[pe[0]][pe[1]][pe[2]]['prev_arr_edges']:
                                        G[pe[0]][pe[1]][pe[2]]['prev_arr_edges'] += [[f['u'],f['v'],f['mykey']]]
                                    if [pe[0],pe[1],pe[2]] not in f['prev_dep_edges']:
                                        f['prev_dep_edges'] += [[pe[0],pe[1],pe[2]]]

                            #else if bedge is the beginnging of the backward path
                            elif startofbpath == index:
                                #append flow contribution of forward edge (the one right before backward path starts) by the amount the first backward edge (bedge) contributes to its departure edges
                                contrib[f['mykey'],[pe[2] for pe in bedge['prev_dep_edges']]] += \
                                    contrib[bedge['mykey'],[pe[2] for pe in bedge['prev_dep_edges']]]
                                #set the flow contribution of first backward edge (bedge) to 0
                                contrib[bedge['mykey'],:] = 0
                                #remove bedge's previous arrival augmented edges and remove bedge from them
                                for pe in bedge['prev_arr_edges']:
                                    G[pe[0]][pe[1]][pe[2]]['prev_dep_edges'].remove([bedge['u'], bedge['v'], bedge['mykey']])
                                    bedge['prev_arr_edges'].remove([pe[0],pe[1],pe[2]])
                                # remove bedge's previous departure augmented edges and remove bedge from them, and f to them and add them to f
                                for pe in bedge['prev_dep_edges']:
                                    G[pe[0]][pe[1]][pe[2]]['prev_arr_edges'].remove([bedge['u'], bedge['v'], bedge['mykey']])
                                    bedge['prev_dep_edges'].remove([pe[0],pe[1],pe[2]])
                                    if [f['u'],f['v'],f['mykey']] not in G[pe[0]][pe[1]][pe[2]]['prev_arr_edges']:
                                        G[pe[0]][pe[1]][pe[2]]['prev_arr_edges'] += [[f['u'],f['v'],f['mykey']]]
                                    if [pe[0],pe[1],pe[2]] not in f['prev_dep_edges']:
                                        f['prev_dep_edges'] += [[pe[0],pe[1],pe[2]]]

                            #else if bedge is the last edge in the backward path
                            elif bedge == prev_e:
                                #add all contributions to bedge to e instead, remove all contributions to and from bedge
                                contrib[[pe[2] for pe in bedge['prev_arr_edges']],e['mykey']] += contrib[[pe[2] for pe in bedge['prev_arr_edges']],bedge['mykey']]
                                contrib[:,bedge['mykey']] = 0
                                contrib[bedge['mykey'],:] = 0
                                #remove bedge's previous arrival augmented edges and remove bedge from them, and add them to e and e to them
                                for pe in bedge['prev_arr_edges']:
                                    G[pe[0]][pe[1]][pe[2]]['prev_dep_edges'].remove([bedge['u'], bedge['v'], bedge['mykey']])
                                    bedge['prev_arr_edges'].remove([pe[0],pe[1],pe[2]])
                                    if [pe[0],pe[1],pe[2]] not in e['prev_arr_edges']:
                                        e['prev_arr_edges'] += [[pe[0],pe[1],pe[2]]]
                                    if [e['u'],e['v'],e['mykey']] not in G[pe[0]][pe[1]][pe[2]]['prev_dep_edges']:
                                        G[pe[0]][pe[1]][pe[2]]['prev_dep_edges'] += [[e['u'],e['v'],e['mykey']]]
                                #remove bedge's previous departure augmented edges and remove bedge from them
                                for pe in bedge['prev_dep_edges']:
                                    G[pe[0]][pe[1]][pe[2]]['prev_arr_edges'].remove([bedge['u'],bedge['v'],bedge['mykey']])
                                    bedge['prev_dep_edges'].remove([pe[0],pe[1],pe[2]])

                            #else bedge is a backward edge in the middle of the backward path
                            elif index>startofbpath and bedge!=prev_e:
                                #remove all contributions from bedge
                                contrib[bedge['mykey'],:] = 0
                                # remove bedge's previous arrival augmented edges and remove bedge from them
                                for pe in bedge['prev_arr_edges']:
                                    G[pe[0]][pe[1]][pe[2]]['prev_dep_edges'].remove([bedge['u'], bedge['v'], bedge['mykey']])
                                    bedge['prev_arr_edges'].remove([pe[0],pe[1],pe[2]])
                                # remove bedge's previous departure augmented edges and remove bedge from them
                                for pe in bedge['prev_dep_edges']:
                                    G[pe[0]][pe[1]][pe[2]]['prev_arr_edges'].remove([bedge['u'], bedge['v'], bedge['mykey']])
                                    bedge['prev_dep_edges'].remove([pe[0],pe[1],pe[2]])

                            else: #bedge is backward edge that is outside the path! CANNOT HAPPEN!
                                print('Backward edge found is outside the backward path! ERROR!')
                                print('edge was',bedge,'with u:',u,'and v:',v, 'and dep port:', bedge['u'], 'and arr port: ', bedge['v'])
                                sys.exit()

                        elif bedge['flow']>0: #flow on bedge is not equal to 0, delta  was less than flow on bedge
                            #bedge is still being used after removing some flow from it

                            #if bedge is a backward edge in the middle of the backward path
                            if index > startofbpath and edges[index]!=prev_e:
                                #edit its contribution to the next edge
                                contrib[bedge['mykey'],edges[index-1]['mykey']] -= delta

                            # if bedge is only edge in backward path
                            elif startofbpath == index and bedge == prev_e:
                                # extract flights that can take contribution from forward edge f (the one right before backward path starts) instead of bedge
                                dflights = [pe for pe in bedge['prev_dep_edges'] if
                                            f['arr_time'] <= G[pe[0]][pe[1]][pe[2]]['dep_time']]
                                # sum up flow contributions to every viable flight in dflights until we reach delta value
                                contribution = 0

                                while contribution < delta:
                                    # get flight index in dflights that has flow contribution from bedge closest to required delta value
                                    closestflightindex = np.argmin(
                                        abs(contrib[bedge['mykey'], [pe[2] for pe in dflights]] - delta))
                                    # save that flight
                                    dflight = G[dflights[closestflightindex][0]][dflights[closestflightindex][1]][
                                        dflights[closestflightindex][2]]
                                    # add up its contribution to sum of contributions
                                    contribution += contrib[bedge['mykey'], dflight['mykey']]

                                    # if sum of contributions is still less than delta
                                    if contribution <= delta:
                                        # add bedge's contribution of dflight to f's contribution of that flight, and set bedge's to 0
                                        contributiontod = contrib[bedge['mykey'], dflight['mykey']]
                                        contrib[f['mykey'], dflight['mykey']] += contributiontod
                                        contrib[bedge['mykey'], dflight['mykey']] = 0
                                        # remove dflight from bedge's dep flights and remove bedge from it, and add it to f and f to it
                                        bedge['prev_dep_edges'].remove([dflight['u'], dflight['v'], dflight['mykey']])
                                        if [dflight['u'], dflight['v'], dflight['mykey']] not in f['prev_dep_edges']:
                                            f['prev_dep_edges'] += [[dflight['u'], dflight['v'], dflight['mykey']]]
                                        dflight['prev_arr_edges'].remove([bedge['u'], bedge['v'], bedge['mykey']])
                                        if [f['u'], f['v'], f['mykey']] not in dflight['prev_arr_edges']:
                                            dflight['prev_arr_edges'] += [[f['u'], f['v'], f['mykey']]]

                                    else:  # contribution > delta. Therefore dflight will take contributions from both bedge and f
                                        # save amount bedge will still contribute to dflight
                                        bedgeconttod = contribution - delta
                                        # add contribution of bedge to dflight to f's contribution to dflight and then subtract amount bedge will keep contributing to dflight
                                        contrib[f['mykey'], dflight['mykey']] += contrib[bedge['mykey'], dflight[
                                            'mykey']] - bedgeconttod
                                        # set amount bedge will contribute to dflight as saved amount
                                        contrib[bedge['mykey'], dflight['mykey']] = bedgeconttod
                                        # add dflight to f's prev dep edges
                                        if [dflight['u'], dflight['v'], dflight['mykey']] not in f['prev_dep_edges']:
                                            f['prev_dep_edges'] += [[dflight['u'], dflight['v'], dflight['mykey']]]
                                        # add f to dflight's prev arr edges
                                        if [f['u'], f['v'], f['mykey']] not in dflight['prev_arr_edges']:
                                            dflight['prev_arr_edges'] += [[f['u'], f['v'], f['mykey']]]

                                # extract flights that can give contribution to forward edge e (the one right after backward path ends) instead of bedge
                                arrflights = [pe for pe in bedge['prev_arr_edges'] if
                                              G[pe[0]][pe[1]][pe[2]]['arr_time'] <= e['dep_time']]
                                # sum up flow contributions to every viable flight in dflights until we reach delta value
                                contribution = 0
                                while contribution < delta:
                                    # get flight index in arrflights that has flow contribution to bedge closest to required delta value
                                    closestflightindex = np.argmin(
                                        abs(contrib[[pe[2] for pe in arrflights], bedge['mykey']] - delta))
                                    # save that flight
                                    arrflight = G[arrflights[closestflightindex][0]][arrflights[closestflightindex][1]][
                                        arrflights[closestflightindex][2]]
                                    # add up its contribution to sum of contributions
                                    contribution += contrib[arrflight['mykey'], bedge['mykey']]

                                    # if sum of contributions is still less than delta
                                    if contribution <= delta:
                                        # add bedge's contribution from arrflight to e's contribution from that flight, and set bedge's to 0
                                        contrib[arrflight['mykey'], e['mykey']] += contrib[
                                            arrflight['mykey'], bedge['mykey']]
                                        contrib[arrflight['mykey'], bedge['mykey']] = 0
                                        # remove arrflight from bedge's arr flights and remove bedge from it, and add it to e and e to it
                                        bedge['prev_arr_edges'].remove(
                                            [arrflight['u'], arrflight['v'], arrflight['mykey']])
                                        if [arrflight['u'], arrflight['v'], arrflight['mykey']] not in e['prev_arr_edges']:
                                            e['prev_arr_edges'] += [[arrflight['u'], arrflight['v'], arrflight['mykey']]]
                                        arrflight['prev_dep_edges'].remove([bedge['u'], bedge['v'], bedge['mykey']])
                                        if [e['u'], e['v'], e['mykey']] not in arrflight['prev_dep_edges']:
                                            arrflight['prev_dep_edges'] += [[e['u'], e['v'], e['mykey']]]

                                    else:  # contribution > delta. Therefore arrflight will give contributions to both bedge and e
                                        # save amount arrflight will keep contributing to bedge
                                        arrflightconttob = contribution - delta
                                        # add contribution of bedge from arrflight to e's contribution from arrflight and then subtract amount arrflight will keep contributing to bedge
                                        contrib[arrflight['mykey'], e['mykey']] += contrib[arrflight['mykey'], bedge[
                                            'mykey']] - arrflightconttob
                                        # set amount bedge will take from arrflight as saved amount
                                        contrib[arrflight['mykey'], bedge['mykey']] = arrflightconttob
                                        # add e to arrflight's prev dep edges
                                        if [e['u'], e['v'], e['mykey']] not in arrflight['prev_dep_edges']:
                                            arrflight['prev_dep_edges'] += [[e['u'], e['v'], e['mykey']]]
                                        # add arrflight to e's prev arr edges
                                        if [arrflight['u'], arrflight['v'], arrflight['mykey']] not in e['prev_arr_edges']:
                                            e['prev_arr_edges'] += [[arrflight['u'], arrflight['v'], arrflight['mykey']]]


                            # else if bedge is the beginnging of the backward path
                            elif startofbpath == index:
                                #extract flights that can take contribution from forward edge f (the one right before backward path starts) instead of bedge
                                dflights = [pe for pe in bedge['prev_dep_edges'] if f['arr_time'] <= G[pe[0]][pe[1]][pe[2]]['dep_time']]
                                #sum up flow contributions to every viable flight in dflights until we reach delta value
                                contribution = 0

                                while contribution < delta:
                                    #get flight index in dflights that has flow contribution from bedge closest to required delta value
                                    closestflightindex = np.argmin(abs(contrib[bedge['mykey'],[pe[2] for pe in dflights]]-delta))
                                    #save that flight
                                    dflight = G[dflights[closestflightindex][0]][dflights[closestflightindex][1]][dflights[closestflightindex][2]]
                                    #add up its contribution to sum of contributions
                                    contribution += contrib[bedge['mykey'],dflight['mykey']]

                                    #if sum of contributions is still less than delta
                                    if contribution <= delta:
                                        #add bedge's contribution of dflight to f's contribution of that flight, and set bedge's to 0
                                        contributiontod = contrib[bedge['mykey'],dflight['mykey']]
                                        contrib[f['mykey'],dflight['mykey']] += contributiontod
                                        contrib[bedge['mykey'], dflight['mykey']] = 0
                                        #remove dflight from bedge's dep flights and remove bedge from it, and add it to f and f to it
                                        bedge['prev_dep_edges'].remove([dflight['u'],dflight['v'],dflight['mykey']])
                                        if [dflight['u'],dflight['v'],dflight['mykey']] not in f['prev_dep_edges']:
                                            f['prev_dep_edges'] += [[dflight['u'],dflight['v'],dflight['mykey']]]
                                        dflight['prev_arr_edges'].remove([bedge['u'],bedge['v'],bedge['mykey']])
                                        if [f['u'],f['v'],f['mykey']] not in dflight['prev_arr_edges']:
                                            dflight['prev_arr_edges'] += [[f['u'],f['v'],f['mykey']]]

                                    else: #contribution > delta. Therefore dflight will take contributions from both bedge and f
                                        #save amount bedge will still contribute to dflight
                                        bedgeconttod = contribution - delta
                                        #add contribution of bedge to dflight to f's contribution to dflight and then subtract amount bedge will keep contributing to dflight
                                        contrib[f['mykey'],dflight['mykey']] += contrib[bedge['mykey'],dflight['mykey']] - bedgeconttod
                                        #set amount bedge will contribute to dflight as saved amount
                                        contrib[bedge['mykey'],dflight['mykey']] = bedgeconttod
                                        #add dflight to f's prev dep edges
                                        if [dflight['u'],dflight['v'],dflight['mykey']] not in f['prev_dep_edges']:
                                            f['prev_dep_edges'] += [[dflight['u'],dflight['v'],dflight['mykey']]]
                                        #add f to dflight's prev arr edges
                                        if [f['u'],f['v'],f['mykey']] not in dflight['prev_arr_edges']:
                                            dflight['prev_arr_edges'] += [[f['u'],f['v'],f['mykey']]]

                            # else if bedge is the last edge in the backward path
                            elif bedge == prev_e:
                                #reduce bedge's contribution to previous edge in backward path by delta
                                contrib[bedge['mykey'],edges[index-1]['mykey']] -= delta
                                #extract flights that can give contribution to forward edge e (the one right after backward path ends) instead of bedge
                                arrflights = [pe for pe in bedge['prev_arr_edges'] if G[pe[0]][pe[1]][pe[2]]['arr_time']<=e['dep_time']]
                                # sum up flow contributions to every viable flight in dflights until we reach delta value
                                contribution = 0
                                while contribution < delta:
                                    # get flight index in arrflights that has flow contribution to bedge closest to required delta value
                                    closestflightindex = np.argmin(abs(contrib[[pe[2] for pe in arrflights],bedge['mykey']]-delta))
                                    # save that flight
                                    arrflight = G[arrflights[closestflightindex][0]][arrflights[closestflightindex][1]][
                                        arrflights[closestflightindex][2]]
                                    # add up its contribution to sum of contributions
                                    contribution += contrib[arrflight['mykey'],bedge['mykey']]

                                    # if sum of contributions is still less than delta
                                    if contribution<=delta:
                                        # add bedge's contribution from arrflight to e's contribution from that flight, and set bedge's to 0
                                        contrib[arrflight['mykey'], e['mykey']] += contrib[arrflight['mykey'],bedge['mykey']]
                                        contrib[arrflight['mykey'], bedge['mykey']] = 0
                                        # remove arrflight from bedge's arr flights and remove bedge from it, and add it to e and e to it
                                        bedge['prev_arr_edges'].remove([arrflight['u'],arrflight['v'],arrflight['mykey']])
                                        if [arrflight['u'],arrflight['v'],arrflight['mykey']] not in e['prev_arr_edges']:
                                            e['prev_arr_edges'] += [[arrflight['u'],arrflight['v'],arrflight['mykey']]]
                                        arrflight['prev_dep_edges'].remove([bedge['u'],bedge['v'],bedge['mykey']])
                                        if [e['u'],e['v'],e['mykey']] not in arrflight['prev_dep_edges']:
                                            arrflight['prev_dep_edges'] += [[e['u'],e['v'],e['mykey']]]

                                    else: #contribution > delta. Therefore arrflight will give contributions to both bedge and e
                                        #save amount arrflight will keep contributing to bedge
                                        arrflightconttob = contribution - delta
                                        # add contribution of bedge from arrflight to e's contribution from arrflight and then subtract amount arrflight will keep contributing to bedge
                                        contrib[arrflight['mykey'],e['mykey']] += contrib[arrflight['mykey'],bedge['mykey']] - arrflightconttob
                                        # set amount bedge will take from arrflight as saved amount
                                        contrib[arrflight['mykey'], bedge['mykey']] = arrflightconttob
                                        # add e to arrflight's prev dep edges
                                        if [e['u'],e['v'],e['mykey']] not in arrflight['prev_dep_edges']:
                                            arrflight['prev_dep_edges'] += [[e['u'],e['v'],e['mykey']]]
                                        # add arrflight to e's prev arr edges
                                        if [arrflight['u'],arrflight['v'],arrflight['mykey']] not in e['prev_arr_edges']:
                                            e['prev_arr_edges'] += [[arrflight['u'],arrflight['v'],arrflight['mykey']]]

                        else: #bedge['flow'] < 0: #NEVER THE CASE!
                            print('Created backward flow that is less than 0 on bedge during augmenting. ERROR!')
                            print('Backward edge',bedge,'had a flow of',bedge['flow'],'!!!')
                            print('u was:',u,'and v was:',v)
                            sys.exit()

                        index += 1

                else: #previous edge was neither forward nor backward, which is never the case!
                    print('Previous Edge was neither backward nor forward. Error during augmenting delta!')
                    print('Previous Edge was',prev_e, 'whose nodes u:',u,'and v:',v,'and dep port:',prev_e['u'],' and arr port:',prev_e['v'])
                    sys.exit()

        # if edge e is backward
        elif G.nodes[v]['l'] == 'b':

            # if we are not at the source node
            if u!=SOURCE:
                # point to previous edge in the path
                prev_e = G[edges[i - 1]['u']][edges[i - 1]['v']][edges[i - 1]['mykey']]

                # if previous edge was forward (fb)
                if G.nodes[u]['l'] == 'f':
                    transition_edges_fb = [prev_e,e]

                elif G.nodes[u]['l'] != 'b': #other than fb and bb
                    # previous edge was neither forward nor backward, which is never the case!
                    print('Pevious Edge was neither backward nor forward. Error during augmenting delta!')
                    print('Previous Edge was', prev_e, 'whose nodes u:', u, 'and v:', v, 'and dep port:', prev_e['u'],
                          ' and arr port:', prev_e['v'])
                    sys.exit()

        else: #edge e is neither forward nor backward error!
            #This case is never reached!
            print('Edge was neither backward nor forward. Error during augmenting delta!')
            print('Edge was', e, 'whose nodes u:', u, 'and v:', v, 'and dep port:', e['u'],
                  ' and arr port:', e['v'])
            sys.exit()

    return G, contrib, netflow



#takes all simple paths of a certain length from graph copy (G2) and removes the ones that cannot reach JFK given current graph G's flow
#and their time constraints
#returns filtered PATHS and keysdict
def filterpaths(PATHS,G,keysdict):
    timedpaths = pd.DataFrame(PATHS)

    times = []

    for path in PATHS:
        G,current_time = reset_labels(G)
        G, edges, foundflights, current_time,keysdict = checknodes(G,path,current_time,keysdict)
        if foundflights:
            times += [current_time]
        else:
            times += [float('nan')]
    timedpaths.insert(timedpaths.shape[1],'times',times)
    timedpaths = timedpaths.dropna(axis=0)
    #timedpaths = timedpaths.sort_values(by=['times'], ascending=[True])
    return timedpaths, keysdict


#takes constructed graph G, source node name s, destination node name t.
#calculate maximum flow of the graph
def Maxflow(G,s,t):
    # store time right before algorithm starts
    start = time.time()
    #set network flow to 0
    netflow = 0

    #Assume that you have not yet reached maximum flow
    maxflowreached = False
    # flow contribution of flight i to flight j, key of edge is index to this matrix, not symmetric. (Can use dictionary instead to drastically
    #reduce space complexity of this variable contrib, but that is a future improvement)
    Contrib = np.zeros((len(flights), len(flights)), int)
    #determines maximum number of edges to consider when looking at all simple paths
    cuttofff = 1
    #store a normal (non multi) undirected copy of the main Graph (much less number of edges and possible paths in this copy)
    G2 = nx.Graph(G)
    #get all possible simple paths from that copy that have a length <= cuttofff (edges in those paths can be either forward or backward)
    PATHS = [p for p in nx.all_simple_paths(G2,s,t,cutoff=cuttofff)]
    # keys dictionary to store sorted keys of earliest arrival flights between every 2 nodes (to avoid sorting again and again)
    keysdict = {}
    #filter all possible node combinations by their arrival time at destination in tpaths (remove ones that don't arrive)
    tpaths, keysdict = filterpaths(PATHS,G,keysdict)

    while not maxflowreached:
        #set labels of all nodes to be none and current time to 00:00
        G, current_time = reset_labels(G)

        #find path combination that reaches destination earliest
        #min_path = list(tpaths.iloc[0,:-1])
        min_path = list(tpaths[tpaths.times == tpaths.times.min()].iloc[0,:-1])

        #check if nodes of selected minpath have a viable path (both time and flow constraints are checked)
        G, edges, foundflights, current_time, keysdict = checknodes(G,min_path,current_time,keysdict)


        #AFTER PUSHING THROUGH THIS MINPATH, SORT TPATHS AGAIN AND SEE. THEREFORE WE DON'T NEED TO SORT TPATHS, WE ONLY NEED THE MIN!!!!
        #if there are flights that satisfy this path
        if foundflights:
            #calculate delta of that path
            delta = calc_delta_of_path(G,min_path,edges,Contrib)

            #augment flow of network with delta of that path
            G, Contrib,netflow = augment_flow(G,delta,edges,Contrib,min_path,netflow)

            # set labels of all nodes to be none and current time to 00:00
            G, current_time = reset_labels(G)

            # check if nodes of selected minpath have a viable path (both time and flow constraints are checked)
            G, edges, foundflights, current_time, keysdict = checknodes(G, min_path, current_time, keysdict)

            if foundflights:
                tpaths.loc[tpaths.times==tpaths.times.min(),'times'] = current_time
            else:
                tpaths = tpaths.drop(axis=0,index = tpaths[tpaths.times==tpaths.times.min()].index[0])

        elif len(tpaths)!=0:
            #remove current minpath since it has no more viable flights
            #PATHS.remove(min(PATHS, key=len))  # to remove that path and then extract another min
            #tpaths = tpaths.drop(tpaths.index[0])
            tpaths = tpaths.drop(axis=0, index=tpaths[tpaths.times == tpaths.times.min()].index[0])

        #if length of all possible paths for current cutoff length = 0
        if len(tpaths) == 0:
            # we are transitioning to higher length of minimum paths

            # increment cutoff to look paths with length = len(previous cuttoff) + 1
            cuttofff += 1
            # store all simple paths that have a length exactly equal to cutoff value
            PATHS = [p for p in nx.all_simple_paths(G2, s, t, cutoff=cuttofff) if len(p) > cuttofff]
            tpaths, keysdict = filterpaths(PATHS, G, keysdict)

            # if not a single flight was found after checking higher length paths
            if len(tpaths) == 0:
                # we have reached maximum flow of the network
                maxflowreached = True
                print('Maximum flow is reached:', netflow)

    #store time right after algorithm terminates
    end = time.time()
    print('Took',end-start,'seconds to run the algorithm')
    return netflow



#load the data
flights = pd.read_csv('Allflights.csv')
#shuffle it (if you want)
flights = flights.sample(frac=1).reset_index(drop=True)
#sort it (only for slight performance improvement)
flights = flights.sort_values(by=['arr_time'],ascending=True)


#set source and destination
s = SOURCE
t = DEST


# ports initialized with label none
G = nx.MultiDiGraph()
G.add_nodes_from(PORTS, label='none',
                 l='none')  # label is index of flight in flights dataframe, l is forward or backward labelling (f or b)

# edges initialized with flow 0 and all other relevant attributes
for index, row in flights.iterrows():
    G.add_edge(u_for_edge=row['dep_port'], v_for_edge=row['arr_port'], key=index,
               dep_time=row['dep_time'], arr_time=row['arr_time'], flow=0, capacity=row['capacities'],
               mykey=index, prev_arr_edges=[], prev_dep_edges=[], u=row['dep_port'], v=row['arr_port'])

#Call maxflow algorithm
mflow = Maxflow(G,s,t)

pos = nx.circular_layout(G)
nx.draw_networkx(G)





"""

##################################################IGNORE THIS!!!!#######################################################



#Step 3
# Search for a vertex v which can be labeled by either a forward or a backward labeling.
# If none exists, halt; the present flow is maximum.
# If such a vertex v exists, label it ‘e’, where e is the edge through which the labeling is possible.
# If v = t, go to step(4); otherwise repeat step(3).

#search for any next vertex from current vertex (backward or forward)
def search_for_v(G,u,current_time):
    # find all successors and predecessors of u
    possible_vs = [suc for suc in G.successors(u)]+[pre for pre in G.predecessors(u) if pre not in G.successors(u)]
    #filter out labeled nodes from them
    possible_vs = [v for v in possible_vs if G.nodes[v]['label']=='none']
    # set boolean to check whether there is a viable flight between u and v
    foundflight = False
    # choose a random flight from possible flights.
    seq = np.random.permutation(len(possible_vs))
    i = 0
    while not foundflight and i < len(possible_vs):
        v = possible_vs[seq[i]]

        ##get all possible flights between u and v
        #possible_flights = G[u][v]
        ##get keys of such flights
        #keys = [j for j in possible_flights]

        # get all possible flights between u and v
        found_possible_forward = True
        found_possible_backward = True
        try:
            possible_for_flights = G[u][v]
            # get keys of such flights
            keys_for = [j for j in possible_for_flights]
        except:
            #print('no flights exist from',u,'to',v)
            found_possible_forward = False
        try:
            possible_bak_flights = G[v][u]
            keys_bak = [j for j in possible_bak_flights]
        except:
            #print('no flights exist from',v,'to',u)
            found_possible_backward = False


        if found_possible_forward:  # found at least 1 forward flight (from u to v)
            j = 0

            while not foundflight and j < len(possible_for_flights):
                # store possible flight
                e = possible_for_flights[keys_for[j]]

                #if departure time of e is greater than current time and flow is less than capacity of e
                if e['dep_time'] >= current_time and e['capacity'] > e['flow'] and G.nodes[v]['label']=='none':

                    # label v with edge e's key (which is index of flight in mydata dataframe)
                    G.nodes[v]['label'] = e['mykey']
                    #print(G.nodes[v]['label'])

                    # label v with either forward labelling
                    G.nodes[v]['l'] = 'f'

                    #update current time to arrival time of this flight
                    current_time = e['arr_time']
                    print('found flight', e, 'from node', u, 'to node', str(v) + '.', 'Now current time is', current_time)
                    foundflight = True

                    return G, e, v, current_time
                j += 1
            if not foundflight:
                print("Couldn't find possible augmenting forward flight from node",u,"to node",v,". Gonna check backward flights between these 2.")

        if found_possible_backward and not foundflight:  # found at least 1 backward flight (from v to u) on path u to v

            if u!=SOURCE:

                if G.nodes[u]['l'] == 'f':          #previous flight was forward (fb)
                    j = 0

                    while not foundflight and j < len(possible_bak_flights):
                        # store possible flight
                        e = possible_bak_flights[keys_bak[j]]

                        # if departure time of at least 1 flight out of the backward edge is greater than current time and flow is greater than 0 and v is unlabeled
                        if e['flow'] > 0 and G.nodes[v]['label'] == 'none':

                            if max([G[pe[0]][pe[1]][pe[2]]['dep_time'] for pe in e['prev_dep_edges']]) >= current_time:
                                # label v with edge e's key (which is index of flight in mydata dataframe)
                                G.nodes[v]['label'] = e['mykey']
                                # print(G.nodes[v]['label'])

                                # label v with either backward labelling
                                G.nodes[v]['l'] = 'b'

                                # update current time to be minimum arrival time of previous arrival edges to this backward edge e
                                current_time = min([G[pe[0]][pe[1]][pe[2]]['arr_time'] for pe in e['prev_arr_edges']])
                                print('found flight', e, 'from node', u, 'to node', str(v) + '.', 'Now current time is',
                                      current_time)
                                foundflight = True

                                return G, e, v, current_time

                        j += 1

                elif G.nodes[u]['l'] == 'b':        #previous edge was b (bb)
                    j = 0

                    while not foundflight and j < len(possible_bak_flights):
                        # store possible flight
                        e = possible_bak_flights[keys_bak[j]]
                        # if flow is greater than 0 and v is unlabeled

                        if e['flow'] > 0 and G.nodes[v]['label'] == 'none':
                            # label v with edge e's key (which is index of flight in mydata dataframe)
                            G.nodes[v]['label'] = e['mykey']
                            # print(G.nodes[v]['label'])

                            # label v with either backward labelling
                            G.nodes[v]['l'] = 'b'

                            # update current time to be minimum arrival time of previous arrival edges to this backward edge e
                            current_time = min([G[pe[0]][pe[1]][pe[2]]['arr_time'] for pe in e['prev_arr_edges']])
                            print('found flight', e, 'from node', u, 'to node', str(v) + '.', 'Now current time is',
                                  current_time)
                            foundflight = True

                            return G, e, v, current_time
                        j += 1

                else: #previous edge was neither forward nor backward
                    print("Previous edge of current backward edge was neither forward nor backward! ERROR!")
                    sys.exit()

            if not foundflight:  # if you can't find any flight in between the nodes of minpath
                print("Couldn't find possible augmenting backward flight from node", v, "to node", u,
                      ". This path cannot be used to augment flow.")

        i += 1
    if not foundflight:
        #backtrack!
        print("no flight found from node",u)
        return G,None,None,None

#backtrack from v to u and look for another node, keep backtracking until u get to source
def backtrack(G,path,times,edges):
    print('Starting to backtrack for path',path)
    print('times:',times)
    print('edges:',edges)
    while len(path)>1:
        #remove last node in path since that was a deadend
        path.pop()
        #assign starting point of search to last node in path
        u = path[-1]
        #remove last time in times
        times.pop()
        #assign starting time of search to last time in times
        current_time = times[-1]
        #remove last edge in edges
        edges.pop()
        #search for another point (not that old v is labelled and won't be checked again)
        G, e, v, current_time = search_for_v(G, u, current_time)
        if v!=None:
            path.append(v)
            times.append(current_time)
            edges.append(e)
            print('New path found',path)
            print('times',times)
            print('edges',edges)
            return G,v,path,times,edges

    else: #path has only source and you can't go anywhere
        #current flow is maximum!! HALT
        print('Current flow is maximum')
        return G,None,path,times,edges

#keep looking for next vertex (while loop!) until you get to destination
def search_for_t(G,s,current_time,t):
    maxflowreached = False
    path = []
    times = []
    edges = []
    path.append(s)
    times.append(current_time) #change u with s
    G, e, v, current_time = search_for_v(G, s, current_time)
    path.append(v)
    times.append(current_time)
    edges.append(e)

    while v!=t and not maxflowreached:
        G, e, v, current_time = search_for_v(G, v, current_time)
        if v == None:
            #must backtrack
            G,v,path,times,edges = backtrack(G,path,times,edges) #change path[0] with s
            if v == None:
                #Reached max flow, stop
                maxflowreached = True
            else: #backtracking worked
                current_time = times[-1]
        else:
            path.append(v)
            times.append(current_time)
            edges.append(e)

    #else: #for while loop, means go to step 4
    # REACHED t !! YAY
    return G,path,times,edges,maxflowreached


"""
