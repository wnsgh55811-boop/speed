import json,subprocess,sys
from PIL import Image,ImageDraw,ImageFont
W=sys.argv[1]; out=sys.argv[2]
d=json.load(open(f"{W}/timeline.json")); cuts=d["cuts"]; ch=d["chunks"]
FPS=30; N=round(d["dur"]*FPS)
font=ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc",54,index=1)
slides=[Image.open(f"{W}/slides/s-{i}.png").convert("RGB") for i in range(1,8)]
BOX_TOP,BOX_H,PAD=971,78,12
def sub_layer(text):
    tw=font.getlength(text); bw=round(tw)+2*PAD
    L=Image.new("RGBA",(1920,1080),(0,0,0,0)); dr=ImageDraw.Draw(L)
    x0=(1920-bw)//2
    dr.rectangle([x0,BOX_TOP,x0+bw-1,BOX_TOP+BOX_H-1],fill=(0,0,0,153))
    dr.text((960,BOX_TOP+BOX_H/2),text,font=font,fill=(255,255,255,255),anchor="mm")
    return L,bw
cache={}
def frame(si,ci):
    k=(si,ci)
    if k not in cache:
        im=slides[si].copy()
        if ci is not None: im=Image.alpha_composite(im.convert("RGBA"),sub_layer(ch[ci]["text"])[0]).convert("RGB")
        cache[k]=im.tobytes()
    return cache[k]
ff=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s","1920x1080","-r",str(FPS),"-i","-",
  "-i",f"{W}/voice.wav","-map","0:v","-map","1:a",
  "-vf","scale=out_color_matrix=bt709:out_range=tv:flags=lanczos+accurate_rnd+full_chroma_int","-c:v","libx264","-preset","slow","-crf","8","-x264-params","keyint=60:min-keyint=30","-tune","stillimage","-pix_fmt","yuv420p",
  "-color_primaries","bt709","-color_trc","bt709","-colorspace","bt709","-profile:v","high","-r",str(FPS),
  "-c:a","aac","-b:a","320k","-ar","48000","-ac","2","-t",f"{N/FPS:.3f}","-movflags","+faststart",out],stdin=subprocess.PIPE)
log=[]
for f in range(N):
    t=(f+0.5)/FPS
    si=max(i for i in range(7) if cuts[i]<=t+1e-9)
    ci=next((i for i,c in enumerate(ch) if c["s"]<=t<c["e"]),None)
    ff.stdin.write(frame(si,ci)); log.append((si,ci))
ff.stdin.close(); ff.wait()
json.dump({"widths":{c["text"]:sub_layer(c["text"])[1] for c in ch},"frames":log},open(f"{W}/render_log.json","w"),ensure_ascii=False)
print("frames",N,"rc",ff.returncode)
