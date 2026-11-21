"""Transcribe narration takes with Gemini (audio in, text out) to catch bad splits. Usage: python3 tools/transcribe.py <id> i j k ..."""
import base64, json, subprocess, sys, io, wave
sys.path.insert(0, 'tools'); import audio
import numpy as np
tl = json.load(open(f'src/episodes/{sys.argv[1]}.timeline.json'))
vo = audio.read(f"public/{tl['vo']}")
for i in map(int, sys.argv[2:]):
    b = tl['beats'][i]
    x = vo[int(b['start'] * 44100):int((b['start'] + b['vo']) * 44100)]
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(44100); w.writeframes((x * 32767).astype(np.int16).tobytes())
    body = {"contents": [{"parts": [{"inline_data": {"mime_type": "audio/wav", "data": base64.b64encode(buf.getvalue()).decode()}},
                                    {"text": "Transcribe this audio clip exactly, word for word. Output only the transcript."}]}]}
    for model in ("gemini-flash-latest", "gemini-3.5-flash", "gemini-3.8-flash"):
        r = subprocess.run(["curl", "-sS", "-m", "120", "-H", "x-goog-api-key: placeholder", "-H", "Content-Type: application/json", "--data-binary", "@-",
                            f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"], input=json.dumps(body), capture_output=True, text=True)
        try:
            t = json.loads(r.stdout)["candidates"][0]["content"]["parts"][0]["text"].strip(); break
        except Exception:
            t = "ERR " + r.stdout[:150]
    ok = "OK " if t.lower().strip(' .') .replace(',', '') == b['text'].lower().strip(' .').replace(',', '') else "?? "
    print(f"{ok}{i}: {t}\n     want: {b['text']}")
