#!/usr/bin/env python3
"""Брендовые картинки для соцсетей (og:image) в стиле полотна.
python3 scripts/polotno/og.py  — пишет PNG в quartz/static/og/ и static/og-image.png."""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '../..'))
OUT = os.path.join(REPO, 'quartz/static/og')
os.makedirs(OUT, exist_ok=True)
W, H = 1200, 630
PAPER, INK, MUTED = (239, 238, 234), (25, 24, 24), (95, 93, 88)
WORLDS = [('ЦС', (252, 87, 33), 'Мир автопилота', 'Autopilot world', (255, 255, 255)),
          ('ЦЗ', (254, 223, 58), 'Мир правил', 'Rules world', INK),
          ('ДС', (30, 127, 240), 'Мир автономии', 'Autonomy world', (255, 255, 255)),
          ('ДЗ', (253, 127, 184), 'Мир сообщества', 'Community world', INK)]
HOLO = [(242, 211, 107), (240, 138, 75), (233, 80, 142), (122, 92, 240), (47, 167, 232), (95, 211, 160), (242, 211, 107)]

def font(name, size, var):
    f = ImageFont.truetype(os.path.join(HERE, 'fonts', name), size)
    try: f.set_variation_by_name(var)
    except Exception: pass
    return f

def holo(w, h):
    g = Image.new('RGB', (w, h))
    px = g.load()
    n = len(HOLO) - 1
    for x in range(w):
        for y in range(h):
            t = ((x + y * 0.45) / (w + h * 0.45)) * n
            i = min(int(t), n - 1); f = t - i
            a, b = HOLO[i], HOLO[i + 1]
            px[x, y] = tuple(int(a[k] + (b[k] - a[k]) * f) for k in range(3))
    return g

HOLO_BAR = holo(W, 14)
HOLO_SQ = holo(64, 64)

def rounded(im, r):
    m = Image.new('L', im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, im.size[0] - 1, im.size[1] - 1], r, fill=255)
    return m

def wrap(d, text, f, maxw):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def fit(d, text, maxw, maxh, sizes=(92, 84, 76, 68, 60, 54, 48, 42)):
    for s in sizes:
        f = font('Oswald.ttf', s, 'Bold')
        lines = wrap(d, text, f, maxw)
        lh = int(s * 1.08)
        if lh * len(lines) <= maxh: return f, lines, lh
    return f, lines[:5], lh

def base(label):
    im = Image.new('RGB', (W, H), PAPER)
    im.paste(HOLO_BAR, (0, 0))
    im.paste(HOLO_SQ, (64, 50), rounded(HOLO_SQ, 14))
    d = ImageDraw.Draw(im)
    d.text((144, 54), 'FUTURE DECODER', font=font('Oswald.ttf', 26, 'Bold'), fill=INK)
    d.text((144, 84), label, font=font('Inter.ttf', 22, 'Medium'), fill=MUTED)
    return im, d

def question(ask, en, path):
    im, d = base('Future Canvas · four answers from the games' if en else 'Полотно будущего · четыре ответа из игр')
    f, lines, lh = fit(d, ask.upper(), W - 128, 300)
    y = 150 + (300 - lh * len(lines)) // 2
    for l in lines:
        d.text((64, y), l, font=f, fill=INK); y += lh
    x, yb = 64, 492
    fp = font('Inter.ttf', 22, 'SemiBold')
    for code, col, ru, eng, tc in WORLDS:
        name = eng if en else ru
        w = int(d.textlength(name, font=fp)) + 40
        d.rounded_rectangle([x, yb, x + w, yb + 52], 26, fill=col)
        d.text((x + 20, yb + 13), name, font=fp, fill=tc); x += w + 12
    d.text((64, 568), 'futuredecoder.org', font=font('Inter.ttf', 22, 'Medium'), fill=MUTED)
    cta = 'Which world are you building?' if en else 'Какой мир строишь ты?'
    fc = font('Oswald.ttf', 30, 'Bold')
    d.text((W - 64 - d.textlength(cta, font=fc), 562), cta, font=fc, fill=INK)
    im.save(path, optimize=True)

def page(title, sub, path, photo=None, label='Декодер Будущего'):
    im, d = base(label)
    maxw = W - 128 - (380 if photo else 0)
    f, lines, lh = fit(d, title.upper(), maxw, 250, (100, 92, 84, 76, 68, 60))
    y = 150
    for l in lines:
        d.text((64, y), l, font=f, fill=INK); y += lh
    fs = font('Inter.ttf', 28, 'Regular')
    y += 34
    for l in wrap(d, sub, fs, maxw)[:3]:
        d.text((64, y), l, font=fs, fill=MUTED); y += 40
    d.text((64, 568), 'futuredecoder.org', font=font('Inter.ttf', 22, 'Medium'), fill=MUTED)
    if photo:
        ph = Image.open(photo).convert('RGB')
        pw, phh = 330, 440
        r = max(pw / ph.width, phh / ph.height)
        ph = ph.resize((int(ph.width * r), int(ph.height * r)))
        ph = ph.crop(((ph.width - pw) // 2, 0, (ph.width - pw) // 2 + pw, phh))
        frame = holo(pw + 12, phh + 12)
        im.paste(frame, (W - 64 - pw - 12, 120), rounded(frame, 26))
        im.paste(ph, (W - 64 - pw - 6, 126), rounded(ph, 22))
    else:
        x = W - 64 - 4 * 60
        for _, col, *_ in WORLDS:
            d.rounded_rectangle([x, 560, x + 48, 590], 15, fill=col); x += 60
    im.save(path, optimize=True)

if __name__ == '__main__':
    data = json.load(open(os.path.join(REPO, 'quartz/static/polotno/data.json'), encoding='utf-8'))
    n = 0
    for q in data['q']:
        if q.get('show') is False: continue
        question(q['ask'], False, os.path.join(OUT, f"q-{q['id']}-ru.png"))
        if q.get('ask_en'): question(q['ask_en'], True, os.path.join(OUT, f"q-{q['id']}-en.png"))
        n += 1
    photo = os.path.join(REPO, 'quartz/static/about/olya-eremina.jpg')
    P = [('polotno-ru', 'Полотно будущего', 'Вопросы о будущем и четыре ответа на каждый от участников игр. Дуэль миров, дилеммы и сигнал дня.', None, 'Декодер Будущего'),
         ('polotno-en', 'Future Canvas', 'Questions about the future and four answers to each from game participants. Duel of worlds, dilemmas, daily signal.', None, 'Future Decoder'),
         ('home-ru', 'Декодер Будущего', 'Цифровой сад о сценариях будущего: четыре мира, сигналы, игры и база знаний.', None, 'Цифровой сад Оли Ерёминой'),
         ('home-en', 'Future Decoder', 'A digital garden about future scenarios: four worlds, signals, games and a knowledge base.', None, "Olga Eremina's digital garden"),
         ('about-ru', 'Оля Ерёмина', 'Футуролог и стратег, автор метода «Декодер Будущего». Игры, лаборатория, сценарии для компаний.', photo, 'Об авторе'),
         ('about-en', 'Olga Eremina', 'Futurist and strategist, author of the Future Decoder method. Games, the lab, scenarios for companies.', photo, 'About the author'),
         ('talks-ru', 'Лекции и выступления', 'Хаос и неопределённость, образ будущего, глобальные тренды, будущее бизнеса и человека.', photo, 'Оля Ерёмина'),
         ('talks-en', 'Talks and lectures', 'Chaos and uncertainty, images of the future, global trends, the future of business and of people.', photo, 'Olga Eremina'),
         ('work-ru', 'Сотрудничество', 'Сценарные игры, лаборатория «Архитектура человека», сценарии и исследования для компаний, обучение.', None, 'Декодер Будущего'),
         ('work-en', 'Work with me', 'Scenario games, the Architecture of a Person lab, scenarios and research for companies, training.', None, 'Future Decoder')]
    for key, t, s, ph, lab in P:
        page(t, s, os.path.join(OUT, key + '.png'), ph, lab)
    # заменить стандартную картинку Quartz
    Image.open(os.path.join(OUT, 'polotno-ru.png')).save(os.path.join(REPO, 'quartz/static/og-image.png'), optimize=True)
    print('questions:', n, 'pages:', len(P))
