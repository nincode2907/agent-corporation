import json, threading
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import uvicorn
from agent_corporation_api import settings
ROOT=Path(__file__).parent
class Gateway(BaseHTTPRequestHandler):
    def do_GET(self):
        mode=(ROOT/'mode').read_text().strip()
        code=401 if mode=='auth' else 429 if mode=='rate' else 200
        payload=({'ok':True} if self.path=='/health' else {'object':'list','data':[{'id':'fixture-model'}]})
        if mode=='schema': payload={'unexpected':True}
        with (ROOT/'requests.jsonl').open('a') as f: f.write(json.dumps({'method':'GET','path':self.path,'mode':mode,'status':code})+'\n')
        self.send_response(code); self.send_header('Content-Type','application/json'); self.end_headers(); self.wfile.write(b'\xff' if mode=='utf8' else json.dumps(payload).encode())
    def log_message(self,*args): pass
server=ThreadingHTTPServer(('127.0.0.1',15590),Gateway)
threading.Thread(target=server.serve_forever,daemon=True).start()
def qa_settings():
    mode=(ROOT/'mode').read_text().strip()
    port=15600 if mode=='live' else 15599 if mode=='offline' else 15590
    return settings.Settings(_env_file=None,database_url='postgresql+psycopg://fixture:fixture@127.0.0.1:15599/fixture',app_database_password='fixture',codex_server_base_url=f'http://127.0.0.1:{port}',codex_server_api_key=None,owner_secret_path=ROOT/'missing-owner-secret',runtime_gate_path=ROOT/'missing-gate')
settings.get_settings=qa_settings
from agent_corporation_api.main import app
uvicorn.run(app,host='127.0.0.1',port=15592)
