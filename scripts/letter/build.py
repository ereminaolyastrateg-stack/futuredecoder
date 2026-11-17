#!/usr/bin/env python3
"""«Письмо из 2035» — страница без ИИ: человек выбирает сферу, подсферу, «как сейчас» и «как хочу»
и получает письмо от себя из 2035 года, собранное из карточки мира (сферы жизни, «Тест · 132»).

python3 scripts/letter/build.py
Источник: scripts/spheres/source_ru.json + scripts/spheres/tr_en.json
Результат: quartz/static/letter/index.html, en/index.html, data-ru.json, data-en.json,
           quartz/static/og/letter-ru.png, letter-en.png
"""
import json, os, re, sys
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '../..'))
sys.path.insert(0, os.path.join(REPO, 'scripts/spheres'))
SP = os.path.join(REPO, 'scripts/spheres')
SRC = json.load(open(os.path.join(SP, 'source_ru.json'), encoding='utf-8'))
TR = json.load(open(os.path.join(SP, 'tr_en.json'), encoding='utf-8'))
OUT = os.path.join(REPO, 'quartz/static/letter')

SPH = OrderedDict([('Здоровье', ('zdorovye', 'health', 'Health')), ('Финансы', ('finansy', 'finance', 'Finance')),
    ('Работа', ('rabota', 'work', 'Work')), ('Образование', ('obrazovanie', 'education', 'Education')),
    ('Близкие отношения и семья', ('semya', 'family', 'Close relationships and family')),
    ('Место жизни и общественная среда', ('sreda', 'place', 'Place of living and public environment')),
    ('Быт, потребление и отдых', ('byt', 'everyday-life', 'Everyday life, consumption and leisure')),
    ('Ценности, смысл и сообщество', ('smysl', 'meaning', 'Values, meaning and community'))])
SL = {'ЦС': 'cs', 'ЦЗ': 'ce', 'ДС': 'ds', 'ДЗ': 'de'}
RES_EN = {'Энергия и здоровье': 'Energy and health', 'Интеллект': 'Intellect', 'Самореализация': 'Self-realisation',
          'Влияние и масштаб': 'Influence and scale', 'Капитал': 'Capital', 'Душа': 'Soul', 'Время': 'Time',
          'Свобода выбора': 'Freedom of choice', 'Деньги': 'Money'}

def anchor(s):
    s = re.sub(r'[^\w\s-]', '', s.lower(), flags=re.U)
    return re.sub(r'\s+', '-', s.strip())

def data(lang):
    out = OrderedDict((k, {'name': k if lang == 'ru' else v[2], 'subs': OrderedDict()}) for k, v in SPH.items())
    for c in SRC:
        sp = out[c['sphere']]
        subname = c['sub'] if lang == 'ru' else TR['subs'][c['sub']]['name']
        q = c['question'] if lang == 'ru' else TR['subs'][c['sub']]['question']
        q = q.split('\n')[0]
        sub = sp['subs'].setdefault(c['sid'], {'id': c['sid'], 'name': subname, 'q': q, 'w': {}})
        t = c if lang == 'ru' else TR['cards'][c['id']]
        pr = c['practices'] if lang == 'ru' else [dict(text=x, src=p['src']) for x, p in zip(t['practices'], c['practices'])]
        res = lambda s: [x.strip() if lang == 'ru' else RES_EN.get(x.strip(), x.strip()) for x in (s or '').split(';') if x.strip()]
        base = f"/chetyre-mira/sfery/{SPH[c['sphere']][0]}" if lang == 'ru' else f"/en/four-worlds/life-spheres/{SPH[c['sphere']][1]}"
        sub['w'][c['sc']] = {'situation': t['situation'], 'plus': t['plus'], 'minus': t['minus'],
                             'spend': res(c['spend']), 'give': res(c['give']),
                             'practices': [{'text': p['text'], 'src': p['src']} for p in pr][:1],
                             'href': f"{base}-{SL[c['sc']]}#{anchor(subname)}"}
    return {'spheres': [{'name': v['name'], 'subs': list(v['subs'].values())} for v in out.values()]}

TX = {
 'ru': dict(
  names={'ЦС': 'Мир автопилота', 'ЦЗ': 'Мир правил', 'ДС': 'Мир автономии', 'ДЗ': 'Мир сообщества'},
  hints={'ЦС': 'решает система, результат не твой', 'ЦЗ': 'участвуешь по общим правилам', 'ДС': 'сам решаешь, сам владеешь', 'ДЗ': 'создаёшь вместе с другими'},
  h1='Письмо из 2035', s1='Выбери сферу жизни', s1n='О чём будет письмо от тебя из будущего.',
  s2='Какая часть этой сферы?', s2n='Под каждой — вопрос, на который ответит письмо.',
  s3='Как у тебя сейчас?', s3n='Выбери, что ближе всего к твоей жизни сегодня. Можно и «ничего из этого».',
  s4='А как хочешь?', s4n='Выбери, как ты хочешь, чтобы стало. Здесь нет правильных ответов.',
  noneNow='Ничего из этого, у меня эта тема пока никак не устроена', noneWant='', back='Назад', another='Написать ещё одно письмо',
  l_hi='Привет! Пишу тебе из 2035 года.', l_hiShort='Привет из 2035!',
  l_nowNone='Помнишь, в 2026-м эта часть жизни у нас была почти никак не устроена?',
  l_now='__NOW__', l_same='__SAME__', l_want='__WANT__', l_world='__WORLD__', l_res='__RES__',
  l_gave='Что это нам дало:', l_paid='Чем пришлось платить:', l_start='С чего мы начали — это уже есть и у вас, в 2026-м:',
  src='источник', l_sign='Твоё будущее', l_ps='P. S. Это не прогноз, а один из четырёх вариантов. Посмотри, как это выглядит в других мирах:',
  l_card='Открыть всю карточку в саду.', l_cta='Хочешь проверить, какое будущее строишь ты, — <a href="/sotrudnichestvo">приходи на игру Декодера или в лабораторию «Архитектура человека»</a>.',
  story='Картинка для сторис', shareT='Поделиться письмом', more='Другие приложения',
  shareText='__SHARE__', sharedBanner='Тебе переслали письмо из 2035 года. Хочешь получить своё?', writeOwn='Написать своё письмо',
  storyCta='А что напишет тебе твоё будущее?', file='letter-2035.png',
  err='Не получилось загрузить данные. Обнови страницу.'),
 'en': dict(
  names={'ЦС': 'Autopilot world', 'ЦЗ': 'Rules world', 'ДС': 'Autonomy world', 'ДЗ': 'Community world'},
  hints={'ЦС': 'the system decides, the result isn’t yours', 'ЦЗ': 'you take part by shared rules', 'ДС': 'you decide, you own it', 'ДЗ': 'you create together with others'},
  h1='A letter from 2035', s1='Choose a life sphere', s1n='What your letter from the future will be about.',
  s2='Which part of this sphere?', s2n='Each comes with the question your letter will answer.',
  s3='How is it for you now?', s3n='Pick what is closest to your life today. "None of these" is fine too.',
  s4='And how do you want it to be?', s4n='Pick how you want things to become. There are no right answers.',
  noneNow='None of these — this part of my life isn’t set up at all yet', noneWant='', back='Back', another='Write another letter',
  l_hi='Hi! I’m writing to you from 2035.', l_hiShort='Hi from 2035!',
  l_nowNone='Remember how in 2026 this part of our life wasn’t really set up at all?',
  l_now='__NOW__', l_same='__SAME__', l_want='__WANT__', l_world='__WORLD__', l_res='__RES__',
  l_gave='What it gave us:', l_paid='What we paid for it:', l_start='Where we started — it already exists for you in 2026:',
  src='source', l_sign='Your future', l_ps='P.S. This isn’t a forecast, just one of four options. See how it looks in the other worlds:',
  l_card='Open the full card in the garden.', l_cta='Want to find out which future you’re building? <a href="/en/work-with-me">Join a Future Decoder game or the «Human Architecture» lab</a>.',
  story='Image for stories', shareT='Share the letter', more='Other apps',
  shareText='__SHARE__', sharedBanner='Someone shared a letter from 2035 with you. Want one of your own?', writeOwn='Write my own letter',
  storyCta='What will your future write to you?', file='letter-2035.png',
  err='Couldn’t load the data. Please refresh the page.'),
}
FN = {
 'ru': {'__NOW__': 'n=>`Помнишь, как было у нас в 2026-м: <q>${esc(trim(n))}</q>? Хотелось по-другому.`',
        '__SAME__': 'n=>`В 2026-м у нас было так: <q>${esc(trim(n))}</q>. Мы решили это не менять — и вот как оно выглядит теперь.`',
        '__WANT__': 'w=>`Теперь у меня так: <q>${esc(trim(w))}</q>.`',
        '__WORLD__': '(n,h)=>`Это ${esc(n.toLocaleLowerCase("ru"))}: ${esc(h)}.`',
        '__RES__': '(s,g)=>`На это ушли ${esc(s)}, а взамен прибавилось: ${esc(g)}.`',
        '__SHARE__': '(sub,w)=>`Мне пришло письмо от себя из 2035 года. Тема: «${sub}», мир: ${w.toLocaleLowerCase("ru")}. А что напишет тебе твоё будущее?`'},
 'en': {'__NOW__': 'n=>`Remember how it was for us in 2026: <q>${esc(trim(n))}</q>? We wanted it to be different.`',
        '__SAME__': 'n=>`In 2026 it was like this for us: <q>${esc(trim(n))}</q>. We decided not to change it — and here is how it looks now.`',
        '__WANT__': 'w=>`Now my life looks like this: <q>${esc(trim(w))}</q>.`',
        '__WORLD__': '(n,h)=>`This is the ${esc(n)}: ${esc(h)}.`',
        '__RES__': '(s,g)=>`It took ${esc(s)}, and in return we gained ${esc(g)}.`',
        '__SHARE__': '(sub,w)=>`I got a letter from myself in 2035. Topic: “${sub}”, world: ${w}. What will your future write to you?`'},
}
PAGE = {
 'ru': dict(TITLE='Письмо из 2035 — Декодер Будущего', DESC='Выбери сферу жизни, отметь, как у тебя сейчас и как хочешь, и получи письмо от себя из 2035 года: что это дало, чем пришлось платить и где это уже есть сегодня.',
            SELF='/static/letter/', HOME='/', POLOTNO='/static/polotno/', OTHER='/static/letter/en/', T_POLOTNO='Полотно будущего', T_GARDEN='← В сад',
            T_OTHER='EN', T_LOGO='Декодер<br>Будущего', T_H1='Письмо из 2035', T_HAND='от тебя — тебе',
            T_LEAD='Выбери сферу жизни, отметь, как у тебя сейчас и как ты хочешь. Будущее ответит письмом: что это тебе дало, чем пришлось платить и где такое уже есть сегодня. Письмо собрано из 132 карточек метода «Декодер Будущего».',
            T_NOJS='Для письма нужен включённый JavaScript.', T_FOOT='Это не прогноз. Четыре мира — четыре логики, по которым может сложиться жизнь. Подробнее — в разделе <a href="/chetyre-mira/sfery/">«Сферы жизни»</a>.'),
 'en': dict(TITLE='A letter from 2035 — Future Decoder', DESC='Pick a life sphere, mark how things are now and how you want them to be, and get a letter from yourself in 2035: what it gave you, what it cost and where it already exists today.',
            SELF='/static/letter/en/', HOME='/en/', POLOTNO='/static/polotno/en/', OTHER='/static/letter/', T_POLOTNO='Canvas of the future', T_GARDEN='← To the garden',
            T_OTHER='RU', T_LOGO='Future<br>Decoder', T_H1='A letter from 2035', T_HAND='from you — to you',
            T_LEAD='Pick a life sphere, mark how things are for you now and how you want them to be. The future will reply with a letter: what it gave you, what it cost and where it already exists today. The letter is built from the 132 cards of the Future Decoder method.',
            T_NOJS='The letter needs JavaScript enabled.', T_FOOT='This isn’t a forecast. The four worlds are four logics by which life can unfold. More in the <a href="/en/four-worlds/life-spheres/">Life Spheres</a> section.'),
}

def main():
    tpl = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
    for lang in ('ru', 'en'):
        d = data(lang)
        os.makedirs(OUT, exist_ok=True)
        json.dump(d, open(os.path.join(OUT, f'data-{lang}.json'), 'w', encoding='utf-8'), ensure_ascii=False)
        tx = json.dumps(TX[lang], ensure_ascii=False)
        for k, v in FN[lang].items():
            tx = tx.replace(json.dumps(k), v)
        h = tpl.replace('__TX__', tx).replace('__LANG__', lang)
        for k, v in PAGE[lang].items():
            h = h.replace(f'__{k}__', v)
        path = os.path.join(OUT, 'index.html') if lang == 'ru' else os.path.join(OUT, 'en', 'index.html')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, 'w', encoding='utf-8').write(h)
    # картинки для соцсетей
    sys.path.insert(0, os.path.join(REPO, 'scripts/polotno'))
    import og
    og.page('Письмо из 2035', 'Выбери сферу жизни — и получи письмо от себя из будущего', os.path.join(REPO, 'quartz/static/og/letter-ru.png'))
    og.page('A letter from 2035', 'Pick a life sphere — and get a letter from your future self', os.path.join(REPO, 'quartz/static/og/letter-en.png'), label='Future Decoder')
    print('ok')

if __name__ == '__main__':
    main()
