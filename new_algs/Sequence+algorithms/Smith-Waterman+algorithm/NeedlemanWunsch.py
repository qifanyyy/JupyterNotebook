def needleman_wunsch(Query,Reference,gap_penalty,match_score,mismatch_score):
    matrix=[[0 for x in range(len(Query)+1)] for y in range(len(Reference)+1)] #For calculating scores
    direction=[['*' for x in range(len(Query)+1)] for y in range(len(Reference)+1)] #For backtracking

    for i in range(len(Reference)+1):
        matrix[i][0]=gap_penalty*i
        direction[i][0]='up'

    for j in range(len(Query)+1):
        matrix[0][j]=gap_penalty*j
        direction[0][j]='left'

    direction_map={0:'diagonal',1:'up',2:'left'}

    #Perform the algorithm here
    for i in range(1,len(Reference)+1):
        for j in range(1,len(Query)+1):
            if Reference[i-1]==Query[j-1]:
                diagonalScore=matrix[i-1][j-1]+match_score
            else:
                diagonalScore=matrix[i-1][j-1]+mismatch_score
            up_score=matrix[i-1][j]+gap_penalty
            left_score=matrix[i][j-1]+gap_penalty
            matrix[i][j]=max(diagonalScore,up_score,left_score)
            max_index=[diagonalScore,up_score,left_score].index(matrix[i][j])
            direction[i][j]=direction_map[max_index]

    #Backtracking
    row=len(Reference)
    col=len(Query)
    Reference_with_gaps=''
    Query_with_gaps=''
    while row>0 or col>0:
        if direction[row][col]=='diagonal':
            Query_with_gaps=''.join((Query_with_gaps,Query[col-1]))
            Reference_with_gaps=''.join((Reference_with_gaps,Reference[row-1]))
            col-=1
            row-=1
        elif direction[row][col]=='up':
            Query_with_gaps=''.join(('-',Query_with_gaps))
            Reference_with_gaps=''.join((Reference[row-1],Reference_with_gaps))
            row-=1
        elif direction[row][col]=='left':
            Reference_with_gaps = ''.join(('-',Reference_with_gaps))
            Query_with_gaps = ''.join((Query[col-1],Query_with_gaps))
            col-=1

    return str(matrix[len(Reference)][len(Query)]),Query_with_gaps,Reference_with_gaps

def string_alignment(aligned_query,aligned_reference):
    identity,gaps,mismatches=0,0,0
    alignment_string=''
    for base1,base2 in zip(aligned_query,aligned_reference):
        if base1==base2:
            alignment_string=''.join((alignment_string,'|'))
            identity+=1
        elif '-' in (base1,base2):
            alignment_string = ''.join((alignment_string, '-'))
            gaps+=1
        else:
            alignment_string = ''.join((alignment_string, ':'))
            mismatches+=1
    return alignment_string,identity,gaps,mismatches

def DataInput(Query,Reference,NuclorAA,match_score,mismatch_penalty,gap_penalty):
    aaSet={'X','A','R','N','D','C','Q','E','G','H','I','L','K','M','F','P','S','T','W','Y','V'}
    nuclSet={'A','T','C','G','U'}
    Query = Query.lstrip().rstrip().upper()
    Reference = Reference.lstrip().rstrip().upper()
    if NuclorAA==1:
        for nucl in Query:
            if nucl not in nuclSet:
                return "Wrong Input!"
        for nucl in Reference:
            if nucl not in nuclSet:
                return "Wrong Input!"
    elif NuclorAA==2:
        for aa in Query:
            if aa not in aaSet:
                return "Wrong Input!"
        for aa in Reference:
            if aa not in aaSet:
                return "Wrong Input!"
    max_score,aligned_query,aligned_reference=needleman_wunsch(Query,Reference,gap_penalty,match_score,mismatch_penalty)
    alignment_string, identity, gaps, mismatches=string_alignment(aligned_query,aligned_reference)
    max_score=' '.join(('alignment score:',str(max_score)))
    aligned_query=' '.join(('aligned query:',aligned_query))
    aligned_reference = ' '.join(('aligned reference:', aligned_reference))
    alignment_stringV1=' '.join(('alignment string:', alignment_string))
    identityV1=' '.join(('alignment identity:',str(identity)))
    identityV2=''.join((str(round(identity/len(alignment_string)*100, 2)),'%'))
    identityV1=' '.join((identityV1,identityV2))
    gapsV1 = ' '.join(('alignment gaps:', str(gaps)))
    gapsV2 = ''.join((str(round(gaps/len(alignment_string)*100, 2)), '%'))
    gapsV1 = ' '.join((gapsV1, gapsV2))
    mismatchesV1 = ' '.join(('alignment mismatches:', str(mismatches)))
    mismatchesV2 = ''.join((str(round(mismatches/len(alignment_string)*100, 2)),'%'))
    mismatchesV1 = ' '.join((mismatchesV1, mismatchesV2))
    return (max_score,aligned_query,aligned_reference,alignment_stringV1,identityV1,gapsV1,mismatchesV1)
