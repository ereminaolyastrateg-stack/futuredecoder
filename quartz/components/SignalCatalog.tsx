import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

// Таблица-каталог сигналов (по образцу медиатеки): поиск и фильтры по миру, сфере, отрасли, теме, макротренду.

type Item = {
  id: string
  name: string
  title: string
  href: string
  scenario: string
  domains: string[]
  industries: string[]
  themes: string[]
  trends: string[]
  geography: string
  period: string
  description: string
}

const PAGES: Record<string, { lang: "ru" | "en"; prefix: string }> = {
  "materialy/signaly/index": { lang: "ru", prefix: "materialy/signaly/" },
  "materialy/signaly/obrazovanie/index": { lang: "ru", prefix: "materialy/signaly/obrazovanie/" },
  "materialy/signaly/education": { lang: "ru", prefix: "materialy/signaly/obrazovanie/" },
  "en/materials/signals/index": { lang: "en", prefix: "en/materials/signals/" },
  "en/materials/signals/education-signals/index": {
    lang: "en",
    prefix: "en/materials/signals/education-signals/",
  },
  "en/materials/signals/education": {
    lang: "en",
    prefix: "en/materials/signals/education-signals/",
  },
}

const WORLDS: Record<string, { ru: string; en: string; cls: string }> = {
  ЦС: { ru: "ЦС · Мир автопилота", en: "", cls: "cs" },
  ЦЗ: { ru: "ЦЗ · Мир правил", en: "", cls: "ce" },
  ДС: { ru: "ДС · Мир автономии", en: "", cls: "ds" },
  ДЗ: { ru: "ДЗ · Мир сообщества", en: "", cls: "de" },
  CS: { ru: "", en: "CS · Autopilot world", cls: "cs" },
  CE: { ru: "", en: "CE · Rules world", cls: "ce" },
  DS: { ru: "", en: "DS · Autonomy world", cls: "ds" },
  DE: { ru: "", en: "DE · Community world", cls: "de" },
}
const ORDER = ["ЦС", "ЦЗ", "ДС", "ДЗ", "CS", "CE", "DS", "DE"]

const script = String.raw`
(() => {
  const root = document.currentScript?.closest(".signal-catalog")
  if (!root || root.dataset.ready === "true") return
  root.dataset.ready = "true"
  const rows = [...root.querySelectorAll("tbody tr[data-row]")]
  const q = (s) => root.querySelector(s)
  const search = q("[data-f-search]"), scen = q("[data-f-scenario]"), dom = q("[data-f-domain]"),
    ind = q("[data-f-industry]"), theme = q("[data-f-theme]"), trend = q("[data-f-trend]"),
    reset = q("[data-f-reset]"), count = q("[data-f-count]"), empty = q("[data-f-empty]")
  const lang = root.dataset.language || "ru"
  const norm = (v) => (v || "").toLocaleLowerCase(lang).trim()
  const has = (list, v) => !v || (list || "").split("|").includes(v)
  const update = () => {
    const query = norm(search.value)
    let n = 0
    for (const r of rows) {
      const ok = (!query || norm(r.dataset.search).includes(query)) &&
        (!scen.value || r.dataset.scenario === scen.value) &&
        has(r.dataset.domains, dom.value) && has(r.dataset.industries, ind.value) &&
        has(r.dataset.themes, theme.value) && has(r.dataset.trends, trend.value)
      r.hidden = !ok
      if (ok) n++
    }
    count.textContent = lang === "ru" ? "Найдено: " + n + " из " + rows.length : "Showing " + n + " of " + rows.length
    empty.hidden = n !== 0
  }
  search.addEventListener("input", update)
  for (const c of [scen, dom, ind, theme, trend]) c.addEventListener("change", update)
  // клик по метке в таблице включает фильтр
  root.addEventListener("click", (e) => {
    const chip = e.target.closest("[data-chip]")
    if (!chip) return
    const sel = q("[data-f-" + chip.dataset.chip + "]")
    if (sel) { sel.value = chip.dataset.value; update(); sel.scrollIntoView({ block: "nearest" }) }
  })
  reset.addEventListener("click", () => {
    search.value = ""; for (const c of [scen, dom, ind, theme, trend]) c.value = ""; update(); search.focus()
  })
  update()
})()
`

const strs = (v: unknown) => (Array.isArray(v) ? v.filter((x): x is string => typeof x === "string") : [])
const uniq = (values: string[], locale: string) =>
  [...new Set(values.filter(Boolean))].sort((a, b) => a.localeCompare(b, locale, { sensitivity: "base" }))

export default (() => {
  const SignalCatalog: QuartzComponent = ({ fileData, allFiles }: QuartzComponentProps) => {
    const conf = PAGES[fileData.slug ?? ""]
    if (!conf) return null
    const ru = conf.lang === "ru"
    const locale = conf.lang

    const items: Item[] = allFiles
      .filter((p) => p.slug?.startsWith(conf.prefix) && (p.frontmatter as any)?.signal_type === "signal")
      .map((p) => {
        const f = (p.frontmatter ?? {}) as Record<string, unknown>
        const s = (k: string) => (typeof f[k] === "string" ? (f[k] as string) : "")
        return {
          id: s("signal_id"),
          name: s("name"),
          title: s("title"),
          href: `/${p.slug}`,
          scenario: s("scenario"),
          domains: strs(f.life_domains),
          industries: strs(f.industries),
          themes: strs(f.themes),
          trends: strs(f.macrotrends),
          geography: s("geography"),
          period: s("period"),
          description: s("description"),
        }
      })
      .sort((a, b) => a.id.localeCompare(b.id))

    const scenarios = ORDER.filter((c) => items.some((i) => i.scenario === c))
    const domains = uniq(items.flatMap((i) => i.domains), locale)
    const industries = uniq(items.flatMap((i) => i.industries), locale)
    const themes = uniq(items.flatMap((i) => i.themes), locale)
    const trends = uniq(items.flatMap((i) => i.trends), locale)
    const world = (c: string) => (WORLDS[c] ? (ru ? WORLDS[c].ru : WORLDS[c].en) : c)

    const L = ru
      ? {
          heading: "Каталог сигналов", search: "Поиск", ph: "Название, страна, слово из описания",
          scenario: "Мир", allS: "Все миры", domain: "Сфера жизни", allD: "Все сферы",
          industry: "Отрасль", allI: "Все отрасли", theme: "Тема", allT: "Все темы",
          trend: "Макротренд", allM: "Все макротренды", reset: "Сбросить фильтры",
          signal: "Сигнал", geo: "Где", when: "Когда", brief: "Коротко",
          empty: "По выбранным параметрам сигналов нет.", hint: "Нажмите на метку в таблице, чтобы отфильтровать по ней.",
        }
      : {
          heading: "Signal catalog", search: "Search", ph: "Name, country, a word from the description",
          scenario: "World", allS: "All worlds", domain: "Life domain", allD: "All domains",
          industry: "Industry", allI: "All industries", theme: "Theme", allT: "All themes",
          trend: "Macrotrend", allM: "All macrotrends", reset: "Reset filters",
          signal: "Signal", geo: "Where", when: "When", brief: "In brief",
          empty: "No signals match the selected filters.", hint: "Click a label in the table to filter by it.",
        }

    const chips = (list: string[], kind: string, extra = "") =>
      list.map((v) => (
        <button type="button" class={`media-chip ${extra}`} data-chip={kind} data-value={v}>
          {v}
        </button>
      ))

    return (
      <section class="signal-catalog media-library-catalog" data-language={conf.lang}>
        <h2>{L.heading}</h2>
        <div class="media-library-filters signal-filters">
          <label class="media-filter-search">
            <span>{L.search}</span>
            <input type="search" placeholder={L.ph} autocomplete="off" data-f-search />
          </label>
          <label>
            <span>{L.scenario}</span>
            <select data-f-scenario>
              <option value="">{L.allS}</option>
              {scenarios.map((c) => (
                <option value={c}>{world(c)}</option>
              ))}
            </select>
          </label>
          <label>
            <span>{L.domain}</span>
            <select data-f-domain>
              <option value="">{L.allD}</option>
              {domains.map((v) => (
                <option value={v}>{v}</option>
              ))}
            </select>
          </label>
          <label>
            <span>{L.industry}</span>
            <select data-f-industry>
              <option value="">{L.allI}</option>
              {industries.map((v) => (
                <option value={v}>{v}</option>
              ))}
            </select>
          </label>
          <label>
            <span>{L.theme}</span>
            <select data-f-theme>
              <option value="">{L.allT}</option>
              {themes.map((v) => (
                <option value={v}>{v}</option>
              ))}
            </select>
          </label>
          <label class="signal-filter-trend">
            <span>{L.trend}</span>
            <select data-f-trend>
              <option value="">{L.allM}</option>
              {trends.map((v) => (
                <option value={v}>{v}</option>
              ))}
            </select>
          </label>
          <button type="button" class="media-filter-reset" data-f-reset>
            {L.reset}
          </button>
        </div>
        <p class="media-filter-count">
          <span data-f-count aria-live="polite">
            {ru ? `Найдено: ${items.length} из ${items.length}` : `Showing ${items.length} of ${items.length}`}
          </span>
          <span class="signal-hint"> · {L.hint}</span>
        </p>
        <div class="media-library-table-wrap">
          <table class="media-library-table signal-table">
            <thead>
              <tr>
                <th>{L.signal}</th>
                <th>{L.scenario}</th>
                <th>{L.brief}</th>
                <th>{L.domain}</th>
                <th>{L.industry}</th>
                <th>{L.geo}</th>
                <th>{L.when}</th>
              </tr>
            </thead>
            <tbody>
              {items.map((i) => (
                <tr
                  data-row
                  data-scenario={i.scenario}
                  data-domains={i.domains.join("|")}
                  data-industries={i.industries.join("|")}
                  data-themes={i.themes.join("|")}
                  data-trends={i.trends.join("|")}
                  data-search={`${i.id} ${i.name} ${i.title} ${i.geography} ${i.description} ${i.themes.join(" ")}`}
                >
                  <td data-label={L.signal}>
                    <a class="internal" href={i.href}>
                      {i.name}
                    </a>
                    <div class="signal-id">{i.id}</div>
                  </td>
                  <td data-label={L.scenario}>
                    <button
                      type="button"
                      class={`media-chip world-chip world-${WORLDS[i.scenario]?.cls ?? ""}`}
                      data-chip="scenario"
                      data-value={i.scenario}
                    >
                      {world(i.scenario)}
                    </button>
                  </td>
                  <td data-label={L.brief}>
                    {i.description}
                    <div class="media-chip-list signal-themes">{chips(i.themes, "theme", "theme-chip")}</div>
                  </td>
                  <td data-label={L.domain}>
                    <div class="media-chip-list">{chips(i.domains, "domain")}</div>
                  </td>
                  <td data-label={L.industry}>
                    <div class="media-chip-list">{chips(i.industries, "industry")}</div>
                  </td>
                  <td data-label={L.geo}>{i.geography}</td>
                  <td data-label={L.when}>{i.period}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p class="media-filter-empty" data-f-empty hidden>
          {L.empty}
        </p>
        <script dangerouslySetInnerHTML={{ __html: script }} />
      </section>
    )
  }
  return SignalCatalog
}) satisfies QuartzComponentConstructor
