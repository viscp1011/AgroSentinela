"""
assistente_voz.py - AgroSentinela
Assistente de voz que comunica o alerta de risco hidrico ao produtor (TTS) e
entende comandos (STT). Caps. 3 (Fala<->Texto) e 7 (IA como servico cognitivo).
TTS: tenta gTTS (MP3) e, offline, pyttsx3. Gera assets/alerta_voz.mp3.
"""
import os, json
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "data"))
ASSETS_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "assets"))
PREVISAO = os.path.join(DATA_DIR, "previsao.json")
CRONOGRAMA = os.path.join(DATA_DIR, "cronograma_soja.json")
AUDIO_SAIDA = os.path.join(ASSETS_DIR, "alerta_voz.mp3")
LIMIAR_CRITICO = 0.20

def _ler(c):
    with open(c, encoding="utf-8") as f: return json.load(f)

def gerar_mensagem():
    prev = _ler(PREVISAO)
    try: cron = _ler(CRONOGRAMA)
    except Exception: cron = {"total_agua_mm": 15.0}
    horas = sum(1 for v in prev["previsao_umidade"] if v < LIMIAR_CRITICO)
    if horas == 0:
        return ("Ola produtor. Aqui e o AgroSentinela. Tudo certo na sua fazenda em "
                "Ribeirao Preto. A umidade do solo deve continuar acima do nivel critico "
                "nas proximas 24 horas. Nao e preciso irrigar com urgencia.")
    return ("Atencao produtor. Aqui e o AgroSentinela. Detectamos risco hidrico na sua "
            "fazenda. A umidade do solo deve ficar abaixo do nivel critico nas proximas " +
            str(horas) + " horas. Recomendamos aplicar " + format(cron["total_agua_mm"], ".1f") +
            " milimetros de agua, comecando agora. Isso protege a lavoura e economiza agua.")

def falar(texto, caminho=AUDIO_SAIDA):
    os.makedirs(ASSETS_DIR, exist_ok=True)
    try:
        from gtts import gTTS
        gTTS(text=texto, lang="pt", slow=False).save(caminho)
        print("[VOZ] Audio gerado (gTTS): " + caminho); return caminho
    except Exception as e:
        print("[VOZ] gTTS indisponivel (" + str(e) + "). Tentando pyttsx3...")
    try:
        import pyttsx3
        m = pyttsx3.init(); m.setProperty("rate", 165)
        wav = caminho.replace(".mp3", ".wav"); m.save_to_file(texto, wav); m.runAndWait()
        print("[VOZ] Audio gerado (pyttsx3): " + wav); return wav
    except Exception as e:
        print("[VOZ] pyttsx3 indisponivel (" + str(e) + ").")
    print("[VOZ-TEXTO] " + texto); return None

def ouvir():
    try: import speech_recognition as sr
    except Exception:
        print("[VOZ] Instale: pip install SpeechRecognition pyaudio"); return None
    rec = sr.Recognizer()
    with sr.Microphone() as fonte:
        print("[VOZ] Fale um comando..."); audio = rec.listen(fonte, phrase_time_limit=5)
    try:
        t = rec.recognize_google(audio, language="pt-BR"); print("[VOZ] Entendi: " + t); return t.lower()
    except Exception as e:
        print("[VOZ] Nao entendi (" + str(e) + ")."); return None

if __name__ == "__main__":
    msg = gerar_mensagem(); print("[VOZ] Mensagem:\n" + msg + "\n"); falar(msg)
