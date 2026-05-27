import socketserver
import time


class HandlerMultiClient(socketserver.StreamRequestHandler):
    def handle(self):
        adresse = self.client_address[0]
        print(f"[connexion] {adresse}")
        time.sleep(2)   # rend le parallélisme visible avec deux clients simultanés
        while True:
            ligne = self.rfile.readline()
            if not ligne:
                break
            self.wfile.write(b"Echo : " + ligne)
        print(f"[deconnexion] {adresse}")


class ServeurMultiClient(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 9999
    with ServeurMultiClient((HOST, PORT), HandlerMultiClient) as serveur:
        print(f"Serveur multi-client en écoute sur {HOST}:{PORT} — Ctrl+C pour arrêter")
        serveur.serve_forever()
