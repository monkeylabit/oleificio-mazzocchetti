#!/usr/bin/env python3
"""Avvia il sito dell'Oleificio Mazzocchetti in locale e lo apre nel browser."""
import http.server, os, re, socket, sys, threading, webbrowser

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map,
                      '.mp4': 'video/mp4', '.webp': 'image/webp', '.js': 'text/javascript'}
    _remaining = None

    def end_headers(self):
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

    def send_head(self):
        rng = self.headers.get('Range')
        path = self.translate_path(self.path)
        if not rng or os.path.isdir(path):
            return super().send_head()
        m = re.match(r'bytes=(\d*)-(\d*)$', rng.strip())
        if not m:
            return super().send_head()
        try:
            f = open(path, 'rb')
        except OSError:
            self.send_error(404)
            return None
        size = os.fstat(f.fileno()).st_size
        a, b = m.groups()
        if a == '':
            start, end = max(0, size - int(b or 0)), size - 1
        else:
            start, end = int(a), min(int(b) if b else size - 1, size - 1)
        if start > end or start >= size:
            f.close()
            self.send_response(416)
            self.send_header('Content-Range', 'bytes */%d' % size)
            self.end_headers()
            return None
        self.send_response(206)
        self.send_header('Content-Type', self.guess_type(path))
        self.send_header('Content-Range', 'bytes %d-%d/%d' % (start, end, size))
        self.send_header('Content-Length', str(end - start + 1))
        self.end_headers()
        f.seek(start)
        self._remaining = end - start + 1
        return f

    def copyfile(self, src, dst):
        try:
            if self._remaining is None:
                return super().copyfile(src, dst)
            rem = self._remaining
            while rem > 0:
                chunk = src.read(min(256 * 1024, rem))
                if not chunk:
                    break
                dst.write(chunk)
                rem -= len(chunk)
        except (BrokenPipeError, ConnectionResetError):
            pass  # il browser ha interrotto la richiesta (normale con i video)
        finally:
            self._remaining = None

    def log_message(self, *args):
        pass


class Server(http.server.ThreadingHTTPServer):
    daemon_threads = True

    def handle_error(self, request, client_address):
        pass


def free_port(start=8080):
    for port in range(start, start + 50):
        with socket.socket() as s:
            try:
                s.bind(('127.0.0.1', port))
                return port
            except OSError:
                continue
    return 0


if __name__ == '__main__':
    port = free_port()
    httpd = Server(('127.0.0.1', port), Handler)
    url = 'http://localhost:%d' % httpd.server_address[1]
    print('\n  Oleificio Mazzocchetti: sito aperto su %s' % url)
    print('  Per fermarlo chiudi questa finestra (o premi Ctrl+C).\n')
    if '--no-browser' not in sys.argv:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
