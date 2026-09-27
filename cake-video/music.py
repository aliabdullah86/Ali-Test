"""Generates an upbeat, royalty-free music bed (music.wav) synced to the video's 120 BPM cuts."""
import os, wave
import numpy as np

SR, DUR, BPM = 44100, 23.0, 120
BEAT = 60 / BPM
t = np.arange(int(SR * DUR)) / SR
rs = np.random.default_rng(1)
mix = np.zeros_like(t)

def place(sig, start, gain=1.0):
    i0 = int(start * SR)
    if i0 >= len(mix):
        return
    n = min(len(sig), len(mix) - i0)
    mix[i0:i0 + n] += gain * sig[:n]

def env_t(length):
    return np.arange(int(length * SR)) / SR

def kick(big=False):
    lt = env_t(0.9 if big else 0.35)
    f = 45 + 110 * np.exp(-lt * 30)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-lt * (3 if big else 9))

def clap():
    lt = env_t(0.25)
    n = rs.standard_normal(len(lt))
    n = n - np.concatenate([[0], n[:-1]]) * .6
    e = np.exp(-lt * 18) * (1 + .6 * (np.sin(lt * 2 * np.pi * 90) > 0) * (lt < .03))
    return n * e * .5

def hat():
    lt = env_t(0.06)
    n = rs.standard_normal(len(lt))
    n = np.diff(np.concatenate([[0], n]))
    return n * np.exp(-lt * 70) * .25

def tone(freq, length, decay, harm=(1, .5, .25), attack=.005):
    lt = env_t(length)
    e = np.minimum(lt / attack, 1) * np.exp(-lt * decay)
    return e * sum(h * np.sin(2 * np.pi * freq * (k + 1) * lt) for k, h in enumerate(harm))

def riser(length):
    lt = env_t(length)
    n = rs.standard_normal(len(lt))
    n = np.diff(np.concatenate([[0], n]))
    sweep = np.sin(2 * np.pi * np.cumsum(200 + 1800 * (lt / length) ** 2) / SR)
    return (n * .3 + sweep * .15) * (lt / length) ** 2

hz = lambda m: 440 * 2 ** ((m - 69) / 12)
chords = [[57, 60, 64, 67], [53, 57, 60, 64], [48, 52, 55, 60], [55, 59, 62, 67]]  # Am7 Fmaj7 C G

groove = lambda s: 3.0 <= s < 17.0 or 18.5 <= s < 22.0
nbeats = int(DUR / BEAT)
for b in range(nbeats):
    s = b * BEAT
    ch = chords[(b // 4) % 4]
    # pads everywhere
    if b % 4 == 0:
        for m in ch:
            place(tone(hz(m), BEAT * 4 + 1, .5, harm=(1, .3), attack=.2), s, .045)
    if groove(s):
        place(kick(), s, .9)
        if b % 2 == 1:
            place(clap(), s, .55)
        for k in range(2):
            place(hat(), s + k * BEAT / 2 + BEAT / 4, 1.0)
        for k in range(2):  # bass 8ths
            place(tone(hz(ch[0] - 24), BEAT / 2, 6, harm=(1, .4, .1)), s + k * BEAT / 2, .35)
        for k in range(4):  # pluck arpeggio 16ths
            m = ch[(b * 4 + k) % 4] + 12 + (12 if k == 3 else 0)
            place(tone(hz(m), .3, 14, harm=(1, .2, .3)), s + k * BEAT / 4, .07)
    elif s < 3.0:  # intro: sparkly music-box
        for k in range(2):
            m = ch[(b * 2 + k) % 4] + 24
            place(tone(hz(m), .8, 4, harm=(1, 0, .3)), s + k * BEAT / 2, .06)

# impacts and risers
for s in (0.5, 3.0, 17.5, 18.5):
    place(kick(big=True), s, 1.3)
place(riser(2.0), 1.0, .5)
place(riser(1.5), 16.0, .5)
place(riser(.9), 17.6, .35)

# light stereo reverb
for d, g in ((0.09, .3), (0.17, .2), (0.27, .12)):
    n = int(d * SR)
    mix[n:] += g * mix[:-n]
mix = np.tanh(mix * 1.4)
fade = np.minimum(1, np.minimum(t / .05, (DUR - t) / 1.5))
mix *= fade
mix = mix / np.abs(mix).max() * .85
stereo = np.stack([mix, np.roll(mix, int(.011 * SR))], axis=1)
with wave.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "music.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((stereo * 32767).astype(np.int16).tobytes())
