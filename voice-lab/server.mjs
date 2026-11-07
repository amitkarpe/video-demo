import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
const HOST = "127.0.0.1", PORT = 8787;
const KEY = process.env.OPENAI_API_KEY;
if (!KEY) { console.error("OPENAI_API_KEY missing. Configure a local secret first."); process.exit(1); }
let issued = false;
function send(res, status, body, type="application/json") {
 res.writeHead(status, {"Content-Type": type, "Cache-Control":"no-store","X-Content-Type-Options":"nosniff"});
 res.end(typeof body==="string"?body:JSON.stringify(body));
}
createServer(async (req,res)=>{
 const origin=req.headers.origin;
 if (req.headers.host!==HOST+":"+PORT || (origin && origin!=="http://"+HOST+":"+PORT)) return send(res,403,{error:"Localhost only"});
 const path=new URL(req.url||"/","http://localhost").pathname;
 if(req.method==="GET" && path==="/") return send(res,200,await readFile(new URL("./index.html",import.meta.url),"utf8"),"text/html; charset=utf-8");
 if(req.method==="POST" && path==="/token") {
  if(issued) return send(res,429,{error:"One session per server start. Restart for a new test."});
  issued=true;
  try {
   const api=await fetch("https://api.openai.com/v1/realtime/client_secrets",{method:"POST",headers:{"Authorization":"Bearer "+KEY,"Content-Type":"application/json"},body:JSON.stringify({session:{type:"realtime",model:"gpt-realtime-2.1-mini",audio:{output:{voice:"cedar"}}}})});
   const data=await api.json();
   if(!api.ok) return send(res,502,{error:data?.error?.message||"Realtime session unavailable"});
   return send(res,200,{value:data.value,model:"gpt-realtime-2.1-mini"});
  } catch { return send(res,502,{error:"Cannot reach API"}); }
 }
 return send(res,404,{error:"Not found"});
}).listen(PORT,HOST,()=>console.log("Voice lab: http://"+HOST+":"+PORT));
