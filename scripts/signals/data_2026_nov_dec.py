# -*- coding: utf-8 -*-
"""Данные подборки «Сигналы 2026: ноябрь — декабрь».

20 трендов × 4 сценария = 80 сигналов. Источники: лекция «Будущее поменяло хозяев»
(11.11.2026, Л), III симпозиум «Создавая будущее» (12–13.11.2026, С),
Stanford Digital Economy Lab «Canaries in the Coal Mine?» (август 2026, Ст).
Сборка: python3 scripts/signals/build_2026.py
"""

SYMP = "https://asafov.ru/avtor/v-moskve-prosel-iii-mezdunarodnyi-simpozium-sozdavaia-budushhee"
SYMP2 = "https://vfokuse.mail.ru/articles/69634841-simpozium-sozdavaya-budushee-projdet-v-moskve-1213-noyabrya-2026-goda/"
FTSG = "https://ftsg.com/convergence"
CIFS = "https://www.cifs.dk/read-listen/reports-knowledge/megatrends"
DFF = "https://www.dubaifuture.ae/the-global-50/"
STAN = "https://digitaleconomy.stanford.edu/publication/canaries-in-the-coal-mine-six-facts-about-the-recent-employment-effects-of-artificial-intelligence/"
CN_OPEN = "https://www.technologyreview.com/2026/04/21/1135658/china-open-source-models-ai-artificial-intelligence/"
CN_TEST = "https://chinamediaproject.org/2025/07/30/how-china-sees-ai-safety/"
ENH = "https://www.euronews.com/health/2026/05/26/inside-the-enhanced-games-everything-that-happened-on-sports-most-controversial-night"
CORT = "https://itbrief.com.au/story/cortical-labs-cl1-commercial-milestone-after-aud-245k-grant"
DC_PROT = "https://www.costar.com/article/1318831312/data-center-opponents-say-protests-signal-growing-resistence"
DC_POLL = "https://www.tomshardware.com/tech-industry/data-centers/over-70-percent-of-americans-oppose-ai-data-centers-us-protests-intensify-as-more-arrests-are-being-made-almost-40-arrested-this-year-in-backlash-to-ai-factory-buildout"
DC_Q2 = "https://www.tomshardware.com/tech-industry/data-centers/local-opposition-blocked-usd68-billion-worth-of-data-center-projects-in-the-second-quarter-of-2026-data-center-investments-reportedly-still-on-track-to-hit-usd32-trillion-by-2050"
NF_DOC = "https://mezha.ua/en/news/netflix-hugging-face-attack-315943/"
KPDH = "https://whats-on-netflix.com/news/kpop-demon-hunters-makes-netflix-history-with-unprecedented-1-year-top-10-streak"
NEPAL = "https://www.aljazeera.com/news/2025/9/15/more-egalitarian-how-nepals-gen-z-used-gaming-app-discord-to-pick-pm"
DRC = "https://www.businessday.co.za/world/2026-08-06-drc-bans-copper-and-cobalt-concentrates-exports/"

SRC = {
    'И': ('Исследование или данные', 'Research or data'),
    'Н': ('Новость или событие', 'News or event'),
    'К': ('Кейс', 'Case'),
    'Л': ('Лекция «Будущее поменяло хозяев», 11 ноября 2026', 'Lecture “The Future Has Changed Hands”, 11 November 2026'),
    'С': ('III симпозиум «Создавая будущее», Москва, 12–13 ноября 2026', 'III Symposium “Creating the Future”, Moscow, 12–13 November 2026'),
    'Ст': ('Stanford Digital Economy Lab, «Canaries in the Coal Mine?», версия августа 2026', 'Stanford Digital Economy Lab, “Canaries in the Coal Mine?”, August 2026 revision'),
}

# Тренды: номер → (RU, EN, суть RU, суть EN, макротренды, сферы, тема RU, тема EN)
TRENDS = {
 1: ('ИИ-посредник между человеком и миром', 'AI as the go-between for people and the world',
     'ИИ уходит в физический мир и становится агентом: ищет, покупает и решает за нас. Вопрос — чей он агент и на каких ценностях обучен.',
     'AI moves into the physical world and becomes an agent that searches, buys and decides for us. The question is whose agent it is and what values it was trained on.',
     [47, 2, 81], ['Быт, потребление и отдых', 'Финансы'], 'ии-агенты', 'ai agents'),
 2: ('Вход в работу закрывается', 'The entrance to work is closing',
     'ИИ пока не уничтожает профессии, но меняет, кого в них нанимают. Главный страх — не восстание машин, а стать ненужным.',
     'AI is not yet destroying professions, but it is changing who gets hired into them. The main fear is not a machine uprising but becoming unnecessary.',
     [66, 7, 14], ['Работа', 'Образование'], 'первая работа', 'first job'),
 3: ('Апгрейд человека как норма', 'Human upgrades as the norm',
     'Улучшать тело и мозг становится нормой, отказ — недостатком. Человек догоняет технологии.',
     'Improving body and brain becomes the norm, and refusing becomes a handicap. People try to keep up with technology.',
     [24, 57, 11], ['Здоровье', 'Работа'], 'улучшение человека', 'human enhancement'),
 4: ('Цифровое бессмертие', 'Digital immortality',
     'Сознание пытаются переносить, оцифровывать и продавать. Граница того, что считать человеком, размывается.',
     'People try to transfer, digitise and sell consciousness. The boundary of what counts as human blurs.',
     [75, 24, 57], ['Здоровье', 'Ценности, смысл и сообщество'], 'бессмертие', 'immortality'),
 5: ('Одиночество как норма', 'Loneliness as the norm',
     'Одиночество из проблемы превратилось в факт и в рынок. Живое общение становится редкостью.',
     'Loneliness has turned from a problem into a fact and a market. Live contact is becoming rare.',
     [27, 56, 76], ['Близкие отношения и семья', 'Ценности, смысл и сообщество'], 'одиночество', 'loneliness'),
 6: ('Депопуляция и новая детность', 'Depopulation and new parenthood',
     'Население стареет, рождаемость падает, а прежние смыслы большой семьи не работают. Выходы ищут в технологиях, у государства и в личных решениях.',
     'Populations age, birth rates fall and the old meanings of a big family no longer work. People look for ways out in technology, the state and personal choices.',
     [17, 67, 16], ['Близкие отношения и семья', 'Место жизни и общественная среда'], 'рождаемость', 'birth rate'),
 7: ('Новое неравенство', 'The new inequality',
     'Доступ к технологиям и апгрейду делит людей на касты. В разговор о будущем вернулась тема сегрегации.',
     'Access to technology and upgrades splits people into castes. Segregation is back in conversations about the future.',
     [38, 57, 65], ['Финансы', 'Ценности, смысл и сообщество'], 'неравенство', 'inequality'),
 8: ('Битва за физические ресурсы', 'The battle for physical resources',
     'Вода, энергия, земля и вычисления становятся основой власти. Геоэкономика превращается в оружие.',
     'Water, energy, land and compute become the basis of power. Geoeconomics turns into a weapon.',
     [63, 71, 40], ['Место жизни и общественная среда', 'Финансы'], 'ресурсы', 'resources'),
 9: ('Сопротивление скорости технологий', 'Resistance to the speed of technology',
     'Общество тормозит прогресс, который обходится ему ценой ресурсов и привычной жизни. Новые луддиты — молодые.',
     'Society slows down progress that costs it resources and its familiar way of life. The new Luddites are young.',
     [44, 60, 29], ['Место жизни и общественная среда', 'Ценности, смысл и сообщество'], 'сопротивление технологиям', 'tech resistance'),
 10: ('Контроль и суверенитет', 'Control and sovereignty',
     'От свободы, глобализации и демократизации — к ограничениям и контролю. Вопрос лишь в том, у кого контроль.',
     'From freedom, globalisation and democratisation to limits and control. The only question is who holds the control.',
     [23, 5, 36], ['Место жизни и общественная среда', 'Быт, потребление и отдых'], 'суверенитет', 'sovereignty'),
 11: ('Ценности как инструмент проектирования', 'Values as a design tool',
     'Будущее идёт туда, куда хотят люди, поэтому ценности становятся рабочим инструментом. Их зашивают в модели, стратегии и личные решения.',
     'The future goes where people want it to go, so values become a working tool. They are built into models, strategies and personal decisions.',
     [44, 54, 30], ['Ценности, смысл и сообщество', 'Образование'], 'ценности', 'values'),
 12: ('Битва нарративов о будущем', 'The battle of narratives about the future',
     'Кто пишет образ будущего, тот задаёт направление. Фантастика, кино и мультфильмы стали мягкой силой.',
     'Whoever writes the image of the future sets the direction. Science fiction, film and animation have become soft power.',
     [30, 26, 72], ['Ценности, смысл и сообщество', 'Быт, потребление и отдых'], 'образ будущего', 'image of the future'),
 13: ('Власть через микросообщества', 'Power through micro-communities',
     'Мир распался на невидимые сообщества, до которых большие системы не достают. Власть у того, кто говорит с ними на их языке.',
     'The world has split into invisible communities that big systems cannot reach. Power belongs to whoever speaks their language.',
     [76, 53, 29], ['Ценности, смысл и сообщество', 'Место жизни и общественная среда'], 'сообщества', 'communities'),
 14: ('Право быть несовершенным', 'The right to be imperfect',
     'Культ идеальности уступает подлинности: можно ошибаться и принимать своих демонов.',
     'The cult of perfection gives way to authenticity: it is fine to make mistakes and accept your demons.',
     [56, 55, 26], ['Ценности, смысл и сообщество', 'Здоровье'], 'подлинность', 'authenticity'),
 15: ('Когнитивная автономия и субъектность', 'Cognitive autonomy and agency',
     'Главный ресурс — своё внимание и мышление. Риск — отдать их алгоритмам и чужим нарративам.',
     'The main resource is your own attention and thinking. The risk is handing them over to algorithms and other people’s narratives.',
     [55, 79, 31], ['Образование', 'Работа'], 'внимание', 'attention'),
 16: ('Образование: от знаний к мышлению', 'Education: from knowledge to thinking',
     'Знания устаревают за неделю, а школьник со смартфоном знает больше профессора. Ценными становятся навыки, способ мышления и ценности.',
     'Knowledge goes stale within a week, and a pupil with a smartphone knows more than a professor. Skills, ways of thinking and values become valuable.',
     [43, 31, 47], ['Образование'], 'мышление', 'thinking'),
 17: ('Будущее проживают через игру и прототип', 'The future is lived through play and prototypes',
     'Будущему учатся в действии: в играх, дизайне и постановках. Форсайт становится навыком, а не прогнозом.',
     'People learn the future by doing: in games, design and staging. Foresight becomes a skill rather than a forecast.',
     [13, 54, 72], ['Образование', 'Ценности, смысл и сообщество'], 'игра и прототип', 'play and prototypes'),
 18: ('Здоровье как среда и образ жизни', 'Health as environment and way of life',
     'Здоровье выходит за рамки медицины: это и препараты, и сон, и дом, и окружение.',
     'Health goes beyond medicine: it is drugs, but also sleep, home and the people around you.',
     [1, 51, 49], ['Здоровье', 'Быт, потребление и отдых'], 'здоровье', 'health'),
 19: ('Симбиоз и сосуществование разных', 'Symbiosis and coexistence of the different',
     'Логику «выживет один» сменяет поиск способов жить вместе: человека и ИИ, разных культур и видов.',
     'The “only one survives” logic gives way to a search for ways of living together: humans and AI, different cultures and species.',
     [2, 39, 34], ['Ценности, смысл и сообщество', 'Работа'], 'симбиоз', 'symbiosis'),
 20: ('Ограниченная экономика и фрагментация', 'The constrained economy and fragmentation',
     'Рост возможен только в пределах локальных возможностей. Глобальный рынок дробится на регионы и слои.',
     'Growth is only possible within local limits. The global market breaks up into regions and layers.',
     [50, 40, 53], ['Финансы', 'Место жизни и общественная среда'], 'ограниченная экономика', 'constrained economy'),
}

from signals_2026_11 import S, NAMES_EN, MONTH

# Что обновить в своде 82: MT → (что поменялось RU, EN, тренды подборки)
MT_UPDATES = [
 (47, 'Добавить агентов, которые платят и решают за человека, и открытые модели как путь к своему ИИ.', 'Add agents that pay and decide for people, and open models as a path to one’s own AI.', [1, 16]),
 (66, 'Добавить данные Стэнфорда: падает найм 22–25-летних в профессиях, где ИИ заменяет задачи.', 'Add the Stanford data: hiring of 22–25-year-olds falls in occupations where AI replaces tasks.', [2]),
 (7, 'Сдвиг от «увольнений» к «закрытому входу» и «владению работой» (агенты и роботы).', 'A shift from “layoffs” to a “closed entrance” and “owning work” (agents and robots).', [2]),
 (24, 'Добавить биокомпьютеры на человеческих нейронах (CL1) и тему переноса сознания.', 'Add biocomputers made of human neurons (CL1) and the theme of consciousness transfer.', [3, 4]),
 (57, 'Добавить неравный доступ к продлению жизни и сообщества отказа.', 'Add unequal access to life extension and communities of refusal.', [3, 4, 7]),
 (27, 'Индивидуализм как условие, а не обещание: CIFS убрал слово «свобода».', 'Individualism as a condition, not a promise: CIFS dropped the word “freedom”.', [5]),
 (17, 'Добавить сценарии «дети в обмен на благосостояние» и позднюю детность при долгой жизни.', 'Add the “children for well-being” scenario and late parenthood in long lives.', [6]),
 (38, 'Вернулась тема сегрегации и «каст» по доступу к апгрейду.', 'Segregation and “castes” based on access to upgrades are back.', [7]),
 (63, 'Добавить запреты на вывоз сырья (ДР Конго) и вычисления как ресурс власти.', 'Add raw-material export bans (DR Congo) and compute as a resource of power.', [8, 20]),
 (44, 'Добавить сопротивление дата-центрам, тесты моделей на ценности и вопрос «чей это агент».', 'Add resistance to data centres, value tests for models and the question “whose agent is it”.', [9, 11]),
 (60, 'Добавить общественное торможение технологий как самостоятельную силу.', 'Add public slowdown of technology as a force in its own right.', [9]),
 (23, 'От демократизации к «суверенным технологиям контроля» (Gartner).', 'From democratisation to “sovereign technologies of control” (Gartner).', [10]),
 (30, 'Фантастика и кино как мягкая сила: «Задача трёх тел», питчинг «Кино против футурошока».', 'Science fiction and film as soft power: “The Three-Body Problem”, the “Film against Future Shock” pitch.', [12]),
 (76, 'Discord как парламент и фандомы на протестах; у фандомов есть хозяева.', 'Discord as parliament and fandoms at protests; fandoms have owners.', [13]),
 (56, 'Право быть несовершенным: «Охотницы на демонов», монстры-герои.', 'The right to be imperfect: “KPop Demon Hunters”, monsters as heroes.', [14]),
 (55, 'Когнитивная автономия: студенты считают ИИ умнее себя; «интеллектуальный фастфуд».', 'Cognitive autonomy: students think AI is smarter than they are; “intellectual fast food”.', [15]),
 (43, 'Учить и людей, и их ИИ-помощников; компетенции из фантастики (ВШЭ).', 'Teach both people and their AI assistants; competencies from science fiction (HSE).', [16]),
 (13, 'Игра как тренажёр для роботов и лаборатория способов работать.', 'Games as a training ground for robots and a lab for ways of working.', [17]),
 (54, 'Предложение сделать футурологию академической дисциплиной; материализация будущего.', 'The proposal to make futures studies an academic discipline; materialising the future.', [11, 17]),
 (1, 'Здоровье как среда: сон, дом, окружение; оземпик меняет норму тела.', 'Health as environment: sleep, home, surroundings; Ozempic changes the body norm.', [18]),
 (2, 'От управления ИИ к совместному управлению и риску, что ИИ управляет нами.', 'From managing AI to co-management, and the risk of AI managing us.', [19]),
 (50, 'Ограниченная экономика: энергия выпала из мегатрендов DFF как «допущение».', 'The constrained economy: energy dropped out of DFF’s megatrends as an “assumption”.', [20]),
 (53, 'Локальность как норма: региональные культурные сцены и тренды Евразии.', 'Locality as the norm: regional cultural scenes and Eurasian trends.', [13, 20]),
]

# Кандидаты в новые макротренды (нет в своде 82 как самостоятельной силы)
NEW_MT = [
 ('Сопротивление скорости технологий', 'Resistance to the speed of technology', 'Сейчас размазано между MT-044 и MT-060. 142 протеста за день, $68 млрд заблокированных проектов за квартал — это уже отдельная сила.', 'Currently spread across MT-044 and MT-060. 142 protests in a day and $68 billion of blocked projects in one quarter make it a force of its own.', 9),
 ('Цифровое бессмертие и границы человека', 'Digital immortality and the boundaries of the human', 'Частично в MT-075 и MT-024, но вопрос «что считать человеком» в своде не поставлен.', 'Partly in MT-075 and MT-024, but the question “what counts as human” is not posed in the set.', 4),
 ('Битва нарративов о будущем', 'The battle of narratives about the future', 'Частично в MT-030. Фантастика, кино и анимация стали инструментом государств и платформ.', 'Partly in MT-030. Science fiction, film and animation have become tools of states and platforms.', 12),
 ('Ценности как инструмент проектирования', 'Values as a design tool', 'Частично в MT-044 и MT-054. Ценности зашивают в модели и стратегии — это рабочий инструмент, а не фон.', 'Partly in MT-044 and MT-054. Values are built into models and strategies: a working tool, not a backdrop.', 11),
 ('Симбиоз человека и ИИ', 'Human–AI symbiosis', 'Частично в MT-002. Нужна сила о сосуществовании разных: человека и ИИ, культур, видов.', 'Partly in MT-002. A force about the coexistence of the different is needed: humans and AI, cultures, species.', 19),
 ('Закрытый вход в работу', 'The closed entrance to work', 'Частично в MT-066. Отдельная сила — исчезновение первой ступени карьеры.', 'Partly in MT-066. A separate force: the disappearance of the first career rung.', 2),
]

# Названия макротрендов из свода 82 (Future_Decoder_ИТОГ_2026_v10)
MT_NAMES = {
 1: 'Holistic Health (целостное здоровье)',
 2: 'Human Machine Interaction (взаимодействие человек–машина)',
 5: 'Super-Safe-Society',
 7: 'Автоматизация труда',
 11: 'Биотехнологии и персонализированная медицина',
 13: 'Геймификация',
 14: 'Гиг-экономика (Gig Economy)',
 16: 'Глобальная миграция и демографические сдвиги',
 17: 'Демографический спад и экономика стареющего населения',
 23: 'Кибербезопасность и суверенитет',
 24: 'Когнитивная инженерия и нейроинтерфейсы',
 26: 'Креативная экономика',
 27: 'Кризис индивидуализма',
 29: 'Кризис социальных институтов',
 30: 'Культура как источник будущего',
 31: 'Мастерство человека',
 34: 'Мир смешанной логики',
 36: 'Национализм 2.0',
 38: 'Неравенство и распределение ресурсов',
 39: 'Новая социальная динамика и инклюзивность',
 40: 'Новые драйверы экономического роста',
 43: 'Образование, знание и грамотность',
 44: 'Общественное доверие и цифровая этика',
 47: 'Передовые системы ИИ и когнитивные вычисления',
 49: 'Переосмысление роли еды',
 50: 'Построст',
 51: 'Превентивная медицина и персонализированное здоровье',
 53: 'Прогрессивная провинция',
 54: 'Проектирование будущего и стратегическое визионерство',
 55: 'Психологическая устойчивость и кризис мышления',
 56: 'Психологическое благополучие и ментальное здоровье',
 57: 'Радикальное долголетие',
 60: 'Снижение производительности человека и деградация технологий',
 63: 'Технонационализм и локализация производства',
 65: 'Трансформационная экономика (Value Vertigo)',
 66: 'Трансформация рынка труда и управление талантами',
 67: 'Трансформация семьи и множественные форматы партнёрств',
 71: 'Устойчивое развитие и климатическая адаптация',
 72: 'Футуристические сценарии и универсальные законы развития',
 75: 'Цифровой двойник (Digital Twin)',
 76: 'Цифровые сообщества и виртуальное взаимодействие',
 79: 'Экономика внимания и новый маркетинг',
 81: 'Экосистемы, супераппы и платформенная экономика',
}

# Ссылки, найденные при проверке источников 20.11.2026 (номер сигнала → источник)
EXTRA_URLS = {
 32: 'https://www.weforum.org/stories/climate-action-and-waste-reduction/research-data-centres-water-scarcity-understanding-risk',
 38: 'https://www.networkworld.com/article/4238030/gartners-top-tech-trends-for-2027-expand-and-accelerate.html',
 39: 'https://www.rand.org/pubs/research_reports/RRA4692-1.html',
 49: 'https://www.koreaherald.com/article/10497759',
 78: 'https://english.www.gov.cn/news/202603/10/content_WS69b02d13c6d00ca5f9a09c9d.html',
 79: 'https://www.fiverr.com/news/fiverr-q2-2026-earnings',
}
