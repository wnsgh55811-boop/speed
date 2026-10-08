import cv2,numpy as np,json,sys
S=sys.argv[1]; sys.path.insert(0,S+'/scripts')
from regions import R
out={}
def bgest(im,regs):
    sc=5
    small=cv2.resize(im,(384,216),interpolation=cv2.INTER_AREA)
    m=np.zeros((216,384),np.uint8)
    for (x0,y0,x1,y1) in regs.values(): m[max(y0//sc-3,0):y1//sc+3,max(x0//sc-3,0):x1//sc+3]=255
    bg=cv2.inpaint(np.clip(small,0,255).astype(np.uint8),m,25,cv2.INPAINT_TELEA).astype(np.float32)
    bl=cv2.GaussianBlur(bg,(0,0),6)
    bg=np.where(m[...,None]>0,bl,bg)
    return cv2.resize(bg,(1920,1080),interpolation=cv2.INTER_CUBIC)
for i,regs in R.items():
    im=cv2.imread(f'{S}/w/slides/s{i:02d}.png').astype(np.float32)
    bg=bgest(im,regs); dev=np.abs(im-bg).max(2); mask=(dev>7).astype(np.uint8)
    plate=im.copy(); out[i]={}
    F=10
    for k,(x0,y0,x1,y1) in regs.items():
        sub=mask[y0:y1,x0:x1]; ys,xs=np.nonzero(sub)
        if len(xs)==0: print('EMPTY',i,k); continue
        bx0,by0,bx1,by1=x0+xs.min()-F,y0+ys.min()-F,x0+xs.max()+F+1,y0+ys.max()+F+1
        bx0,by0=max(bx0,0),max(by0,0); bx1,by1=min(bx1,1920),min(by1,1080)
        w,h=bx1-bx0,by1-by0
        a=np.ones((h,w),np.float32)
        r=np.minimum(np.minimum(np.arange(w)[None,:]+1,w-np.arange(w)[None,:]),np.minimum(np.arange(h)[:,None]+1,h-np.arange(h)[:,None]))
        a=np.clip(r/F,0,1)
        crop=np.dstack([im[by0:by1,bx0:bx1],a[...,None]*255]).astype(np.uint8)
        cv2.imwrite(f'{S}/eng/assets/c{i:02d}_{k}.png',crop)
        # fill plate: blend toward bg with same alpha
        plate[by0:by1,bx0:bx1]=plate[by0:by1,bx0:bx1]*(1-a[...,None])+bg[by0:by1,bx0:bx1]*a[...,None]
        out[i][k]=[int(bx0),int(by0),int(w),int(h)]
    cv2.imwrite(f'{S}/eng/assets/p{i:02d}.jpg',np.clip(plate,0,255).astype(np.uint8),[cv2.IMWRITE_JPEG_QUALITY,96])
json.dump(out,open(f'{S}/eng/crops.json','w'))
print(json.dumps(out)[:3000])
