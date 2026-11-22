"""Topic sound-effect pack (synthesised, royalty-free): writes WAVs into hf/_sfx_extra/.
Usage: python3 tools/sfx_extra.py"""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, 'tools')
import audio
SR = audio.SR
OUT = Path('hf/_sfx_extra'); OUT.mkdir(parents=True, exist_ok=True)
t = lambda s: np.arange(int(s * SR)) / SR
def env(x, a=0.005, r=None):
    e = np.ones(len(x)); n = int(a * SR); e[:n] = np.linspace(0, 1, n)
    if r: m = int(r * SR); e[-m:] *= np.linspace(1, 0, m)
    return x * e
def norm(x, p=0.8): return x / (np.abs(x).max() + 1e-9) * p
def noise(n, seed=1): return np.random.default_rng(seed).standard_normal(n)
def lp(x, k): return np.convolve(x, np.ones(k) / k, mode='same')
S = {}
tt = t(1.2); S['ping'] = norm(np.sin(2 * np.pi * 1320 * tt) * np.exp(-tt * 4) + 0.3 * np.sin(2 * np.pi * 2640 * tt) * np.exp(-tt * 7))
tt = t(0.35); S['chirp'] = norm(env(np.sin(2 * np.pi * (900 + 2600 * tt / 0.35) * tt), r=0.08) * np.exp(-tt * 3))
tt = t(0.5); S['lock'] = norm(np.concatenate([env(np.sin(2 * np.pi * 1760 * t(0.09)), r=0.03), np.zeros(int(.05 * SR)), env(np.sin(2 * np.pi * 2349 * t(0.16)), r=0.08)]))
_c = env(noise(len(t(.03)), 3) * np.exp(-t(.03) * 120)); _b = np.sin(2 * np.pi * 3000 * t(.012)); _c[:len(_b)] += _b; S['tick2'] = norm(_c)
keys = np.zeros(int(1.8 * SR))
for k, at in enumerate(np.cumsum(np.random.default_rng(5).uniform(.05, .11, 14))):
    i = int(at * SR); c = env(noise(len(t(.025)), k) * np.exp(-t(.025) * 140)); keys[i:i + len(c)] += c * np.random.default_rng(k).uniform(.5, 1)
S['keys'] = norm(keys)
tt = t(0.45); S['flip'] = norm(env(lp(noise(len(tt), 9), 6) * np.sin(np.pi * tt / 0.45) ** 2, r=0.05))
tt = t(0.25); S['stamp'] = norm(np.sin(2 * np.pi * (90 + 60 * np.exp(-tt * 40)) * tt) * np.exp(-tt * 18) + 0.4 * lp(noise(len(tt), 2), 3) * np.exp(-tt * 40))
tt = t(1.3); S['powerdown'] = norm(env(np.sin(2 * np.pi * np.cumsum(420 * np.exp(-tt * 2.2) + 30) / SR) * np.exp(-tt * 1.6), r=0.2))
tt = t(0.7); S['static'] = norm(env(noise(len(tt), 11) * (0.6 + 0.4 * np.sin(2 * np.pi * 13 * tt)), r=0.15), 0.6)
tt = t(1.6); S['rumble'] = norm(env(lp(noise(len(tt), 4), 400) * np.sin(np.pi * tt / 1.6), r=0.3))
chain = np.zeros(int(1.0 * SR))
for k in range(9):
    i = int(k * 0.1 * SR); c = env(np.sin(2 * np.pi * (2200 + 300 * k % 3) * t(.06)) * np.exp(-t(.06) * 60) + 0.5 * noise(len(t(.06)), k) * np.exp(-t(.06) * 80)); chain[i:i + len(c)] += c
S['chain'] = norm(chain)
tt = t(0.4); _n = np.zeros(len(tt)); _n[:len(t(.02))] = noise(len(t(.02)), 8); S['snap'] = norm(_n + np.sin(2 * np.pi * 70 * tt) * np.exp(-tt * 10))
tt = t(0.8); S['servo'] = norm(env(np.sign(np.sin(2 * np.pi * (180 + 240 * np.sin(np.pi * tt / 0.8)) * tt)) * 0.3 + 0.2 * noise(len(tt), 6), r=0.1) * np.sin(np.pi * tt / 0.8), 0.6)
tt = t(0.5); S['hiss'] = norm(env(lp(noise(len(tt), 7), 2) * np.exp(-tt * 5), r=0.1), 0.55)
tt = t(0.12); S['switch'] = norm(np.sin(2 * np.pi * 1800 * tt) * np.exp(-tt * 90) + 0.6 * noise(len(tt), 12) * np.exp(-tt * 120))
tt = t(1.6); S['hum'] = norm(env((np.sin(2 * np.pi * 60 * tt) + 0.5 * np.sin(2 * np.pi * 120 * tt)) * (0.8 + 0.2 * np.sin(2 * np.pi * 3 * tt)), r=0.3), 0.5)
for k, x in S.items():
    audio.write(OUT / f'{k}.wav', np.asarray(x, dtype=float))
print('wrote', sorted(S))
