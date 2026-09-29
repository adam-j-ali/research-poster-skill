// qr.swift: make or read a QR code with macOS's built-in CoreImage (nothing to install).
//   qr encode "<text>" out.png [pixels]   crisp black-on-white PNG with a 4-module quiet zone
//   qr decode in.png                      prints the decoded text (exit 1 if none found)
import AppKit
import CoreImage
import Foundation

func fail(_ msg: String) -> Never {
    FileHandle.standardError.write((msg + "\n").data(using: .utf8)!)
    exit(1)
}

let args = CommandLine.arguments
guard args.count >= 3 else { fail("usage: qr encode <text> <out.png> [pixels] | qr decode <in.png>") }

if args[1] == "encode" {
    guard args.count >= 4 else { fail("encode needs <text> <out.png>") }
    let pixels = args.count >= 5 ? Int(args[4]) ?? 1200 : 1200
    let filter = CIFilter(name: "CIQRCodeGenerator")!
    filter.setValue(args[2].data(using: .utf8), forKey: "inputMessage")
    filter.setValue("M", forKey: "inputCorrectionLevel")
    guard let raw = filter.outputImage else { fail("QR generation failed") }
    let modules = Int(raw.extent.width)          // CoreImage already adds a 1-module margin
    let total = modules + 6                      // widen it to the standard 4-module quiet zone
    let scale = max(1, pixels / total)
    let size = total * scale
    let rep = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: size, pixelsHigh: size, bitsPerSample: 8,
                               samplesPerPixel: 3, hasAlpha: false, isPlanar: false,
                               colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0)!
    let ctx = CIContext()
    guard let cg = ctx.createCGImage(raw, from: raw.extent) else { fail("render failed") }
    let src = NSBitmapImageRep(cgImage: cg)
    for py in 0..<size {
        for px in 0..<size {
            let mx = px / scale - 3, my = py / scale - 3
            var dark = false
            if mx >= 0 && my >= 0 && mx < modules && my < modules {
                let c = src.colorAt(x: mx, y: my)!.usingColorSpace(.deviceRGB)!
                dark = c.redComponent < 0.5
            }
            let v: CGFloat = dark ? 0 : 1
            rep.setColor(NSColor(deviceRed: v, green: v, blue: v, alpha: 1), atX: px, y: py)
        }
    }
    try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: args[3]))
    print("wrote \(args[3]) \(size)x\(size) px, \(modules - 2) modules")
} else if args[1] == "decode" {
    guard let img = CIImage(contentsOf: URL(fileURLWithPath: args[2])) else { fail("cannot read \(args[2])") }
    let detector = CIDetector(ofType: CIDetectorTypeQRCode, context: nil,
                              options: [CIDetectorAccuracy: CIDetectorAccuracyHigh])!
    let found = detector.features(in: img).compactMap { ($0 as? CIQRCodeFeature)?.messageString }
    guard let first = found.first else { fail("no QR code found") }
    print(first)
} else {
    fail("unknown command \(args[1])")
}
