#!/bin/bash
# End-to-end remote build. Runs in one pass because the sandbox does not survive
# between calls: fetch -> narration -> align -> time -> audio -> compose -> render.
set -e
SHA="$1"
R=https://raw.githubusercontent.com/wnsgh55811-boop/speed/$SHA/video
export PATH=/opt/node22/bin:$PATH
export PRODUCER_PAGE_NAVIGATION_TIMEOUT_MS=300000
export PRODUCER_PLAYER_READY_TIMEOUT_MS=300000
export PRODUCER_PUPPETEER_PROTOCOL_TIMEOUT_MS=1800000
cd /home/user && rm -rf v2 && mkdir -p v2/build v2/assets/fonts v2/assets/img v2/assets/audio v2/out
cd v2
for f in index.html package.json hyperframes.json meta.json assets/anim2.js assets/gsap.min.js \
  build/gen2.py build/css2.py build/render2.py build/scenes2.json build/beats.json \
  build/blocks2.json build/vo_ledger.json build/image_ledger2.json build/sub_widths2.json \
  build/align.py build/maptimes.py build/build_master2.py build/build_sfx.py; do
  curl -fsSL --retry 3 -o "$f" "$R/$f"
done
for w in Regular Medium SemiBold Bold ExtraBold Black; do
  curl -fsSL --retry 3 -o assets/fonts/Pretendard-$w.otf "$R/assets/fonts/Pretendard-$w.otf"; done

echo "== assets =="
cd build && python3 - <<'PY'
import json, subprocess, concurrent.futures as cf
vo  = json.load(open('vo_ledger.json'))
img = {k:v for k,v in json.load(open('image_ledger2.json')).items() if not k.startswith('_')}
def a(kv):
    k,v=kv; return subprocess.run(['curl','-fsSL','--retry','4','-o',
        f'../assets/audio/b{int(k):02d}_raw.mp3', v['url']]).returncode
def i(kv):
    n,v=kv; t=f'/tmp/{n}.src'
    if subprocess.run(['curl','-fsSL','--retry','4','-o',t,v['url']]).returncode: return 1
    if v['kind']=='photo':
        subprocess.run(['ffmpeg','-v','error','-i',t,'-vf',
          'scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080','-q:v','3',
          '-y',f'../assets/img/{n}.jpg'],check=True)
    else:
        subprocess.run(['ffmpeg','-v','error','-i',t,'-y',f'../assets/img/{n}.png'],check=True)
    return 0
with cf.ThreadPoolExecutor(16) as ex:
    ra=list(ex.map(a, vo.items())); ri=list(ex.map(i, img.items()))
print('narration', len(ra)-sum(ra), 'images', len(ri)-sum(ri))
# 3D objects come on flat white; key them to alpha
for n,v in img.items():
    if v['kind']!='icon3d' or 'cut_job' in v: continue
    p=f'../assets/img/{n}.png'
    subprocess.run(['ffmpeg','-v','error','-i',p,'-vf',
        'format=rgba,colorkey=0xFFFFFF:0.16:0.06,format=rgba','-y','/tmp/k.png'],check=True)
    subprocess.run(['cp','/tmp/k.png',p],check=True)
# 1.2x once, pitch preserved, levels matched
for k in vo:
    i2=int(k)
    subprocess.run(['ffmpeg','-v','error','-i',f'../assets/audio/b{i2:02d}_raw.mp3',
        '-af','atempo=1.2,loudnorm=I=-20:TP=-2:LRA=11','-ar','48000','-ac','1','-b:a','128k',
        '-y',f'../assets/audio/b{i2:02d}.mp3'],check=True)
print('narration at 1.2x ready')
PY

echo "== word alignment =="
python3 align.py 12
echo "== cue timing =="
python3 maptimes.py
echo "== compose (pass 1, for scene order) =="
HF_NO_AUDIO=1 python3 gen2.py
echo "== soundtrack =="
python3 build_sfx.py && python3 build_master2.py
echo "== compose (render pass, picture only) =="
HF_NO_AUDIO=1 python3 gen2.py
cd .. && npx --yes hyperframes@0.8.56 lint 2>&1 | grep -E "error\(s\)"

echo "== bundle =="
cd /home/user && tar -cf bundle.tar v2
ls -la bundle.tar
. /home/user/up_urls.sh
curl -f -X PUT -H "Content-Type: application/octet-stream" --data-binary @bundle.tar "$U_BUNDLE" \
     -s -o /dev/null -w "bundle:%{http_code} %{size_upload}\n"
echo PHASE_A_DONE
