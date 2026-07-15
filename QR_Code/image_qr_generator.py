#!/usr/bin/env python3
import argparse
import html
import http.server
import os
import re
import socket
import socketserver
import subprocess
import sys
import threading
import time
from pathlib import Path
from urllib.parse import quote


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
PAGES_DIR = "pages"


def make_slug(path, used):
    stem = path.stem.strip()
    match = re.search(r"(EV\d+[A-Za-z]*)", stem, re.IGNORECASE)
    if match:
        base = match.group(1).upper()
    else:
        base = re.sub(r"[^A-Za-z0-9]+", "-", stem).strip("-").lower()
        if not base:
            base = "image"

    slug = base
    counter = 2
    while slug in used:
        slug = f"{base}-{counter}"
        counter += 1
    used.add(slug)
    return slug


def page_title(image_path):
    return image_path.stem


def image_files(root):
    files = []
    for item in sorted(root.iterdir(), key=lambda p: p.name.lower()):
        if item.is_file() and item.suffix.lower() in IMAGE_EXTENSIONS:
            files.append(item)
    return files


def write_text(path, content):
    path.write_text(content, encoding="utf-8")


def build(root):
    pages = root / PAGES_DIR
    pages.mkdir(exist_ok=True)

    used = set()
    entries = []

    for image_path in image_files(root):
        slug = make_slug(image_path, used)
        title = page_title(image_path)
        image_src = "../" + quote(image_path.name)
        html_path = pages / f"{slug}.html"

        page = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    html, body {{
      margin: 0;
      min-height: 100%;
      background: #fff;
    }}

    img {{
      display: block;
      width: 100%;
      max-width: 720px;
      height: auto;
      margin: 0 auto;
    }}
  </style>
</head>
<body>
  <img src="{image_src}" alt="{html.escape(title)}">
</body>
</html>
"""
        write_text(html_path, page)
        entries.append(
            {
                "title": title,
                "image": image_path.name,
                "page": f"{PAGES_DIR}/{slug}.html",
            }
        )

    cards = "\n".join(
        f"""      <article class="card" data-page="{html.escape(entry['page'])}">
        <div>
          <h2>{html.escape(entry['title'])}</h2>
          <p>{html.escape(entry['image'])}</p>
        </div>
        <img class="qr" alt="{html.escape(entry['title'])} QR code">
        <div class="actions">
          <a class="button open-page" href="{html.escape(entry['page'])}" target="_blank" rel="noopener">打开页面</a>
          <a class="button download-qr" href="#" download="{html.escape(Path(entry['page']).stem)}-qr.png">下载二维码</a>
          <button type="button" class="copy-url">复制链接</button>
        </div>
      </article>"""
        for entry in entries
    )

    empty = ""
    if not entries:
        empty = '<p class="empty">当前文件夹里没有找到 PNG/JPG/WEBP/GIF 图片。</p>'

    index = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>图片二维码目录</title>
  <style>
    :root {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: #172033;
      background: #f5f7fb;
    }}

    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      padding: 24px;
    }}

    main {{
      width: min(1120px, 100%);
      margin: 0 auto;
    }}

    header {{
      margin-bottom: 18px;
    }}

    h1 {{
      margin: 0 0 8px;
      font-size: 26px;
      line-height: 1.2;
    }}

    .note {{
      margin: 0;
      color: #596579;
      font-size: 14px;
      line-height: 1.6;
    }}

    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
      gap: 14px;
    }}

    .card {{
      display: grid;
      gap: 12px;
      align-content: start;
      min-width: 0;
      padding: 16px;
      border: 1px solid #dbe2ef;
      border-radius: 8px;
      background: #fff;
      box-shadow: 0 10px 28px rgba(23, 32, 51, 0.06);
    }}

    h2 {{
      margin: 0 0 6px;
      font-size: 16px;
      line-height: 1.35;
      overflow-wrap: anywhere;
    }}

    p {{
      margin: 0;
      color: #596579;
      font-size: 12px;
      line-height: 1.45;
      overflow-wrap: anywhere;
    }}

    .qr {{
      width: 180px;
      height: 180px;
      justify-self: center;
      background: #fff;
      image-rendering: pixelated;
    }}

    .actions {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 8px;
    }}

    .button,
    button {{
      min-height: 38px;
      border: 0;
      border-radius: 6px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 0 12px;
      color: #fff;
      background: #1769e0;
      font-size: 14px;
      font-weight: 700;
      text-decoration: none;
      cursor: pointer;
    }}

    button {{
      background: #344054;
    }}

    .empty {{
      padding: 20px;
      border: 1px dashed #c7d0df;
      border-radius: 8px;
      background: #fff;
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <h1>图片二维码目录</h1>
      <p class="note">每张图片都会生成一个单独网页。二维码内容使用当前打开目录页的同源地址，适合本地 Wi-Fi 测试，也适合上传服务器后直接生成公网二维码。</p>
    </header>
    {empty}
    <section class="grid">
{cards}
    </section>
  </main>

  <script>
    function qrUrl(value) {{
      return "https://api.qrserver.com/v1/create-qr-code/?size=720x720&margin=24&format=png&data=" + encodeURIComponent(value);
    }}

    document.querySelectorAll(".card").forEach((card) => {{
      const pageUrl = new URL(card.dataset.page, window.location.href).href;
      const qr = card.querySelector(".qr");
      const openPage = card.querySelector(".open-page");
      const downloadQr = card.querySelector(".download-qr");
      const copyUrl = card.querySelector(".copy-url");
      const imageUrl = qrUrl(pageUrl);

      qr.src = imageUrl;
      openPage.href = pageUrl;
      downloadQr.href = imageUrl;
      copyUrl.addEventListener("click", async () => {{
        await navigator.clipboard.writeText(pageUrl);
        copyUrl.textContent = "已复制";
        setTimeout(() => {{
          copyUrl.textContent = "复制链接";
        }}, 1200);
      }});
    }});
  </script>
</body>
</html>
"""
    write_text(root / "index.html", index)
    return entries


def local_ip():
    for command in (["ipconfig", "getifaddr", "en0"], ["ipconfig", "getifaddr", "en1"]):
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=False)
            value = result.stdout.strip()
            if value:
                return value
        except OSError:
            pass

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        value = sock.getsockname()[0]
        sock.close()
        return value
    except OSError:
        return "127.0.0.1"


def find_port(start):
    for port in range(start, start + 20):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind(("0.0.0.0", port))
                return port
            except OSError:
                continue
    raise RuntimeError("No available port found.")


def serve(root, preferred_port):
    port = find_port(preferred_port)
    os.chdir(root)
    handler = http.server.SimpleHTTPRequestHandler
    server = socketserver.TCPServer(("0.0.0.0", port), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    url = f"http://{local_ip()}:{port}/index.html"
    subprocess.run(["open", url], check=False)
    print("")
    print("Batch QR directory is ready:")
    print(url)
    print("")
    print("Keep this window open while testing on a phone.")
    print("Phone and computer must be on the same Wi-Fi.")
    print("Press Ctrl+C to stop.")
    print("")

    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        server.shutdown()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    entries = build(root)
    print(f"Generated {len(entries)} page(s).")
    if args.serve:
      serve(root, args.port)


if __name__ == "__main__":
    main()
