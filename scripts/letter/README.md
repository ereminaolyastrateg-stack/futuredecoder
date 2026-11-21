# Письмо из 2035

Страница без ИИ: сфера → подсфера → «как сейчас» → «как хочу» → письмо от себя из 2035 года.
Данные — те же 132 карточки, что в «Сферах жизни» (`scripts/spheres/source_ru.json`, `tr_en.json`).

`python3 scripts/letter/build.py` пересобирает `quartz/static/letter/` (RU, EN, data-ru.json, data-en.json) и картинки `quartz/static/og/letter-*.png`.
Текст письма и подписи — в `build.py` (TX, FN, PAGE), вёрстка — `template.html`.
Ссылка на письмо: `#H1-cs-de` (подсфера, сейчас, хочу; `0` — «ничего из этого»).
