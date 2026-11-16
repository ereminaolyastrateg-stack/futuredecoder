#!/usr/bin/env python3
"""Переводит плоские теги сада в иерархические (раздел/, тип/, тема/, сфера/ …)."""
import re, glob, os
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
THEME = {'control':('контроль','control'),'future':('будущее','future'),'inequality':('неравенство','inequality'),
 'tech':('технологии','technology'),'systems':('системы','systems'),'attention':('внимание','attention'),'human':('человек','human'),
 'ecology':('экология','ecology'),'culture':('культура','culture'),'education':('образование','education'),'language':('язык','language'),
 'artificial-intelligence':('ии','ai'),'loneliness':('одиночество','loneliness'),'mastery':('мастерство','mastery'),
 'digital-ethics':('цифровая-этика','digital-ethics'),'identity':('идентичность','identity')}
TYPE = {'film':('фильм','film'),'series':('сериал','series'),'novella':('повесть','novella')}
FIX = {'ru': {'media-library':'раздел/медиатека','об_авторе':'раздел/об-авторе','лекции':'раздел/лекции','сотрудничество':'раздел/сотрудничество',
              'образ_будущего':'тема/образ-будущего','введение':'тип/введение','личная_история':'тип/личная-история','работа_и_учеба':'тема/работа-и-учёба'},
       'en': {'media-library':'section/media-library','about':'section/about','talks':'section/talks','work_with_me':'section/work-with-me',
              'images_of_the_future':'theme/images-of-the-future','introduction':'type/introduction','personal_story':'type/personal-story',
              'work_and_education':'theme/work-and-education'}}
def map_tag(t, lang, path):
    if '/' in t: return t
    i = 0 if lang == 'ru' else 1
    if t in ('book', 'книга'):
        media = 'media' in path or 'mediateka' in path
        return (('тип/книга','type/book') if media else ('раздел/книга','section/book'))[i]
    if t in TYPE: return ('тип/','type/')[i] + TYPE[t][i]
    if t in THEME: return ('тема/','theme/')[i] + THEME[t][i]
    if t in FIX[lang]: return FIX[lang][t]
    return t
n = 0
for f in glob.glob(os.path.join(REPO, 'content/**/*.md'), recursive=True):
    s = open(f, encoding='utf-8').read()
    m = re.match(r'---\n(.*?)\n---', s, re.S)
    if not m: continue
    fm = m.group(1)
    lang = 'en' if '/content/en/' in f else 'ru'
    def repl(mm):
        tags = re.findall(r'  - (.*)', mm.group(1)); new = []
        for t in tags:
            x = map_tag(t.strip(), lang, f)
            if x not in new: new.append(x)
        return 'tags:\n' + ''.join(f'  - {x}\n' for x in new)
    fm2 = re.sub(r'^tags:\n((?:  - .*\n?)+)', repl, fm + '\n', flags=re.M).rstrip('\n')
    if fm2 != fm:
        open(f, 'w', encoding='utf-8').write('---\n' + fm2 + '\n---' + s[m.end():]); n += 1
print('retagged', n)
