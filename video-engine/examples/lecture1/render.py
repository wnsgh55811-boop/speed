"""Render the lecture: slide stills + in-slide clips on slide 11 + FishAudio/clip audio + burned ASS subtitles."""
import json,sys,subprocess,os
S=sys.argv[1]; W=S+"/work"; OUT=sys.argv[2]; GAIN=json.load(open(W+"/gain.json"))
T=json.load(open(W+"/timeline.json")); FPS=30
CLIP={"H":S+"/dl/1강/1강 하이에나의 태도.mp4","L":S+"/dl/1강/1강 사자의 태도.mp4"}
BOX={"H":(128,409,800,496),"L":(992,409,800,496)}   # PPT media frames (EMU -> px)
FISH=S+"/dl/1강/1강 음성.wav"

def ts(t):
    h=int(t//3600); m=int(t%3600//60); s=t%60
    return "%d:%02d:%05.2f"%(h,m,s)
# ---- ASS subtitles: fixed bottom-centre position, one line, white on 60% black box
ass=["[Script Info]","ScriptType: v4.00+","PlayResX: 1920","PlayResY: 1080","WrapStyle: 2","ScaledBorderAndShadow: yes","",
"[V4+ Styles]",
"Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
"Style: Sub,Noto Sans CJK KR Medium,54,&H00FFFFFF,&H00FFFFFF,&H66000000,&H66000000,0,0,0,0,100,100,0,0,3,12,0,2,60,60,46,1",
"","[Events]","Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
for s in T["subs"]:
    ass.append("Dialogue: 0,%s,%s,Sub,,0,0,0,,{\\an2\\pos(960,1037)}%s"%(ts(s["s"]),ts(s["e"]),s["text"]))
open(W+"/subs.ass","w",encoding="utf-8").write("\n".join(ass)+"\n")

# ---- slide stills via concat demuxer
lst=[]
for k,a,b in T["slides"]:
    lst+=["file '%s/slides/s-%02d.png'"%(S,k),"duration %.6f"%(b-a)]
lst.append("file '%s/slides/s-%02d.png'"%(S,T["slides"][-1][0]))
open(W+"/slides.txt","w").write("\n".join(lst)+"\n")

s11=[x for x in T["slides"] if x[0]==11][0]
clips=[g for g in T["segs"] if g["kind"]=="clip"]
inputs=["-f","concat","-safe","0","-i",W+"/slides.txt"]
for g in clips: inputs+=["-i",CLIP[g["clip"]]]
inputs+=["-i",FISH]
fi=1+len(clips)
fc=["[0:v]fps=%d,format=yuv420p,setsar=1[base]"%FPS]
v="base"
for n,g in enumerate(clips):
    x,y,w,h=BOX[g["clip"]]; hold=s11[2]-g["out1"]+1
    fc.append("[%d:v]fps=%d,scale=%d:%d:flags=lanczos,setsar=1,format=yuv420p,tpad=stop_mode=clone:stop_duration=%.3f,setpts=PTS-STARTPTS+%.4f/TB[c%d]"%(n+1,FPS,w,h,hold,g["out0"],n))
    fc.append("[%s][c%d]overlay=%d:%d:eof_action=pass:enable='between(t,%.4f,%.4f)'[v%d]"%(v,n,x,y,g["out0"],s11[2]-0.001,n)); v="v%d"%n
fc.append("[%s]ass=%s/subs.ass,trim=duration=%.4f[vout]"%(v,W,T["total"]))
# audio: narration pieces and clip originals, never overlapping
al=[]
for n,g in enumerate(T["segs"]):
    if g["kind"]=="fish":
        fc.append("[%d:a]atrim=%.5f:%.5f,asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo[a%d]"%(fi,g["src0"],g["src1"],n))
    else:
        ci=1+[c["clip"] for c in clips].index(g["clip"])
        fc.append("[%d:a]atrim=0:%.5f,asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,volume=%.2fdB,apad=whole_dur=%.5f[a%d]"%(ci,g["out1"]-g["out0"],GAIN[g["clip"]],g["out1"]-g["out0"],n))
    al.append("[a%d]"%n)
fc.append("%sconcat=n=%d:v=0:a=1[aout]"%("".join(al),len(al)))
cmd=["ffmpeg","-y","-v","error","-stats"]+inputs+["-filter_complex",";".join(fc),"-map","[vout]","-map","[aout]",
 "-c:v","libx264","-preset","slow","-crf","14","-tune","stillimage","-profile:v","high","-pix_fmt","yuv420p","-r",str(FPS),"-g","60",
 "-x264-params","vbv-maxrate=20000:vbv-bufsize=40000",
 "-c:a","aac","-b:a","320k","-ar","48000","-ac","2","-movflags","+faststart","-t","%.4f"%T["total"],OUT]
print(" ".join(cmd[:8]),"...")
subprocess.run(cmd,check=True)
