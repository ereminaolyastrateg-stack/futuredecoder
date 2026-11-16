"""Генератор «Полотна будущего» для цифрового сада.

Берёт базу (data.json, русский) и переводы (tr.json: русская строка -> английская),
и пишет в репозиторий сада:
  quartz/static/polotno/data.json        — база для интерактивной страницы (RU + EN поля)
  quartz/static/polotno/index.html       — интерактивная страница (мета-теги и noscript обновляются)
  content/polotno/*.md                   — по странице на вопрос (RU), видны поисковикам и ИИ
  content/en/future-canvas/*.md          — то же на английском (если есть перевод)
  content/llms.txt                       — краткое описание базы для ИИ-ассистентов
"""
import json, os, re, sys, html

REPO = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/futuredecoder'
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://futuredecoder.org'
TODAY = '2026-11-16'
ORDER = ['ЦС', 'ЦЗ', 'ДС', 'ДЗ']
NAMES = {
    'ru': {'ЦС': 'Мир автопилота', 'ЦЗ': 'Мир правил', 'ДС': 'Мир автономии', 'ДЗ': 'Мир сообщества'},
    'en': {'ЦС': 'Autopilot world', 'ЦЗ': 'Rules world', 'ДС': 'Autonomy world', 'ДЗ': 'Community world'},
}
CODES_EN = {'ЦС': 'CS', 'ЦЗ': 'CE', 'ДС': 'DS', 'ДЗ': 'DE'}
HINTS = {
    'ru': {'ЦС': 'решает система, результат не твой', 'ЦЗ': 'участвуешь по общим правилам',
           'ДС': 'сам решаешь, сам владеешь', 'ДЗ': 'создаёшь вместе с другими'},
    'en': {'ЦС': 'the system decides, the result is not yours', 'ЦЗ': 'you take part by shared rules',
           'ДС': 'you decide and you own it', 'ДЗ': 'you create together with others'},
}

data = json.load(open(os.path.join(REPO, 'quartz/static/polotno/data.json')))
# data.json in the repo may already carry *_en fields from an earlier run; the RU source of truth is the plain fields
trp = os.path.join(HERE, 'tr.json')
TR = json.load(open(trp)) if os.path.exists(trp) else {}


def tr(s):
    if not s:
        return s
    return TR.get(s.strip(), '')


def hid(s):
    h = 5381
    for ch in s:
        h = ((h << 5) + h + ord(ch)) & 0xFFFFFFFF
    out, n, dig = '', h, '0123456789abcdefghijklmnopqrstuvwxyz'
    if n == 0:
        return '0'
    while n:
        out = dig[n % 36] + out
        n //= 36
    return out


TL = dict(zip('абвгдеёжзийклмнопрстуфхцчшщъыьэюя',
              ['a', 'b', 'v', 'g', 'd', 'e', 'e', 'zh', 'z', 'i', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'f', 'kh', 'ts', 'ch', 'sh', 'shch', '', 'y', '', 'e', 'yu', 'ya']))


def slugify(s, latin=False):
    s = s.lower()
    if not latin:
        s = ''.join(TL.get(c, c) for c in s)
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    words = s.split('-')
    out = ''
    for w in words:
        if len(out) + len(w) + 1 > 60:
            break
        out = (out + '-' + w) if out else w
    return out or 'q'


def pl(n, forms):
    n10, n100 = n % 10, n % 100
    f = forms[0] if n10 == 1 and n100 != 11 else forms[1] if 2 <= n10 <= 4 and not 12 <= n100 <= 14 else forms[2]
    return f'{n} {f}'


def yq(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


# ---- ids, slugs, EN fields ----
used_ru, used_en = set(), set()
has_en = bool(TR)
for q in data['q']:
    q['id'] = hid(q['q'])
    s = slugify(q['ask'])
    while s in used_ru:
        s += '-2'
    used_ru.add(s); q['slug'] = s
    if has_en:
        q['q_en'], q['ask_en'], q['src_en'], q['sphere_en'] = tr(q['q']), tr(q['ask']), tr(q['src']), tr(q['sphere'])
        for w in q['w'].values():
            for k in ['one', 'dev', 'price', 'step', 'sig', 'quote']:
                w[k + '_en'] = tr(w.get(k, ''))
        se = slugify(q['ask_en'] or q['ask'], latin=True)
        while se in used_en:
            se += '-2'
        used_en.add(se); q['slug_en'] = se
if has_en:
    for s in data['s']:
        for k in ['t', 'where', 'src', 'type']:
            s[k + '_en'] = tr(s.get(k, ''))
    for m in data['m']:
        for k in ['title', 'looks', 'exp', 'par', 'src']:
            m[k + '_en'] = tr(m.get(k, ''))

missing = []
if has_en:
    def chk(v):
        if v and not tr(v):
            missing.append(v)
    for q in data['q']:
        for v in [q['q'], q['ask'], q['src'], q['sphere']]:
            chk(v)
        for w in q['w'].values():
            for k in ['one', 'dev', 'price', 'step', 'sig', 'quote']:
                chk(w.get(k, ''))
    for s in data['s']:
        for k in ['t', 'where', 'src', 'type']:
            chk(s.get(k, ''))
    for m in data['m']:
        for k in ['title', 'looks', 'exp', 'par', 'src']:
            chk(m.get(k, ''))
    print('missing translations:', len(missing))

data['updated'] = TODAY
json.dump(data, open(os.path.join(REPO, 'quartz/static/polotno/data.json'), 'w'), ensure_ascii=False, separators=(',', ':'))


# ---- markdown pages ----
def mixes_for(q):
    return [m for m in data['m'] if m['src'] == q['src']][:3]


def page(q, lang):
    en = lang == 'en'
    g = (lambda o, k: o.get(k + '_en') or '') if en else (lambda o, k: o.get(k) or '')
    ask, qq, src = g(q, 'ask'), g(q, 'q'), g(q, 'src')
    app = f"/static/polotno/{'en/' if en else ''}#q-{q['id']}"
    duel = f"/static/polotno/{'en/' if en else ''}#new-{q['id']}"
    if en:
        title = ask
        desc = f"Four answers to “{ask}” designed by participants of the Future Decoder scenario games: signals, the price of each world and a step for this week."
        intro = (f"**{qq}** Four answers from four worlds of the Future Decoder method. "
                 f"They come from participants of the scenario games, not from experts.")
    else:
        title = ask
        desc = f"Четыре ответа на вопрос «{ask}» от участников игр «Декодер Будущего»: сигналы, цена каждого мира и шаг на неделю."
        intro = (f"**{qq}** Четыре ответа из четырёх миров метода «Декодер Будущего». "
                 f"Их придумали участники сценарных игр, а не эксперты.")
    fm = ['---', f'title: {yq(title)}',
          f"seoTitle: {yq(title + (' — Future Canvas' if en else ' — Полотно будущего'))}",
          f'description: {yq(desc)}', f'lang: {lang}', 'translations:',
          f"  ru: /polotno/{q['slug']}"]
    if has_en:
        fm.append(f"  en: /en/future-canvas/{q['slug_en']}")
    fm += ['tags:', '  - polotno' if not en else '  - future-canvas', f'created: {TODAY}', f'updated: {TODAY}', '---', '']
    body = [intro, '']
    body.append(f"[{'Open in the interactive canvas' if en else 'Открыть в интерактивном полотне'}]({app}) · "
                f"[{'Challenge a friend to a duel of worlds' if en else 'Вызвать друга на дуэль миров'}]({duel})")
    body.append('')
    L = 'en' if en else 'ru'
    for c in ORDER:
        w = q['w'].get(c)
        code = CODES_EN[c] if en else c
        body.append(f"## {NAMES[L][c]} ({code})")
        body.append('')
        if not w:
            body.append('Nobody has designed this world for this question yet.' if en else 'Этот мир по вопросу ещё никто не спроектировал.')
            body.append('')
            continue
        body.append(f"*{HINTS[L][c]}*")
        body.append('')
        body.append(f"**{g(w, 'one')}**")
        body.append('')
        rows = [('How it develops' if en else 'Как развивается', g(w, 'dev')),
                ('The price' if en else 'Цена', g(w, 'price')),
                ('Signal' if en else 'Сигнал', g(w, 'sig'))]
        for h, v in rows:
            if v:
                body.append(f"- **{h}:** {v}")
        if g(w, 'quote'):
            body.append(f"- **{'Heard at the game' if en else 'Прозвучало на игре'}:** {g(w, 'quote')}")
        if g(w, 'step'):
            body.append(f"- **{'Step for this week' if en else 'Шаг на неделю'}:** {g(w, 'step')}")
        body.append('')
    mx = mixes_for(q)
    if mx:
        body.append('## ' + ('Mixes and paradoxes from this game' if en else 'Смеси и парадоксы с этой игры'))
        body.append('')
        for m in mx:
            body.append(f"**{g(m, 'title')}** ({m['L']}). {g(m, 'looks')}")
            body.append('')
            body.append(f"- **{'Paradox' if en else 'Парадокс'}:** {g(m, 'par')}")
            body.append(f"- **{'Experiment for a week' if en else 'Эксперимент на неделю'}:** {g(m, 'exp')}")
            body.append('')
    body.append('---')
    body.append('')
    body.append((f"Source: {src}. Draft of the Future Decoder knowledge base, updated after every game. "
                 f"[All questions](/en/future-canvas/)") if en else
                (f"Источник: {src}. Черновик базы знаний Декодера, дополняется после каждой игры. "
                 f"[Все вопросы](/polotno/)"))
    return '\n'.join(fm + body) + '\n'


def index_page(lang):
    en = lang == 'en'
    g = (lambda o, k: o.get(k + '_en') or '') if en else (lambda o, k: o.get(k) or '')
    spheres = []
    for q in data['q']:
        if g(q, 'sphere') not in spheres:
            spheres.append(g(q, 'sphere'))
    if en:
        fm = ['---', 'title: "Future Canvas"', 'seoTitle: "Future Canvas — Future Decoder knowledge base"',
              'description: "Questions about the future and four answers to each, designed by participants of Future Decoder scenario games: signals, prices and weekly steps."',
              'lang: en', 'translations:', '  ru: /polotno/', '  en: /en/future-canvas/', f'created: {TODAY}', f'updated: {TODAY}', '---', '']
        intro = [f"Questions people ask about the future, and four answers to each. The answers were designed by participants of Future Decoder scenario games: {len(data['q'])} questions and {len(data['s'])} signals so far, updated after every game.", '',
                 'Each answer belongs to one of four worlds of the Decoder method:', '']
        intro += [f"- **{NAMES['en'][c]} ({CODES_EN[c]})**: {HINTS['en'][c]}" for c in ORDER]
        intro += ['', '[Open the interactive canvas](/static/polotno/en/): duels of worlds, dilemmas and a daily signal.', '']
    else:
        fm = ['---', 'title: "Полотно будущего"', 'seoTitle: "Полотно будущего — база знаний Декодера"',
              'description: "Вопросы о будущем и четыре ответа на каждый от участников игр «Декодер Будущего»: сигналы, цена каждого мира и шаг на неделю."',
              'lang: ru', 'translations:', '  ru: /polotno/'] + (['  en: /en/future-canvas/'] if has_en else []) + [f'created: {TODAY}', f'updated: {TODAY}', '---', '']
        intro = [f"Вопросы, которые люди задают о будущем, и четыре ответа на каждый. Их спроектировали участники игр «Декодер Будущего»: сейчас здесь {pl(len(data['q']), ('вопрос','вопроса','вопросов'))} и {pl(len(data['s']), ('сигнал','сигнала','сигналов'))}, база дополняется после каждой игры.", '',
                 'Каждый ответ относится к одному из четырёх миров метода Декодера:', '']
        intro += [f"- **{NAMES['ru'][c]} ({c})**: {HINTS['ru'][c]}" for c in ORDER]
        intro += ['', '[Открыть интерактивное полотно](/static/polotno/): дуэль миров, дилеммы и сигнал дня.', '']
    body = []
    for sp in spheres:
        body.append(f'## {sp}')
        body.append('')
        for q in data['q']:
            if g(q, 'sphere') == sp:
                link = f"/en/future-canvas/{q['slug_en']}" if en else f"/polotno/{q['slug']}"
                body.append(f"- [{g(q, 'ask')}]({link})")
        body.append('')
    return '\n'.join(fm + intro + body) + '\n'


def write_dir(d, pages):
    os.makedirs(d, exist_ok=True)
    for f in os.listdir(d):
        if f.endswith('.md'):
            os.remove(os.path.join(d, f))
    for name, text in pages.items():
        open(os.path.join(d, name), 'w').write(text)


write_dir(os.path.join(REPO, 'content/polotno'),
          {'index.md': index_page('ru'), **{q['slug'] + '.md': page(q, 'ru') for q in data['q']}})
if has_en:
    write_dir(os.path.join(REPO, 'content/en/future-canvas'),
              {'index.md': index_page('en'), **{q['slug_en'] + '.md': page(q, 'en') for q in data['q']}})

# ---- llms.txt ----
llms = [
    '# Декодер Будущего / Future Decoder',
    '',
    '> Цифровой сад Ольги Ереминой о сценариях будущего. Метод «Декодер Будущего» раскладывает любой вопрос о будущем на четыре мира: '
    'автопилот (ЦС, решает система), правила (ЦЗ, участие по общим правилам), автономия (ДС, сам решаешь и владеешь), сообщество (ДЗ, создаёшь вместе с другими).',
    '',
    '## Полотно будущего (база знаний)',
    '',
    f'- [Все вопросы, RU]({SITE}/polotno/): {len(data["q"])} вопросов о будущем, на каждый до четырёх ответов из игр, с сигналами, ценой и шагом на неделю.',
]
if has_en:
    llms.append(f'- [All questions, EN]({SITE}/en/future-canvas/): the same knowledge base in English.')
llms += [f'- [Интерактивное полотно]({SITE}/static/polotno/): дуэль миров, дилеммы, сигнал дня.', '', '## Вопросы', '']
for q in data['q']:
    llms.append(f"- [{q['ask']}]({SITE}/polotno/{q['slug']})" + (f" / [{q['ask_en']}]({SITE}/en/future-canvas/{q['slug_en']})" if has_en else ''))
llms += ['', '## Сайты', '', '- [futuredecoder.ru](https://futuredecoder.ru): игры и форматы «Декодер Будущего»', '']
open(os.path.join(REPO, 'content/llms.txt'), 'w').write('\n'.join(llms))

# ---- app head + noscript ----
ip = os.path.join(REPO, 'quartz/static/polotno/index.html')
t = open(ip).read()
head = f'''<!--seo-->
<meta name="description" content="Вопросы о будущем и четыре ответа на каждый от участников игр «Декодер Будущего»: дуэль миров, дилеммы и сигнал дня.">
<link rel="canonical" href="{SITE}/static/polotno/">
<link rel="alternate" hreflang="ru" href="{SITE}/static/polotno/">
<link rel="alternate" hreflang="en" href="{SITE}/static/polotno/en/">
<meta property="og:type" content="website">
<meta property="og:title" content="Полотно будущего — Декодер Будущего">
<meta property="og:description" content="Выбери, какое будущее строишь ты, и вызови друга на дуэль миров.">
<meta property="og:url" content="{SITE}/static/polotno/">
<meta property="og:image" content="{SITE}/static/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@type": "WebApplication", "name": "Полотно будущего", "alternateName": "Future Canvas", "url": SITE + "/static/polotno/", "applicationCategory": "EducationalApplication", "inLanguage": ["ru", "en"] if has_en else ["ru"], "isAccessibleForFree": True, "description": "Вопросы о будущем и четыре сценарных ответа на каждый из игр «Декодер Будущего».", "creator": {"@type": "Person", "name": "Ольга Еремина", "url": "https://futuredecoder.ru"}, "isPartOf": {"@type": "WebSite", "name": "Декодер Будущего", "url": SITE + "/"}}, ensure_ascii=False)}</script>
<!--/seo-->'''
t = re.sub(r'<!--seo-->.*?<!--/seo-->\n?', '', t, flags=re.S)
t = t.replace('<title>Полотно будущего</title>', '<title>Полотно будущего</title>\n' + head, 1)
nos = '<!--noscript--><noscript><div class="wrap"><h2>Вопросы полотна</h2><ul>' + ''.join(
    f'<li><a href="/polotno/{q["slug"]}">{html.escape(q["ask"])}</a></li>' for q in data['q']) + '</ul></div></noscript><!--/noscript-->'
t = re.sub(r'<!--noscript-->.*?<!--/noscript-->', '', t, flags=re.S)
t = t.replace('<body>', '<body>\n' + nos, 1)
open(ip, 'w').write(t)
print('pages ru:', len(data['q']), 'en:', len(data['q']) if has_en else 0)
