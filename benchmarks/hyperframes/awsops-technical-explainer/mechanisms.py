"""Narration-linked mechanism lenses, attached to the same AWSOps spatial map."""
from visuals import *
def lost_response():
 s=t(25,48,'THE REQUEST CROSSED. THE ANSWER DID NOT.',40,'white',750)
 s+=tag(1135,8,510,'APPROVED MOCK ALTERNATIVE','purple')
 s+=database('u-db',50,115,310,225)+t(205,400,'Run A · policy',36,'blue',700,'middle')
 s+=g('u-sdk',rect(575,130,290,185,'blue','ink',20)+t(720,185,'SDK boundary',37,'blue',700,'middle')+t(720,240,'put_bucket_policy',30,'white',500,'middle'))
 s+=icon('s3',1325,115,190)+t(1420,355,'Amazon S3',42,'teal',700,'middle')+tag(1220,378,400,'SYNTHETIC PROVIDER','teal')
 s+=path('M375,213 H555','blue',6,arrow=True)+path('M885,213 H1295','teal',6,arrow=True)
 s+=g('u-request',document('u-request-doc',382,180,88,100,'',[],'teal')+t(426,248,'A',36,'teal',750,'middle'))
 s+=g('u-reply',path('M1310,330 H900','amber',7,False,arrow=True)+t(1060,376,'ACK?',34,'amber',700,'middle'))
 s+=g('u-fracture',path('M1020,300 L1075,355 M1075,300 L1020,355','red',10)+t(1045,420,'REPLY LOST',44,'red',800,'middle'))
 s+=g('u-state',rect(28,442,475,170,'amber','ink',18)+t(52,487,'Durable operation: CALLING',31,'amber',750)+t(52,544,'execution = UNKNOWN',36,'amber',750)+t(52,590,'Attempt ≠ confirmed change',28,'muted'))
 s+=g('u-retry',path('M520,480 H1260','red',7,True,arrow=True)+lock('u-retry-lock',845,420,'red')+tag(590,552,650,'AUTOMATIC WRITE RETRY BLOCKED','red'))
 s+=g('u-reconcile',path('M1400,445 C1360,520 700,535 380,365 L360,335','green',7,False,arrow=True)+tag(600,550,660,'READ-ONLY RECONCILIATION → SAME RUN A','green'))
 s+=code('u-recovery',548,445,665,'OTHER CASE · ALL FOUR ACK','all four setup rows = ACK\nrecover execution = SUCCEEDED',165)
 s+=code('u-counts',548,445,665,'MOCK ATTEMPTS · NOT PROVEN CLOUD CHANGES','simulatedWrites: 4\nrealWrites: 0',165)
 s+=code('u-code',548,445,665,'SOURCE · s3_canary.py / reconcile',"if \"CALLING\" in write_ops.values():\n    r[\"status\"] = \"NEEDS_REVIEW\"",165)
 return s

def evidence_wheel(prefix='e'):
 s=t(25,50,'FOUR SOURCES. FOUR CLAIMS. NO AUTOMATIC GREEN.',39,'white',750)
 s+=document(prefix+'-execution',40,98,480,195,'EXECUTION RECEIPT',['execution','SUCCEEDED'],'blue')
 s+=g(prefix+'-readback',icon('s3',1230,100,130)+t(1390,145,'POLICY READBACK',31,'teal',750)+t(1390,206,'MATCH',44,'green',750))
 s+=g(prefix+'-config',icon('config',60,380,140)+t(235,430,'CONFIG EVALUATION',30,'amber',750)+t(235,488,'UNKNOWN',44,'amber',750))
 s+=g(prefix+'-fresh',clock(prefix+'-clock',1290,450,65)+t(1400,420,'FRESHNESS',31,'amber',750)+t(1400,479,'NOT_VERIFIED',37,'amber',750))
 s+=path('M540,205 L690,285','blue',5,arrow=True)+path('M1200,205 L1010,285','teal',5,arrow=True)+path('M540,455 L690,380','amber',5,True,arrow=True)+path('M1200,455 L1010,380','amber',5,True,arrow=True)
 s+=g(prefix+'-review',f'<circle cx="850" cy="330" r="138" fill="#152c3b" stroke="{C["amber"]}" stroke-width="5"/>'+lock(prefix+'-lock',795,232,'amber')+t(850,432,'NEEDS_REVIEW',38,'amber',800,'middle'))
 s+=tag(560,557,610,'SUCCEEDED + MATCH ≠ VERIFIED','amber',prefix+'-equation')
 s+=g(prefix+'-gate',path('M685,490 H1020','red',8)+t(850,530,'VERIFIED gate stays closed',29,'red',750,'middle'))
 return s

def imported():
 s=t(25,48,'A FINDING CAN MOVE. AUTHORITY CANNOT.',40,'white',750)
 s+=document('i-raw',35,105,565,340,'SYNTHETIC IMPORT',['findingId: finding-canary','accountAlias: mock-a','resourceAlias:','resource-disposable-s3-canary','controlId: s3-ssl-requests-only'],'amber')
 s+=g('i-boundary',path('M840,95 V470','blue',8,True)+t(840,530,'BOUNDED INTAKE',32,'blue',750,'middle')+t(840,572,'262,144 bytes / 500 rows',28,'muted',500,'middle'))
 s+=document('i-envelope',1080,105,565,340,'CANONICAL ENVELOPE',['schemaVersion: defence-factory/1','kind: Finding','record: { … }','revision: 1','provenance: IMPORTED_ASSERTION'],'amber')
 for j,(v,y) in enumerate([('findingId',185),('resourceAlias',265),('controlId',345)]):
  s+=g(f'i-field{j}',tag(585,y,250,v,'amber')+path(f'M840,{y+26} H1060','amber',4,arrow=True))
 s+=tag(620,408,405,'extraField → REJECT','red','i-extra')
 s+=g('i-assertion',tag(1080,475,565,'REMAINS IMPORTED_ASSERTION','amber'))
 s+=g('i-separation',path('M35,620 H1640','purple',3,True)+t(40,605,'Offline planner: APPROVE_BLOCKED',31,'amber',750)+t(920,605,'Private acquisition / binding: separate',31,'blue',750))
 s+=g('i-private',rect(470,95,680,445,'blue','ink',22)+lock('i-lock',755,125,'blue')+t(810,330,'PUBLIC ALIAS ≠ PRIVATE CREDENTIAL',32,'blue',750,'middle')+icon('sts',530,385,105,100,True)+t(675,410,'Expected non-root identity',31)+t(675,459,'Registration ≠ IAM trust',31))
 return s

def frozen(digest):
 s=t(25,48,'THE COMPLETE PAYLOAD IS THE APPROVAL SUBJECT.',38,'white',750)
 s+=g('b-paper',document('b-doc',35,90,1170,480,'Batch A · canonical record',[],'blue'))
 fields=[('batchId','batch-canary-aaaa…'),('datasetId / registryVersion','dataset-canary / 1'),('mode / frozenAt / expiresAt','MOCK / 00:00Z / 00:05Z'),('targets[0].resource','resource-disposable-s3-canary'),('targets[0].revision','1'),('evidenceDigest','synthetic observation digest'),('capabilityId','s3-require-tls'),('expectedChange','DENY_INSECURE_TRANSPORT')]
 for i,(k,v) in enumerate(fields):
  x=65+(i//4)*565;y=185+(i%4)*92
  s+=g(f'b-field{i}',t(x,y,k,28,'muted')+t(x,y+40,v,31,'white',700,id='b-revision' if i==4 else ''))
 s+=g('b-seal',f'<circle cx="1430" cy="268" r="157" fill="#143c3d" stroke="{C["teal"]}" stroke-width="5"/>'+t(1430,225,'SHA-256',40,'teal',800,'middle')+t(1430,290,digest[:12]+'…',32,'white',700,'middle')+t(1430,343,'scopeDigest',31,'teal',700,'middle'))
 s+=g('b-break',path('M1390,102 L1450,205 L1390,290 L1460,430','red',8)+tag(1245,464,395,'DIGEST MISMATCH','red'))
 s+=g('b-auth',lock('b-auth-lock',1365,120,'purple')+t(1420,330,'Hash ≠ identity',35,'purple',750,'middle')+t(1420,390,'Separate trusted principal',29,'muted',500,'middle'))
 s+=g('b-expiry',clock('b-clock',1430,280,75)+t(1430,417,'Expiry / drift',38,'amber',750,'middle')+t(1430,470,'BLOCKED',40,'amber',750,'middle'))
 s+=t(50,620,'Canonical keys · retain array order · omit scopeDigest · legacy FrozenScope is a separate type',29,'muted')
 return s

def decision():
 s=t(25,48,'ONE TERMINAL CHOICE. COMMIT BEFORE DISPATCH.',39,'white',750)
 s+=g('d-principal',person('d-person',65,105)+t(210,150,'Trusted principal',34,'purple',750)+t(210,200,'Illustrative binding',29,'muted'))
 s+=database('d-db',720,95,345,205)+code('d-code',635,380,520,'SOURCE · decide()', 'BEGIN IMMEDIATE',110)+tag(665,310,455,'DECISION + RUN COMMITTED','blue','d-atomic')
 s+=g('d-approve',tag(50,280,460,'APPROVE_ONCE','purple'))+g('d-reject',tag(50,407,460,'REJECT','purple'))
 s+=path('M530,306 L700,235','purple',5,arrow=True)+path('M530,432 L700,260','purple',5,arrow=True)
 s+=g('d-winning',tag(700,512,440,'REJECTED · SDK WRITES: 0','amber'))
 s+=g('d-consumed',tag(35,503,540,'COMPETING CHOICE: CONSUMED','red'))
 s+=g('d-branch',path('M1190,90 V555','purple',3,True)+t(1415,105,'SEPARATE MOCK SCENARIO',28,'teal',750,'middle')+document('d-mock-scenario',1230,145,390,180,'TEST_SIMULATION',['APPROVE_ONCE','MOCK provider only'],'teal')+t(1425,402,'No arrow from Reject.\nNo decision replay.',29,'muted',600,'middle')+tag(1220,495,410,'ALTERNATIVE OUTCOME','teal'))
 s+=t(890,85,'COUNTERFACTUAL REJECT',28,'amber',750,'middle')

 s+=tag(35,590,1610,'LIVE: TRUSTED_HUMAN_APPROVAL_BINDING_REQUIRED · FAIL CLOSED','amber','d-live')
 return s

def execution():
 s=t(25,48,'FIXED METHODS. EXACT PRIVATE BINDING. MOCK HERE.',38,'white',750)
 s+=g('x-identity',icon('sts',70,145,145,145,True)+t(250,185,'Fresh non-root STS identity',37,'blue',750)+t(250,244,'Exact expected account / Region',33)+lock('x-owned',880,130,'purple')+t(1040,180,'New task-owned bucket only',34,'purple',750)+t(1040,239,'Preexisting resource → refuse',32,'muted'))
 s+=g('x-s3',icon('s3',1390,120,190)+t(1485,365,'Amazon S3',38,'teal',750,'middle'))
 calls=''
 for i,(step,method) in enumerate([('CREATE','create_bucket'),('TAG','put_bucket_tagging'),('PUBLIC BLOCK','put_public_access_block'),('TLS POLICY','put_bucket_policy')]):
  y=95+i*112
  calls+=g(f'x-call{i}',rect(370,y,940,90,'blue','ink',14)+t(392,y+38,step,28,'blue',750)+t(392,y+73,method,30)+tag(1045,y+20,235,'INTENT','amber',f'x-state{i}'))
 calls+=database('x-ledger',30,175,285,210)+t(170,470,'Run A · ledger',30,'blue',750,'middle')
 s+=g('x-calls',calls)
 s+=g('x-policy',path('M180,200 L420,240','red',5,arrow=True)+path('M180,410 L420,370','teal',5,arrow=True)+t(170,165,'Insecure request',32,'red',750)+t(170,375,'Secure request',32,'teal',750)+f'<path d="M650,170 L990,305 L650,445 L310,305Z" fill="#113647" stroke="{C["amber"]}" stroke-width="3"/>'+t(650,283,'aws:SecureTransport',34,'white',750,'middle')+t(650,333,'false ?',34,'amber',750,'middle')+path('M1000,305 H1275','red',6,arrow=True)+lock('x-deny-lock',1280,240,'red')+t(1415,420,'DENY',52,'red',800,'middle')+path('M650,447 V482 H1260','teal',5,arrow=True)+tag(1270,455,365,'OTHER PERMISSIONS','teal')+t(925,528,'NO: other permissions still apply',31,'teal',650,'middle')+t(1120,270,'YES',34,'red',750)+tag(45,558,1590,'ILLUSTRATIVE CONDITION · NOT ENCRYPTION AT REST · PUBLIC BLOCK IS SEPARATE','amber'))
 s+=g('x-preconditions',t(50,110,'Before the policy call, fresh reads must agree:',36,'blue',750))
 for i,(name,detail) in enumerate([('CREATION','ACK in this ledger'),('OWNERSHIP','Exact task tags'),('EMPTY','No objects / versions / delete markers'),('PUBLIC BLOCK','All four flags true'),('POLICY','Absent; do not overwrite')]):
  y=170+i*82
  s+=g(f'x-check{i}',f'<circle cx="85" cy="{y+6}" r="19" fill="#153a46" stroke="{C["teal"]}" stroke-width="3"/>'+t(130,y+17,name,31,'teal',750)+t(470,y+17,detail,32))
 s+=g('x-journal',database('x-durable',50,150,330,245)+t(555,160,'Journal the boundary, not an assumption',36,'blue',750)+tag(515,235,300,'INTENT','blue')+path('M830,260 H940','blue',6,arrow=True)+tag(970,235,300,'CALLING','amber')+path('M1290,260 H1390','teal',6,arrow=True)+tag(1410,235,235,'ACK','green')+code('x-sdkcode',510,370,1130,'OPERATION STATES · _attempt',"state='CALLING'  →  SDK call  →  state='ACK'",145))
 return s

def cleanup():
 s=t(35,85,'CLEANUP IS A SEPARATE CONDITIONAL AUTHORITY.',38,'white',750)
 for i,(title,body) in enumerate([('EXACT SCOPE','Owner / resource binding'),('EMPTY STATE','Objects / versions / markers'),('VALID WINDOW','Approved cleanup + expiry')]):
  x=35+i*555
  s+=g(f'c-gate{i}',lock(f'c-lock{i}',x+150,145,'purple')+t(x+210,350,title,34,'purple',750,'middle')+t(x+210,405,body,28,'muted',500,'middle'))
 s+=g('c-stop',rect(35,455,1610,95,'red','ink')+t(840,518,'CALLING / UNKNOWN → DELETE LOCKED',40,'red',800,'middle'))
 s+=g('c-ttl',t(840,616,'TTL tag ≠ scheduled deletion',37,'amber',750,'middle'))
 return s

def provenance():
 s=t(25,48,'THESE EVIDENCE CLASSES DO NOT COLLAPSE.',40,'white',750)
 s+=g('p-source',document('p-source-paper',40,95,680,215,'SOURCE IMPLEMENTED',['15c12fb5362d…','Frozen scope / durable states'],'blue')+icon('python',460,120,210,75,True))
 s+=g('p-fake',rect(915,95,700,215,'teal','ink')+t(950,150,'FAKE SDK TEST',35,'teal',750)+t(950,215,'TEST_SIMULATION',34,'white',750)+t(950,270,'realWrites: 0 · not owner approval',31,'muted'))
 s+=g('p-history',rect(40,365,680,240,'muted','ink')+icon('github-actions',70,400,75,75,True)+path('M170,440 H270','muted',5,arrow=True)+icon('config',300,390,105)+t(450,425,'11 OCT 2026',34,'white',800)+t(450,478,'Historical read',30,'muted')+t(75,565,'Bounded read only / freshness not verified',28,'muted'))
 s+=g('p-pending',lock('p-human-lock',955,375,'amber')+t(1110,415,'PENDING LIVE',37,'amber',800)+t(1110,468,'Genuine human decision',31)+t(1110,515,'Ledger provenance / deployed pins',29)+t(1110,565,'Provider + compliance proof',31))
 return s
