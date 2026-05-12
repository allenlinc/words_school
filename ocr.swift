#!/usr/bin/swift
import Vision
import AppKit
import Foundation

guard CommandLine.arguments.count >= 2 else {
    print("Usage: \(CommandLine.arguments[0]) <image_path>")
    exit(1)
}

let imagePath = CommandLine.arguments[1]
guard let image = NSImage(contentsOfFile: imagePath),
      let cgImage = image.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
    print("ERROR: Cannot load image from \(imagePath)")
    exit(1)
}

let semaphore = DispatchSemaphore(value: 0)
var allText = ""

let request = VNRecognizeTextRequest { (request, error) in
    defer { semaphore.signal() }
    guard let observations = request.results as? [VNRecognizedTextObservation] else { return }
    for observation in observations {
        if let top = observation.topCandidates(1).first {
            allText += top.string + "\n"
        }
    }
}
request.recognitionLevel = .accurate
request.recognitionLanguages = ["en-US", "zh-Hans"]
request.usesLanguageCorrection = true

let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
try? handler.perform([request])
semaphore.wait()

print(allText)