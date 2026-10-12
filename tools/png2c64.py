"""PNG (320x200 GB64 screenshot) -> C64 bitmap slot.
Slot layout (10240 bytes): [0]=mode (0=hires,1=multicolor) [1]=bg color [2..15]=reserved
[16..8015]=bitmap  [8016..9015]=screen RAM  [9016..10015]=color RAM  rest padding."""
import zlib, struct, sys
SLOT=10240
PAL=[(0,0,0),(255,255,255),(136,57,50),(103,182,189),(139,63,150),(85,160,73),(64,49,141),(191,206,114),
     (139,84,41),(87,66,0),(184,105,98),(80,80,80),(120,120,120),(148,224,137),(120,105,196),(159,159,159)]
def read_png(path):
    d=open(path,'rb').read(); assert d[:8]==b'\x89PNG\r\n\x1a\n'
    i=8; idat=b''; plte=None
    while i<len(d):
        ln,typ=struct.unpack('>I4s',d[i:i+8]); body=d[i+8:i+8+ln]; i+=12+ln
        if typ==b'IHDR': w,h,bd,ct,_,_,il=struct.unpack('>IIBBBBB',body)
        elif typ==b'PLTE': plte=[tuple(body[j:j+3]) for j in range(0,len(body),3)]
        elif typ==b'IDAT': idat+=body
    assert il==0, 'interlaced'
    ch={0:1,2:3,3:1,4:2,6:4}[ct]; bpp=max(1,ch*bd//8); stride=(w*ch*bd+7)//8
    raw=zlib.decompress(idat); out=[]; prev=bytearray(stride); p=0
    for y in range(h):
        f=raw[p]; line=bytearray(raw[p+1:p+1+stride]); p+=1+stride
        for x in range(stride):
            a=line[x-bpp] if x>=bpp else 0; b=prev[x]; c=prev[x-bpp] if x>=bpp else 0
            if f==1: line[x]=(line[x]+a)&255
            elif f==2: line[x]=(line[x]+b)&255
            elif f==3: line[x]=(line[x]+((a+b)>>1))&255
            elif f==4:
                pa,pb,pc=abs(b-c),abs(a-c),abs(a+b-2*c)
                line[x]=(line[x]+(a if pa<=pb and pa<=pc else b if pb<=pc else c))&255
        prev=line; row=[]
        for x in range(w):
            if bd==8: v=line[x*ch:x*ch+ch]
            else:
                bit=x*bd; v=[(line[bit>>3]>>(8-bd-(bit&7)))&((1<<bd)-1)]
            if ct==3: row.append(plte[v[0]])
            elif ct in (0,4): row.append((v[0],)*3)
            else: row.append(tuple(v[:3]))
        out.append(row)
    return w,h,out
CCS64=[(16,16,16),(255,255,255),(224,64,64),(96,255,255),(224,96,224),(64,224,64),(64,64,224),(255,255,64),
       (224,160,64),(156,116,72),(255,160,160),(84,84,84),(136,136,136),(160,255,160),(160,160,255),(192,192,192)]
PEPTO=[(0,0,0),(255,255,255),(104,55,43),(112,164,178),(111,61,134),(88,141,67),(53,40,121),(184,199,111),
       (111,79,37),(67,57,0),(154,103,89),(68,68,68),(108,108,108),(154,210,132),(108,94,181),(149,149,149)]
REFS=[(c,i) for pal in (CCS64,PEPTO,PAL) for i,c in enumerate(pal)]
_cache={}
def near(rgb):
    if rgb not in _cache:
        _cache[rgb]=min(REFS,key=lambda ci:sum((a-b)**2 for a,b in zip(ci[0],rgb)))[1]
    return _cache[rgb]
def dist(a,b): return sum((x-y)**2 for x,y in zip(PAL[a],PAL[b]))
def convert(path):
    w,h,px=read_png(path)
    if (w,h)!=(320,200):  # crop/scale crude: center crop or nearest scale
        px=[[px[int(y*h/200)][int(x*w/320)] for x in range(320)] for y in range(200)]
    idx=[[near(p) for p in row] for row in px]
    # detect multicolor: pixel pairs equal almost always
    pairs=sum(idx[y][x]==idx[y][x+1] for y in range(0,200,2) for x in range(0,320,2))
    mc = pairs/(100*160) > 0.97
    from collections import Counter
    bm=bytearray(8000); scr=bytearray(1000); col=bytearray(1000)
    if mc:
        bg=Counter(idx[y][x] for y in range(200) for x in range(0,320,2)).most_common(1)[0][0]
        for cy in range(25):
            for cx in range(40):
                cell=[[idx[cy*8+r][cx*8+2*c] for c in range(4)] for r in range(8)]
                cnt=Counter(v for row in cell for v in row if v!=bg)
                cols=[c for c,_ in cnt.most_common(3)]+[0]*3; c1,c2,c3=cols[:3]
                choices=[bg,c1,c2,c3]
                scr[cy*40+cx]=(c1<<4)|c2; col[cy*40+cx]=c3
                for r in range(8):
                    b=0
                    for c in range(4):
                        v=cell[r][c]; sel=min(range(4),key=lambda i:dist(v,choices[i]))
                        b=(b<<2)|sel
                    bm[(cy*40+cx)*8+r]=b
        mode=1
    else:
        bg=0
        for cy in range(25):
            for cx in range(40):
                cell=[[idx[cy*8+r][cx*8+c] for c in range(8)] for r in range(8)]
                cnt=Counter(v for row in cell for v in row).most_common(2)
                f=cnt[0][0]; g=cnt[1][0] if len(cnt)>1 else cnt[0][0]
                # fg = less common (bit=1), bg = most common (bit=0)
                scr[cy*40+cx]=(g<<4)|f
                for r in range(8):
                    b=0
                    for c in range(8):
                        v=cell[r][c]; b=(b<<1)|(1 if dist(v,g)<dist(v,f) else 0)
                    bm[(cy*40+cx)*8+r]=b
        mode=0
    slot=bytearray(SLOT); slot[0]=mode; slot[1]=bg
    slot[16:8016]=bm; slot[8016:9016]=scr; slot[9016:10016]=col
    return bytes(slot)
def preview(slot,out_ppm):
    mode,bg=slot[0],slot[1]; bm=slot[16:8016]; scr=slot[8016:9016]; col=slot[9016:10016]
    img=[[0]*320 for _ in range(200)]
    for cy in range(25):
        for cx in range(40):
            s=scr[cy*40+cx]; 
            for r in range(8):
                b=bm[(cy*40+cx)*8+r]
                for c in range(8 if mode==0 else 4):
                    if mode==0: v=(s>>4) if (b>>(7-c))&1 else (s&15); img[cy*8+r][cx*8+c]=v
                    else:
                        sel=(b>>(6-2*c))&3; v=[bg,s>>4,s&15,col[cy*40+cx]&15][sel]
                        img[cy*8+r][cx*8+2*c]=img[cy*8+r][cx*8+2*c+1]=v
    with open(out_ppm,'wb') as f:
        f.write(b'P6 320 200 255\n'+bytes(c for row in img for v in row for c in CCS64[v]))
if __name__=='__main__':
    s=convert(sys.argv[1]); preview(s,sys.argv[2]); print('mode',s[0])
