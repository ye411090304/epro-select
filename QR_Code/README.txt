Batch image QR tool

What it does:
- Scans all PNG/JPG/JPEG/WEBP/GIF images in this folder.
- Creates one HTML page for each image under the pages folder.
- Creates index.html as a QR code directory.
- Starts a local web server for phone testing when you double-click start-batch-qr.command.

How to use on Mac:
1. Put new or updated images in this folder.
2. Double-click start-batch-qr.command.
3. The tool regenerates all pages and opens index.html in the browser.
4. Scan the QR code for each image with a phone.
5. The phone and computer must be on the same Wi-Fi.
6. Keep the terminal window open while testing.

How to update:
- Add, remove, or replace images in this folder.
- Double-click start-batch-qr.command again.
- The pages and QR directory will be regenerated.

How to publish:
1. Run start-batch-qr.command once to generate pages and index.html.
2. Upload this folder to a web server.
3. Open the server URL for index.html.
4. The QR codes will automatically point to the server URLs.

Important:
- Do not generate QR codes from file:/// local paths. Phones cannot open local files from another computer.
- QR code images are generated through api.qrserver.com.
