"""Prüft, ob die Beschreibung in SKILL.md den Skill bei den richtigen Anfragen auslöst.

Aufruf: python3 scripts/trigger_test.py [evals/trigger-queries.json]
Braucht die Claude-Code-CLI (`claude`, sonst Pfad in CLAUDE_BIN) und den
installierten Skill unter ~/.claude/skills/multi-expert-panel. Jede Anfrage
startet eine kurze `claude -p`-Sitzung.
"""
import json,os,subprocess,sys,select,time,tempfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
CL=os.environ.get("CLAUDE_BIN","claude")
ev=json.load(open(sys.argv[1] if len(sys.argv)>1 else Path(__file__).resolve().parent.parent/"evals"/"trigger-queries.json"))
work=tempfile.mkdtemp()
env={k:v for k,v in os.environ.items() if k!="CLAUDECODE"}
def one(item):
    p=subprocess.Popen([CL,"-p",item["q"],"--output-format","stream-json","--verbose","--include-partial-messages"],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,cwd=work,env=env)
    buf="";hit=False;t0=time.time();pend=False;acc=""
    try:
        while time.time()-t0<60:
            r,_,_=select.select([p.stdout],[],[],1)
            if not r:
                if p.poll() is not None: break
                continue
            c=os.read(p.stdout.fileno(),8192)
            if not c: break
            buf+=c.decode(errors="replace")
            while "\n" in buf:
                l,buf=buf.split("\n",1)
                try:e=json.loads(l)
                except: continue
                if e.get("type")=="stream_event":
                    se=e["event"];ty=se.get("type")
                    if ty=="content_block_start":
                        cb=se.get("content_block",{})
                        if cb.get("type")=="tool_use":
                            pend=cb.get("name") in("Skill","Read");acc=""
                            if not pend: return item,False
                    elif ty=="content_block_delta" and pend:
                        acc+=se.get("delta",{}).get("partial_json","")
                        if "multi-expert-panel" in acc: return item,True
                    elif ty=="content_block_stop" and pend:
                        return item,"multi-expert-panel" in acc
                    elif ty=="message_stop": return item,False
                elif e.get("type")=="result": return item,False
    finally:
        if p.poll() is None: p.kill(); p.wait()
    return item,hit
with ThreadPoolExecutor(6) as ex: res=list(ex.map(one,ev))
ok=0
for it,h in res:
    good=(h==it["t"]); ok+=good
    print(("OK  " if good else "FAIL"),"soll" if it["t"] else "nicht","| ausgelöst" if h else "| -", "|",it["q"][:70])
print(f"{ok}/{len(res)} richtig")
