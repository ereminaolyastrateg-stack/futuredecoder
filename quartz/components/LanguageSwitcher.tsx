import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

const languageLabels: Record<string, string> = {
  ru: "RU",
  en: "EN",
}

const languageOrder = ["ru", "en"]

export default (() => {
  const LanguageSwitcher: QuartzComponent = ({ fileData }: QuartzComponentProps) => {
    const frontmatter = (fileData.frontmatter ?? {}) as Record<string, unknown>
    const currentLanguage = typeof frontmatter.lang === "string" ? frontmatter.lang : "ru"
    const translations = frontmatter.translations

    if (!translations || typeof translations !== "object" || Array.isArray(translations)) {
      return null
    }

    const links = Object.entries(translations as Record<string, unknown>)
      .filter((entry): entry is [string, string] => typeof entry[1] === "string")
      .sort(([first], [second]) => {
        const firstIndex = languageOrder.indexOf(first)
        const secondIndex = languageOrder.indexOf(second)
        return (firstIndex === -1 ? 99 : firstIndex) - (secondIndex === -1 ? 99 : secondIndex)
      })

    if (links.length < 2) {
      return null
    }

    return (
      <nav class="language-switcher" aria-label="Language / Язык">
        {links.map(([language, href], index) => (
          <>
            {index > 0 && <span class="language-separator">/</span>}
            {language === currentLanguage ? (
              <span class="language-current" aria-current="page">
                {languageLabels[language] ?? language.toUpperCase()}
              </span>
            ) : (
              <a href={href} hreflang={language} lang={language}>
                {languageLabels[language] ?? language.toUpperCase()}
              </a>
            )}
          </>
        ))}
      </nav>
    )
  }

  return LanguageSwitcher
}) satisfies QuartzComponentConstructor
