import re
BLUE="#569cd6"; ORANGE="#ce9178"; GREEN="#4ec96a"; PURPLE="#c586c0"

def row(values, markers=None, hi=frozenset(), cls_map=None):
    markers=markers or {}; cls_map=cls_map or {}
    out=['<div class="vz-str">']
    for ix,v in enumerate(values):
        cls="vz-ch"+(" take" if ix in hi else "")+((" "+cls_map[ix]) if ix in cls_map else "")
        ptr="".join('<span style="color:%s">%s</span>'%(c,l) for l,c in markers.get(ix,[]))
        out.append('<span class="vz-col"><span class="vz-ptrs">%s</span><span class="%s">%s</span><span class="vz-ix">%d</span></span>'%(ptr,cls,v,ix))
    out.append("</div>")
    return "".join(out)

def chips(label, items, win=frozenset()):
    inner="".join('<span class="vz-chip%s">%s</span>'%(" win" if i in win else "", it) for i,it in enumerate(items))
    return '<div class="vz-row"><span class="vz-lab">%s</span>%s</div>'%(label,inner)

def vz(label,*bodies):
    return '<div class="vz"><div class="vz-lab">%s</div>%s</div>'%(label,"".join(bodies))

def edit_chunk(chunk, steps):
    wstart=chunk.index("  walkthrough: |")
    send=chunk.index("\n  source:", wstart)+1
    wblock=chunk[wstart:send]
    cut=wblock.index("\n    ===\n")
    idea=wblock[:cut]
    body="".join("    ===\n    %s | %s\n    %s\n"%(r,c,v) for r,c,v in steps)
    return chunk[:wstart]+idea+"\n"+body+chunk[send:]

def apply(path, edits):
    text=open(path,encoding="utf-8").read()
    chunks=re.split(r"(?m)^(?=- instruction:)", text)
    done=set()
    for i,ch in enumerate(chunks):
        if not ch.startswith("- instruction:"): continue
        fl=""
        for ln in ch.split("\n")[1:]:
            if ln.strip(): fl=ln.strip(); break
        best=None
        for prefix,steps in edits:
            if fl.startswith(prefix) and (best is None or len(prefix)>len(best[0])):
                best=(prefix,steps)
        if best:
            chunks[i]=edit_chunk(ch,best[1]); done.add(best[0])
    open(path,"w",encoding="utf-8").write("".join(chunks))
    missing=[p for p,_ in edits if p not in done]
    print("%s: edited %d, missing %s"%(path.split('/')[-1], len(done), missing))
    return missing
