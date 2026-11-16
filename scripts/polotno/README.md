# Полотно будущего: как обновлять

Данные: `quartz/static/polotno/data.json` (общие для RU и EN; английские поля с суффиксом `_en`).

1. Обновить `data.json` новыми вопросами, сигналами и смесями.
2. Дописать переводы новых строк в `tr.json` (русская строка → английская). `build.py` покажет, каких переводов не хватает.
3. `python3 scripts/polotno/build.py .` — страницы вопросов `content/polotno/` и `content/en/future-canvas/`, поля `_en`, `llms.txt`, SEO-блок русской страницы.
4. `python3 scripts/polotno/gen_en.py` — английская версия приложения `quartz/static/polotno/en/index.html`.
5. Закоммитить в ветку `v5`: сайт пересоберётся сам.

Адреса: RU https://futuredecoder.org/static/polotno/ и /polotno/; EN https://futuredecoder.org/static/polotno/en/ и /en/future-canvas/.
