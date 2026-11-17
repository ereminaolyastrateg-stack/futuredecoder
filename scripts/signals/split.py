#!/usr/bin/env python3
"""Разбивает обзор сигналов на атомарные заметки (Цеттелькастен).

python3 scripts/signals/split.py
Источник:  content/materialy/signaly/education.md        (RU)
           content/en/materials/signals/education.md     (EN)
Результат: content/materialy/signaly/obrazovanie/sig-edu-NNN.md
           content/en/materials/signals/education-signals/sig-edu-NNN.md
           обзорные файлы переписываются в «карты» со ссылками на заметки.
Повторный запуск безопасен только на исходных (неразбитых) обзорах; оригиналы
сохраняются в scripts/signals/source/ при первом запуске и читаются оттуда.
"""
import os, re, shutil

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'source')

LANGS = {
    'ru': dict(hub='content/materialy/signaly/education.md', dir='content/materialy/signaly/obrazovanie',
               url='materialy/signaly/obrazovanie', hub_url='materialy/signaly/education',
               other='en/materials/signals/education-signals',
               L=dict(scen='Сценарий', sph='Сферы', ind='Отрасли', tags='Тематические теги', mt='Макротренды-драйверы',
                      brief='Кратко', geo='География', period='Дата / период', stage='Тип и стадия', other_lang='Этот сигнал на английском', other_label='Этот сигнал на английском',
                      back='Все сигналы обзора', hubname='Образование — сигналы и обсуждения игр',
                      t_type='тип', t_sig='сигнал', t_scen='сценарий', t_sph='сфера', t_ind='отрасль', t_theme='тема', t_mt='макротренд',
                      t_hub='обзор', topic='сфера/образование')),
    'en': dict(hub='content/en/materials/signals/education.md', dir='content/en/materials/signals/education-signals',
               url='en/materials/signals/education-signals', hub_url='en/materials/signals/education',
               other='materialy/signaly/obrazovanie',
               L=dict(scen='Scenario', sph='Life domains', ind='Industries', tags='Thematic tags', mt='Macrotrend drivers',
                      brief='In brief', geo='Geography', period='Date / period', stage='Type and stage', other_lang='This signal in Russian', other_label='This signal in Russian',
                      back='All signals in this overview', hubname='Education — signals and game discussions',
                      t_type='type', t_sig='signal', t_scen='scenario', t_sph='domain', t_ind='industry', t_theme='theme', t_mt='macrotrend',
                      t_hub='overview', topic='domain/education')),
}

def slugtag(s):
    s = s.strip().strip('.').strip().lower()
    s = re.sub(r'[«»“”"\'()\[\],:;!?]', '', s)
    s = re.sub(r'[\s_/]+', '-', s)
    s = re.sub(r'-+', '-', s).strip('-')
    return s

def yq(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'

def field(body, label):
    m = re.search(r'^\*\*' + re.escape(label) + r':\*\*\s*(.+?)\s*$', body, re.M)
    return m.group(1).strip() if m else ''

# заметки макротрендов: MT-id → базовый путь; к нему добавляется -cs/-ce/-ds/-de по сценарию сигнала
MT_NOTES = {'ru': {'MT-031': 'materialy/makrotrendy/masterstvo-cheloveka'}, 'en': {}}
SCEN_SLUG = {'ЦС': 'cs', 'ЦЗ': 'ce', 'ДС': 'ds', 'ДЗ': 'de', 'CS': 'cs', 'CE': 'ce', 'DS': 'ds', 'DE': 'de'}

def link_mt(m, lang, code):
    text, mid = m.group(1), m.group(1)[:6]
    base = MT_NOTES[lang].get(mid)
    if not base:
        return text
    sl = SCEN_SLUG.get(code)
    return f'[[{base}-{sl}|{text}]]' if sl else f'[[{base}|{text}]]'

def link_sig(m, url):
    text, sid = m.group(1), m.group(2).lower()
    return f'[[{url}/{sid}|{text}]]'

def process(lang):
    c = LANGS[lang]; L = c['L']
    hub_path = os.path.join(REPO, c['hub'])
    os.makedirs(SRC, exist_ok=True)
    src_copy = os.path.join(SRC, f'education.{lang}.md')
    if not os.path.exists(src_copy):
        shutil.copy(hub_path, src_copy)
    text = open(src_copy, encoding='utf-8').read()
    fm_end = text.index('\n---\n', 4) + 5
    fm, body = text[:fm_end], text[fm_end:]
    parts = re.split(r'^## (SIG-EDU-\d{3})\s*$', body, flags=re.M)
    head = parts[0]
    sigs = []
    tail = ''
    for i in range(1, len(parts), 2):
        sid, chunk = parts[i], parts[i + 1]
        # последний сигнал содержит хвост с «Макротренды в обзоре»
        m = re.search(r'^## ', chunk, re.M)
        if m:
            tail = chunk[m.start():]; chunk = chunk[:m.start()]
        sigs.append((sid, chunk.strip().rstrip('-').strip()))
    os.makedirs(os.path.join(REPO, c['dir']), exist_ok=True)
    titles = {}
    for sid, chunk in sigs:
        lines = chunk.split('\n')
        headline = re.sub(r'^\*\*(.+)\*\*$', r'\1', lines[0].strip())
        rest = '\n'.join(lines[1:]).strip()
        titles[sid] = headline
        name = headline.split(':')[0].strip()
        scen = field(rest, L['scen'])
        code = scen.split('—')[0].strip()
        sph = [x for x in re.split(r';', field(rest, L['sph'])) if x.strip()]
        ind = [x for x in re.split(r';', field(rest, L['ind'])) if x.strip()]
        themes = re.findall(r'`#([^`]+)`', field(rest, L['tags']))
        mts = re.findall(r'\[(MT-\d{3})[^\]]*\]', field(rest, L['mt']))
        # тегов немного (как в медиатеке); остальное — поля шапки для таблицы-каталога
        seen = [f"{L['t_type']}/{L['t_sig']}", f"{L['t_scen']}/{code}", L['topic']]
        seen += [f"{L['t_theme']}/{slugtag(x)}" for x in themes if f"{L['t_theme']}/{slugtag(x)}" not in seen]
        ym = re.search(r'(19|20)\d\d', field(rest, L['period']))
        mt_full = re.findall(r'\[(MT-\d{3}[^\]]*)\]', field(rest, L['mt']))
        clean = lambda x: x.strip().rstrip('.').strip()
        # тело: ссылки на соседние сигналы → вики-ссылки, теги → кликабельные, макротренды → текст до появления заметок
        b = rest
        b = re.sub(r'\[([^\]]+)\]\(#(sig-edu-\d{3})\)', lambda m: link_sig(m, c['url']), b)
        b = re.sub(r'\[([^\]]+)\]\((?:\.\./)+[^)]*?#(sig-edu-\d{3})\)', lambda m: f"[[{c['other']}/{m.group(2)}|{m.group(1)}]]", b)
        b = re.sub(r'\[(MT-\d{3}[^\]]*)\]\(#mt-\d{3}\)', lambda m: link_mt(m, lang, code), b)
        b = re.sub(r'^(\*\*' + re.escape(L['tags']) + r':\*\*).*$',
                   lambda m: m.group(1) + ' ' + ', '.join(x.strip().replace('-', ' ') for x in themes) + '.', b, flags=re.M)
        desc = field(rest, L['brief'])
        out = ['---', f'title: {yq(headline)}', f'description: {yq(desc)}', f'lang: {lang}',
               'translations:',
               f"  ru: /{LANGS['ru']['url']}/{sid.lower()}", f"  en: /{LANGS['en']['url']}/{sid.lower()}",
               'aliases:', f'  - {sid}', 'tags:'] + [f'  - {t}' for t in seen] + [
               'signal_type: signal', f'signal_id: {sid}', f"year: {ym.group(0) if ym else '\"\"'}", 'added: 2026-11-12', f'name: {yq(name)}', f'scenario: {code}',
               f"period: {yq(field(rest, L['period']).strip())}", f"geography: {yq(clean(field(rest, L['geo'])))}",
               f"stage: {yq(clean(field(rest, L['stage'])))}",
               'life_domains:'] + [f'  - {yq(clean(x))}' for x in sph] + ['industries:'] + [f'  - {yq(clean(x))}' for x in ind] + [
               'themes:'] + [f'  - {yq(clean(x).replace(chr(45), chr(32)))}' for x in themes] + ['macrotrends:'] + [f'  - {yq(clean(x))}' for x in mt_full] + [
               'created: 2026-11-12', 'updated: 2026-11-16', '---', '',
               f'*{sid} · {name}*', '', b, '', '---', '',
               f"{L['back']}: [[{c['hub_url']}|{L['hubname']}]]", '']
        open(os.path.join(REPO, c['dir'], sid.lower() + '.md'), 'w', encoding='utf-8').write('\n'.join(out))
    # карта (бывший обзор)
    hub_head = re.sub(r'\[([^\]]+)\]\(#(sig-edu-\d{3})\)', lambda m: link_sig(m, c['url']), head)
    hub_head = re.sub(r'\[([^\]]+)\]\(#(macro[^)]*|макро[^)]*)\)', r'[\1](#\2)', hub_head)
    hub_tail = re.sub(r'\[([^\]]+)\]\(#(sig-edu-\d{3})\)', lambda m: link_sig(m, c['url']), tail)
    fm2 = re.sub(r'tags:\n(  - .*\n)+', 'tags:\n' + f"  - {L['t_type']}/{L['t_hub']}\n  - {L['topic']}\n", fm)
    fm2 = fm2.replace('updated: 2026-11-13', 'updated: 2026-11-16')
    note = ({'ru': '> Каждый сигнал — отдельная заметка со своими тегами и обратными ссылками: [[materialy/signaly/obrazovanie/index|все сигналы по образованию]]. Теги сценариев: #сценарий/ЦС #сценарий/ЦЗ #сценарий/ДС #сценарий/ДЗ',
             'en': '> Each signal is a separate note with its own tags and backlinks: [[en/materials/signals/education-signals/index|all education signals]]. Scenario tags: #scenario/CS #scenario/CE #scenario/DS #scenario/DE'})[lang]
    # обзор = вводный текст; списки по мирам и макротрендам заменяет таблица-каталог (SignalCatalog)
    intro = hub_head.split('\n## ')[0].rstrip().rstrip('-').rstrip()
    note = ({'ru': '> Каждый сигнал — отдельная заметка. Ниже — каталог: ищите и фильтруйте по миру, сфере, отрасли, теме и макротренду.',
             'en': '> Each signal is a separate note. Below is the catalog: search and filter by world, life domain, industry, theme and macrotrend.'})[lang]
    open(hub_path, 'w', encoding='utf-8').write(fm2 + intro + '\n\n' + note + '\n')
    return len(sigs)

if __name__ == '__main__':
    for lang in ('ru', 'en'):
        print(lang, process(lang))
