'''
input:
matrix =[
    [
        tf-idf, word-to-vector
    ]
]
output:
    algorithms_type
'''
import subprocess
from collections import defaultdict
import python_minifier
#subprocess.check_output(['ls', '-l'])  # All that is technically needed...
# print(subprocess.run(['pyminify', '--remove-literal-statements', '/Users/yuqifan/Documents/GitHub/JupyterNotebook/machine_learning_data/Best-first+search+algorithm/8 puzzle_v2.clean.py']))

# lines_without_comment = []
path = '/Users/yuqifan/Documents/GitHub/JupyterNotebook/machine_learning_data/'
from pathlib import Path
p = Path(path)
# # for kind in p.iterdir():
# #     for i in kind.iterdir(): 
# #         if '.py' in i.suffixes and i.is_file() and '.clean' not in i.suffixes:
# #             text= i.read()
dir_length_total=0
unicode_error=0
errdict=defaultdict(int)
syntax_error_total=0
kind_dict=defaultdict(int)
for kind in p.iterdir():
    kind_length=0
    if not kind.is_dir():
        continue
    for i in kind.iterdir(): 
        kind_length+=1
        if '.py' in i.suffixes and i.is_file() and '.clean' not in i.suffixes:
            try:
                # print (i)
                text= i.open().read()
                text= python_minifier.minify(text, remove_literal_statements= True, rename_globals=True)
                with open (i.parent / (i.stem + '.clean' + i.suffix), "w") as newfile:
                    newfile.write(text)
            except UnicodeDecodeError:
                # print ("UnicodeDecodeError",i)
                unicode_error+=1
            except SyntaxError:
                i.unlink()
                syntax_error_total+=1
                errdict[kind.name]+=1
                print (f"removed {kind.name}",i)
            finally:
                dir_length_total+=1
                kind_length+=1
                # break
    kind_dict[kind.name]= kind_length
    kind_length
    # break
print(f'{dir_length_total}')
print(f'{syntax_error_total}')
print(f'{unicode_error}')
for k, i in errdict.items():
    for g, q in kind_dict.items():
        if (k==g):
            print (k,i,q)

