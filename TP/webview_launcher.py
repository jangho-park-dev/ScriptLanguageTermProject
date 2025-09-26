import sys
import webview

if len(sys.argv) < 2:
    print("URL이 필요합니다.")
    sys.exit(1)

url = sys.argv[1]

webview.create_window('Google Map', url, width=1280, height=720)
webview.start()