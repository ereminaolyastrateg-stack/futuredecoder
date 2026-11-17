import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

// Общий каталог-таблица (по образцу медиатеки и сигналов): поиск, фильтры, клик по метке включает фильтр.
// Правило сада: большие наборы карточек показываем не списком, а такой таблицей.
// Виды: "mt" — карточки макротрендов по мирам; "sph" — варианты подсфер (сфера × подсфера × мир).

type Lang = "ru" | "en"
type Kind = "mt" | "sph"
type Row = { href: string; search: string; f: Record<string, string[]>; order: string; d: Record<string, any> }

const PAGES: Record<string, { kind: Kind; lang: Lang; prefix: string }> = {
  "materialy/makrotrendy/index": { kind: "mt", lang: "ru", prefix: "materialy/makrotrendy/" },
  "en/materials/macrotrends/index": { kind: "mt", lang: "en", prefix: "en/materials/macrotrends/" },
  "chetyre-mira/sfery/index": { kind: "sph", lang: "ru", prefix: "chetyre-mira/sfery/" },
  "en/four-worlds/life-spheres/index": { kind: "sph", lang: "en", prefix: "en/four-worlds/life-spheres/" },
}

const WORLDS: Record<string, { label: string; cls: string; n: number }> = {
  ЦС: { label: "ЦС · Мир автопилота", cls: "cs", n: 1 },
  ЦЗ: { label: "ЦЗ · Мир правил", cls: "ce", n: 2 },
  ДС: { label: "ДС · Мир автономии", cls: "ds", n: 3 },
  ДЗ: { label: "ДЗ · Мир сообщества", cls: "de", n: 4 },
  CS: { label: "CS · Autopilot world", cls: "cs", n: 1 },
  CE: { label: "CE · Rules world", cls: "ce", n: 2 },
  DS: { label: "DS · Autonomy world", cls: "ds", n: 3 },
  DE: { label: "DE · Community world", cls: "de", n: 4 },
}

const script = String.raw`
(() => {
  const root = document.currentScript?.closest(".card-catalog")
  if (!root || root.dataset.ready === "true") return
  root.dataset.ready = "true"
  const rows = [...root.querySelectorAll("tbody tr[data-row]")]
  const sels = [...root.querySelectorAll("select[data-f]")]
  const search = root.querySelector("[data-f-search]"), count = root.querySelector("[data-f-count]"),
    empty = root.querySelector("[data-f-empty]"), reset = root.querySelector("[data-f-reset]")
  const lang = root.dataset.language || "ru"
  const norm = (v) => (v || "").toLocaleLowerCase(lang).trim()
  const update = () => {
    const qv = norm(search.value); let n = 0
    for (const r of rows) {
      let ok = !qv || norm(r.dataset.search).includes(qv)
      for (const s of sels) if (ok && s.value) ok = (r.dataset["k" + s.dataset.f] || "").split("|").includes(s.value)
      r.hidden = !ok; if (ok) n++
    }
    count.textContent = lang === "ru" ? "Найдено: " + n + " из " + rows.length : "Showing " + n + " of " + rows.length
    empty.hidden = n !== 0
  }
  search.addEventListener("input", update)
  for (const s of sels) s.addEventListener("change", update)
  root.addEventListener("click", (e) => {
    const chip = e.target.closest("[data-chip]"); if (!chip) return
    const sel = root.querySelector('select[data-f="' + chip.dataset.chip + '"]')
    if (sel) { sel.value = chip.dataset.value; update(); sel.scrollIntoView({ block: "nearest" }) }
  })
  reset.addEventListener("click", () => {
    search.value = ""; for (const s of sels) s.value = s.dataset.preset || ""; update(); search.focus()
  })
  update()
})()
`

const strs = (v: unknown) => (Array.isArray(v) ? v.filter((x): x is string => typeof x === "string") : [])
const uniq = (values: string[], locale: string) =>
  [...new Set(values.filter(Boolean))].sort((a, b) => a.localeCompare(b, locale, { sensitivity: "base" }))

export default (() => {
  const CardCatalog: QuartzComponent = ({ fileData, allFiles }: QuartzComponentProps) => {
    const slug = fileData.slug ?? ""
    let conf = PAGES[slug]
    let preset: Record<string, string> = {}
    const fm = (fileData.frontmatter ?? {}) as Record<string, unknown>
    const tags = strs(fm.tags)
    if (!conf && (tags.includes("тип/сфера") || tags.includes("type/sphere"))) {
      const ru = slug.startsWith("chetyre-mira/")
      conf = PAGES[ru ? "chetyre-mira/sfery/index" : "en/four-worlds/life-spheres/index"]
      preset = { sphere: String(fm.title ?? "") }
    }
    if (!conf) return null
    const ru = conf.lang === "ru"
    const locale = conf.lang
    const files = allFiles.filter((p) => p.slug?.startsWith(conf.prefix))
    const rows: Row[] = []

    if (conf.kind === "mt") {
      for (const p of files) {
        const f = (p.frontmatter ?? {}) as Record<string, unknown>
        if (typeof f.essence !== "string") continue
        const sc = String(f.scenario ?? "")
        const mt = `${f.macrotrend_id ?? ""} · ${f.mt_name ?? ""}`
        const themes = strs(f.themes)
        rows.push({
          href: `/${p.slug}`,
          search: `${mt} ${f.essence} ${f.scene} ${themes.join(" ")} ${f.description ?? ""}`,
          f: { mt: [mt], scenario: [sc], theme: themes },
          order: `${f.macrotrend_id}-${WORLDS[sc]?.n ?? 9}`,
          d: { mt, sc, essence: f.essence, scene: f.scene, themes, signals: strs(f.related_signals).length || (Array.isArray(f.related_signals) ? f.related_signals.length : 0) },
        })
      }
    } else {
      for (const p of files) {
        const f = (p.frontmatter ?? {}) as Record<string, unknown>
        if (!Array.isArray(f.items)) continue
        const sc = String(f.scenario ?? "")
        const sphere = String(f.sphere ?? "")
        f.items.forEach((it: any, k: number) => {
          rows.push({
            href: `/${p.slug}#${it.anchor}`,
            search: `${sphere} ${it.sub} ${it.name} ${it.situation}`,
            f: { sphere: [sphere], sub: [it.sub], scenario: [sc], spend: strs(it.spend), give: strs(it.give) },
            order: `${String(f.sphere_order ?? 9).padStart(2, "0")}-${String(k).padStart(2, "0")}-${WORLDS[sc]?.n ?? 9}`,
            d: { sphere, sub: it.sub, sc, name: it.name, situation: it.situation, spend: strs(it.spend), give: strs(it.give) },
          })
        })
      }
    }
    rows.sort((a, b) => a.order.localeCompare(b.order, locale))
    if (!rows.length) return null

    const world = (c: string) => WORLDS[c]?.label ?? c
    const opts = (key: string) => {
      const vals = rows.flatMap((r) => r.f[key] ?? [])
      if (key === "scenario") return [...new Set(vals)].sort((a, b) => (WORLDS[a]?.n ?? 9) - (WORLDS[b]?.n ?? 9))
      if (key === "sphere" || key === "sub" || key === "mt") return [...new Set(vals)] // в порядке строк
      return uniq(vals, locale)
    }
    const chip = (key: string, v: string, cls = "") => (
      <button type="button" class={`media-chip ${cls}`} data-chip={key} data-value={v}>
        {key === "scenario" ? world(v) : v}
      </button>
    )
    const chips = (key: string, list: string[], cls = "") => <div class="media-chip-list">{list.map((v) => chip(key, v, cls))}</div>
    const worldChip = (sc: string) => chip("scenario", sc, `world-chip world-${WORLDS[sc]?.cls ?? ""}`)

    const T = ru
      ? { search: "Поиск", reset: "Сбросить фильтры", all: "Все", hint: "Нажмите на метку в таблице, чтобы отфильтровать по ней.", empty: "По выбранным параметрам ничего нет." }
      : { search: "Search", reset: "Reset filters", all: "All", hint: "Click a label in the table to filter by it.", empty: "Nothing matches the selected filters." }

    const spec =
      conf.kind === "mt"
        ? {
            heading: ru ? "Каталог макротрендов по мирам" : "Macrotrends by world",
            ph: ru ? "Макротренд, сцена, слово из описания" : "Macrotrend, scene, a word from the description",
            filters: [
              ["mt", ru ? "Макротренд" : "Macrotrend"],
              ["scenario", ru ? "Мир" : "World"],
              ["theme", ru ? "Тема" : "Theme"],
            ],
            cols: ru ? ["Макротренд", "Мир", "Суть в этом мире", "Сцена 2035", "Темы", "Сигналов"] : ["Macrotrend", "World", "Essence in this world", "2035 scene", "Themes", "Signals"],
            cells: (r: Row) => [
              <a class="internal" href={r.href}>{r.d.mt}</a>,
              worldChip(r.d.sc),
              r.d.essence,
              <a class="internal" href={r.href}>{r.d.scene}</a>,
              chips("theme", r.d.themes, "theme-chip"),
              r.d.signals || "—",
            ],
          }
        : {
            heading: ru ? "Каталог: сферы жизни в четырёх мирах" : "Catalog: life spheres in four worlds",
            ph: ru ? "Подсфера, вариант, слово из ситуации" : "Subsphere, option, a word from the situation",
            filters: [
              ["sphere", ru ? "Сфера" : "Sphere"],
              ["sub", ru ? "Подсфера" : "Subsphere"],
              ["scenario", ru ? "Мир" : "World"],
              ["spend", ru ? "Тратит" : "Spends"],
              ["give", ru ? "Даёт" : "Gives"],
            ],
            cols: ru ? ["Сфера", "Подсфера", "Мир", "Вариант", "Ситуация из жизни", "Тратит", "Даёт"] : ["Sphere", "Subsphere", "World", "Option", "Life situation", "Spends", "Gives"],
            cells: (r: Row) => [
              chips("sphere", [r.d.sphere]),
              chips("sub", [r.d.sub]),
              worldChip(r.d.sc),
              <a class="internal" href={r.href}>{r.d.name}</a>,
              r.d.situation,
              chips("spend", r.d.spend),
              chips("give", r.d.give, "theme-chip"),
            ],
          }

    const visible = rows.filter((r) => Object.entries(preset).every(([k, v]) => (r.f[k] ?? []).includes(v))).length

    return (
      <section class={`signal-catalog card-catalog media-library-catalog card-catalog-${conf.kind}`} data-language={conf.lang}>
        <h2>{spec.heading}</h2>
        <div class="media-library-filters signal-filters">
          <label class="media-filter-search">
            <span>{T.search}</span>
            <input type="search" placeholder={spec.ph} autocomplete="off" data-f-search />
          </label>
          {spec.filters.map(([key, label]) => (
            <label>
              <span>{label}</span>
              <select data-f={key} data-preset={preset[key] ?? ""}>
                <option value="">{T.all}</option>
                {opts(key).map((v) => (
                  <option value={v} selected={preset[key] === v}>
                    {key === "scenario" ? world(v) : v}
                  </option>
                ))}
              </select>
            </label>
          ))}
          <button type="button" class="media-filter-reset" data-f-reset>
            {T.reset}
          </button>
        </div>
        <p class="media-filter-count">
          <span data-f-count aria-live="polite">
            {ru ? `Найдено: ${visible} из ${rows.length}` : `Showing ${visible} of ${rows.length}`}
          </span>
          <span class="signal-hint"> · {T.hint}</span>
        </p>
        <div class="media-library-table-wrap">
          <table class="media-library-table signal-table">
            <thead>
              <tr>
                {spec.cols.map((c) => (
                  <th>{c}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => {
                const data: Record<string, string> = {}
                for (const [k, v] of Object.entries(r.f)) data[`data-k${k}`] = v.join("|")
                const hidden = !Object.entries(preset).every(([k, v]) => (r.f[k] ?? []).includes(v))
                return (
                  <tr data-row data-search={r.search} hidden={hidden} {...data}>
                    {spec.cells(r).map((c, i) => (
                      <td data-label={spec.cols[i]}>{c}</td>
                    ))}
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
        <p class="media-filter-empty" data-f-empty hidden>
          {T.empty}
        </p>
        <script dangerouslySetInnerHTML={{ __html: script }} />
      </section>
    )
  }
  return CardCatalog
}) satisfies QuartzComponentConstructor
