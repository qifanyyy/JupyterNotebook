from tkinter import *
import NeedlemanWunsch as NW
import SmithWaterman as SW
from tkinter import filedialog
import ReadExternalFile as RE
def DefineFileDialog(label,QueryEntry,ReferenceEntry,Output,para):
    if NuclorAA==1:
        queryFile=filedialog.askopenfilename(title='Open the query file',filetypes=(("fna files","*.fna"),))
        ReferenceFile=filedialog.askopenfilename(title='Open the reference file',filetypes=(("fna files","*.fna"),))
    elif NuclorAA==2:
        queryFile=filedialog.askopenfilename(title='Open the query file',filetypes=(("faa files","*.faa"),))
        ReferenceFile=filedialog.askopenfilename(title='Open the reference file',filetypes=(("faa files","*.faa"),))
    with open(queryFile,"r") as query:
        QueryEntry.insert("1.0", query.read())
    with open(ReferenceFile,"r") as Reference:
        ReferenceEntry.insert("1.0",Reference.read())
    ResultList=RE.Processing(queryFile,ReferenceFile)
    if ResultList == 'These two files are not paired!':
        label.configure(text=ResultList)
    else:
        OutputName = Output.get().rstrip()
        outPutFile = filedialog.askdirectory(title='Specify the output directory')
        outputFile = '/'.join((outPutFile, OutputName))
        gap_penalty, mismatch_penalty, matchScore=para
        with open(outputFile, "a") as Results:
            for query,reference in zip(ResultList[0],ResultList[1]):
                if NWorSW == 2:
                    SWAlignmentResults = SW.DataInput(Query=query,
                                                      Reference=reference, NuclorAA=NuclorAA,
                                                      gap_penalty=int(gap_penalty), match_score=int(matchScore),
                                                      mismatch_penalty=int(mismatch_penalty))
                    Results.write('\n'.join((SWAlignmentResults)))
                    Results.write('\n\n')
                elif NWorSW == 1:
                    NWAlignmentResults = NW.DataInput(Query=query,
                                                      Reference=reference, NuclorAA=NuclorAA,
                                                      gap_penalty=int(gap_penalty), match_score=int(matchScore),
                                                      mismatch_penalty=int(mismatch_penalty))
                    Results.write('\n'.join((NWAlignmentResults)))
                    Results.write('\n\n')

def DefineClearButton1(window,entry):
    thisButton = Button(window, text="Clear the query", font=("Arial Bold", 15), bg="orange", fg="white",
                         command=lambda:ClearanceClicked(entry))
    thisButton.grid(column=0, row=3)
    return thisButton

def DefineClearButton2(window, entry):
    thisButton = Button(window, text="Clear the reference", font=("Arial Bold", 15), bg="black", fg="green",
                         command=lambda: ClearanceClicked(entry))
    thisButton.grid(column=1, row=3)
    return thisButton

def ClearanceClicked(entry):
    entry.delete("1.0", END)

def OutputFilename(window):
    name=Entry(window,width=20,font=('Verdana',12),fg='black')
    name.grid(column=1,row=10)
    return name

def setTextEntry1(window):
    this_font = ('Verdana', 15)
    queryEntry=Text(window,width=20,height=5,font=this_font,fg='black')
    queryEntry.grid(column=0,row=2)
    return queryEntry

def setTextEntry2(window):
    this_font = ('Verdana', 15)
    referenceEntry=Text(window,width=20,height=5,font=this_font,fg='black')
    referenceEntry.grid(column=1,row=2)
    return referenceEntry

def defineGapPenalty(window):
    this_font = ('Verdana', 12)
    thisEntry=Entry(window,width=5,font=this_font,fg='grey')
    thisEntry.grid(column=0,row=5)
    return thisEntry

def defineMismatchPenalty(window):
    this_font = ('Verdana', 12)
    thisEntry = Entry(window, width=5, font=this_font, fg='grey')
    thisEntry.grid(column=1, row=5)
    return thisEntry

def defineMatchScore(window):
    this_font = ('Verdana', 12)
    thisEntry = Entry(window, width=5, font=this_font, fg='grey')
    thisEntry.grid(column=0, row=7)
    return thisEntry

def getTextButton(window,label):
    TextEnterButton = Button(window, text="TextAlignment-Enter", font=("Arial Bold", 20), bg="white", fg="blue",
                             command=lambda:Textclicked(window,label))
    TextEnterButton.grid(column=0, row=9)
    return TextEnterButton

def getFileButton(window,label):
    FileEnterButton = Button(window, text="FileAlignment-Enter", font=("Arial Bold", 20), bg="blue", fg="white")
    FileEnterButton.grid(column=0, row=10)
    return FileEnterButton

def DefineRetryButton(window,label):
    RetryButton = Button(window, text="Retry", font=("Arial Bold", 20), bg="orange", fg="black")
    RetryButton.grid(column=0, row=2)
    RetryButton['command']=lambda:Retryclicked(window,RetryButton,label)

def Fileclicked(label,queryEntry,referenceEntry,gap_penaltyEntry,
    mismatch_penaltyEntry,matchScoreEntry,outputName):
    gap_penalty = gap_penaltyEntry.get()
    mismatch_penalty = mismatch_penaltyEntry.get()
    matchScore = matchScoreEntry.get()
    para = (gap_penalty, mismatch_penalty, matchScore)
    if ifRepresetentsInt(para) == False:
        label.configure(text='Parameters should be integers!')
    else:
        DefineFileDialog(label,queryEntry,referenceEntry,outputName,para)

def ifRepresetentsInt(para):
    for s in para:
        try:
            int(s)
        except ValueError:
            return False
    return True

def RadioButtonclicked(index):
    global NuclorAA,NWorSW
    if index==1:
        NuclorAA=1
    elif index==2:
        NuclorAA=2
    elif index==3:
        NWorSW=1
    elif index==4:
        NWorSW=2

def Textclicked(window,label,fileButton,textButton,queryEntry,referenceEntry,EntryClearance,ReferenceClearance,gap_penaltyEntry,mismatch_penaltyEntry,matchScoreEntry,hints,radios,outputName):
    gap_penalty = gap_penaltyEntry.get()
    mismatch_penalty = mismatch_penaltyEntry.get()
    matchScore = matchScoreEntry.get()
    para=(gap_penalty,mismatch_penalty,matchScore)
    if ifRepresetentsInt(para)==False:
        label.configure(text='Parameters should be integers!')
    elif ifRepresetentsInt(para) and NWorSW==2:
        SWAlignmentResults = SW.DataInput(Query=queryEntry.get("1.0", END), Reference=referenceEntry.get("1.0", END), NuclorAA=NuclorAA,
                                              gap_penalty=int(gap_penalty), match_score=int(matchScore),
                                              mismatch_penalty=int(mismatch_penalty))

        label.configure(text='\n'.join(SWAlignmentResults), font=("Arial Bold", 15), bg="blue", fg="white")
    elif ifRepresetentsInt(para) and NWorSW==1:
        NWAlignmentResults=NW.DataInput(Query=queryEntry.get("1.0", END), Reference=referenceEntry.get("1.0", END), NuclorAA=NuclorAA,
                                              gap_penalty=int(gap_penalty), match_score=int(matchScore),
                                              mismatch_penalty=int(mismatch_penalty))
        label.configure(text='\n'.join(NWAlignmentResults), font=("Arial Bold", 15), bg="blue", fg="white")
    fileButton.destroy()
    textButton.destroy()
    queryEntry.destroy()
    referenceEntry.destroy()
    EntryClearance.destroy()
    ReferenceClearance.destroy()
    gap_penaltyEntry.destroy()
    mismatch_penaltyEntry.destroy()
    matchScoreEntry.destroy()
    outputName.destroy()
    for hint in hints:
        hint.configure(text="")
    for radio in radios:
        radio.destroy()
    DefineRetryButton(window,label)

def Retryclicked(window,RetryButton,label):
    configuration(window)
    RetryButton.destroy()
    label.configure(text="")

def configuration(window):
    label = Label(window, text="Nucleotide/Protein Sequence Alignment Tool", font=("Arial Bold", 25))
    label.grid(column=0, row=0, padx=10, pady=10)
    hint1=Label(window,text='Enter your query here')
    hint1.grid(column=0, row=1, padx=10, pady=8)
    hint2=Label(window,text='Enter your reference here')
    hint2.grid(column=1, row=1, padx=10, pady=8)
    queryEntry = setTextEntry1(window)
    referenceEntry = setTextEntry2(window)
    EntryClearance = DefineClearButton1(window,queryEntry)
    ReferenceClearance = DefineClearButton2(window, referenceEntry)
    hint3 = Label(window, text='gap penalty')
    hint3.grid(column=0, row=4, padx=8, pady=6)
    hint4 = Label(window, text='mismatch penalty')
    hint4.grid(column=1, row=4, padx=8, pady=6)
    hint5 = Label(window, text='match score')
    hint5.grid(column=0, row=6, padx=8, pady=6)
    hint6 = Label(window, text='OutputFilename',font=("Arial Bold", 15))
    hint6.grid(column=1, row=9, padx=8, pady=6)
    hints=(hint1,hint2,hint3,hint4,hint5,hint6)
    gap_penaltyEntry = defineGapPenalty(window)
    mismatch_penaltyEntry = defineMismatchPenalty(window)
    matchScoreEntry = defineMatchScore(window)
    selectedNuclorAA=IntVar()
    Nucl=Radiobutton(window,text='Nucleotide sequences',value=1,variable=selectedNuclorAA)
    Nucl.grid(column=1,row=7)
    Nucl['command']=lambda:RadioButtonclicked(1)
    AA=Radiobutton(window,text='Amino acid sequences',value=2,variable=selectedNuclorAA)
    AA['command']=lambda:RadioButtonclicked(2)
    AA.grid(column=2,row=7)
    selectedNWorSW=IntVar()
    NW=Radiobutton(window,text='Needleman-Wunsch Algorithm',value=1,variable=selectedNWorSW)
    NW['command']=lambda:RadioButtonclicked(3)
    SW=Radiobutton(window,text='Smith-Waterman Algorithm',value=2,variable=selectedNWorSW)
    SW['command']=lambda :RadioButtonclicked(4)
    NW.grid(column=1,row=8)
    SW.grid(column=2,row=8)
    TextButton = getTextButton(window, label)
    FileButton = getFileButton(window, label)
    radios=(Nucl,AA,NW,SW)
    output = OutputFilename(window)
    TextButton['command'] = lambda: Textclicked(window, label, FileButton, TextButton, queryEntry, referenceEntry,
                                                EntryClearance, ReferenceClearance,gap_penaltyEntry,mismatch_penaltyEntry,matchScoreEntry,hints,radios,output)
    FileButton['command'] = lambda: Fileclicked(label, queryEntry, referenceEntry,
                                                gap_penaltyEntry,mismatch_penaltyEntry,matchScoreEntry,output)

def main():
    window = Tk()
    window.title("Welcome to Sequence Alignment App")
    configuration(window)
    window.geometry('1200x480')
    window.mainloop()

if __name__ == '__main__':
    main()



