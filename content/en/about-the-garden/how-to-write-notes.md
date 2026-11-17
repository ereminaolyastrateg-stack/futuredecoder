---
title: "How a Note in the Garden Works"
seoTitle: "How to write notes in the Future Decoder digital garden: Zettelkasten, tags, SEO"
description: "Rules for notes in the Future Decoder digital garden: one idea per note, front matter, hierarchical tags, links, translations, and requirements for search engines and AI."
lang: en
translations:
  ru: /o-sade/kak-pisat-zametki
  en: /en/about-the-garden/how-to-write-notes
tags:
  - section/about-the-garden
  - type/guidelines
  - theme/zettelkasten
date: 2026-11-16
updated: 2026-11-17
---

*In short: the garden follows the Zettelkasten method. Each note holds one idea, signal or story; it has front matter with a description and tags, links to other notes and a "Connections" block at the end. That way the garden grows as a network, and search engines and AI understand what each page is about.*

## Five principles

1. **One idea, one note.** Not "everything about education" but one signal, one concept, one story. If a text holds two ideas, it becomes two notes linking to each other.
2. **In your own words.** A note retells and makes sense of a source rather than copying it. Quotes are short and attributed.
3. **Links matter more than folders.** A note is found not because it sits in the right folder but because other notes link to it. Every new note links to at least two existing ones.
4. **Tags are for finding by attribute, links are for meaning.** A tag says "this is a signal from the DS world"; a link says "this idea continues that one".
5. **Notes stay alive.** They can be extended; the `updated` date changes with every notable edit.

## Kinds of notes

| Kind | What it holds | Where it lives | Type tag |
|---|---|---|---|
| Signal | One example from the world: what, where, when, why it is a signal, scenario, sources | `en/materials/signals/<topic>/` | `type/signal` |
| Macrotrend | A large force of change and its four expressions | `en/materials/macrotrends/` | `type/macrotrend` |
| Concept | A term or idea: definition, examples, origin | `en/theory/` | `type/concept` |
| Theory | An analysis or essay | `en/theory/` | `type/theory` |
| Story | A personal story or book chapter | `en/book/` | `type/personal-story` |
| Lecture long read | A text based on a lecture, with video and sources | `en/talks/` | `type/long-read` |
| Index (map) | A list of links to notes on a topic, without content of its own | `index.md` in a folder | `type/index` |

## File name

Latin letters, lower case, hyphens: `sig-edu-041.md`, `image-of-the-future.md`. The file name becomes the page address, so it is best not to change it after publishing. If you must, add the old address to `aliases`.

## Front matter

```yaml
---
title: "A short, clear title"
seoTitle: "A search title, up to 60 characters"
description: "What the note is about, 120–160 characters, with the key words"
lang: en
translations:
  ru: /russian-version-address
  en: /en/english-version-address
tags:
  - type/signal
  - scenario/DS
  - domain/education
  - theme/self-directed-learning
aliases:
  - SIG-EDU-041
date: 2026-11-16
updated: 2026-11-17
---
```

- `title`: what a person would call this idea. For a signal: "Project name: what happens in it".
- `seoTitle`: optional; use it when the title is too short or lacks the words people search for.
- `description`: one or two sentences; search engines and AI use it to decide whether to show the page.
- `translations`: only when a second language version exists; the other version gets the same in reverse.
- `socialImage`: optional; without it the garden generates a social image itself.

### Signal front matter

A signal has fields in its front matter from which the [[en/materials/signals/education|signal catalog]] with search and filters is built:

```yaml
signal_type: signal
signal_id: SIG-EDU-041
name: "Short project name"
scenario: DS            # CS, CE, DS or DE
year: 2025              # year of the signal; empty if unknown
period: "2025 — launch; 2035 — scenario horizon."
added: 2026-11-16       # when the signal was added to the garden
geography: "France"
stage: "Pilot"
life_domains: ["Education", "Work"]
industries: ["EdTech"]
themes: ["learning by doing", "peer review"]   # the essence of the signal, 2–4 labels
macrotrends: ["MT-043 — Education, knowledge and literacy"]
```

Signal tags: `type/signal`, `scenario/…`, `domain/…` and thematic `theme/…` tags, one for each label in `themes`. Thematic labels describe the essence of the signal, not the industry: not "edtech" but "learning by doing".

## Tags

Tags are hierarchical: `group/value`. Lower case, words joined with hyphens.

| Group | Purpose | Examples |
|---|---|---|
| `type/` | Kind of note | `type/signal`, `type/concept`, `type/long-read` |
| `scenario/` | Decoder world | `scenario/CS`, `scenario/CE`, `scenario/DS`, `scenario/DE` |
| `domain/` | Life domain | `domain/education`, `domain/work`, `domain/health` |
| `industry/` | Industry | `industry/edtech`, `industry/retail` |
| `theme/` | Subject | `theme/images-of-the-future`, `theme/attention` |
| `macrotrend/` | Related macrotrend | `macrotrend/mt-043` |
| `person/` | Thinker whose ideas are discussed | `person/fred-polak` |
| `section/` | Site section | `section/book`, `section/talks` |

Before creating a new tag, check whether a similar one exists: click any tag on the site and open the list of all tags in its group. One `theme/ai` is better than three variants such as `theme/ai`, `theme/artificial-intelligence` and `theme/a-i`.

The Russian version uses the same groups in Russian: `тип/`, `сценарий/` (`ЦС`, `ЦЗ`, `ДС`, `ДЗ`), `сфера/`, `отрасль/`, `тема/`, `макротренд/`, `персона/`, `раздел/`.

## Body of the note

1. **"In short"**: the first paragraph, in italics. A direct answer to the question the note is about, in two or three sentences. This is what search engines and AI quote most often.
2. **Main text** with `##` subheadings. Facts come with a date and source; interpretation is labelled as such: "our reading", "hypothesis".
3. **"Questions and answers"**: optional, for concepts and long reads: three to five questions as a person would ask them, with short answers.
4. **"Sources"**: for signals and long reads: links to primary sources.
5. **"Connections"**: at the very end, a list of links to other notes explaining how they relate.

## Links

- To garden notes: `[[path/to/note|display text]]`. Full path without `.md`, for example `[[en/materials/signals/education-signals/sig-edu-016|Solar Mamas]]`.
- To a Future Canvas question: `[[en/future-canvas/how-do-i-choose-a-profession-when-everything-keeps-changing|How do I choose a profession?]]`.
- To external sites: a normal link `[text](https://...)`.
- Backlinks appear by themselves: the page you linked to shows on the right who links to it.

## Large sets go into a filterable table

If there are more than a dozen notes of one kind — signals, books and films, macrotrend cards, life-sphere options — we don't publish them as a long list. The section page gathers them in a **catalog table** with search and filters: by world, sphere, theme, macrotrend. Clicking a label in the table switches the filter on. In the side menu such a folder is collapsed so navigation stays short.

For a note to appear in a catalog, its front matter needs the fields the table is built from: for a signal — `signal_id`, `scenario`, `themes` and others (see "Signal front matter"); for a macrotrend card — `macrotrend_id`, `mt_name`, `scenario`, `essence`, `scene`, `themes`; for a sphere card — `sphere`, `scenario` and an `items` list. A new kind of note means a new catalog, not a new list.

## Ethics

- No names of game participants, no identifiable private stories, no politics.
- Host claims that cannot be verified are marked "(according to the host)".
- Discussing an example at a game does not mean the example works or that the group agrees.

## Checklist before publishing

- [ ] One idea per note.
- [ ] `title`, `description`, `lang`, `tags` and `date` are filled in.
- [ ] There is a `type/…` tag; for a signal also `scenario/…` and `domain/…`.
- [ ] The first paragraph answers the note's main question.
- [ ] At least two links to existing notes and a "Connections" block.
- [ ] Facts have dates and sources.
- [ ] If there is a translation, `translations` is set in both versions.
- [ ] The file name uses Latin letters.

## Obsidian templates

The garden repository includes templates: `templates/zametka.md` (Russian) and `templates/note-en.md` (English). In Obsidian: Settings → Core plugins → Templates, set the template folder to `templates`, then use "Insert template" in a new note.

## Connections

- Atomic notes in practice: [[en/materials/signals/education-signals/index|education signals]]
- Theory with questions and answers: [[en/theory/the-future-as-a-mental-model|The Limits of Our Mental Models]]
- A personal story with connections: [[en/book/chapter-1/life-ends-at-eighteen|Life Ends at Eighteen]]
- Why this garden exists: [[en/why-talk-about-the-future|Why Talk About the Future]]
