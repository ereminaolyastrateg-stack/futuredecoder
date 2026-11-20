#!/usr/bin/env python3
"""Собирает подборку «Сигналы 2026: ноябрь — декабрь» (RU + EN).

python3 scripts/signals/build_2026.py
Данные: scripts/signals/data_2026_nov_dec.py
Результат:
  content/materialy/signaly/2026-noyabr-dekabr.md            — обзор (RU)
  content/materialy/signaly/2026-11-12/sig-2026-NNN.md        — 80 сигналов (RU)
  content/en/materials/signals/2026-november-december.md     — overview (EN)
  content/en/materials/signals/2026-nov-dec/sig-2026-NNN.md  — 80 signals (EN)
Повторный запуск перезаписывает эти файлы целиком.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data_2026_nov_dec as D

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
TODAY = '2026-11-20'

MT_EN = {
 1: 'Holistic health', 2: 'Human–machine interaction', 5: 'Super-safe society', 7: 'Automation of labour',
 11: 'Biotechnology and personalised medicine', 13: 'Gamification', 14: 'Gig economy',
 16: 'Global migration and demographic shifts', 17: 'Demographic decline and the ageing economy',
 23: 'Cybersecurity and sovereignty', 24: 'Cognitive engineering and neural interfaces', 26: 'Creative economy',
 27: 'Crisis of individualism', 29: 'Crisis of social institutions', 30: 'Culture as a source of the future',
 31: 'Human mastery', 34: 'World of mixed logic', 36: 'Nationalism 2.0', 38: 'Inequality and resource distribution',
 39: 'New social dynamics and inclusion', 40: 'New drivers of economic growth', 43: 'Education, knowledge and literacy',
 44: 'Public trust and digital ethics', 47: 'Advanced AI systems and cognitive computing', 49: 'Rethinking the role of food',
 50: 'Post-growth', 51: 'Preventive medicine and personalised health', 53: 'Progressive province',
 54: 'Future design and strategic vision', 55: 'Psychological resilience and the crisis of thinking',
 56: 'Psychological well-being and mental health', 57: 'Radical longevity',
 60: 'Declining human productivity and technological degradation', 63: 'Techno-nationalism and localised production',
 65: 'Transformational economy (value vertigo)', 66: 'Labour-market transformation and talent management',
 67: 'Family transformation and multiple partnership formats', 71: 'Sustainable development and climate adaptation',
 72: 'Futuristic scenarios and universal laws of development', 75: 'Digital twin',
 76: 'Digital communities and virtual interaction', 79: 'Attention economy and new marketing',
 81: 'Ecosystems, super-apps and the platform economy',
}
MT_NOTES = {'ru': {31: 'materialy/makrotrendy/masterstvo-cheloveka', 43: 'materialy/makrotrendy/obrazovanie-znanie-gramotnost'},
            'en': {31: 'en/materials/macrotrends/human-mastery', 43: 'en/materials/macrotrends/education-knowledge-literacy'}}
SC = {'ЦС': ('CS', 'cs'), 'ЦЗ': ('CE', 'ce'), 'ДС': ('DS', 'ds'), 'ДЗ': ('DE', 'de')}
WORLD = {'ru': {'ЦС': ('chetyre-mira/centr-sintetika', 'ЦС — Центр — Синтетика'), 'ЦЗ': ('chetyre-mira/centr-zemlya', 'ЦЗ — Центр — Земля'),
                'ДС': ('chetyre-mira/decentr-sintetika', 'ДС — Децентр — Синтетика'), 'ДЗ': ('chetyre-mira/decentr-zemlya', 'ДЗ — Децентр — Земля')},
         'en': {'ЦС': ('en/four-worlds/centralized-synthetic', 'CS — Centralized — Synthetic'), 'ЦЗ': ('en/four-worlds/centralized-earth', 'CE — Centralized — Earth'),
                'ДС': ('en/four-worlds/decentralized-synthetic', 'DS — Decentralized — Synthetic'), 'ДЗ': ('en/four-worlds/decentralized-earth', 'DE — Decentralized — Earth')}}
WHY_SCEN = {
 'ru': {'ЦС': 'Решение принимает система, платформа или инфраструктура, а человек получает готовый результат.',
        'ЦЗ': 'Направление задаёт государство, институт или общая норма, а человек встраивается в предложенный путь.',
        'ДС': 'Человек сам выбирает и собирает инструменты, и сам отвечает за результат.',
        'ДЗ': 'Опора — свой круг, связи и локальное сообщество, а не система сверху.'},
 'en': {'ЦС': 'A system, platform or infrastructure makes the decision, and the person receives a ready result.',
        'ЦЗ': 'The state, an institution or a shared norm sets the direction, and the person fits into the path offered.',
        'ДС': 'The person chooses and assembles the tools and is responsible for the outcome.',
        'ДЗ': 'Support comes from one’s own circle, connections and local community rather than a system above.'}}
SPH = [('Здоровье', 'zdorovye', 'Health', 'health'), ('Финансы', 'finansy', 'Finance', 'finance'), ('Работа', 'rabota', 'Work', 'work'),
       ('Образование', 'obrazovanie', 'Education', 'education'), ('Близкие отношения и семья', 'semya', 'Close relationships and family', 'family'),
       ('Место жизни и общественная среда', 'sreda', 'Place of living and public environment', 'place'),
       ('Быт, потребление и отдых', 'byt', 'Everyday life, consumption and leisure', 'everyday-life'),
       ('Ценности, смысл и сообщество', 'smysl', 'Values, meaning and community', 'meaning')]
SPH_RU = {a: (b, c, d) for a, b, c, d in SPH}
SPH_TAG = {'zdorovye': 'здоровье', 'finansy': 'финансы', 'rabota': 'работа', 'obrazovanie': 'образование', 'semya': 'семья', 'sreda': 'среда', 'byt': 'быт', 'smysl': 'смысл'}
from urllib.parse import urlparse
STAGE = {'Л': ('Пример из лекции', 'Example from the lecture'), 'С': ('Выступление или проект на симпозиуме', 'Symposium talk or project'),
         'Ст': ('Исследование', 'Research paper')}

L = {
 'ru': dict(dir='content/materialy/signaly/2026-11-12', url='materialy/signaly/2026-11-12', hub='content/materialy/signaly/2026-noyabr-dekabr.md',
            hub_url='materialy/signaly/2026-noyabr-dekabr', hubname='Сигналы 2026: ноябрь — декабрь', sph_base='chetyre-mira/sfery',
            t=('тип/сигнал', 'сценарий/', 'сфера/', 'тема/', 'макротренд/mt-', 'подборка/сигналы-2026'),
            f=dict(brief='Кратко', period='Дата / период', geo='География', stage='Тип и стадия', scen='Сценарий', why_scen='Почему этот сценарий',
                   trend='Тренд подборки', mt='Макротренды-драйверы', sph='Сферы', tags='Тематические теги', descr='Описание', why='Почему это сигнал',
                   where='Где прозвучало', bounds='Границы вывода', links='Связи', other='Этот сигнал на английском', same='Тот же тренд в других мирах',
                   src='Источник', back='Все сигналы подборки')),
 'en': dict(dir='content/en/materials/signals/2026-nov-dec', url='en/materials/signals/2026-nov-dec', hub='content/en/materials/signals/2026-november-december.md',
            hub_url='en/materials/signals/2026-november-december', hubname='Signals 2026: November — December', sph_base='en/four-worlds/life-spheres',
            t=('type/signal', 'scenario/', 'domain/', 'theme/', 'macrotrend/mt-', 'collection/signals-2026'),
            f=dict(brief='In brief', period='Date / period', geo='Geography', stage='Type and stage', scen='Scenario', why_scen='Why this scenario',
                   trend='Collection trend', mt='Macrotrend drivers', sph='Life domains', tags='Thematic tags', descr='Description', why='Why this is a signal',
                   where='Where it came up', bounds='Limits of the conclusion', links='Links', other='This signal in Russian', same='The same trend in other worlds',
                   src='Source', back='All signals in this collection')),
}
BOUNDS = {
 'Л': ('Пример приведён в лекции как иллюстрация тренда; цифры взяты из указанного источника.', 'The example was used in the lecture to illustrate the trend; figures come from the source given.'),
 'С': ('Это высказывание или проект участника симпозиума, а не подтверждённая практика. Пересказ сделан по машинной расшифровке сессии.', 'This is a statement or project by a symposium participant, not a confirmed practice. The summary is based on a machine transcript of the session.'),
 'Ст': ('Авторы называют свои выводы ранними описательными индикаторами, а не причинной оценкой.', 'The authors describe their findings as early descriptive indicators rather than causal estimates.'),
}

def slug(s):
    s = s.strip().lower()
    s = re.sub(r'[«»“”"\'()\[\],:;!?.]', '', s)
    return re.sub(r'[\s_/]+', '-', s).strip('-')

def yq(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'

def mt_label(i, lang):
    return f"MT-{i:03d} — {D.MT_NAMES[i] if lang == 'ru' else MT_EN[i]}"

def mt_link(i, lang, sc):
    base = MT_NOTES[lang].get(i)
    return f'[[{base}-{SC[sc][1]}|{mt_label(i, lang)}]]' if base else mt_label(i, lang)

SIGS = []
for n, s in enumerate(D.S, 1):
    SIGS.append(dict(zip(['trend', 'sc', 'src', 'year', 'name_ru', 't_ru', 't_en', 'd_ru', 'd_en', 'w_ru', 'w_en', 'url', 'g_ru', 'g_en'], s), id=f'SIG-2026-{n:03d}', name_en=D.NAMES_EN[n - 1]))
assert len(D.NAMES_EN) == len(D.S)
by_trend = {}
for s in SIGS:
    by_trend.setdefault(s['trend'], []).append(s)

def first_sentence(t):
    m = re.match(r'(.+?[.!?])(\s|$)', t)
    return m.group(1) if m else t

def note(s, lang):
    c = L[lang]; f = c['f']; ru = lang == 'ru'
    tr = D.TRENDS[s['trend']]
    sc = s['sc']; code = sc if ru else SC[sc][0]
    title = s['t_ru'] if ru else s['t_en']
    descr = s['d_ru'] if ru else s['d_en']
    why = s['w_ru'] if ru else s['w_en']
    theme = tr[6] if ru else tr[7]
    trend_name = tr[0] if ru else tr[1]
    mts = tr[4]
    sph = tr[5]
    sph_names = sph if ru else [SPH_RU[x][1] for x in sph]
    sph_slugs = [SPH_RU[x][0] if ru else SPH_RU[x][2] for x in sph]
    tags = [c['t'][0], c['t'][1] + code, c['t'][2] + (SPH_TAG[sph_slugs[0]] if ru else sph_slugs[0]), c['t'][3] + slug(theme), f"{c['t'][4]}{mts[0]:03d}", c['t'][5]]
    sid = s['id'].lower()
    nm = s['name_ru'] if ru else s['name_en']
    other = L['en' if ru else 'ru']['url']
    src_label = D.SRC[s['src']][0 if ru else 1]
    period = (f"{s['year']}" if s['src'] != 'С' else ('12–13 ноября 2026' if ru else '12–13 November 2026'))
    if s['src'] == 'Л' and s['year'] == 2026:
        period = '2026'
    stage = STAGE[s['src']][0 if ru else 1]
    world_path, world_name = WORLD[lang][sc]
    sib = [x for x in by_trend[s['trend']] if x is not s]
    fm = ['---', f'title: {yq(title)}', f'description: {yq(first_sentence(descr))}', f'lang: {lang}', 'translations:',
          f"  ru: /{L['ru']['url']}/{sid}", f"  en: /{L['en']['url']}/{sid}", 'aliases:', f"  - {s['id']}", 'tags:'] + [f'  - {t}' for t in tags] + [
          'signal_type: signal', f"signal_id: {s['id']}", f"year: {s['year']}", f'added: {TODAY}', f"name: {yq(nm)}", f'scenario: {code}',
          f'period: {yq(period)}', f"geography: {yq(s['g_ru'] if ru else s['g_en'])}", f'stage: {yq(stage)}',
          'life_domains:'] + [f'  - {yq(x)}' for x in sph_names] + ['industries: []', 'themes:', f'  - {yq(theme)}', f'  - {yq(trend_name)}',
          'macrotrends:'] + [f'  - {yq(mt_label(i, lang))}' for i in mts] + [f'created: {TODAY}', f'updated: {TODAY}', '---', '']
    body = [f"*{s['id']} · {nm}*", '',
            f"**{f['brief']}:** {first_sentence(descr)}", '',
            f"**{f['period']}:** {period}.  ",
            f"**{f['geo']}:** {s['g_ru'] if ru else s['g_en']}.  ",
            f"**{f['stage']}:** {stage}.  ",
            f"**{f['scen']}:** [[{world_path}|{world_name}]].", '',
            f"**{f['why_scen']}:** {WHY_SCEN[lang][sc]}", '',
            f"**{f['trend']}:** [[{c['hub_url']}#{'тренд' if ru else 'trend'}-{s['trend']}|{s['trend']}. {trend_name}]] — {tr[2] if ru else tr[3]}", '',
            f"**{f['mt']}:** " + '; '.join(mt_link(i, lang, sc) for i in mts) + '.', '',
            f"**{f['sph']}:** " + '; '.join(f"[[{c['sph_base']}/{sl}-{SC[sc][1]}|{nm}]]" for sl, nm in zip(sph_slugs, sph_names)) + '.  ',
            f"**{f['tags']}:** {theme}.", '',
            f"### {f['descr']}", '', descr, '',
            f"### {f['why']}", '', why, '',
            f"### {f['where']}", '', src_label + '.', '',
            f"### {f['bounds']}", '', BOUNDS[s['src']][0 if ru else 1], '',
            f"### {f['links']}", '',
            f"- [[{other}/{sid}|{f['other']}]].",
            f"- {f['same']}: " + '; '.join(f"[[{c['url']}/{x['id'].lower()}|{(WORLD[lang][x['sc']][1].split(' — ')[0])} · {x['name_ru'] if ru else x['name_en']}]]" for x in sib) + '.', '']
    if s['url']:
        body += [f"**{f['src']}:** [{urlparse(s['url']).netloc.replace('www.', '')}]({s['url']}).", '']
    else:
        body += [f"**{f['src']}:** {src_label}.", '']
    body += ['---', '', f"{f['back']}: [[{c['hub_url']}|{c['hubname']}]]", '']
    return '\n'.join(fm + body)

def link_md(s, lang):
    c = L[lang]
    return f"[{s['name_ru'] if lang == 'ru' else s['name_en']}](/{c['url']}/{s['id'].lower()})"

def hub(lang):
    ru = lang == 'ru'; c = L[lang]
    other_hub = L['en' if ru else 'ru']['hub_url']
    fm = ['---', f"title: {yq(c['hubname'])}",
          f"seoTitle: {yq('Сигналы 2026: 20 трендов × 4 сценария' if ru else 'Signals 2026: 20 trends × 4 scenarios')}",
          f"description: {yq('80 сигналов ноября — декабря 2026 года из лекции об институтах будущего и симпозиума «Создавая будущее»: 20 трендов в четырёх мирах Декодера и что обновить в своде макротрендов.' if ru else '80 signals from November–December 2026, drawn from a lecture on futures institutes and the “Creating the Future” symposium: 20 trends across the four Decoder worlds and what to update in the macrotrend set.')}",
          f'lang: {lang}', 'translations:', f"  ru: /{L['ru']['hub_url']}", f"  en: /{L['en']['hub_url']}",
          'aliases:', '  - signals-2026' if not ru else '  - signaly-2026', 'tags:',
          f"  - {'тип/обзор' if ru else 'type/overview'}", f"  - {c['t'][5]}", f'created: {TODAY}', f'updated: {TODAY}', '---', '']
    if ru:
        intro = [
         'В этой подборке — 80 сигналов ноября 2026 года, собранных в 20 трендов. У каждого тренда четыре сигнала, по одному на каждый мир Декодера: ЦС — мир автопилота, ЦЗ — мир правил, ДС — мир автономии, ДЗ — мир сообщества. Подборка будет пополняться сигналами декабря.',
         '',
         'Откуда сигналы:',
         '',
         '- **лекция «Будущее поменяло хозяев»** (11 ноября 2026) — как институты будущего переписали свои тренды и методы за год, чего они не видят и что делают люди снизу;',
         f'- **III Международный симпозиум «Создавая будущее»** (Москва, 12–13 ноября 2026) — сессии о научной фантастике, будущем человечества и ИИ, питчинг «Кино как инструмент борьбы с футурошоком», лекция нейрофизиолога Дубынина, сессия о нейроморфных вычислениях ([обзор программы]({D.SYMP2}), [итоги]({D.SYMP}));',
         f'- **исследование Стэнфорда «Canaries in the Coal Mine?»** (версия августа 2026) — как ИИ меняет найм молодых ([исследование]({D.STAN})).',
         '',
         'Распределение сигналов по мирам — наше прочтение, его можно оспорить. Высказывания со симпозиума пересказаны по машинным расшифровкам: это мнения выступавших, а не подтверждённые факты. Цифры из лекции сверены с источниками, которые указаны в каждом сигнале. Дата подборки — 20 ноября 2026 года.',
         '',
         '> Каждый сигнал — отдельная заметка. Ниже — карта 20 трендов, что обновить в своде макротрендов и каталог: ищите и фильтруйте по миру, сфере, теме и макротренду.',
         '', '## 20 трендов × 4 мира', '',
         '| Тренд | ЦС · автопилот | ЦЗ · правила | ДС · автономия | ДЗ · сообщество |', '|---|---|---|---|---|']
    else:
        intro = [
         'This collection holds 80 signals from November 2026, grouped into 20 trends. Each trend has four signals, one for each Decoder world: CS, the autopilot world; CE, the rules world; DS, the autonomy world; DE, the community world. December signals will be added.',
         '',
         'Where the signals come from:',
         '',
         '- **the lecture “The Future Has Changed Hands”** (11 November 2026): how futures institutes rewrote their trends and methods in a year, what they miss and what people do from below;',
         f'- **the III International Symposium “Creating the Future”** (Moscow, 12–13 November 2026): sessions on science fiction, the future of humanity and AI, the film pitch “Cinema as a Tool against Future Shock”, a lecture by neurophysiologist Dubynin and a session on neuromorphic computing ([programme overview]({D.SYMP2}), [summary]({D.SYMP}));',
         f'- **the Stanford study “Canaries in the Coal Mine?”** (August 2026 revision): how AI is changing the hiring of young people ([paper]({D.STAN})).',
         '',
         'Assigning signals to worlds is our reading and can be challenged. Symposium statements are summarised from machine transcripts: they are speakers’ opinions, not confirmed facts. Lecture figures were checked against the sources listed in each signal. Collection date: 20 November 2026.',
         '',
         '> Each signal is a separate note. Below are a map of the 20 trends, what to update in the macrotrend set, and the catalog: search and filter by world, life domain, theme and macrotrend.',
         '', '## 20 trends × 4 worlds', '',
         '| Trend | CS · autopilot | CE · rules | DS · autonomy | DE · community |', '|---|---|---|---|---|']
    rows = []
    for k in sorted(D.TRENDS):
        tr = D.TRENDS[k]
        cells = {x['sc']: link_md(x, lang) for x in by_trend[k]}
        rows.append(f"| <span id=\"{'тренд' if ru else 'trend'}-{k}\"></span>**{k}. {tr[0] if ru else tr[1]}.** {tr[2] if ru else tr[3]} | " + ' | '.join(cells.get(x, '') for x in ['ЦС', 'ЦЗ', 'ДС', 'ДЗ']) + ' |')
    mt = ['', '## Что обновить в своде 82 макротрендов' if ru else '## What to update in the set of 82 macrotrends', '',
          ('Эти макротренды из свода получили новые сигналы. Их описания и сценарные гипотезы стоит проверить и дополнить.' if ru else
           'These macrotrends from the set received new signals. Their descriptions and scenario hypotheses should be reviewed and extended.'), '',
          '| Макротренд | Что добавить | Тренды подборки |' if ru else '| Macrotrend | What to add | Collection trends |', '|---|---|---|']
    for i, a, b, trs in D.MT_UPDATES:
        base = MT_NOTES[lang].get(i)
        name = f'[{mt_label(i, lang)}](/{base})' if base else mt_label(i, lang)
        mt.append(f"| {name} | {a if ru else b} | " + ', '.join(f"[{t}](#{'тренд' if ru else 'trend'}-{t})" for t in trs) + ' |')
    new = ['', '## Кандидаты в новые макротренды' if ru else '## Candidates for new macrotrends', '',
           ('Этих сил в своде нет как самостоятельных — они размазаны по нескольким макротрендам. Предлагаем проверить, не выделить ли их отдельно.' if ru else
            'These forces are not in the set as standalone macrotrends: they are spread across several. We suggest checking whether to separate them.'), '']
    for a, b, ca, cb, t in D.NEW_MT:
        new.append(f"- **{a if ru else b}.** {ca if ru else cb} [{'Тренд' if ru else 'Trend'} {t}](#{'тренд' if ru else 'trend'}-{t}).")
    tail = ['', ('Обзор на английском' if ru else 'This overview in Russian') + f': [[{other_hub}]].', '',
            '[Все сигналы](/materialy/signaly/)' if ru else '[All signals](/en/materials/signals/)', '']
    return '\n'.join(fm + intro + rows + mt + new + tail)

def folder_index(lang):
    ru = lang == 'ru'; c = L[lang]
    return '\n'.join(['---', f"title: {yq('Сигналы 2026: ноябрь — декабрь, все заметки' if ru else 'Signals 2026: November — December, all notes')}",
        f"description: {yq('80 сигналов ноября — декабря 2026 года — каждый отдельной заметкой с тегами по миру, сфере, теме и макротренду.' if ru else '80 signals from November–December 2026, each a separate note tagged by world, life domain, theme and macrotrend.')}",
        f'lang: {lang}', 'translations:', f"  ru: /{L['ru']['url']}/", f"  en: /{L['en']['url']}/", 'tags:',
        f"  - {'тип/указатель' if ru else 'type/index'}", f"  - {c['t'][5]}", f'created: {TODAY}', f'updated: {TODAY}', '---', '',
        ('Каждый сигнал — отдельная заметка. Карта 20 трендов и что обновить в макротрендах — в ' if ru else 'Each signal is a separate note. The map of 20 trends and macrotrend updates are in ')
        + f"[[{c['hub_url']}|{'обзоре подборки' if ru else 'the collection overview'}]].", ''])

if __name__ == '__main__':
    for lang in ('ru', 'en'):
        c = L[lang]
        os.makedirs(os.path.join(REPO, c['dir']), exist_ok=True)
        for s in SIGS:
            open(os.path.join(REPO, c['dir'], s['id'].lower() + '.md'), 'w', encoding='utf-8').write(note(s, lang))
        open(os.path.join(REPO, c['dir'], 'index.md'), 'w', encoding='utf-8').write(folder_index(lang))
        open(os.path.join(REPO, c['hub']), 'w', encoding='utf-8').write(hub(lang))
        print(lang, len(SIGS))
