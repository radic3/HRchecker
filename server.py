#!/usr/bin/env python3
"""
Server HTTP semplice per servire la dashboard HR
Ottimizzato per Render.com
"""

import http.server
import socketserver
import os
from pathlib import Path

# Porta da Render (variabile ambiente) o default 8000
PORT = int(os.environ.get('PORT', 8000))

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Handler personalizzato con CORS abilitato"""
    
    def end_headers(self):
        # Abilita CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()
    
    def do_GET(self):
        # Redirect root a dashboard
        if self.path == '/':
            self.path = '/dashboard_completa.html'
        return super().do_GET()

def main():
    # Cambia directory alla cartella corrente
    web_dir = Path(__file__).parent
    os.chdir(web_dir)
    
    print("=" * 70)
    print("🌐 SERVER HR DASHBOARD")
    print("=" * 70)
    print(f"\n✅ Server attivo su porta {PORT}")
    print(f"📁 Directory: {web_dir}")
    print(f"\n🌐 Accedi alla dashboard:")
    print(f"   http://localhost:{PORT}/")
    print(f"   http://localhost:{PORT}/dashboard_completa.html")
    print("\n🔒 Dati censurati: Solo prime 3 lettere dei nomi")
    print("\n⏹  Premi CTRL+C per fermare il server")
    print("=" * 70)
    print()
    
    # Avvia server
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛑 Server fermato")
            print("=" * 70)

if __name__ == '__main__':
    main()

