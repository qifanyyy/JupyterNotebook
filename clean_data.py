import re

# print(stripComments("""#foo bar
# bar foo
# # buz"""))
lines_without_comment = []
path = '/Users/yuqifan/Documents/GitHub/JupyterNotebook/machine learning data/'
from pathlib import Path
p = Path(path)
# for kind in p.iterdir():
#     for i in kind.iterdir(): 
#         if '.py' in i.suffixes and i.is_file() and '.clean' not in i.suffixes:
#             text= i.read()
        
for kind in p.iterdir():
    if not kind.is_dir():
        continue
    for i in kind.iterdir(): 
        if '.py' in i.suffixes and i.is_file() and '.clean' not in i.suffixes:
            print (i)
            try:
                function_name_dict={}
                quote_flag=0
                lines_without_comment = []
                function_default_num = 0
                for line in i.open():
                    # if '"""' in i:
                    #     if quote_flag==0:
                    #         quote_flag= 1
                    #     else:
                    #         quote_flag= 0
                    # if quote_flag==1:
                    #     rematch_thing= re.match("def ([_a-zA-Z][_a-zA-Z0-9]*)",line)
                    
                    ##remove and replace all function_name and every time their name appears
                    for k in function_name_dict.keys():
                        if k in line:
                            print("replaced!")
                            # line = line.replace(k, function_name_dict[k])
                            print(line)
                    comment_start_index = line.rfind('#')
                    if re.match("def ([_a-zA-Z][_a-zA-Z0-9]*)",line) is not None:
                        print("??")
                        ##get and replace function name
                        rematch_thing= re.match("def ([_a-zA-Z][_a-zA-Z0-9]*)",line)
                        function_original = rematch_thing.group(1)
                        print ("group1:"+function_original)
                        ##add function names to dict, so could replace whenever function name appears
                        function_name_dict[function_original]= "default"+ str(function_default_num)
                        # print (function_original)
                        #replace function name with default
                        # line= re.sub("def ([_a-zA-Z][_a-zA-Z0-9]*)","def "+"default"+str(function_default_num),line)
                        function_default_num+=1 
                    # newline = line[:comment_start_index].rstrip()
                    newline= line
                    if len(newline) > 0:
                        lines_without_comment.append(newline+"\n")
                text=''.join(lines_without_comment)
                with open (i.parent / (i.stem + '.clean' + i.suffix), "w") as newfile:
                    # remove_comments_and_docstrings(text)
                    newfile.write(text)
            except UnicodeDecodeError:
                pass
        print (i)
    # break
