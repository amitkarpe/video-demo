import AppKit
import Foundation
let W: CGFloat = 1920, H: CGFloat = 1080
func c(_ rgb: UInt32, _ a: CGFloat = 1) -> NSColor { NSColor(srgbRed: CGFloat((rgb >> 16) & 255)/255, green: CGFloat((rgb >> 8) & 255)/255, blue: CGFloat(rgb & 255)/255, alpha: a) }
func box(_ x: CGFloat,_ y: CGFloat,_ w: CGFloat,_ h: CGFloat,_ color: UInt32,_ a: CGFloat = 1,_ radius: CGFloat = 0) { c(color,a).setFill(); NSBezierPath(roundedRect: NSRect(x:x,y:H-y-h,width:w,height:h),xRadius:radius,yRadius:radius).fill() }
func text(_ s: String,_ x: CGFloat,_ y: CGFloat,_ w: CGFloat,_ h: CGFloat,_ size: CGFloat,_ color: UInt32,_ weight: NSFont.Weight = .regular,_ align: NSTextAlignment = .left) { let p=NSMutableParagraphStyle(); p.alignment=align; p.lineBreakMode = .byWordWrapping; (s as NSString).draw(in:NSRect(x:x,y:H-y-h,width:w,height:h),withAttributes:[.font:NSFont.systemFont(ofSize:size,weight:weight),.foregroundColor:c(color),.paragraphStyle:p]) }
let out = URL(fileURLWithPath:CommandLine.arguments[1],isDirectory:true)
try FileManager.default.createDirectory(at:out,withIntermediateDirectories:true)
let heads=["AN ALERT.\nA DECISION.","INVESTIGATE\nTHE RISK.","A HUMAN\nAPPROVES.","VERIFY\nEVERY ACTION."]
let labels=["01 / DETECT", "02 / INVESTIGATE", "03 / APPROVE", "04 / VERIFY"]
let captions=["An alert becomes a decision.", "Investigate the risk.", "Approve the fix.", "Verify every action."]
for i in 0..<6 {
 let b=NSBitmapImageRep(bitmapDataPlanes:nil,pixelsWide:Int(W),pixelsHigh:Int(H),bitsPerSample:8,samplesPerPixel:4,hasAlpha:true,isPlanar:false,colorSpaceName:.deviceRGB,bytesPerRow:0,bitsPerPixel:0)!
 let ctx=NSGraphicsContext(bitmapImageRep:b)!
 NSGraphicsContext.saveGraphicsState(); NSGraphicsContext.current=ctx
 if i == 0 {
   box(62,48,253,44,0x092231,0.88,10); text("SIMULATION  /  AI VOICE",76,57,225,27,16,0xB3F4EC,.bold,.center)
   text("CLOUD SECURITY   /   EXPLAINED", 68, 1000, 540, 27, 16,0x9FC9D8,.bold)
 } else if i == 5 {
   for (x,y) in [(160,620),(220,690),(40,740)] {
     box(CGFloat(x)-18,CGFloat(y)-18,48,48,0x29EAD9,0.09,24)
     box(CGFloat(x)-5,CGFloat(y)-5,22,22,0x76FFF0,0.35,11)
     box(CGFloat(x),CGFloat(y),12,12,0xD8FFFF,0.9,6)
   }
 } else {
   let j=i-1
   box(67,132,824,330,0x071321,0.92,24)
   box(99,168,5,236,0x38E6D4,1,2)
   text(labels[j],133,179,700,32,20,0x56E5D5,.bold)
   text(heads[j],129,226,710,173,63,0xF4FBFF,.heavy)
   box(383,886,1154,106,0x06111E,0.91,20)
   text(captions[j],415,912,1090,54,34,0xFFFFFF,.semibold,.center)
   for k in 0..<4 { box(CGFloat(132+k*54),419,38,4,k <= j ? 0x44E1D2 : 0x365367,1,2) }
 }
 NSGraphicsContext.restoreGraphicsState()
 try b.representation(using:.png,properties:[:])!.write(to:out.appendingPathComponent("overlay-\(i).png"))
}
