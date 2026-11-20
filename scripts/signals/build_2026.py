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
         'Ст': ('Исследование', 'Research paper'), 'И': ('Исследование или данные', 'Research or data'),
         'Н': ('Новость или событие', 'News or event'), 'К': ('Кейс компании или проекта', 'Company or project case'),
         'Ин': ('Доклад института будущего: что добавлено и что убрано', 'Futures institute report: what was added and removed')}

L = {
 'ru': dict(dir='content/materialy/signaly/2026-11-12', url='materialy/signaly/2026-11-12', hub='content/materialy/signaly/2026-11-12/index.md',
            hub_url='materialy/signaly/2026-11-12/index', hubname='Сигналы: большие тренды, ноябрь 2026', tr_dir='content/materialy/trendy', tr_url='materialy/trendy', sph_base='chetyre-mira/sfery',
            t=('тип/сигнал', 'сценарий/', 'сфера/', 'тема/', 'макротренд/mt-', 'подборка/сигналы-2026'),
            f=dict(brief='Кратко', period='Дата / период', geo='География', stage='Тип и стадия', scen='Сценарий', why_scen='Почему этот сценарий',
                   trend='Тренд подборки', mt='Макротренды-драйверы', sph='Сферы', tags='Тематические теги', descr='Описание', why='Почему это сигнал',
                   where='Откуда сигнал', bounds='Границы вывода', links='Связи', other='Этот сигнал на английском', same='Другие сигналы этого тренда',
                   src='Источник', back='Все сигналы подборки')),
 'en': dict(dir='content/en/materials/signals/2026-nov-dec', url='en/materials/signals/2026-nov-dec', hub='content/en/materials/signals/2026-nov-dec/index.md',
            hub_url='en/materials/signals/2026-nov-dec/index', hubname='Signals: big trends, November 2026', tr_dir='content/en/materials/trends', tr_url='en/materials/trends', sph_base='en/four-worlds/life-spheres',
            t=('type/signal', 'scenario/', 'domain/', 'theme/', 'macrotrend/mt-', 'collection/signals-2026'),
            f=dict(brief='In brief', period='Date / period', geo='Geography', stage='Type and stage', scen='Scenario', why_scen='Why this scenario',
                   trend='Collection trend', mt='Macrotrend drivers', sph='Life domains', tags='Thematic tags', descr='Description', why='Why this is a signal',
                   where='Where the signal comes from', bounds='Limits of the conclusion', links='Links', other='This signal in Russian', same='Other signals of this trend',
                   src='Source', back='All signals in this collection')),
}
BOUNDS = {
 'Л': ('Пример приведён в лекции как иллюстрация тренда; цифры взяты из указанного источника.', 'The example was used in the lecture to illustrate the trend; figures come from the source given.'),
 'С': ('Это высказывание или проект участника симпозиума, а не подтверждённая практика. Пересказ сделан по машинной расшифровке сессии.', 'This is a statement or project by a symposium participant, not a confirmed practice. The summary is based on a machine transcript of the session.'),
 'И': ('Цифры взяты из указанного исследования или опроса; выборка и методика — у авторов. Отнесение к миру Декодера — наше прочтение.', 'Figures come from the study or survey given; sample and method are the authors’. Assigning it to a Decoder world is our reading.'),
 'Н': ('Это отдельное событие, а не устойчивая практика. Сигнал показывает направление, а не масштаб.', 'This is a single event, not an established practice. The signal shows a direction, not a scale.'),
 'К': ('Это один кейс. Он показывает, что так уже можно, но не что так делают все.', 'This is one case. It shows that it can already be done, not that everyone does it.'),
 'Ин': ('Это прочтение доклада института: что в нём появилось и исчезло по сравнению с прошлой версией. Названия трендов даны в нашем переводе.', 'This is a reading of the institute’s report: what appeared and disappeared compared with its previous edition.'),
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

NAME_EN = dict(zip([x[4] for x in D.S], D.NAMES_EN))
assert len(NAME_EN) == len(D.S)
SIGS = []
for n, s in enumerate(sorted(D.S, key=lambda x: (x[0], ['ЦС', 'ЦЗ', 'ДС', 'ДЗ'].index(x[1]))), 1):
    SIGS.append(dict(zip(['trend', 'sc', 'src', 'year', 'name_ru', 't_ru', 't_en', 'd_ru', 'd_en', 'w_ru', 'w_en', 'url', 'g_ru', 'g_en'], s), id=f'SIG-2026-{n:03d}', name_en=NAME_EN[s[4]]))
assert len(D.NAMES_EN) == len(D.S)
by_trend = {}
for s in SIGS:
    by_trend.setdefault(s['trend'], []).append(s)

def tr_id(k):
    return f'TR-2026-11-{k:02d}'

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
            f"**{f['trend']}:** [[{c['tr_url']}/{tr_id(s['trend']).lower()}|{trend_name}]] — {tr[2] if ru else tr[3]}", '',
            f"**{f['mt']}:** " + '; '.join(mt_link(i, lang, sc) for i in mts) + '.', '',
            f"**{f['sph']}:** " + '; '.join(f"[[{c['sph_base']}/{sl}-{SC[sc][1]}|{nm}]]" for sl, nm in zip(sph_slugs, sph_names)) + '.  ',
            f"**{f['tags']}:** {theme}.", '',
            f"### {f['descr']}", '', descr, '',
            f"### {f['why']}", '', why, '',
            f"### {f['where']}", '', src_label + (f" — {urlparse(s['url']).netloc.replace('www.', '')}" if s['url'] else '') + '.', '',
            f"### {f['bounds']}", '', BOUNDS[s['src']][0 if ru else 1], '',
            f"### {f['links']}", '',
            f"- [[{other}/{sid}|{f['other']}]].",
            (f"- {f['same']}: " if sib else '') + '; '.join(f"[[{c['url']}/{x['id'].lower()}|{(WORLD[lang][x['sc']][1].split(' — ')[0])} · {x['name_ru'] if ru else x['name_en']}]]" for x in sib) + ('.' if sib else ''), '']
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
          f"seoTitle: {yq('Фронтирные сигналы 2026: ноябрь' if ru else 'Frontier signals 2026: November')}",
          f"description: {yq(f'{len(SIGS)} фронтирных сигналов ноября 2026 года: исследования, данные, события и кейсы, разложенные по 20 трендам и четырём мирам Декодера.' if ru else f'{len(SIGS)} frontier signals from November 2026: research, data, events and cases arranged by 20 trends and the four Decoder worlds.')}",
          f'lang: {lang}', 'translations:', f"  ru: /{L['ru']['url']}/", f"  en: /{L['en']['url']}/",
          'aliases:', '  - signals-2026' if not ru else '  - signaly-2026', f"  - {'materialy/signaly/2026-noyabr-dekabr' if ru else 'en/materials/signals/2026-november-december'}", 'tags:',
          f"  - {'тип/обзор' if ru else 'type/overview'}", f"  - {c['t'][5]}", f'created: {TODAY}', f'updated: {TODAY}', '---', '']
    if ru:
        intro = [
         f'В этой подборке — {len(SIGS)} фронтирных сигналов ноября 2026 года. Фронтирный значит: новое (2025–2026), удивляет, опирается на конкретный факт с первоисточником, а не на мнение спикера. Мы добавляем не больше 50 сигналов в месяц — лучше меньше, но таких, которые меняют картину. Декабрьские сигналы будут отдельной подборкой.',
         '',
         'Сигналы разложены по 20 трендам и четырём мирам Декодера: ЦС — мир автопилота, ЦЗ — мир правил, ДС — мир автономии, ДЗ — мир сообщества.',
         '',
         'Откуда сигналы:',
         '',
         '- **исследования и данные** — Stanford Digital Economy Lab, Art Basel и UBS, Gallup, Edelman, Reuters/Ipsos, Hugging Face, OpenAI и Upwork, ВОЗ и другие;',
         '- **доклады институтов будущего** — что за год добавили и что убрали CIFS, FTSG, IFTF, Dubai Future Foundation, RAND, McKinsey, Gartner, WEF, VML и обзор трендов kleinkleinklein; по сигналу на институт (материалы к лекции «Будущее поменяло хозяев», 11 ноября 2026);',
         '- **события и кейсы** — новости и решения компаний, правительств и сообществ, у каждого — ссылка на первоисточник;',
         f'- **III Международный симпозиум «Создавая будущее»** (Москва, 12–13 ноября 2026) — только проекты и исследования, которые сами по себе удивляют. Отдельная заметка по итогам симпозиума выйдет позже.',
         '',
         'Распределение сигналов по мирам — наше прочтение, его можно оспорить. Дата подборки — 20 ноября 2026 года.',
         '',
         f'Сигналы сгруппированы в 20 трендов — у каждого своя карточка в разделе [[{c["tr_url"]}/index|Тренды]]. Ссылка «Тренд подборки» в карточке сигнала ведёт туда.', '',
         '> Каждый сигнал — отдельная заметка. Ниже — каталог: ищите и фильтруйте по миру, сфере, теме и макротренду.',
         '']
    else:
        intro = [
         f'This collection holds {len(SIGS)} frontier signals from November 2026. Frontier means new (2025–2026), surprising and resting on a concrete fact with a primary source rather than a speaker’s opinion. We add no more than 50 signals a month: fewer, but ones that change the picture. December signals will be a separate collection.',
         '',
         'The signals are arranged by 20 trends and the four Decoder worlds: CS, the autopilot world; CE, the rules world; DS, the autonomy world; DE, the community world.',
         '',
         'Where the signals come from:',
         '',
         '- **research and data**: Stanford Digital Economy Lab, Art Basel and UBS, Gallup, Edelman, Reuters/Ipsos, Hugging Face, OpenAI and Upwork, WHO and others;',
         '- **futures institutes’ reports**: what CIFS, FTSG, IFTF, Dubai Future Foundation, RAND, McKinsey, Gartner, WEF, VML and the kleinkleinklein trend review added and dropped over the year, one signal per institute (material for the lecture “The Future Has Changed Hands”, 11 November 2026);',
         '- **events and cases**: news and decisions by companies, governments and communities, each linked to a primary source;',
         f'- **the III International Symposium “Creating the Future”** (Moscow, 12–13 November 2026): only projects and studies that surprise in their own right. A separate note on the symposium will follow.',
         '',
         'Assigning signals to worlds is our reading and can be challenged. Collection date: 20 November 2026.',
         '',
         f'The signals are grouped into 20 trends, each with its own card in [[{c["tr_url"]}/index|Trends]]. The “Collection trend” link on a signal card leads there.', '',
         '> Each signal is a separate note. Below is the catalog: search and filter by world, life domain, theme and macrotrend.',
         '']
    rows = []
    for k in sorted(D.TRENDS):
        if k not in by_trend:
            continue
        tr = D.TRENDS[k]
        cells = {}
        for x in by_trend.get(k, []):
            cells[x['sc']] = (cells[x['sc']] + '<br>' if x['sc'] in cells else '') + link_md(x, lang)
        rows.append(f"| <span id=\"{'тренд' if ru else 'trend'}-{k}\"></span>**[{tr[0] if ru else tr[1]}](/{c['tr_url']}/{tr_id(k).lower()})** | " + ' | '.join(cells.get(x, '') for x in ['ЦС', 'ЦЗ', 'ДС', 'ДЗ']) + ' |')
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
    tail = ['', ('Обзор на английском' if ru else 'This overview in Russian') + f': [[{other_hub}|{L['en' if ru else 'ru']['hubname']}]].', '',
            ('Все тренды — карточками: ' if ru else 'All trends as cards: ') + f"[[{c['tr_url']}/index|{'Тренды' if ru else 'Trends'}]].", '',
            '[Все сигналы](/materialy/signaly/)' if ru else '[All signals](/en/materials/signals/)', '']
    return '\n'.join(fm + intro)

TR = {
 'ru': dict(brief='Кратко', period='Период', mt='Макротренды-драйверы', sph='Сферы', tags='Тематические теги', descr='Описание',
            worlds='Как тренд проявляется в четырёх мирах', none='сигналов этого мира пока нет', links='Связи', other='Этот тренд на английском',
            coll='Подборка', back='Все тренды', t=('тип/тренд', 'сфера/', 'тема/', 'макротренд/mt-', 'подборка/сигналы-2026'),
            stage='Тренд подборки', period_v='ноябрь 2026', geo='мир', idx='Тренды'),
 'en': dict(brief='In brief', period='Period', mt='Macrotrend drivers', sph='Life domains', tags='Thematic tags', descr='Description',
            worlds='How the trend shows up in the four worlds', none='no signals from this world yet', links='Links', other='This trend in Russian',
            coll='Collection', back='All trends', t=('type/trend', 'domain/', 'theme/', 'macrotrend/mt-', 'collection/signals-2026'),
            stage='Collection trend', period_v='November 2026', geo='global', idx='Trends'),
}

def trend_card(k, lang):
    ru = lang == 'ru'; c = L[lang]; f = TR[lang]
    tr = D.TRENDS[k]; tid = tr_id(k); slug_ = tid.lower()
    name = tr[0] if ru else tr[1]; summ = tr[2] if ru else tr[3]; theme = tr[6] if ru else tr[7]; mts = tr[4]
    sph_names = tr[5] if ru else [SPH_RU[x][1] for x in tr[5]]
    sph_slugs = [SPH_RU[x][0] if ru else SPH_RU[x][2] for x in tr[5]]
    tags = [f['t'][0], f['t'][1] + (SPH_TAG[sph_slugs[0]] if ru else sph_slugs[0]), f['t'][2] + slug(theme), f"{f['t'][3]}{mts[0]:03d}", f['t'][4]]
    other = L['en' if ru else 'ru']['tr_url']
    fm = ['---', f'title: {yq(name)}', f'description: {yq(first_sentence(summ))}', f'lang: {lang}', 'translations:',
          f"  ru: /{L['ru']['tr_url']}/{slug_}", f"  en: /{L['en']['tr_url']}/{slug_}", 'aliases:', f'  - {tid}', 'tags:'] + [f'  - {x}' for x in tags] + [
          'signal_type: trend', f'signal_id: {tid}', 'year: 2026', f'added: {TODAY}', f'name: {yq(name)}', 'scenario: ""',
          f"period: {yq(f['period_v'])}", f"geography: {yq(f['geo'])}", f"stage: {yq(f['stage'])}",
          'life_domains:'] + [f'  - {yq(x)}' for x in sph_names] + ['industries: []', 'themes:', f'  - {yq(theme)}',
          'macrotrends:'] + [f'  - {yq(mt_label(i, lang))}' for i in mts] + [f'created: {TODAY}', f'updated: {TODAY}', '---', '']
    body = [f'*{tid} · {name}*', '', f"**{f['brief']}:** {first_sentence(summ)}", '',
            f"**{f['period']}:** {f['period_v']}.", '',
            f"**{f['mt']}:** " + '; '.join(mt_label(i, lang) for i in mts) + '.', '',
            f"**{f['sph']}:** " + '; '.join(f"[[{c['sph_base']}/{sl}|{nm}]]" for sl, nm in zip(sph_slugs, sph_names)) + '.  ',
            f"**{f['tags']}:** {theme}.", '',
            f"### {f['descr']}", '', summ, '',
            f"### {f['worlds']}", '']
    for sc in ['ЦС', 'ЦЗ', 'ДС', 'ДЗ']:
        wp, wn = WORLD[lang][sc]
        body += [f'**[[{wp}|{wn}]]**', '']
        sigs = [x for x in by_trend.get(k, []) if x['sc'] == sc]
        if not sigs:
            body += [f"- {f['none']}.", '']
            continue
        for x in sigs:
            body.append(f"- [[{c['url']}/{x['id'].lower()}|{x['t_ru'] if ru else x['t_en']}]]. {x['w_ru'] if ru else x['w_en']}")
        body.append('')
    body += [f"### {f['links']}", '', f"- [[{other}/{slug_}|{f['other']}]].",
             f"- {f['coll']}: [[{c['hub_url']}|{c['hubname']}]].", '', '---', '', f"{f['back']}: [[{c['tr_url']}/index|{f['idx']}]]", '']
    return '\n'.join(fm + body)

def trends_index(lang):
    ru = lang == 'ru'; c = L[lang]
    return '\n'.join(['---', f"title: {yq('Тренды' if ru else 'Trends')}",
        f"description: {yq('Тренды, которые мы выявили по фронтирным сигналам: каждый отдельной карточкой с сигналами из четырёх миров Декодера.' if ru else 'Trends we identified from frontier signals: each a separate card with signals from the four Decoder worlds.')}",
        f'lang: {lang}', 'translations:', f"  ru: /{L['ru']['tr_url']}/", f"  en: /{L['en']['tr_url']}/", 'tags:',
        f"  - {'тип/указатель' if ru else 'type/index'}", f'created: {TODAY}', f'updated: {TODAY}', '---', '',
        ('Каждый тренд — отдельная карточка: что происходит, на какие макротренды из свода 82 опирается и какими сигналами проявляется в каждом из четырёх миров. Ноябрь 2026 — 20 трендов из подборки ' if ru else
         'Each trend is a separate card: what is happening, which macrotrends from the set of 82 drive it and which signals show it in each of the four worlds. November 2026: 20 trends from the collection ')
        + f"[[{c['hub_url']}|{c['hubname']}]].", ''])

if __name__ == '__main__':
    for lang in ('ru', 'en'):
        c = L[lang]
        os.makedirs(os.path.join(REPO, c['dir']), exist_ok=True)
        for s in SIGS:
            open(os.path.join(REPO, c['dir'], s['id'].lower() + '.md'), 'w', encoding='utf-8').write(note(s, lang))
        os.makedirs(os.path.join(REPO, c['tr_dir']), exist_ok=True)
        for k in D.TRENDS:
            open(os.path.join(REPO, c['tr_dir'], tr_id(k).lower() + '.md'), 'w', encoding='utf-8').write(trend_card(k, lang))
        open(os.path.join(REPO, c['tr_dir'], 'index.md'), 'w', encoding='utf-8').write(trends_index(lang))
        open(os.path.join(REPO, c['hub']), 'w', encoding='utf-8').write(hub(lang))
        print(lang, len(SIGS))
