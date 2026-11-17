#!/usr/bin/env python3
"""Собирает раздел «Сферы жизни» (8 сфер × 4 мира) на русском и английском.

python3 scripts/spheres/build.py
Источник:  scripts/spheres/source_ru.json — выгрузка листов «Тест · 132» и «Справочник v7»
           из Future_Decoder_v12_132 (ситуация, плюсы, цена, ресурсы, подтверждённые примеры);
           scripts/spheres/tr_en.json — английский перевод тех же полей (по id карточки).
Результат: content/chetyre-mira/sfery/…  и  content/en/four-worlds/life-spheres/…
Примеры без источника (статус «кандидат») не публикуются.
"""
import json, os, re
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '../..'))
SRC = json.load(open(os.path.join(HERE, 'source_ru.json'), encoding='utf-8'))
TR_PATH = os.path.join(HERE, 'tr_en.json')
TR = json.load(open(TR_PATH, encoding='utf-8')) if os.path.exists(TR_PATH) else None
DATE = '2026-11-17'

SPHERES = OrderedDict([
    ('Здоровье', ('zdorovye', 'здоровье', 'health', 'Health')),
    ('Финансы', ('finansy', 'финансы', 'finance', 'Finance')),
    ('Работа', ('rabota', 'работа', 'work', 'Work')),
    ('Образование', ('obrazovanie', 'образование', 'education', 'Education')),
    ('Близкие отношения и семья', ('semya', 'семья', 'family', 'Close relationships and family')),
    ('Место жизни и общественная среда', ('sreda', 'среда', 'place', 'Place of living and public environment')),
    ('Быт, потребление и отдых', ('byt', 'быт', 'everyday-life', 'Everyday life, consumption and leisure')),
    ('Ценности, смысл и сообщество', ('smysl', 'смысл', 'meaning', 'Values, meaning and community')),
])
SC = ['ЦС', 'ЦЗ', 'ДС', 'ДЗ']
SC_EN = {'ЦС': 'CS', 'ЦЗ': 'CE', 'ДС': 'DS', 'ДЗ': 'DE'}
SC_SLUG = {'ЦС': 'cs', 'ЦЗ': 'ce', 'ДС': 'ds', 'ДЗ': 'de'}
WORLD = {
    'ru': {'ЦС': ('chetyre-mira/centr-sintetika', 'Центр — Синтетика', 'порядок через систему, стандарт и воспроизводимость'),
           'ЦЗ': ('chetyre-mira/centr-zemlya', 'Центр — Земля', 'порядок через общий смысл, авторитет и живое мастерство'),
           'ДС': ('chetyre-mira/decentr-sintetika', 'Децентр — Синтетика', 'самостоятельность через свой инструмент, способ и воспроизводимость'),
           'ДЗ': ('chetyre-mira/decentr-zemlya', 'Децентр — Земля', 'порядок и знание возникают в участии, взаимодействии и пересмотре опыта')},
    'en': {'ЦС': ('en/four-worlds/centralized-synthetic', 'Centralized — Synthetic', 'order through system, standard and reproducibility'),
           'ЦЗ': ('en/four-worlds/centralized-earth', 'Centralized — Earth', 'order through shared meaning, authority and living mastery'),
           'ДС': ('en/four-worlds/decentralized-synthetic', 'Decentralized — Synthetic', 'independence through one’s own tool, method and reproducibility'),
           'ДЗ': ('en/four-worlds/decentralized-earth', 'Decentralized — Earth', 'order and knowledge emerging through participation, interaction and revisiting experience')},
}
RES_EN = {'Энергия и здоровье': 'Energy and health', 'Интеллект': 'Intellect', 'Самореализация': 'Self-realisation',
          'Влияние и масштаб': 'Influence and scale', 'Капитал': 'Capital', 'Душа': 'Soul', 'Время': 'Time',
          'Свобода выбора': 'Freedom of choice', 'Деньги': 'Money'}
EXTRA = {  # связи сфер с макротрендами и сигналами
    'Образование': {'ru': ['[[materialy/makrotrendy/obrazovanie-znanie-gramotnost|Макротренд «Образование, знание и грамотность»]] — как четыре мира отвечают на вопрос, кто ведёт учебный путь и кто признаёт результат.',
                           '[[materialy/signaly/education|Каталог сигналов об образовании]] — 40 сигналов с фильтром по миру.'],
                    'en': ['[[en/materials/macrotrends/education-knowledge-literacy|Macrotrend "Education, Knowledge and Literacy"]] — how the four worlds answer who leads the learning path and who recognises the result.',
                           '[[en/materials/signals/education|Education signals catalog]] — 40 signals with a filter by world.']},
    'Работа': {'ru': ['[[materialy/makrotrendy/masterstvo-cheloveka|Макротренд «Мастерство человека»]] — что значит быть мастером рядом с ИИ в четырёх мирах.'],
               'en': ['[[en/materials/macrotrends/human-mastery|Macrotrend "Human Mastery"]] — what it means to be a master next to AI in four worlds.']},
}

L = {
    'ru': dict(base='chetyre-mira/sfery', idx_title='Сферы жизни', in_world='в мире', gives='Что даёт.', costs='Чем платишь.',
               spend='Тратит', give='Даёт', where='Где это уже есть', src='источник', other_worlds='Эта сфера в других мирах',
               other_spheres='Мир {sc} в других сферах', sub='Подсфера', sphere_tag='сфера', type_card='тип/сфера-в-мире',
               type_hub='тип/сфера', type_idx='тип/указатель', sc_tag='сценарий', q='Вопросы подсфер', boundary='Граница',
               links='Связи', kind={'known': 'Известная практика', 'current': 'Сейчас', 'experiment': 'Эксперимент'}),
    'en': dict(base='en/four-worlds/life-spheres', idx_title='Life Spheres', in_world='in the', gives='What it gives.', costs='What it costs.',
               spend='Spends', give='Gives', where='Where this already exists', src='source', other_worlds='This sphere in other worlds',
               other_spheres='The {sc} world in other spheres', sub='Subsphere', sphere_tag='domain', type_card='type/sphere-in-world',
               type_hub='type/sphere', type_idx='type/index', sc_tag='scenario', q='Subsphere questions', boundary='Boundary',
               links='Connections', kind={'known': 'Known practice', 'current': 'Today', 'experiment': 'Experiment'}),
}

def slug_heading(s):
    s = s.lower()
    s = re.sub(r'[^\w\s-]', '', s, flags=re.U)
    return re.sub(r'\s+', '-', s.strip())

def yq(s):
    return '"' + str(s).replace('\\', '\\\\').replace('"', '\\"') + '"'

def clip(s, n=158):
    s = re.sub(r'\s+', ' ', s).strip()
    return s if len(s) <= n else s[:n].rsplit(' ', 1)[0].rstrip(',;:') + '…'

def tr(lang, card, field):
    if lang == 'ru':
        return card[field]
    return TR['cards'][card['id']][field]

def sphere_name(lang, ru):
    return ru if lang == 'ru' else SPHERES[ru][3]

def sub_name(lang, ru):
    return ru if lang == 'ru' else TR['subs'][ru]['name']

def res(lang, s):
    items = [x.strip() for x in (s or '').split(';') if x.strip()]
    return ', '.join(items if lang == 'ru' else [RES_EN.get(x, x) for x in items])

def path_hub(lang, sp):
    return f"{L[lang]['base']}/{SPHERES[sp][0] if lang == 'ru' else SPHERES[sp][2]}"

def path_card(lang, sp, sc):
    return f"{path_hub(lang, sp)}-{SC_SLUG[sc]}"

def code(lang, sc):
    return sc if lang == 'ru' else SC_EN[sc]

def tag_sphere(lang, sp):
    return f"{L[lang]['sphere_tag']}/{SPHERES[sp][1] if lang == 'ru' else SPHERES[sp][2]}"

def write(lang, rel, text):
    p = os.path.join(REPO, 'content', rel + '.md')
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(text)

def by_sphere():
    d = OrderedDict((sp, OrderedDict()) for sp in SPHERES)
    for c in SRC:
        d[c['sphere']].setdefault(c['sub'], {})[c['sc']] = c
    return d

def build(lang):
    l = L[lang]; data = by_sphere(); other = 'en' if lang == 'ru' else 'ru'
    has_other = TR is not None
    def trans(rel_self, rel_other):
        if not has_other:
            return ''
        ru, en = (rel_self, rel_other) if lang == 'ru' else (rel_other, rel_self)
        return f'translations:\n  ru: /{ru}\n  en: /{en}\n'
    # карточки сфера × мир
    for sp, subs in data.items():
        spn = sphere_name(lang, sp)
        for sc in SC:
            wpath, wname, wline = WORLD[lang][sc]
            cards = [subs[s][sc] for s in subs]
            if lang == 'ru':
                title = f'{spn} в мире {sc}'
                seo = f'{spn} в сценарии {sc} ({wname})'
                lead = f"*Сфера [[{path_hub(lang, sp)}|«{spn}»]] в мире [[{wpath}|{wname}]]: {wline}. Ниже — как эта логика выглядит в каждой подсфере: ситуация из жизни, что она даёт, чем за неё платишь и где это уже есть.*"
                desc = clip(f'{spn} в мире {sc}: ' + '; '.join(tr(lang, c, 'name').lower() if i else tr(lang, c, 'name') for i, c in enumerate(cards)) + '.')
            else:
                title = f'{spn} in the {SC_EN[sc]} world'
                seo = f'{spn} in the {SC_EN[sc]} scenario ({wname})'
                lead = f"*The [[{path_hub(lang, sp)}|{spn}]] sphere in the [[{wpath}|{wname}]] world: {wline}. Below is how this logic looks in each subsphere: a life situation, what it gives, what it costs and where it already exists.*"
                desc = clip(f'{spn} in the {SC_EN[sc]} world: ' + '; '.join(tr(lang, c, 'name').lower() if i else tr(lang, c, 'name') for i, c in enumerate(cards)) + '.')
            out = ['---', f'title: {yq(title)}', f'seoTitle: {yq(seo)}', f'description: {yq(desc)}', f'lang: {lang}',
                   trans(path_card(lang, sp, sc), path_card(other, sp, sc)).rstrip('\n'),
                   f'scenario: {code(lang, sc)}', 'tags:', f"  - {l['type_card']}", f'  - {tag_sphere(lang, sp)}',
                   f"  - {l['sc_tag']}/{code(lang, sc)}", 'aliases:', f'  - {yq(sp + "_" + sc) if lang == "ru" else yq(SPHERES[sp][2] + "-" + SC_EN[sc])}',
                   f'sphere: {yq(spn)}', f'sphere_order: {list(SPHERES).index(sp) + 1}',
                   'items: ' + json.dumps([dict(sub=sub_name(lang, c['sub']), anchor=slug_heading(sub_name(lang, c['sub'])),
                                               name=tr(lang, c, 'name'), situation=tr(lang, c, 'situation'),
                                               spend=[x for x in res(lang, c['spend']).split(', ') if x],
                                               give=[x for x in res(lang, c['give']).split(', ') if x]) for c in cards],
                                         ensure_ascii=False),
                   f'date: {DATE}', f'updated: {DATE}', '---']
            out = [x for x in out if x != ''] + ['', lead, '']
            for c in cards:
                out += [f"## {sub_name(lang, c['sub'])}", '', f"**{tr(lang, c, 'name')}**", '', f"> {tr(lang, c, 'situation')}", '',
                        f"**{l['gives']}** {tr(lang, c, 'plus')}", '', f"**{l['costs']}** {tr(lang, c, 'minus')}", '',
                        f"*{l['spend']}: {res(lang, c['spend'])} · {l['give']}: {res(lang, c['give'])}.*", '']
                pr = c['practices'] if lang == 'ru' else TR['cards'][c['id']]['practices']
                if pr:
                    out += [f"**{l['where']}:**", '']
                    for p0, p in zip(c['practices'], pr):
                        txt = p if isinstance(p, str) else p['text']
                        out.append(f"- {l['kind'][p0['kind']]}: {txt.rstrip('.')}. [{l['src']}]({p0['src']})")
                    out.append('')
                out.append(f"<!-- {c['id']} · Тест · 132 / Справочник v7 -->")
                out.append('')
            out += [f"## {l['other_worlds']}", '']
            out += [f"- [[{path_card(lang, sp, s2)}|{title.replace(code(lang, sc), code(lang, s2))}]]" for s2 in SC if s2 != sc]
            out += ['', f"## {l['other_spheres'].format(sc=code(lang, sc))}", '']
            out += [f"- [[{path_card(lang, sp2, sc)}|{sphere_name(lang, sp2)}]]" for sp2 in SPHERES if sp2 != sp]
            out.append('')
            write(lang, path_card(lang, sp, sc), '\n'.join(out))
        # заметка сферы
        rows = []
        for s, d4 in subs.items():
            cells = [f"[[{path_card(lang, sp, sc)}#{slug_heading(sub_name(lang, s))}\\|{tr(lang, d4[sc], 'name')}]]" for sc in SC]
            rows.append(f"| {sub_name(lang, s)} | " + ' | '.join(cells) + ' |')
        any_c = next(iter(subs.values()))
        if lang == 'ru':
            lead = f"*«{spn}» — одна из восьми сфер жизни, через которые метод Декодер Будущего смотрит на человека. В сфере {len(subs)} подсферы; каждая выглядит по-разному в четырёх мирах. Ниже — все варианты в таблице с фильтрами и ссылки на четыре карточки.*"
            seo = f'{spn}: сфера жизни в четырёх сценариях будущего'
            desc = clip(f'{spn} в четырёх мирах Декодера Будущего: ' + ', '.join(s.lower() for s in subs) + '. Ситуации, плюсы, цена и примеры.')
        else:
            lead = f"*{spn} is one of the eight life spheres through which the Future Decoder method looks at a person. The sphere has {len(subs)} subspheres; each looks different in the four worlds. Below are all the options in a filterable table and links to the four cards.*"
            seo = f'{spn}: a life sphere in four future scenarios'
            desc = clip(f'{spn} in the four Future Decoder worlds: ' + ', '.join(sub_name(lang, s).lower() for s in subs) + '. Situations, benefits, costs and examples.')
        hub = ['---', f'title: {yq(spn)}', f'seoTitle: {yq(seo)}', f'description: {yq(desc)}', f'lang: {lang}']
        t_ = trans(path_hub(lang, sp), path_hub(other, sp))
        if t_: hub.append(t_.rstrip('\n'))
        hub += ['tags:', f"  - {l['type_hub']}", f'  - {tag_sphere(lang, sp)}', f'date: {DATE}', f'updated: {DATE}', '---', '', lead, '',
                ' · '.join(f"[[{path_card(lang, sp, sc)}|{spn} {'в мире' if lang == 'ru' else 'in'} {code(lang, sc)}]]" for sc in SC), '',
                f"## {l['q']}", '']
        for s in subs:
            q = any_c and (subs[s]['ЦС']['question'] if lang == 'ru' else TR['subs'][s]['question'])
            b = subs[s]['ЦС']['boundary'] if lang == 'ru' else TR['subs'][s]['boundary']
            q = q.replace('\nДополнение v7: ', ' '); b = b.replace('\nДополнение v7: ', ' ')
            hub += [f"**{sub_name(lang, s)}.** {q}", '', f"*{l['boundary']}: {b}*", '']
        ex = EXTRA.get(sp, {}).get(lang, [])
        hub += [f"## {l['links']}", ''] + [f'- {x}' for x in ex] + [f"- [[{L[lang]['base']}/index|{l['idx_title']}]]", '']
        write(lang, path_hub(lang, sp), '\n'.join(hub))
    # указатель
    if lang == 'ru':
        head = ('Сферы жизни', 'Сферы жизни в четырёх мирах Декодера Будущего',
                'Восемь сфер жизни — здоровье, финансы, работа, образование, семья, среда, быт, смысл — в четырёх сценариях будущего: 33 подсферы, 132 карточки.',
                '*Метод Декодер Будущего смотрит на жизнь человека через восемь сфер и 33 подсферы. Каждая из них по-разному устроена в четырёх мирах, поэтому всего 132 карточки. Каждая клетка таблицы ведёт к карточке: ситуации из жизни, что даёт этот путь, чем за него платишь и где он уже встречается.*',
                'Сфера')
    else:
        head = ('Life Spheres', 'Life spheres in the four Future Decoder worlds',
                'Eight life spheres — health, finance, work, education, family, place, everyday life, meaning — in four future scenarios: 33 subspheres, 132 cards.',
                '*The Future Decoder method looks at a person’s life through eight spheres and 33 subspheres. Each is organised differently in the four worlds, so there are 132 cards in total. Every cell of the table leads to a card: life situations, what this path gives, what it costs and where it already exists.*',
                'Sphere')
    idx = ['---', f'title: {head[0]}', f'seoTitle: {yq(head[1])}', f'description: {yq(head[2])}', f'lang: {lang}']
    t_ = trans(f"{L[lang]['base']}/", f"{L[other]['base']}/")
    if t_: idx.append(t_.rstrip('\n'))
    idx += ['tags:', f"  - {l['type_idx']}", f'date: {DATE}', f'updated: {DATE}', '---', '', head[3], '',
            f"| {head[4]} | " + ' | '.join(f"[[{WORLD[lang][sc][0]}\\|{code(lang, sc)}]]" for sc in SC) + ' |', '|---|---|---|---|---|']
    for sp in SPHERES:
        idx.append(f"| [[{path_hub(lang, sp)}\\|{sphere_name(lang, sp)}]] | " + ' | '.join(f"[[{path_card(lang, sp, sc)}\\|{code(lang, sc)}]]" for sc in SC) + ' |')
    idx.append('')
    write(lang, f"{L[lang]['base']}/index", '\n'.join(idx))

if __name__ == '__main__':
    build('ru')
    if TR:
        build('en')
    print('ok', 'en' if TR else 'ru only')
