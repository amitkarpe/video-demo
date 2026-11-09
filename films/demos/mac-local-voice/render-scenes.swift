import AppKit
import Foundation

struct Story: Decodable { let scenes: [Scene] }
struct Scene: Decodable {
    let step, title, eyebrow, status, cardTitle, cardBody, detail, result: String
    let captions: [String]
}
let W: CGFloat = 1920, H: CGFloat = 1080
func color(_ hex: UInt32) -> NSColor {
    NSColor(srgbRed: CGFloat((hex >> 16) & 255)/255, green: CGFloat((hex >> 8) & 255)/255, blue: CGFloat(hex & 255)/255, alpha: 1)
}
func box(_ x: CGFloat, _ y: CGFloat, _ w: CGFloat, _ h: CGFloat, _ fill: UInt32, radius: CGFloat = 0) {
    color(fill).setFill()
    NSBezierPath(roundedRect: NSRect(x: x, y: H-y-h, width: w, height: h), xRadius: radius, yRadius: radius).fill()
}
func label(_ value: String, _ x: CGFloat, _ y: CGFloat, _ w: CGFloat, _ h: CGFloat, size: CGFloat, color hex: UInt32, weight: NSFont.Weight = .regular, align: NSTextAlignment = .left) {
    let style = NSMutableParagraphStyle(); style.alignment = align; style.lineBreakMode = .byWordWrapping
    let attrs: [NSAttributedString.Key: Any] = [.font: NSFont.systemFont(ofSize: size, weight: weight), .foregroundColor: color(hex), .paragraphStyle: style]
    (value as NSString).draw(in: NSRect(x: x, y: H-y-h, width: w, height: h), withAttributes: attrs)
}
let args = CommandLine.arguments
if args.count != 3 { fputs("usage: render-scenes storyboard.json output-directory\n", stderr); exit(2) }
let story = try JSONDecoder().decode(Story.self, from: Data(contentsOf: URL(fileURLWithPath: args[1])))
let out = URL(fileURLWithPath: args[2], isDirectory: true)
try FileManager.default.createDirectory(at: out, withIntermediateDirectories: true)
for (i, scene) in story.scenes.enumerated() {
    for (j, caption) in scene.captions.enumerated() {
        guard let bitmap = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: Int(W), pixelsHigh: Int(H), bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false, colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0), let ctx = NSGraphicsContext(bitmapImageRep: bitmap) else { fatalError("Cannot allocate image") }
        NSGraphicsContext.saveGraphicsState(); NSGraphicsContext.current = ctx
        box(0,0,W,H,0x0A101B); box(0,0,338,H,0x101B2B); box(338,0,3,H,0x24364B)
        box(55,58,42,42,0x36D9CC,radius: 12)
        label("V", 67,64,25,30,size:23,color:0x061820,weight:.bold)
        label("SECURITY WORKFLOW", 112,59,220,35,size:18,color:0xD8E9F3,weight:.bold)
        label("DEMO  /  01", 57,116,220,30,size:16,color:0x7691A7,weight:.medium)
        label("THE WORKFLOW", 57,217,240,26,size:15,color:0x7D95A9,weight:.bold)
        for (k, item) in story.scenes.enumerated() {
            let y = CGFloat(271 + k * 100)
            if k == i { box(35,y-10,270,72,0x1B3542,radius:14) }
            box(59,y,40,40,k == i ? 0x37D9CA : 0x26374A,radius:20)
            label("\(k+1)", 59,y+7,40,26,size:17,color:k == i ? 0x071920 : 0xA7BBC8,weight:.bold,align:.center)
            label(item.step, 116,y+7,175,30,size:17,color:k == i ? 0xE9FFFF : 0x8FA8BA,weight:.bold)
        }
        label("FICTIONAL SCENARIO", 58,948,230,30,size:15,color:0x748CA0,weight:.bold)
        box(1500,54,345,51,0x423827,radius:12)
        label("SIMULATION / MOCK", 1512,64,320,30,size:20,color:0xFFD57C,weight:.bold,align:.center)
        label(scene.eyebrow, 414,75,960,32,size:20,color:0x42D5C9,weight:.bold)
        label(scene.title, 414,143,1380,80,size:53,color:0xF4F8FC,weight:.bold)
        label("From alert to accountable action", 416,235,1100,40,size:24,color:0x95ACBD)
        box(414,322,1400,406,0x162538,radius:25)
        box(449,359,180,42,0x263C48,radius:10)
        label(scene.status, 461,366,160,25,size:15,color:0x63E3D6,weight:.bold,align:.center)
        label(scene.cardTitle, 451,441,1280,64,size:35,color:0xF5F9FC,weight:.bold)
        label(scene.cardBody, 451,512,1250,48,size:25,color:0xA9BCCD)
        box(450,588,1322,2,0x314459)
        label(scene.detail, 451,619,760,30,size:17,color:0x829BAD,weight:.medium)
        label("→  " + scene.result, 451,665,1260,32,size:20,color:0x77E8DC,weight:.semibold)
        box(414,768,1400,5,0x24384A,radius:2)
        box(414,768,1400 * CGFloat(i+1)/CGFloat(story.scenes.count),5,0x3BDBCC,radius:2)
        label("\(i+1) / \(story.scenes.count)", 1710,785,100,30,size:18,color:0x8BA5B8,weight:.medium,align:.right)
        box(379,844,1465,175,0x050A10,radius:18)
        label(caption, 439,872,1345,125,size:36,color:0xFFFFFF,weight:.semibold,align:.center)
        NSGraphicsContext.restoreGraphicsState()
        guard let data = bitmap.representation(using: .png, properties: [:]) else { fatalError("PNG encoding failed") }
        try data.write(to: out.appendingPathComponent(String(format: "scene-%02d-caption-%02d.png",i+1,j+1)))
    }
}
