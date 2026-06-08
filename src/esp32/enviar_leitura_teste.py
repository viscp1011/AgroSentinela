"""
enviar_leitura_teste.py - simula 1 ou VARIOS ESP32 enviando leituras ao backend.
Uso:
  python enviar_leitura_teste.py                      # 1 leitura (soja, 0.15)
  python enviar_leitura_teste.py 0.30 cafe sitio-01   # umidade, cultura, id
  python enviar_leitura_teste.py --demo               # cria 4 campos de uma vez
"""
import sys, json, urllib.request
API = "http://localhost:8000/api/leitura"
def enviar(u, cultura, idf):
    corpo = json.dumps({"id_fazenda":idf,"umidade_solo":u,"temperatura":31.0,
                        "umidade_ar":40.0,"cultura":cultura}).encode("utf-8")
    req = urllib.request.Request(API, data=corpo, headers={"Content-Type":"application/json"})
    r = json.loads(urllib.request.urlopen(req, timeout=8).read())
    print("  " + idf.ljust(14) + cultura.ljust(9) + "umid=" + str(u) + " -> risco=" + str(r.get("em_risco")))
def main():
    if "--demo" in sys.argv:
        campos = [(0.11,"soja","campo-soja"),(0.24,"milho","campo-milho"),
                  (0.38,"arroz","campo-arroz"),(0.27,"cafe","campo-cafe")]
        print("Enviando 4 campos (multi-ESP32)...")
        for u,c,i in campos:
            try: enviar(u,c,i)
            except Exception as e: print("  ERRO:", e); return
        print("\nVeja em: http://localhost:8000/app"); return
    u = float(sys.argv[1]) if len(sys.argv)>1 else 0.15
    c = sys.argv[2] if len(sys.argv)>2 else "soja"
    i = sys.argv[3] if len(sys.argv)>3 else "campo-soja"
    try: enviar(u,c,i); print("Atualize o painel: http://localhost:8000/app")
    except Exception as e: print("ERRO: backend rodando? (RODAR_AGROSENTINELA.bat).", e)
if __name__ == "__main__": main()
