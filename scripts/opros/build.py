"""Собирает данные анонимного опросника «Как сейчас и каким хочу» из карточек сфер жизни.

Источник: scripts/spheres/source_ru.json + tr_en.json (те же 132 карточки, что в саду).
Результат: quartz/static/opros/data.json — общий для RU и EN страниц.
Запуск: python3 scripts/opros/build.py
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts' / 'spheres'))
from build import SPHERES  # noqa: E402

src = json.loads((ROOT / 'scripts/spheres/source_ru.json').read_text())
tr = json.loads((ROOT / 'scripts/spheres/tr_en.json').read_text())
stories = json.loads((ROOT / 'scripts/opros/stories.json').read_text())

spheres = []
by_sphere = {}
for ru, (slug, _tag, _en_slug, en) in SPHERES.items():
    s = {'id': slug, 'ru': ru, 'en': en, 'subs': []}
    spheres.append(s)
    by_sphere[ru] = s

subs = {}
for c in src:
    s = by_sphere[c['sphere']]
    key = c['sid']
    if key not in subs:
        te = tr['subs'].get(c['sub'], {})
        subs[key] = {'id': key, 'ru': c['sub'], 'en': te.get('name', c['sub']),
                     'q_ru': re.sub(r'\s*Дополнение v\d+:\s*', ' ', c['question']).strip(), 'q_en': te.get('question', ''), 'v': []}
        s['subs'].append(subs[key])
    ce = tr['cards'].get(c['id'], {})
    en_pr = ce.get('practices', [])
    ex = []
    for i, p in enumerate(c['practices']):
        if p['status'].startswith('Кандидат'):
            continue
        ex.append({'ru': p['text'], 'en': en_pr[i] if i < len(en_pr) else '', 'src': p.get('src', '')})
    subs[key]['v'].append({
        'id': c['id'], 'w': c['sc'],
        'n_ru': c['name'], 'n_en': ce.get('name', ''),
        't_ru': c['situation'], 't_en': ce.get('situation', ''),
        'p_ru': c['plus'], 'p_en': ce.get('plus', ''),
        'm_ru': c['minus'], 'm_en': ce.get('minus', ''),
        'ex': ex[:2],
    })
    st = stories.get(c['id'])
    if st:  # мини-история из одной фразы на базе фронтирного сигнала
        subs[key]['v'][-1].update({'s_ru': st['ru'], 's_en': st['en'],
            'g_ru': st['sig_ru'], 'g_en': st['sig_en'], 'g_src': st['src'], 'g_src_en': st.get('src_en', st['src']), 'g_date': st['date']})

out = ROOT / 'quartz/static/opros/data.json'
out.write_text(json.dumps({'spheres': spheres}, ensure_ascii=False, separators=(',', ':')))
n = sum(len(x['subs']) for x in spheres)
print(f'{out.relative_to(ROOT)}: {len(spheres)} сфер, {n} подсфер, {len(src)} вариантов, историй {sum(1 for k in stories if k in {c["id"] for c in src})}, {out.stat().st_size//1024} КБ')

# --- страницы RU и EN из одного шаблона ---
tpl = (ROOT / 'scripts/opros/template.html').read_text()
PAGES = {
    'ru': dict(LANG='ru', PATH='', TITLE='Как сейчас и каким хочу',
               DESC='Анонимный опросник по сферам жизни: выбери сферы, отметь, что есть и что хочешь, и собери свой образ будущего. Ответы не уходят с устройства.',
               BRAND='Декодер Будущего', HOME='/', NAVLABEL='Разделы', T_START='Сферы', T_RUN='Опрос', T_RESULT='Итог',
               OTHER='en/', OTHERLANG='en', OTHERLABEL='EN', DATA='data.json', LAB='/sotrudnichestvo',
               REDIRECT='if(/[?&]lang=en\\b/.test(location.search)){location.replace("en/"+location.hash)}',
               FOOTER='Варианты взяты из <a href="/chetyre-mira/sfery/">сфер жизни</a> метода «Декодер Будущего». Ответы хранятся только в этом браузере.'),
    'en': dict(LANG='en', PATH='en/', TITLE='Now and wanted',
               DESC='An anonymous questionnaire on life spheres: pick spheres, mark what you have and what you want, and build your image of the future. Answers never leave your device.',
               BRAND='Future Decoder', HOME='/en/', NAVLABEL='Sections', T_START='Spheres', T_RUN='Questionnaire', T_RESULT='Result',
               OTHER='../', OTHERLANG='ru', OTHERLABEL='RU', DATA='../data.json', LAB='/en/work-with-me',
               REDIRECT='',
               FOOTER='Options come from the <a href="/en/four-worlds/life-spheres/">life spheres</a> of the Future Decoder method. Answers are kept only in this browser.'),
}
for lang, kv in PAGES.items():
    html = tpl
    for k, v in kv.items():
        html = html.replace('{{' + k + '}}', v)
    assert '{{' not in html, lang
    dst = ROOT / 'quartz/static/opros' / ('index.html' if lang == 'ru' else 'en/index.html')
    dst.write_text(html)
    print(dst.relative_to(ROOT))
