#Matthew Smith-Kennedy ms11ag


def runPrim(self, edgelist, nodecount):
        edgelist.sort(key=returnweight)
        setlist =set()   ##just a set not a list of sets
        edgelist[0].selected =True
        setlist.add(edgelist[0])  #add first edge to set
        flag = 0
        edgelist[0].extra = 0
        while flag < nodecount -1:  #run for nodecount -1
            count = 1
            not_set = False
            while count < len(edgelist) and not_set is False:    ##iteration
                foundfirst = False
                foundsecond = False
                discard = False
                if edgelist[count].extra == 1:    ##skip processed edges where extra == 0
                    for k in setlist:
                        if edgelist[count].Vertex2 == k.Vertex1:
                            foundsecond = True
                        if edgelist[count].Vertex2 == k.Vertex2:
                            foundsecond = True
                        if edgelist[count].Vertex1 == k.Vertex1:
                            foundfirst = True
                        if edgelist[count].Vertex1 == k.Vertex2:
                            foundfirst = True
                    if foundfirst and foundsecond:      ##creates cycle //ignore edge
                        discard = True
                        edgelist[count].extra = 0
                    elif foundsecond or foundfirst and not discard:
                        setlist.add(edgelist[count])
                        edgelist[count].selected = True
                        edgelist[count].extra = 0
                        not_set = True       ##break on adding edge
                count += 1
            flag += 1
        return


def returnweight(value):
    return value.weight



