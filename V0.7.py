# JARVIS v0.7 - modo apresentação + memórias musicais + playlists especiais
# Atenção: substitua "SUA_API_KEY_AQUI" pela sua OpenAI API key ou use variável de ambiente.

import speech_recognition as sr
import pyttsx3
import tkinter as tk
from threading import Thread
import openai
import math, time, random, json, os, re, webbrowser, subprocess
from datetime import datetime, timedelta
from pathlib import Path

# extras
import pyautogui
import cv2
import numpy as np
import psutil
import pygetwindow as gw
import yt_dlp
import wikipedia
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import langdetect

# ====== CONFIG ======
openai.api_key = os.getenv("OPENAI_API_KEY", "SUA_API_KEY_AQUI")
MEMORY_FILE = "jarvis_memory.json"
ICONS_DIR = "ICONS"
DOWNLOADS_DIR = Path.home() / "Downloads" / "JARVIS_Music"
DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)

# Hotword/listen tuning
IDLE_SECONDS_TO_NUDGE = 45
NUDGE_INTERVAL_MIN = 60

# Presentation mode tuning
PRESENTATION_NUDGE_INTERVAL = 15  # nudges every 15s when idle in presentation mode
PRESENTATION_VOICE_RATE = 160
PRESENTATION_ANGLE_SPEED = 8

# Spotify env (optional)
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI", "http://localhost:8080/callback")

sp = None
if SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET:
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=SPOTIPY_CLIENT_ID,
            client_secret=SPOTIPY_CLIENT_SECRET,
            redirect_uri=SPOTIPY_REDIRECT_URI,
            scope="user-read-playback-state,user-modify-playback-state,user-read-currently-playing"
        ))
    except Exception:
        sp = None

# ====== MEMÓRIA ======
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "user_name": "Senhor",
        "preferences": {"lang": "pt", "presentation_mode": False},
        "history": [],
        "music": {"favorites": [], "last_played": []}
    }

def save_memory():
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=4, ensure_ascii=False)

memory = load_memory()

# ====== VOZ ======
engine = pyttsx3.init()
voices = engine.getProperty('voices')
# tenta definir uma voz brasileira se houver
for voice in voices:
    if "brazil" in voice.name.lower() or "brazil" in voice.id.lower() or "pt" in voice.languages[0].decode('utf-8').lower() if isinstance(voice.languages[0], bytes) else False:
        engine.setProperty('voice', voice.id)
        break
engine.setProperty('rate', 180)

def set_voice_rate(rate):
    engine.setProperty('rate', rate)

def falar(texto, short=False):
    """
    short=True -> fala mais curta e direta (usado em modo apresentação)
    """
    if memory["preferences"].get("presentation_mode", False) and short:
        # em modo apresentação, fala curta e com ênfase
        set_voice_rate(PRESENTATION_VOICE_RATE)
    else:
        set_voice_rate(180)
    engine.say(texto)
    engine.runAndWait()
    # após falar, volte para padrão se não estiver em apresentação
    if not memory["preferences"].get("presentation_mode", False):
        set_voice_rate(180)

# ====== GPT ======
def conversar_gpt(mensagem):
    try:
        contexto = [{"role": "system", "content": "Você é o JARVIS, assistente pessoal útil, direto e levemente bem-humorado."}]
        for h in memory["history"][-6:]:
            contexto.append({"role": "user", "content": h["user"]})
            contexto.append({"role": "assistant", "content": h["jarvis"]})
        contexto.append({"role": "user", "content": mensagem})

        resposta = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=contexto)
        texto_resposta = resposta.choices[0].message["content"]

        memory["history"].append({"user": mensagem, "jarvis": texto_resposta, "time": time.time()})
        if len(memory["history"]) > 100:
            memory["history"] = memory["history"][-100:]
        save_memory()
        return texto_resposta
    except Exception as e:
        return f"Erro ao conectar com ChatGPT: {e}"

# ====== GUI (Rasengan) ======
root = tk.Tk()
root.title("J.A.R.V.I.S. v0.7")
root.geometry("520x520")
root.config(bg="black")
canvas = tk.Canvas(root, width=520, height=520, bg="black", highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Estado
cor_atual = "blue"
angulo = 0
estrelas = [(random.randint(0, 520), random.randint(0, 520), random.randint(1, 3)) for _ in range(80)]
animation_speed = 50  # ms
angle_speed = 2

def atualizar_cor(cor):
    global cor_atual
    cor_atual = "orange" if cor == "laranja" else "blue"

def desenhar_rasengan():
    global angulo, angle_speed
    canvas.delete("all")
    # estrelas
    for (x, y, r) in estrelas:
        if random.random() > 0.65:
            canvas.create_oval(x, y, x+r, y+r, fill="white", outline="")
    # central glow
    cor_rgb = "#1E90FF" if cor_atual == "blue" else "#FFA500"
    for i in range(8, 0, -1):
        offset = i * 10
        canvas.create_oval(160-offset, 160-offset, 360+offset, 360+offset, fill=cor_rgb, outline=cor_rgb)
    # rotating particles
    for i in range(4):
        raio = 100 + i*20
        for j in range(0, 360, 20):
            ang = math.radians(j + angulo * (i+1))
            x = 260 + math.cos(ang) * raio
            y = 260 + math.sin(ang) * raio
            size = 4 + (i % 3)
            canvas.create_oval(x-size, y-size, x+size, y+size, fill="white", outline="")
    angulo += angle_speed
    root.after(animation_speed, desenhar_rasengan)

# ====== Nudger / perguntas humanizadas ======
last_interaction = time.time()
last_nudge = 0

def hora_bucket():
    h = datetime.now().hour
    if 5 <= h < 12: return "manha"
    if 12 <= h < 18: return "tarde"
    if 18 <= h < 23: return "noite"
    return "madrugada"

def humanized_question(lang="pt"):
    nome = memory.get("user_name", "Senhor")
    hb = hora_bucket()
    weekday = datetime.now().weekday()
    base_pt = {
        "manha": [f"Bom dia, {nome}. Tudo bem?", "Quer revisar seus planos?"],
        "tarde": [f"{nome}, como vai a tarde?", "Quer que eu resuma as notícias?"],
        "noite": [f"{nome}, como foi o dia?", "Quer relaxar com música?"],
        "madrugada": ["Ainda acordado? Precisa de um timer?"]
    }
    base_en = {
        "manha": [f"Good morning, {nome}. Everything okay?", "Shall we review today's plan?"],
        "tarde": [f"Good afternoon, {nome}. How's it going?", "Want a quick news summary?"],
        "noite": [f"Good evening, {nome}. How was your day?", "Do you want some relaxing music?"],
        "madrugada": ["Still awake? Need a short timer?"]
    }
    pool = base_en.get(hb, []) if lang=="en" else base_pt.get(hb, [])
    if weekday >= 5:
        pool.append("Planos para o fim de semana?" if lang=="pt" else "Any plans for the weekend?")
    return random.choice(pool) if pool else ("Posso ajudar?" if lang=="pt" else "Can I help?")

def nudger_loop():
    global last_nudge
    while True:
        time.sleep(5)
        idle = time.time() - last_interaction
        since_last_nudge = time.time() - last_nudge
        if memory["preferences"].get("presentation_mode", False):
            interval = PRESENTATION_NUDGE_INTERVAL
        else:
            interval = IDLE_SECONDS_TO_NUDGE
        min_between = 5 if memory["preferences"].get("presentation_mode", False) else NUDGE_INTERVAL_MIN
        if idle >= interval and since_last_nudge >= min_between:
            lang = memory["preferences"].get("lang", "pt")
            pergunta = humanized_question("en" if lang=="en" else "pt")
            atualizar_cor("laranja")
            # fala curta se em apresentação
            falar(pergunta, short=memory["preferences"].get("presentation_mode", False))
            last_nudge = time.time()
            atualizar_cor("azul")

# ====== utilidades PC ======
def keyboard_shortcut(cmd):
    if cmd == "copiar": pyautogui.hotkey("ctrl", "c")
    elif cmd == "colar": pyautogui.hotkey("ctrl", "v")
    elif cmd == "minimizar": pyautogui.hotkey("win", "d")
    elif cmd == "print":
        dest = Path.home() / "Desktop" / f"print_{int(time.time())}.png"
        pyautogui.screenshot(dest)
        return f"Print salvo em {dest}"
    return None

def draw_mouse_circle(radius=120, steps=60):
    x0, y0 = pyautogui.position()
    for i in range(steps+1):
        angle = 2 * math.pi * i / steps
        x = x0 + radius * math.cos(angle)
        y = y0 + radius * math.sin(angle)
        pyautogui.moveTo(x, y, duration=0.01)
    return True, "Círculo desenhado."

def open_documents():
    docs = os.path.join(os.path.expanduser("~"), "Documents")
    if os.path.isdir(docs):
        os.startfile(docs)
        return True, "Abrindo Documentos."
    return False, "Pasta Documentos não encontrada."

def close_windows_by_keyword(keyword):
    wins = [w for w in gw.getAllTitles() if keyword.lower() in w.lower()]
    if not wins:
        return False, f"Nenhuma janela com '{keyword}' encontrada."
    for wtitle in wins:
        try:
            w = gw.getWindowsWithTitle(wtitle)[0]
            w.activate()
            time.sleep(0.2)
            w.close()
        except Exception:
            pass
    return True, f"Fechando janelas com '{keyword}'."

# ====== Música: YouTube (abrir / baixar+tocar) ======
def youtube_search_url(query):
    return f"https://www.youtube.com/results?search_query={requests.utils.quote(query)}"

def youtube_play_in_browser(query):
    webbrowser.open(youtube_search_url(query))
    return "Abrindo YouTube no navegador."

def youtube_download_and_play(query, play_local=True):
    ydl_opts = {
        "format": "bestaudio/best",
        "default_search": "ytsearch1",
        "outtmpl": str(DOWNLOADS_DIR / "%(title)s.%(ext)s"),
        "quiet": True,
        "noplaylist": True,
        "postprocessors": [{"key": "FFmpegExtractAudio","preferredcodec": "mp3","preferredquality": "192"}],
    }
    file_path = None
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=True)
        title = info["entries"][0]["title"] if "entries" in info else info["title"]
        file_path = DOWNLOADS_DIR / f"{title}.mp3"
    if play_local:
        try:
            subprocess.Popen(["ffplay", "-nodisp", "-autoexit", str(file_path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return f"Tocando localmente: {file_path.name}"
        except Exception:
            return f"Baixado em: {file_path}"
    return f"Baixado em: {file_path}"

# ====== Música: Spotify (melhor esforço) ======
def spotify_play(query):
    if not sp:
        webbrowser.open(f"https://open.spotify.com/search/{requests.utils.quote(query)}")
        return "Abrindo busca no Spotify (sem credenciais)."
    # tenta track/playlist/artist
    track_results = sp.search(q=query, type="track", limit=1)
    if track_results.get("tracks", {}).get("items"):
        uri = track_results["tracks"]["items"][0]["uri"]
    else:
        playlist_results = sp.search(q=query, type="playlist", limit=1)
        if playlist_results.get("playlists", {}).get("items"):
            uri = playlist_results["playlists"]["items"][0]["uri"]
        else:
            artist_results = sp.search(q=query, type="artist", limit=1)
            if artist_results.get("artists", {}).get("items"):
                uri = artist_results["artists"]["items"][0]["uri"]
            else:
                webbrowser.open(f"https://open.spotify.com/search/{requests.utils.quote(query)}")
                return "Não encontrei via API. Abrindo busca no Spotify."
    try:
        devices = sp.devices().get("devices", [])
        if devices:
            device_id = devices[0]["id"]
            if uri.startswith("spotify:track:"):
                sp.start_playback(device_id=device_id, uris=[uri])
            else:
                sp.start_playback(device_id=device_id, context_uri=uri)
            return "Reprodução iniciada no seu dispositivo Spotify."
        else:
            webbrowser.open(f"https://open.spotify.com/search/{requests.utils.quote(query)}")
            return "Nenhum dispositivo Spotify ativo. Abri a busca no navegador."
    except Exception:
        webbrowser.open(f"https://open.spotify.com/search/{requests.utils.quote(query)}")
        return "Erro ao tentar reproduzir no Spotify. Abrindo busca no navegador."

# ====== Pesquisa (Google/G1/Omelete/Wikipedia) ======
def google_search(query):
    url = f"https://www.google.com/search?q={requests.utils.quote(query)}"
    webbrowser.open(url)
    return "Abrindo results no Google."

def g1_search(query):
    url = f"https://g1.globo.com/busca/?q={requests.utils.quote(query)}"
    webbrowser.open(url)
    return "Abrindo notícias no G1."

def omelete_search(query):
    url = f"https://www.omelete.com.br/busca/{requests.utils.quote(query)}"
    webbrowser.open(url)
    return "Abrindo resultados no Omelete."

def wikipedia_summary(query, sentences=2):
    try:
        wikipedia.set_lang("pt" if memory["preferences"].get("lang","pt")=="pt" else "en")
        hits = wikipedia.search(query)
        if not hits:
            webbrowser.open(f"https://pt.wikipedia.org/w/index.php?search={requests.utils.quote(query)}")
            return "Abrindo Wikipédia."
        page = wikipedia.page(hits[0])
        summary = wikipedia.summary(page.title, sentences=sentences)
        webbrowser.open(page.url)
        return f"{page.title}: {summary}"
    except Exception:
        lang_code = "pt" if memory["preferences"].get("lang","pt")=="pt" else "en"
        webbrowser.open(f"https://{lang_code}.wikipedia.org/w/index.php?search={requests.utils.quote(query)}")
        return "Abrindo Wikipédia."

# ====== Timer / Pomodoro ======
def start_timer_seconds(seconds, label="Timer"):
    def timer_thread():
        falar(f"{label} iniciado por {seconds//60} minutos.", short=memory["preferences"].get("presentation_mode", False))
        end_time = time.time() + seconds
        while time.time() < end_time:
            time.sleep(1)
        falar(f"{label} finalizado.", short=True)
    Thread(target=timer_thread, daemon=True).start()

# ====== Helpers para favoritos musicais ======
def add_favorite(query):
    # adiciona string simples ao memory["music"]["favorites"]
    favs = memory["music"].get("favorites", [])
    if query not in favs:
        favs.append(query)
        memory["music"]["favorites"] = favs
        save_memory()
        return True, f"{query} salvo nos favoritos."
    return False, f"{query} já está nos favoritos."

def list_favorites():
    return memory["music"].get("favorites", [])

def play_favorites(source="youtube"):
    favs = list_favorites()
    if not favs:
        return "Nenhum favorito salvo."
    # toca o primeiro favorito (poderíamos criar playlist iterável)
    q = favs[0]
    memory["music"]["last_played"].insert(0, {"query": q, "time": time.time(), "source": source})
    memory["music"]["last_played"] = memory["music"]["last_played"][:20]
    save_memory()
    if source == "spotify":
        return spotify_play(q)
    else:
        return youtube_play_in_browser(q)

# ====== Roteador de comandos (expansivo) ======
def detectar_idioma(texto):
    try:
        lang = langdetect.detect(texto)
        memory["preferences"]["lang"] = "en" if lang.startswith("en") else "pt"
        save_memory()
    except:
        pass

def toggle_presentation_mode(on_or_off=None):
    cur = memory["preferences"].get("presentation_mode", False)
    if on_or_off is None:
        new = not cur
    else:
        new = bool(on_or_off)
    memory["preferences"]["presentation_mode"] = new
    save_memory()
    # adjust animation and voice
    global angle_speed, animation_speed
    if new:
        angle_speed = PRESENTATION_ANGLE_SPEED
        animation_speed = 30
        set_voice_rate(PRESENTATION_VOICE_RATE)
        return f"Modo apresentação ativado." if memory["preferences"].get("lang","pt")=="pt" else "Presentation mode ON."
    else:
        angle_speed = 2
        animation_speed = 50
        set_voice_rate(180)
        return f"Modo apresentação desativado." if memory["preferences"].get("lang","pt")=="pt" else "Presentation mode OFF."

def route_command(text):
    t = text.lower().strip()

    # atalhos
    if "copiar" in t or "copy" in t:
        keyboard_shortcut("copiar"); return True, "Copiado.", None
    if "colar" in t or "paste" in t:
        keyboard_shortcut("colar"); return True, "Colado.", None
    if "minimizar" in t or "minimize" in t:
        keyboard_shortcut("minimizar"); return True, "Minimizando.", None
    if "print" in t or "tire um print" in t or "capturar" in t:
        p = keyboard_shortcut("print"); return True, p, None

    # apps fixos
    fixed_apps = {"bloco de notas":"notepad","calculadora":"calc","explorador de arquivos":"explorer","vscode":"code","paint":"mspaint"}
    for k, cmd in fixed_apps.items():
        if k in t:
            subprocess.Popen(cmd, shell=True)
            return True, f"Abrindo {k}.", None

    # círculo com mouse
    if "círculo" in t or "circle" in t:
        draw_mouse_circle(); return True, "Círculo feito.", None

    # documentos
    if "documentos" in t or "documents" in t:
        ok, msg = open_documents(); return True, msg, None

    # fechar janela
    m_close = re.search(r"(fech(ar|e)|close).*(janela|window|window of)?\s*(do|de|of)?\s*([a-z0-9 ._-]+)", t)
    if m_close:
        keyword = m_close.group(5).strip()
        ok, msg = close_windows_by_keyword(keyword); return True, msg, None

    # ===== música: favoritagem / playbacks / playlists =====
    if re.search(r"(salvar|adicionar|favorito|favorite|save).*(música|musica|artista|song|artist|track)", t):
        # pega depois do verbo
        q = re.sub(r".*(salvar|adicionar|favorito|favorite|save)\s*", "", t)
        q = q.replace("como favorito","").strip()
        ok, msg = add_favorite(q)
        return True, msg, None

    if "tocar favoritos" in t or "play favorites" in t or "tocar favoritos" in t:
        msg = play_favorites(source="spotify" if "spotify" in t else "youtube")
        return True, msg, None

    # playlists especiais
    if "playlist de foco" in t or "focus playlist" in t:
        # por padrão 25 minutos
        secs = 25 * 60
        # try to play via spotify if requested
        if "spotify" in t:
            spotify_play("instrumental focus playlist")
            start_timer_seconds(secs, label="Foco 25 minutos")
            return True, "Playlist de foco iniciada no Spotify.", None
        else:
            youtube_play_in_browser("instrumental focus 25 minutes playlist")
            start_timer_seconds(secs, label="Foco 25 minutos")
            return True, "Playlist de foco iniciada.", None

    if "playlist relaxar" in t or "playlist relax" in t:
        if "spotify" in t:
            spotify_play("relaxing music playlist")
            return True, "Playlist relaxante iniciada no Spotify.", None
        else:
            youtube_play_in_browser("relaxing music playlist")
            return True, "Playlist relaxante iniciada.", None

    if "playlist animar" in t or "playlist animada" in t:
        if "spotify" in t:
            spotify_play("workout upbeat playlist")
            return True, "Playlist animar iniciada no Spotify.", None
        else:
            youtube_play_in_browser("upbeat music playlist")
            return True, "Playlist animar iniciada.", None

    # direta: tocar X no youtube/spotify
    m_youtube = re.search(r"(tocar|toque|play).*(no youtube|youtube)", t)
    if m_youtube:
        q = re.sub(r".*(tocar|toque|play)\s*", "", t)
        q = q.replace("no youtube","").replace("youtube","").strip()
        return True, youtube_play_in_browser(q if q else t), None

    m_spotify = re.search(r"(tocar|toque|play).*(no spotify|spotify)", t)
    if m_spotify:
        q = re.sub(r".*(tocar|toque|play)\s*", "", t)
        q = q.replace("no spotify","").replace("spotify","").strip()
        return True, spotify_play(q if q else t), None

    # baixar música do youtube
    if "baixar" in t and "youtube" in t or ("baixar" in t and "música" in t):
        q = re.sub(r".*(baixar)\s*", "", t)
        q = q.replace("no youtube","").replace("youtube","").replace("música","").strip()
        return True, youtube_download_and_play(q if q else t, play_local=True), None

    # favoritos list
    if "listar favoritos" in t or "mostrar favoritos" in t or "list favorites" in t:
        favs = list_favorites()
        if not favs: return True, "Nenhum favorito salvo.", None
        texto = " | ".join(favs[:8])
        return True, f"Seus favoritos: {texto}", None

    # wikipédia / google / g1 / omelete
    if "wikip" in t:
        q = re.sub(r".*(buscar|pesquisar|procure|search|look up)\s*", "", t)
        return True, wikipedia_summary(q.strip() if q.strip() else t), None
    if "google" in t or "pesquise" in t:
        q = re.sub(r".*(pesquisar|pesquise|buscar|procure)\s*", "", t)
        return True, google_search(q.strip() if q.strip() else t), None
    if "g1" in t:
        q = re.sub(r".*(notícias|noticia|buscar|pesquisar|procure)\s*", "", t)
        return True, g1_search(q.strip() if q.strip() else t), None
    if "omelete" in t:
        q = re.sub(r".*(matéria|materia|buscar|pesquisar|procure)\s*", "", t)
        return True, omelete_search(q.strip() if q.strip() else t), None

    # timers diretos
    m_timer = re.search(r"(timer|temporizador|pomodoro|(\d+)\s*min)", t)
    if "25 minutos" in t or "25 min" in t or ("pomodoro" in t and "25" in t):
        start_timer_seconds(25*60, label="Pomodoro 25 minutos")
        return True, "Pomodoro de 25 minutos iniciado.", None
    if m_timer and m_timer.group(2):
        mins = int(m_timer.group(2))
        start_timer_seconds(mins*60, label=f"Timer {mins} minutos")
        return True, f"Timer de {mins} minutos iniciado.", None

    # modo apresentação on/off
    if "apresentação" in t or "presentation mode" in t or "modo apresentação" in t:
        if "ativar" in t or "on" in t or "ligar" in t:
            msg = toggle_presentation_mode(True); return True, msg, None
        if "desativar" in t or "off" in t or "desligar" in t:
            msg = toggle_presentation_mode(False); return True, msg, None
        # toggle
        msg = toggle_presentation_mode(); return True, msg, None

    return False, "", None

# ====== Hotword listener (contínuo) ======
def hotword_listener():
    global last_interaction
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            try:
                audio = r.listen(source, timeout=None)
                comando = r.recognize_google(audio, language="pt-BR").lower()
                if "jarvis" in comando:
                    last_interaction = time.time()
                    atualizar_cor("laranja")
                    # resposta curta
                    falar("Sim?", short=memory["preferences"].get("presentation_mode", False))
                    atualizar_cor("azul")
                    # ouvir próximo comando
                    audio_cmd = r.listen(source, timeout=8)
                    cmd_text = r.recognize_google(audio_cmd, language="pt-BR")
                    detectar_idioma(cmd_text)
                    last_interaction = time.time()
                    handled, feedback, extra = route_command(cmd_text)
                    if handled:
                        atualizar_cor("laranja")
                        # fala curta se em apresentação
                        falar(feedback, short=memory["preferences"].get("presentation_mode", False))
                        if extra: falar(extra)
                        atualizar_cor("azul")
                    else:
                        atualizar_cor("laranja")
                        resp = conversar_gpt(cmd_text)
                        # em modo apresentação, resposta curta
                        falar(resp, short=memory["preferences"].get("presentation_mode", False))
                        atualizar_cor("azul")
            except sr.UnknownValueError:
                continue
            except Exception as e:
                print("[Erro hotword_listener]", e)
                time.sleep(0.5)
                continue

# ====== START ======
# iniciar GUI anim
desenhar_rasengan()
# threads
Thread(target=hotword_listener, daemon=True).start()
Thread(target=nudger_loop, daemon=True).start()

# início com boas-vindas reduzida
if memory["preferences"].get("presentation_mode", False):
    falar("Jarvis online. Modo apresentação.", short=True)
else:
    falar("Jarvis online. Estou à disposição.")

root.mainloop()
