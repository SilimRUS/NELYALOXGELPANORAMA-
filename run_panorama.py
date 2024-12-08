import http.server
import socketserver
import webbrowser
import os
import sys
from threading import Timer

def open_browser():
    webbrowser.open('http://localhost:8000')

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

def run_server():
    port = 8000
    
    # Получаем путь к директории, где находится скрипт
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    try:
        with socketserver.TCPServer(("", port), CustomHandler) as httpd:
            print(f"🌍 Сервер запущен на порту {port}")
            print("🔗 Открываю панораму в браузере...")
            print("❌ Для выхода нажмите Ctrl+C")
            
            # Открываем браузер через 1.5 секунды после запуска сервера
            Timer(1.5, open_browser).start()
            
            # Запускаем сервер
            httpd.serve_forever()
            
    except OSError as e:
        if e.errno == 98 or e.errno == 10048:  # Порт занят
            print(f"⚠️ Порт {port} уже используется.")
            print("🔄 Попробуйте закрыть все браузеры и перезапустить программу.")
            sys.exit(1)
        else:
            raise
    except KeyboardInterrupt:
        print("\n👋 Сервер остановлен")
        sys.exit(0)

if __name__ == '__main__':
    run_server()
