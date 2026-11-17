# Опросник «Как сейчас и каким хочу»

Статичная страница `quartz/static/opros/` (RU) и `quartz/static/opros/en/` (EN), описание в саду: `content/opros/index.md` и `content/en/questionnaire/index.md`.

- Варианты берутся из карточек сфер жизни: `scripts/spheres/source_ru.json` + `tr_en.json`. Примеры со статусом «Кандидат…» не выгружаются, на вариант берётся не больше двух.
- Обе страницы собираются из `template.html`. Правишь шаблон или карточки, потом запускаешь `python3 scripts/opros/build.py`.
- Данные человека никуда не отправляются. Черновик хранится в `localStorage` (ключ `fd-opros-v1`), итог выгружается в `.md`, в `.json` (формат `futuredecoder-opros/1`, для бота) и на печать.
