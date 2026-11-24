"""Ask a Gemini model about an audio clip (through the session proxy). gem(path_or_bytes, prompt, model) -> text."""
import base64, json, subprocess, tempfile


def gem(wav, prompt, model='gemini-2.5-flash', mime='audio/wav'):
    parts = [{"text": prompt}]
    if wav is not None:
        data = wav if isinstance(wav, bytes) else open(wav, 'rb').read()
        parts.insert(0, {"inline_data": {"mime_type": mime, "data": base64.b64encode(data).decode()}})
    body = {"contents": [{"parts": parts}],
            "generationConfig": {"temperature": 0}}
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as f:
        json.dump(body, f)
    import time
    for attempt in range(6):
        r = subprocess.run(["curl", "-sS", "-m", "180", "-H", "x-goog-api-key: placeholder", "-H", "Content-Type: application/json",
                            "-d", "@" + f.name, f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"],
                       capture_output=True, text=True).stdout
        if '"candidates"' in r or attempt == 5:
            break
        time.sleep(10 * (attempt + 1))
    try:
        return ''.join(p.get('text', '') for p in json.loads(r)['candidates'][0]['content']['parts'])
    except Exception:
        raise RuntimeError(r[:500])
