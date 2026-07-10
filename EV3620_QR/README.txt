EV3620 QR web package

Files:
1. ev3620-user-guide.html
   The web page opened after scanning the QR code. It only displays the user guide image.

2. EV3620 Laser Robotic Vacuum User Guide_00.png
   The user guide image.

3. qr-tool.html
   QR code generator tool.

4. start-qr-tool.command
   Mac local test launcher. Double-click it to start a local web server and open the QR generator.


Local test:
1. Double-click start-qr-tool.command.
2. The browser will open qr-tool.html and fill in the local network URL automatically.
3. Click the generate button and scan the QR code with a phone.
4. The phone and computer must be connected to the same Wi-Fi.
5. Keep the terminal window open during testing.


Publish online:
1. Upload ev3620-user-guide.html and the PNG image to the same folder on a server.
2. Get the public URL, for example:
   https://example.com/ev3620-user-guide.html
3. Open qr-tool.html, enter the public URL, and generate the QR code.


Important:
Do not generate a QR code from a file:/// local path. Phones cannot open local files from another computer.
