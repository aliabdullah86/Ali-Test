"""Generates a soft, royalty-free music bed (music.wav) for the promo: warm pad + music-box arpeggio."""
import os, wave
import numpy as np

SR, DUR, BPM = 44100, 26.0, 84
t = np.arange(int(SR * DUR)) / SR
beat = 60 / BPM

def note(freq, start, length, amp, harmonics=(1, .35, .12), decay=3.0):
    out = np.zeros_like(t)
    i0, i1 = int(start * SR), min(len(t), int((start + length) * SR))
    if i0 >= len(t):
        return out
    lt = t[i0:i1] - start
    env = np.minimum(lt / 0.01, 1) * np.exp(-lt * decay)
    out[i0:i1] = amp * env * sum(h * np.sin(2 * np.pi * freq * (k + 1) * lt) for k, h in enumerate(harmonics))
    return out

hz = lambda m: 440 * 2 ** ((m - 69) / 12)
chords = [[57, 60, 64, 67], [53, 57, 60, 64], [48, 52, 55, 60], [55, 59, 62, 67]]  # Am7 Fmaj7 C G
mix = np.zeros_like(t)
bar = beat * 4
for b in range(int(DUR / bar) + 1):
    ch = chords[b % 4]
    for m in ch:  # pad
        mix += note(hz(m), b * bar, bar + 1.5, .05, harmonics=(1, .2), decay=.6)
    mix += note(hz(ch[0] - 12), b * bar, bar, .12, harmonics=(1, .1), decay=.8)
    arp = [ch[0] + 12, ch[2] + 12, ch[1] + 12, ch[3] + 12, ch[2] + 12, ch[1] + 24, ch[3] + 12, ch[2] + 12]
    for k, m in enumerate(arp):  # music box
        if b * bar + k * beat / 2 > 1.0:
            mix += note(hz(m), b * bar + k * beat / 2, 1.6, .07, harmonics=(1, .0, .25), decay=2.5)

# light reverb (feedback delays)
for d, g in ((0.113, .35), (0.187, .25), (0.29, .18)):
    n = int(d * SR)
    mix[n:] += g * mix[:-n]
fade = np.minimum(1, np.minimum(t / 1.0, (DUR - t) / 2.0))
mix = mix * fade
mix = mix / np.abs(mix).max() * 0.6
stereo = np.stack([mix, np.roll(mix, int(.012 * SR))], axis=1)
with wave.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "music.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((stereo * 32767).astype(np.int16).tobytes())
