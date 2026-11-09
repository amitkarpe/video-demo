"""SVG vocabulary: native service assets, front-facing code, editable diagrams."""
from html import escape
C={'ink':'#06131f','panel':'#102c40','line':'#47697e','white':'#f2f7fc','muted':'#b6cbd9','blue':'#7cc6ff','teal':'#62e0cf','amber':'#ffc66c','red':'#ff9b9b','purple':'#c7a5ff','green':'#b5e59b'}
def g(id,s,**attrs):return '<g id="'+id+'" '+ ' '.join(f'{k}="{v}"' for k,v in attrs.items())+'>'+s+'</g>'
def t(x,y,s,size=34,c='white',weight=500,anchor='start',id=''):
 color=C.get(c,c);a=f' id="{id}"' if id else ''
 return f'<text{a} x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}">'+''.join(f'<tspan x="{x}" dy="{0 if i==0 else size*1.3}">{escape(l)}</tspan>' for i,l in enumerate(s.split('\n')))+'</text>'
def rect(x,y,w,h,c='line',fill='panel',rx=18,stroke=2):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{C.get(fill,fill)}" stroke="{C.get(c,c)}" stroke-width="{stroke}"/>'
def path(d,c='blue',w=4,dash=False,id='',arrow=False):
 color=C.get(c,c);marker='arrowhead-'+(c if c in C else 'blue')
 return f'<path id="{id}" d="{d}" fill="none" stroke="{color}" stroke-width="{w}"'+(' stroke-dasharray="13 12"' if dash else '')+(f' marker-end="url(#{marker})"' if arrow else '')+'/>'

def tag(x,y,w,label,c='teal',id=''):
 return g(id,rect(x,y,w,52,c,'ink',10)+t(x+w/2,y+36,label,29,c,700,'middle'))
def icon(name,x,y,w=128,h=None,plate=False):
 h=h or w;s=rect(x-12,y-12,w+24,h+24,'#e4edf2','#ffffff',16) if plate else ''
 return s+f'<image href="assets/icons/{name}.svg" x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet"/>'
def document(id,x,y,w,h,title,lines,c='blue'):
 s=f'<path d="M{x},{y} H{x+w-52} L{x+w},{y+52} V{y+h} H{x}Z" fill="{C["panel"]}" stroke="{C[c]}" stroke-width="3"/>'
 s+=path(f'M{x+w-52},{y} V{y+52} H{x+w}',c,3)+t(x+24,y+50,title,32,c,700)
 for i,l in enumerate(lines):s+=t(x+24,y+104+i*48,l,32)
 return g(id,s)
def database(id,x,y,w=300,h=205):
 s=f'<path d="M{x},{y+35} V{y+h-35} C{x},{y+h+14} {x+w},{y+h+14} {x+w},{y+h-35} V{y+35}" fill="{C["panel"]}" stroke="{C["blue"]}" stroke-width="3"/><ellipse cx="{x+w/2}" cy="{y+35}" rx="{w/2}" ry="35" fill="#174360" stroke="{C["blue"]}" stroke-width="3"/>'
 s+=path(f'M{x},{y+h*.55} C{x},{y+h*.55+48} {x+w},{y+h*.55+48} {x+w},{y+h*.55}','blue',2)
 s+=icon('sqlite',x+30,y+65,w-60,65,True)
 return g(id,s)
def lock(id,x,y,c='purple',size=1):
 s=path(f'M{x+20},{y+45} V{y+23} C{x+20},{y-16} {x+90},{y-16} {x+90},{y+23} V{y+45}',c,7)
 s+=rect(x,y+45,110,82,c,'ink',16,4)+f'<circle cx="{x+55}" cy="{y+80}" r="10" fill="{C[c]}"/>'+path(f'M{x+55},{y+82} V{y+107}',c,7)
 return g(id,s)
def person(id,x,y):
 return g(id,f'<circle cx="{x+45}" cy="{y+34}" r="30" fill="#26334f" stroke="{C["purple"]}" stroke-width="4"/>'+path(f'M{x},{y+136} V{y+105} C{x},{y+61} {x+90},{y+61} {x+90},{y+105} V{y+136}','purple',5))
def clock(id,x,y,r=62,c='amber'):
 s=f'<circle cx="{x}" cy="{y}" r="{r}" fill="{C["ink"]}" stroke="{C[c]}" stroke-width="4"/>'+path(f'M{x},{y-r*.65} V{y} L{x+r*.48},{y+r*.22}',c,5)
 return g(id,s)
def code(id,x,y,w,title,lines,h=145):
 return g(id,rect(x,y,w,h,'line','ink',12)+t(x+20,y+34,title,28,'muted',700)+t(x+20,y+80,lines,30,'teal'))
def defs():
 return '<defs>'+''.join(f'<marker id="arrowhead-{name}" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="8" markerHeight="8" orient="auto"><path d="M0,0 L12,6 L0,12Z" fill="{color}"/></marker>' for name,color in C.items())+'</defs>'

def master():
 s=''
 # Two distinct source rails. No connector promotes imported data into canary authority.
 s+=rect(760,40,3500,1480,'blue','ink',65,5)+t(1150,175,'AWSOps · Python trusted backend',110,'blue',700)
 s+=rect(4370,820,1180,1420,'teal','ink',65,5)+t(4460,950,'Personal LAB',100,'teal',700)
 s+=rect(20,1650,2100,735,'line','ink',50,4)+t(95,1775,'Historical read only',100,'muted',700)
 s+=t(80,115,'COMPANION',100,'amber',700)+t(80,245,'UI',100,'amber')
 def n(id,x,y,label,asset=None,sub='',c='blue'):
  a=f'<circle cx="{x}" cy="{y}" r="145" fill="#133247" stroke="{C[c]}" stroke-width="5"/>'
  if asset:a+=icon(asset,x-94,y-94,188,188,asset in ('python','sqlite','github-actions','sts'))
  else:a+=t(x,y+30,{'ui':'UI','intake':'{ }','plan':'PLAN','batch':'BATCH','approval':'HUMAN','sdk':'SDK','receipt':'RUN','clock':'TIME','observe':'READ'}.get(id,id),100,c,700,'middle')
  a+=t(x,y+245,label,100,c,700,'middle')
  # Secondary qualifications are carried by the stable front-facing map note and focused lenses.
  return g('map-'+id,a)
 s+=n('ui',310,480,'AgentCore2',c='amber')+n('intake',1110,480,'Intake',sub='IMPORTED ASSERTION',c='amber')+n('plan',1850,480,'Offline plan',sub='APPROVE BLOCKED',c='amber')
 s+=path('M470,480 H940','amber',8,True,arrow=True)+path('M1270,480 H1670','amber',8,arrow=True)
 s+=n('observe',1080,1120,'Observation',sub='separate acquisition')+n('batch',1840,1120,'Batch',sub='exact frozen scope')+n('approval',2600,1120,'Approval',sub='live binding PENDING',c='purple')
 s+=n('ledger',3370,1120,'SQLite','sqlite',sub='decision + operations')+n('sdk',4060,1120,'Provider',sub='fixed methods')+n('s3',4920,1250,'Amazon S3','s3',sub='MOCK / live not accepted',c='teal')
 for x,y,xx,yy,col,dash in [(1240,1120,1660,1120,'blue',False),(2000,1120,2420,1120,'purple',False),(2760,1120,3200,1120,'purple',True),(3530,1120,3900,1120,'blue',False),(4220,1160,4750,1250,'amber',True)]:s+=path(f'M{x},{y} L{xx},{yy}',col,8,dash,arrow=True)
 s+=path('M2900,820 V1510','purple',12,True)+t(2930,1495,'LIVE GATE',100,'purple',750)
 s+=n('actions',310,1980,'Actions','github-actions',c='muted')+n('historyconfig',1190,1980,'AWS Config','config',sub='11 Oct 2026',c='muted')+path('M475,1980 H1000','muted',8,arrow=True)
 s+=n('receipt',2710,1930,'Execution',sub='receipt',c='blue')+n('readback',3490,1930,'Readback','s3',sub='independent observation',c='teal')+n('config',4270,1930,'Config','config',sub='fresh evaluation unproved',c='amber')+n('clock',5070,1930,'Freshness',sub='not verified',c='amber')
 s+=path('M3380,1490 V1660 H2730 V1755','blue',7,arrow=True)+path('M4920,1560 V1640 H3510 V1750','teal',7,True,arrow=True)
 s+=t(1190,2306,'11 Oct 2026',100,'muted',650,'middle')
 s+=icon('python',3790,80,360,120,True)
 return s
