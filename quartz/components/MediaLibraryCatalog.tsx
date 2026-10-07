import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

type CatalogItem = {
  title: string
  href: string
  type: "film" | "book"
  year: number
  credit: string
  domains: string[]
  scenario: string
  trends: string[]
  description: string
}

const filterScript = String.raw`
(() => {
  const script = document.currentScript
  const root = script?.closest(".media-library-catalog")
  if (!root || root.dataset.ready === "true") return
  root.dataset.ready = "true"

  const rows = [...root.querySelectorAll("tbody tr[data-media-row]")]
  const search = root.querySelector("[data-filter-search]")
  const type = root.querySelector("[data-filter-type]")
  const domain = root.querySelector("[data-filter-domain]")
  const scenario = root.querySelector("[data-filter-scenario]")
  const trend = root.querySelector("[data-filter-trend]")
  const yearFrom = root.querySelector("[data-filter-year-from]")
  const yearTo = root.querySelector("[data-filter-year-to]")
  const reset = root.querySelector("[data-filter-reset]")
  const count = root.querySelector("[data-filter-count]")
  const empty = root.querySelector("[data-filter-empty]")
  const language = root.dataset.language || "ru"

  const normalize = (value) => (value || "").toLocaleLowerCase(language).trim()
  const includesValue = (values, selected) =>
    !selected || (values || "").split("|").includes(selected)

  const update = () => {
    const query = normalize(search.value)
    const from = Number(yearFrom.value) || 0
    const to = Number(yearTo.value) || Number.MAX_SAFE_INTEGER
    let visible = 0

    for (const row of rows) {
      const year = Number(row.dataset.year)
      const matches =
        (!query || normalize(row.dataset.search).includes(query)) &&
        (!type.value || row.dataset.type === type.value) &&
        includesValue(row.dataset.domains, domain.value) &&
        (!scenario.value || row.dataset.scenario === scenario.value) &&
        includesValue(row.dataset.trends, trend.value) &&
        year >= from &&
        year <= to

      row.hidden = !matches
      if (matches) visible += 1
    }

    count.textContent =
      language === "ru"
        ? "Найдено: " + visible + " из " + rows.length
        : "Showing " + visible + " of " + rows.length
    empty.hidden = visible !== 0
  }

  for (const control of [search, type, domain, scenario, trend, yearFrom, yearTo]) {
    control.addEventListener(
      control === search || control === yearFrom || control === yearTo ? "input" : "change",
      update,
    )
  }

  reset.addEventListener("click", () => {
    search.value = ""
    type.value = ""
    domain.value = ""
    scenario.value = ""
    trend.value = ""
    yearFrom.value = ""
    yearTo.value = ""
    update()
    search.focus()
  })

  update()
})()
`

const uniqueSorted = (values: string[], locale: string) =>
  [...new Set(values.filter(Boolean))].sort((first, second) =>
    first.localeCompare(second, locale, { sensitivity: "base" }),
  )

export default (() => {
  const MediaLibraryCatalog: QuartzComponent = ({ fileData, allFiles }: QuartzComponentProps) => {
    const slug = fileData.slug ?? ""
    const isRussian = slug === "mediateka/index"
    const isEnglish = slug === "en/media-library/index"

    if (!isRussian && !isEnglish) return null

    const language = isRussian ? "ru" : "en"
    const locale = isRussian ? "ru" : "en"
    const prefixes = isRussian
      ? ["mediateka/filmy/", "mediateka/knigi/"]
      : ["en/media-library/films/", "en/media-library/books/"]

    const items: CatalogItem[] = allFiles
      .filter((page) => {
        const frontmatter = (page.frontmatter ?? {}) as Record<string, unknown>
        return (
          prefixes.some((prefix) => page.slug?.startsWith(prefix)) &&
          (frontmatter.media_type === "film" || frontmatter.media_type === "book")
        )
      })
      .map((page) => {
        const frontmatter = (page.frontmatter ?? {}) as Record<string, unknown>
        const type: CatalogItem["type"] = frontmatter.media_type === "book" ? "book" : "film"
        const domains = Array.isArray(frontmatter.life_domains)
          ? frontmatter.life_domains.filter((value): value is string => typeof value === "string")
          : []
        const trends = Array.isArray(frontmatter.macrotrends)
          ? frontmatter.macrotrends.filter((value): value is string => typeof value === "string")
          : []

        return {
          title: typeof frontmatter.title === "string" ? frontmatter.title : (page.slug ?? ""),
          href: `/${page.slug}`,
          type,
          year: Number(frontmatter.year) || 0,
          credit:
            typeof frontmatter.director === "string"
              ? frontmatter.director
              : typeof frontmatter.author === "string"
                ? frontmatter.author
                : "",
          domains,
          scenario: typeof frontmatter.scenario === "string" ? frontmatter.scenario : "",
          trends,
          description: typeof frontmatter.description === "string" ? frontmatter.description : "",
        }
      })
      .sort((first, second) =>
        first.title.localeCompare(second.title, locale, { sensitivity: "base" }),
      )

    const domains = uniqueSorted(
      items.flatMap((item) => item.domains),
      locale,
    )
    const scenarios = uniqueSorted(
      items.map((item) => item.scenario),
      locale,
    )
    const trends = uniqueSorted(
      items.flatMap((item) => item.trends),
      locale,
    )
    const years = items.map((item) => item.year).filter((year) => year > 0)
    const minimumYear = Math.min(...years)
    const maximumYear = Math.max(...years)

    const labels = isRussian
      ? {
          heading: "Каталог",
          search: "Поиск",
          searchPlaceholder: "Название, автор или режиссёр",
          type: "Тип",
          allTypes: "Все типы",
          films: "Фильмы и сериалы",
          books: "Книги",
          domain: "Сфера жизни",
          allDomains: "Все сферы",
          scenario: "Сценарий",
          allScenarios: "Все сценарии",
          trend: "Макротренд",
          allTrends: "Все макротренды",
          yearFrom: "Год от",
          yearTo: "Год до",
          reset: "Сбросить фильтры",
          title: "Название",
          year: "Год",
          creator: "Автор / режиссёр",
          why: "Зачем смотреть или читать",
          empty: "По выбранным параметрам ничего не найдено.",
        }
      : {
          heading: "Catalog",
          search: "Search",
          searchPlaceholder: "Title, author, or director",
          type: "Type",
          allTypes: "All types",
          films: "Films and series",
          books: "Books",
          domain: "Life domain",
          allDomains: "All domains",
          scenario: "Scenario",
          allScenarios: "All scenarios",
          trend: "Macrotrend",
          allTrends: "All macrotrends",
          yearFrom: "Year from",
          yearTo: "Year to",
          reset: "Reset filters",
          title: "Title",
          year: "Year",
          creator: "Author / director",
          why: "Why watch or read",
          empty: "No works match the selected filters.",
        }

    return (
      <section class="media-library-catalog" data-language={language}>
        <h2>{labels.heading}</h2>
        <div class="media-library-filters" aria-label={labels.heading}>
          <label class="media-filter-search">
            <span>{labels.search}</span>
            <input
              type="search"
              placeholder={labels.searchPlaceholder}
              autocomplete="off"
              data-filter-search
            />
          </label>
          <label>
            <span>{labels.type}</span>
            <select data-filter-type>
              <option value="">{labels.allTypes}</option>
              <option value="film">{labels.films}</option>
              <option value="book">{labels.books}</option>
            </select>
          </label>
          <label>
            <span>{labels.domain}</span>
            <select data-filter-domain>
              <option value="">{labels.allDomains}</option>
              {domains.map((domain) => (
                <option value={domain}>{domain}</option>
              ))}
            </select>
          </label>
          <label>
            <span>{labels.scenario}</span>
            <select data-filter-scenario>
              <option value="">{labels.allScenarios}</option>
              {scenarios.map((scenario) => (
                <option value={scenario}>{scenario}</option>
              ))}
            </select>
          </label>
          <label>
            <span>{labels.trend}</span>
            <select data-filter-trend>
              <option value="">{labels.allTrends}</option>
              {trends.map((trend) => (
                <option value={trend}>{trend}</option>
              ))}
            </select>
          </label>
          <label>
            <span>{labels.yearFrom}</span>
            <input
              type="number"
              min={minimumYear}
              max={maximumYear}
              placeholder={String(minimumYear)}
              data-filter-year-from
            />
          </label>
          <label>
            <span>{labels.yearTo}</span>
            <input
              type="number"
              min={minimumYear}
              max={maximumYear}
              placeholder={String(maximumYear)}
              data-filter-year-to
            />
          </label>
          <button type="button" class="media-filter-reset" data-filter-reset>
            {labels.reset}
          </button>
        </div>

        <p class="media-filter-count" data-filter-count aria-live="polite">
          {isRussian
            ? `Найдено: ${items.length} из ${items.length}`
            : `Showing ${items.length} of ${items.length}`}
        </p>

        <div class="media-library-table-wrap">
          <table class="media-library-table">
            <thead>
              <tr>
                <th>{labels.title}</th>
                <th>{labels.type}</th>
                <th>{labels.year}</th>
                <th>{labels.creator}</th>
                <th>{labels.domain}</th>
                <th>{labels.scenario}</th>
                <th>{labels.trend}</th>
                <th>{labels.why}</th>
              </tr>
            </thead>
            <tbody>
              {items.map((item) => (
                <tr
                  data-media-row
                  data-type={item.type}
                  data-year={item.year}
                  data-domains={item.domains.join("|")}
                  data-scenario={item.scenario}
                  data-trends={item.trends.join("|")}
                  data-search={`${item.title} ${item.credit} ${item.description}`}
                >
                  <td data-label={labels.title}>
                    <a class="internal" href={item.href}>
                      {item.title}
                    </a>
                  </td>
                  <td data-label={labels.type}>
                    {item.type === "film" ? labels.films : labels.books}
                  </td>
                  <td data-label={labels.year}>{item.year}</td>
                  <td data-label={labels.creator}>{item.credit}</td>
                  <td data-label={labels.domain}>
                    <div class="media-chip-list">
                      {item.domains.map((domain) => (
                        <span class="media-chip">{domain}</span>
                      ))}
                    </div>
                  </td>
                  <td data-label={labels.scenario}>
                    <span class="media-chip media-chip-scenario">{item.scenario}</span>
                  </td>
                  <td data-label={labels.trend}>
                    <div class="media-chip-list">
                      {item.trends.map((trend) => (
                        <span class="media-chip">{trend}</span>
                      ))}
                    </div>
                  </td>
                  <td data-label={labels.why}>{item.description}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <p class="media-filter-empty" data-filter-empty hidden>
          {labels.empty}
        </p>
        <script dangerouslySetInnerHTML={{ __html: filterScript }} />
      </section>
    )
  }

  return MediaLibraryCatalog
}) satisfies QuartzComponentConstructor
