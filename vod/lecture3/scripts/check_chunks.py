import sys; sys.path.insert(0, sys.argv[3])
from chunks import *
import re
sl=load_chunks(sys.argv[1]); sc=load_script(sys.argv[2])
print(len(sl),len(sc))
norm=lambda s: re.sub(r'\s+',' ',s).strip()
bad=0
for i,(a,b) in enumerate(zip(sl,sc),1):
    j=' '.join(' '.join(x) for x in a if not x[0].startswith('@'))
    if norm(j)!=norm(b):
        bad+=1; print('MISMATCH slide',i); 
        import difflib
        for k,(x,y) in enumerate(zip(norm(j),norm(b))):
            if x!=y: print(' at',k, repr(norm(j)[k-10:k+20]),'|',repr(norm(b)[k-10:k+20])); break
        else: print(' len',len(norm(j)),len(norm(b)))
    for x in a:
        if x[0].startswith('@'): continue
        for c in x:
            if len(c)>25: bad+=1; print('LONG',i,len(c),c)
print('bad',bad)
