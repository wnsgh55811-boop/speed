import json, os, sys
P='audio_ledger.json'
def load():
    return json.load(open(P)) if os.path.exists(P) else {}
def add(pairs):
    d=load()
    for idx,job,url in pairs: d[str(idx)]={'job_id':job,'url':url}
    json.dump(d,open(P,'w'),indent=1,sort_keys=True)
    print('ledger entries:',len(d))
    S=json.load(open('scenes.json'))
    miss=[i for i in range(len(S)) if str(i) not in d]
    print('missing:',miss[:20],'...' if len(miss)>20 else '','count',len(miss))
if __name__=='__main__':
    add(json.loads(sys.argv[1]))
