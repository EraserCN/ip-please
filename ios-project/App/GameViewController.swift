import UIKit
import WebKit

class GameViewController: UIViewController {
    private var webView: WKWebView!

    override var prefersStatusBarHidden: Bool {
        return true
    }

    override var prefersHomeIndicatorAutoHidden: Bool {
        return true
    }

    override var supportedInterfaceOrientations: UIInterfaceOrientationMask {
        return .landscape
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = UIColor(red: 22/255.0, green: 19/255.0, blue: 19/255.0, alpha: 1.0)

        let config = WKWebViewConfiguration()
        config.allowsInlineMediaPlayback = true
        config.mediaTypesRequiringUserActionForPlayback = []
        config.preferences.setValue(true, forKey: "allowFileAccessFromFileURLs")
        config.setValue(true, forKey: "allowUniversalAccessFromFileURLs")

        webView = WKWebView(frame: view.bounds, configuration: config)
        webView.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        webView.isOpaque = false
        webView.backgroundColor = .clear
        webView.scrollView.backgroundColor = .clear
        webView.scrollView.isScrollEnabled = false
        webView.scrollView.bounces = false
        webView.scrollView.contentInsetAdjustmentBehavior = .never

        view.addSubview(webView)

        let bundleURL = Bundle.main.resourceURL ?? Bundle.main.bundleURL
        let htmlURL = bundleURL.appendingPathComponent("web/index.html")

        if FileManager.default.fileExists(atPath: htmlURL.path) {
            webView.loadFileURL(htmlURL, allowingReadAccessTo: bundleURL.appendingPathComponent("web"))
        } else {
            let altURL = bundleURL.appendingPathComponent("index.html")
            webView.loadFileURL(altURL, allowingReadAccessTo: bundleURL)
        }
    }
}
