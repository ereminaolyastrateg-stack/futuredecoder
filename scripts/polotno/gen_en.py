#!/usr/bin/env python3
"""Собирает английскую версию полотна: quartz/static/polotno/en/index.html
из русского index.html. Запускать после build.py (тот обновляет data.json и SEO-блок).
Данные общие (../data.json): в EN-режиме поля *_en подставляются вместо русских."""
import json, os, re, sys

REPO = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/futuredecoder'
HERE = os.path.dirname(os.path.abspath(__file__))
if len(sys.argv) < 2 and os.path.isdir(os.path.join(HERE, '../../quartz')): REPO = os.path.abspath(os.path.join(HERE, '../..'))
SRC = os.path.join(REPO, 'quartz/static/polotno/index.html')
DST = os.path.join(REPO, 'quartz/static/polotno/en/index.html')
TR = json.load(open(os.path.join(HERE, 'tr.json'), encoding='utf-8'))
DATA = json.load(open(os.path.join(REPO, 'quartz/static/polotno/data.json'), encoding='utf-8'))

h = open(SRC, encoding='utf-8').read()

# --- head: SEO for EN
seo_en = '''<!--seo-->
<meta name="description" content="Questions about the future and four answers to each, designed by participants of Future Decoder scenario games: duel of worlds, dilemmas and a daily signal.">
<link rel="canonical" href="https://futuredecoder.org/static/polotno/en/">
<link rel="alternate" hreflang="ru" href="https://futuredecoder.org/static/polotno/">
<link rel="alternate" hreflang="en" href="https://futuredecoder.org/static/polotno/en/">
<meta property="og:type" content="website">
<meta property="og:title" content="Future Canvas — Future Decoder">
<meta property="og:description" content="Choose the future you are building, and challenge a friend to a duel of worlds.">
<meta property="og:url" content="https://futuredecoder.org/static/polotno/en/">
<meta property="og:image" content="https://futuredecoder.org/static/og-image.png">
<meta property="og:locale" content="en_GB">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{"@context": "https://schema.org", "@type": "WebApplication", "name": "Future Canvas", "alternateName": "Полотно будущего", "url": "https://futuredecoder.org/static/polotno/en/", "applicationCategory": "EducationalApplication", "inLanguage": "en", "isAccessibleForFree": true, "description": "Questions about the future and four scenario answers to each, from Future Decoder games.", "creator": {"@type": "Person", "name": "Olga Eremina", "url": "https://futuredecoder.ru"}, "isPartOf": {"@type": "WebSite", "name": "Future Decoder", "url": "https://futuredecoder.org/"}}</script>
<!--/seo-->'''
h = re.sub(r'<!--seo-->.*?<!--/seo-->', lambda m: seo_en, h, flags=re.S)

# --- noscript links to EN pages
qs = [q for q in DATA['q'] if q.get('show') is not False]
ns = '<!--noscript--><noscript><div class="wrap"><h2>Canvas questions</h2><ul>' + ''.join(
    f'<li><a href="/en/future-canvas/{q["slug_en"]}">{q["ask_en"]}</a></li>' for q in qs) + '</ul></div></noscript><!--/noscript-->'
h = re.sub(r'<!--noscript-->.*?<!--/noscript-->', lambda m: ns, h, flags=re.S)

# --- dilemmas block (rewritten whole)
DIL_EN = [
 ("Комфорт против устойчивости", "A convenient platform owned by someone else, right now, or your own tool that's pricier and harder?", ["I take the convenient platform", "I build my own"], ["ЦС","ДС"]),
 ("Автоматизировать, чтобы отдыхать, — ловушка", "AI has taken all the routine, and there's enough money. What next?", ["Finally, I rest", "I look for something new to do"], ["ЦС","ДС"]),
 ("Шаг вперёд — два шага назад", "You want to start something new. How do you go in?", ["Guarantees first, then the step", "I give up part of my comfort and go"], ["ЦЗ","ДС"]),
 ("Сказать первым", "Everyone around sees the problem and stays silent. What do you do?", ["I speak first", "I wait for someone else to say it"], ["ДЗ","ЦЗ"]),
 ("Ответственность всё равно на нас", "The decision can be handed to experts or an algorithm. Do you hand it over?", ["Yes, let those who know decide", "I decide myself, even if I'm wrong"], ["ЦС","ДС"]),
 ("Таблетка и тревога", "An anti-ageing pill has appeared. Do you take it, knowing the wish to live healthily may fade?", ["I take it", "I don't; I'll get there myself"], ["ЦС","ДС"]),
 ("Ограничение или свобода времени", "Which is closer to you?", ["A short life where you have to choose", "A long life where you can try everything"], ["ЦЗ","ДС"]),
 ("Чем больше узнаёшь, тем сложнее говорить", "You're new to a topic. What next?", ["I'll study more until I get it", "I start speaking with what I already know"], ["ЦЗ","ДС"]),
 ("Советы детям — из стереотипов двадцатилетней давности", "A teenager is choosing who to become. What do you advise?", ["A reliable profession", "First understand what world they want to live in"], ["ЦЗ","ДЗ"]),
 ("Минимальный комфорт и великая цель", "There's a chance to become part of a big shared cause, but you'll have to give up part of your comfort.", ["I stay in my comfort", "I join the shared cause"], ["ЦС","ДЗ"]),
]
def js(s): return json.dumps(s, ensure_ascii=False)
dil_js = 'const DIL=[\n' + ',\n'.join(
    f' {{t:{js(TR[t])},q:{js(q)},a:{js(a)},w:{js(w)}}}' for t, q, a, w in DIL_EN) + '\n];'
h, n = re.subn(r'const DIL=\[.*?\n\];', lambda m: dil_js, h, flags=re.S)
assert n == 1

PAIRS_EN = '''const PAIRS = {
 "ЦС|ЦС":["Double autopilot","You both hand decisions to the system. It's convenient while the system works and counts you as its own.","A question for the pair: which of you will be first to notice it's time to take back the wheel?"],
 "ЦЗ|ЦЗ":["A shared charter","You both play by the rules and hold on to what's shared. Together you're stable.","The danger is that you don't write the rules. What will you do when they change?"],
 "ДС|ДС":["Two islands","Each is their own master and their own guarantor. Free and reliable.","Islands don't build bridges. Where will you need a third person?"],
 "ДЗ|ДЗ":["A shared cause","You both want to create together and set the rules yourselves.","Maximum agency demands maximum responsibility. Which of you will carry it when it gets hard?"],
 "ЦС|ЦЗ":["The result isn't yours","You're both in the top half of the board: the result belongs to someone else. The difference is whether you take part yourself.","One waits for the system to do everything, the other dutifully follows the rules. Which of you will tire first?"],
 "ДС|ДЗ":["The result is yours","You both want to own the result. One protects what's theirs, the other invests in what's shared.","Where does “mine” end and “ours” begin? Worth agreeing on in advance."],
 "ЦС|ДС":["The machine and the workshop","You both save energy and don't want extra involvement. One trusts the service, the other relies on themselves.","If the service goes down, who will come to whom for help?"],
 "ЦЗ|ДЗ":["Choir and orchestra","You both choose participation and people around you. One fits into what exists, the other builds their own.","The rules of the old world and the rules of a new community rarely match. Whose will you choose?"],
 "ЦС|ДЗ":["Opposite corners","The greatest distance on the board: one gave the wheel to the system, the other wants to build their own with people.","You have something to learn from each other. One knows how not to spend energy, the other knows how to find it."],
 "ЦЗ|ДС":["Norm and freedom","Opposite corners of the board: one holds on to shared rules, the other steps outside them.","One gives support, the other gives a way out. Together it works, as long as nobody demands the other become like them."]
};'''
h, n = re.subn(r'const PAIRS = \{.*?\n\};', lambda m: PAIRS_EN, h, flags=re.S)
assert n == 1

# --- plain string replacements (order matters: longer first where they overlap)
R = [
 ('<html lang="ru">', '<html lang="en">'),
 ('<title>Полотно будущего</title>', '<title>Future Canvas — Future Decoder</title>'),
 ('fetch("data.json"', 'fetch("../data.json"'),
 # data swap: keep ids from Russian text, then show English fields
 ('DATA.q.forEach(q=>q.id=hid(q.q));',
  'DATA.q.forEach(q=>q.id=hid(q.q));\n'
  'const EN=o=>{for(const k of Object.keys(o)){if(k.endsWith("_en")&&o[k]!==undefined&&o[k]!==null){o[k.slice(0,-3)]=o[k]}}};\n'
  'DATA.q.forEach(q=>{EN(q);Object.values(q.w).forEach(EN)});DATA.s.forEach(EN);DATA.m.forEach(EN);\n'
  'const LC=s=>String(s??"").replace(/ЦС/g,"CS").replace(/ЦЗ/g,"CE").replace(/ДС/g,"DS").replace(/ДЗ/g,"DE");'),
 ('esc(m.L)', 'esc(LC(m.L))'),
 ('const NAMES = {"ЦС":"Мир автопилота","ЦЗ":"Мир правил","ДС":"Мир автономии","ДЗ":"Мир сообщества"};',
  'const NAMES = {"ЦС":"Autopilot world","ЦЗ":"Rules world","ДС":"Autonomy world","ДЗ":"Community world"};'),
 ('const HINTS = {"ЦС":"решает система, результат не твой","ЦЗ":"участвуешь по общим правилам","ДС":"сам решаешь, сам владеешь","ДЗ":"создаёшь вместе с другими"};',
  'const HINTS = {"ЦС":"the system decides, the result isn\'t yours","ЦЗ":"you take part by shared rules","ДС":"you decide, you own it","ДЗ":"you create together with others"};'),
 ('Не получилось загрузить базу (data.json). Если вы открыли файл с компьютера, загрузите папку на сайт: браузер не читает соседние файлы локально.',
  'Could not load the knowledge base (data.json). If you opened the file from your computer, upload the folder to a site: browsers don\'t read neighbouring files locally.'),
 ('<a class="logo" href="/" title="Цифровой сад Декодера">', '<a class="logo" href="/en/" title="Future Decoder digital garden">'),
 ('<a class="garden" href="/">← В сад</a>', '<a class="garden" href="/en/">← To the garden</a>'),
 ('aria-label="Разделы"', 'aria-label="Sections"'),
 ('data-tab="canvas">Полотно</a>', 'data-tab="canvas">Canvas</a>'),
 ('data-tab="dilemmas">Дилеммы</a>', 'data-tab="dilemmas">Dilemmas</a>'),
 ('data-tab="signal">Сигнал дня</a>', 'data-tab="signal">Daily signal</a>'),
 ('<a href="en/" hreflang="en" lang="en" class="langsw">EN</a>', '<a href="../" hreflang="ru" lang="ru" class="langsw">RU</a>'),
 ('{База знаний Декодера}', '{Decoder knowledge base}'),
 ('<h1>Полотно<br>будущего</h1>', '<h1>Future<br>Canvas</h1>'),
 ('спроектировано людьми на играх', 'designed by people at the games'),
 ('<b>Будущее не приговор</b>', '<b>The future is not a verdict</b>'),
 ('Вопросы, которые волнуют всех, и четыре ответа на каждый. Их придумали участники игр «Декодер Будущего»: живые сигналы, цена каждого мира и шаг, который можно сделать уже на этой неделе.',
  'Questions everyone worries about, and four answers to each. They were designed by participants of Future Decoder games: real signals, the price of each world, and a step you can take this week.'),
 ('{Вопросы}', '{Questions}'),
 ('Выбери вопрос', 'Choose a question'),
 ('placeholder="Найти вопрос: деньги, ИИ, долголетие…" aria-label="Поиск по вопросам"',
  'placeholder="Find a question: money, AI, longevity…" aria-label="Search questions"'),
 ('Открой любой вопрос и нажми «Вызвать друга на дуэль миров». Друг получит ссылку, выберет свой мир, и вы увидите, какое будущее строит каждый.',
  'Open any question and press “Challenge a friend to a duel of worlds”. Your friend gets a link, picks their world, and you\'ll both see what future each of you is building.'),
 ('{Дилеммы}', '{Dilemmas}'),
 ('Реши, как бы ты поступил', 'Decide what you would do'),
 ('Парадоксы, которые всплыли на играх, в виде выбора из двух. Правильного ответа нет. Выбери, и откроется, к чему пришли участники.',
  'Paradoxes that surfaced at the games, as a choice between two. There\'s no right answer. Choose, and you\'ll see what participants concluded.'),
 ('{Сигнал дня}', '{Daily signal}'),
 ('В каком он мире?', 'Which world is it in?'),
 ('Каждый день один реальный сигнал с игр. Угадай, в каком мире он живёт. Правильного квадрата нет, но интересно, совпадёшь ли ты с теми, кто был на игре.',
  'Every day, one real signal from the games. Guess which world it lives in. There\'s no right quadrant, but it\'s interesting to see whether you match the people who were at the game.'),
 ('База знаний Декодера. Полотно дополняется после каждой игры.', 'Decoder knowledge base. The canvas grows after every game.'),
 ('const spheres = ["Все", ', 'const spheres = ["All", '),
 ('let curSphere="Все"', 'let curSphere="All"'),
 ('aria-pressed="${s==="Все"}"', 'aria-pressed="${s==="All"}"'),
 ('curSphere==="Все"||', 'curSphere==="All"||'),
 ('Такого вопроса пока нет. Может, его стоит принести на следующую игру.', 'No such question yet. Maybe it\'s worth bringing to the next game.'),
 ('← Ко всем вопросам', '← All questions'),
 ('Вызвать друга на дуэль миров</button>', 'Challenge a friend to a duel of worlds</button>'),
 ('Скопировать ссылку на вопрос', 'Copy link to question'),
 ('Если копирование не сработало, выдели текст и скопируй вручную.', 'If copying didn\'t work, select the text and copy it manually.'),
 ('Этот мир по вопросу ещё никто не спроектировал. Приходи на игру и сделай это первым.', 'Nobody has designed this world for this question yet. Come to a game and be the first.'),
 ('<h4>Как развивается</h4>', '<h4>How it unfolds</h4>'),
 ('<h4>Цена</h4>', '<h4>The price</h4>'),
 ('<h4>Сигнал</h4>', '<h4>Signal</h4>'),
 ('<h4>Шаг на неделю</h4>', '<h4>Step for the week</h4>'),
 ('Смеси и парадоксы с этой игры', 'Mixes and paradoxes from this game'),
 ('Парадокс: ', 'Paradox: '),
 ('Эксперимент: ', 'Experiment: '),
 ('← К вопросу', '← Back to question'),
 ('Дуэль миров. Шаг 1 из 2', 'Duel of worlds. Step 1 of 2'),
 ('Выбери ответ, который тебе ближе. Друг увидит вопрос, выберет свой, и только потом вы оба узнаете, какие миры строите.',
  'Choose the answer closest to you. Your friend will see the question, choose theirs, and only then will you both find out which worlds you\'re building.'),
 ('<b>Готово.</b> Отправь другу этот текст со ссылкой:', '<b>Done.</b> Send your friend this text with the link:'),
 ('id="dcopy">Скопировать</button>', 'id="dcopy">Copy</button>'),
 ('Я выбрал(а) свой мир в вопросе «${q.ask}». А ты? Откроем вместе, кто какое будущее строит:',
  'I\'ve chosen my world for the question “${q.ask}”. Have you? Let\'s see who\'s building which future:'),
 ('Тебя вызвали на дуэль миров', 'You\'ve been challenged to a duel of worlds'),
 ('Друг уже выбрал. Выбери свой ответ, и откроем оба.', 'Your friend has already chosen. Choose your answer, and we\'ll reveal both.'),
 ('<div class="who">Друг</div>', '<div class="who">Friend</div>'),
 ('<div class="who">Ты</div>', '<div class="who">You</div>'),
 ('Похожая смесь с игр', 'A similar mix from the games'),
 ('Посмотреть все четыре мира', 'See all four worlds'),
 ('Вызвать кого-то в другом вопросе', 'Challenge someone on another question'),
 ('Сигнал дня · ${d.toLocaleDateString("ru-RU",{day:"numeric",month:"long"})}', 'Daily signal · ${d.toLocaleDateString("en-GB",{day:"numeric",month:"long"})}'),
 ('Сигнал дня Декодера, ${d.toLocaleDateString("ru-RU")}', 'Decoder daily signal, ${d.toLocaleDateString("en-GB")}'),
 ('"Совпал(а) с игрой":"Увидел(а) этот сигнал по-своему"} · серия', '"Matched the game":"Saw this signal my own way"} · streak'),
 ('"Ты совпал(а) с участниками игры.":"На игре этот сигнал положили в "+NAMES[s.L].toLowerCase()+"."',
  '"You matched the game participants.":"At the game this signal was placed in the "+NAMES[s.L]+"."'),
 ('Где он всплыл: ${esc(s.where)}.', 'Where it came up: ${esc(s.where)}.'),
 ('Это не ошибка: в Декодере сигнал попадает в разные квадраты в зависимости от того, кто на него смотрит.',
  'That\'s not a mistake: in the Decoder a signal lands in different quadrants depending on who\'s looking at it.'),
 ('<span>Сыграно: ${cur.played}</span><span>Совпадений: ${cur.hits}</span><span>Серия: ${cur.streak}</span>',
  '<span>Played: ${cur.played}</span><span>Matches: ${cur.hits}</span><span>Streak: ${cur.streak}</span>'),
 ('Поделиться результатом', 'Share result'),
 ('Открыть полотно', 'Open the canvas'),
 ('Завтра будет новый сигнал.', 'A new signal tomorrow.'),
 ('"dec-sig"', '"dec-sig-en"'),
 ('<span class="sph">Дилемма ${i+1}</span>', '<span class="sph">Dilemma ${i+1}</span>'),
 ('${esc(d.a[0])} или ${esc(d.a[1]).toLowerCase()}', '${esc(d.a[0])} or ${esc(d.a[1]).toLowerCase()}'),
 ('← Все дилеммы', '← All dilemmas'),
 ('"Тебе прислали дилемму. Друг уже выбрал, выбери и ты":"Дилемма "+(i+1)+" из "+DIL.length',
  '"Someone sent you a dilemma. Your friend has chosen; now you choose":"Dilemma "+(i+1)+" of "+DIL.length'),
 ('${j===k?"твой выбор · ":""}${friend===j?"выбор друга · ":""}ближе к: ${NAMES[d.w[j]].toLowerCase()}',
  '${j===k?"your choice · ":""}${friend===j?"friend\'s choice · ":""}closer to: ${NAMES[d.w[j]]}'),
 ('"Вы с другом выбрали одно и то же.":"Вы с другом выбрали по-разному."', '"You and your friend chose the same.":"You and your friend chose differently."'),
 ('"Посмотрите, какая цена у вашего общего выбора.":"Самое интересное: спросите друг друга почему."',
  '"Look at the price of your shared choice.":"The most interesting part: ask each other why."'),
 ('<h4>К чему пришли на игре</h4>', '<h4>What the game concluded</h4>'),
 ('<h4>Парадокс</h4>', '<h4>Paradox</h4>'),
 ('<h4>Проверь на этой неделе</h4>', '<h4>Try it this week</h4>'),
 ('id="dilcopy">Спросить друга</button>', 'id="dilcopy">Ask a friend</button>'),
 ('Следующая дилемма', 'Next dilemma'),
 ('Друг увидит дилемму без твоего ответа и узнает его только после своего выбора.',
  'Your friend will see the dilemma without your answer and learn it only after choosing.'),
 ('Я уже выбрал(а). А ты?', 'I\'ve already chosen. Have you?'),
 ('btn.textContent="Скопировано"', 'btn.textContent="Copied"'),
 ('`База знаний Декодера · вопросов: ${DATA.q.length} · сигналов: ${DATA.s.length} · обновлено ${DATA.updated||""}. Полотно дополняется после каждой игры.`',
  '`Decoder knowledge base · questions: ${DATA.q.length} · signals: ${DATA.s.length} · updated ${DATA.updated||""}. The canvas grows after every game.`'),
]
for a, b in R:
    b = b.replace("'", "\u2019")
    c = h.count(a)
    if c == 0:
        sys.exit('NOT FOUND: ' + a[:80])
    h = h.replace(a, b)

# leftover Cyrillic outside allowed spots (CSS classes / world codes / comments)
left = set()
for m in re.finditer(r'[А-Яа-яЁё][А-Яа-яЁё ,.:;!?«»()—–-]*', h):
    t = m.group(0).strip()
    if t not in ('ЦС','ЦЗ','ДС','ДЗ') and not re.fullmatch(r'(ЦС|ЦЗ|ДС|ДЗ)', t):
        left.add(t)
print('cyrillic left:', sorted(left)[:60])

os.makedirs(os.path.dirname(DST), exist_ok=True)
open(DST, 'w', encoding='utf-8').write(h)
print('written', DST, len(h))
