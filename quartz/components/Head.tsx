import { i18n } from "../i18n"
import { FullSlug, getFileExtension, joinSegments, pathToRoot, simplifySlug } from "../util/path"
import { CSSResourceToStyleElement, JSResourceToScriptElement } from "../util/resources"
import { googleFontHref, googleFontSubsetHref } from "../util/theme"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { unescapeHTML } from "../util/escape"
import { CustomOgImagesEmitterName } from "../../.quartz/plugins"
export default (() => {
  const Head: QuartzComponent = ({
    cfg,
    fileData,
    externalResources,
    ctx,
  }: QuartzComponentProps) => {
    const frontmatter = (fileData.frontmatter ?? {}) as Record<string, unknown>
    const titleSuffix = cfg.pageTitleSuffix ?? ""
    const pageTitle =
      typeof frontmatter.seoTitle === "string"
        ? frontmatter.seoTitle
        : (fileData.frontmatter?.title ?? i18n(cfg.locale).propertyDefaults.title)
    const title = pageTitle + titleSuffix
    const description =
      fileData.frontmatter?.socialDescription ??
      fileData.frontmatter?.description ??
      unescapeHTML(fileData.description?.trim() ?? i18n(cfg.locale).propertyDefaults.description)

    const { css, js, additionalHead } = externalResources

    const url = new URL(`https://${cfg.baseUrl ?? "example.com"}`)
    const path = url.pathname as FullSlug
    const baseDir = fileData.slug === "404" ? path : pathToRoot(fileData.slug!)
    const iconPath = joinSegments(baseDir, "static/icon.png")

    const simplifiedSlug = fileData.slug ? simplifySlug(fileData.slug) : "/"
    const pagePath = simplifiedSlug === "/" ? "/" : `/${simplifiedSlug}`
    const socialUrl =
      fileData.slug === "404" ? url.toString() : new URL(pagePath, url.origin).toString()

    const rawTranslations = frontmatter.translations
    const translations =
      rawTranslations && typeof rawTranslations === "object" && !Array.isArray(rawTranslations)
        ? Object.entries(rawTranslations as Record<string, unknown>).filter(
            (entry): entry is [string, string] => typeof entry[1] === "string",
          )
        : []
    const language = typeof frontmatter.lang === "string" ? frontmatter.lang : undefined
    const openGraphLocale =
      language === "ru" ? "ru_RU" : language === "en" ? "en_US" : language?.replace("-", "_")
    const absoluteTranslationUrl = (href: string) =>
      new URL(href.startsWith("/") ? href : `/${href}`, url.origin).toString()

    const usesCustomOgImage = ctx.cfg.plugins.emitters.some(
      (e) => e.name === CustomOgImagesEmitterName,
    )
    const ogImageDefaultPath = `https://${cfg.baseUrl}/static/og-image.png`

    const coreStylesheet = css[0]?.content
    const coreScript = js.find(
      (r) => r.loadTime === "beforeDOMReady" && r.contentType === "external",
    )

    return (
      <head>
        <title>{title}</title>
        <meta charSet="utf-8" />
        {coreStylesheet && <link rel="preload" href={coreStylesheet} as="style" />}
        {coreScript && coreScript.contentType === "external" && (
          <link rel="preload" href={coreScript.src} as="script" />
        )}
        {cfg.theme.cdnCaching && cfg.theme.fontOrigin === "googleFonts" && (
          <>
            <link rel="preconnect" href="https://fonts.googleapis.com" />
            <link rel="preconnect" href="https://fonts.gstatic.com" />
            <link rel="stylesheet" href={googleFontHref(cfg.theme)} />
            {cfg.theme.typography.title && (
              <link rel="stylesheet" href={googleFontSubsetHref(cfg.theme, cfg.pageTitle)} />
            )}
          </>
        )}
        <link rel="preconnect" href="https://cdnjs.cloudflare.com" crossOrigin="anonymous" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />

        <meta name="og:site_name" content={cfg.pageTitle}></meta>
        <meta property="og:title" content={title} />
        <meta property="og:type" content="website" />
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content={title} />
        <meta name="twitter:description" content={description} />
        <meta property="og:description" content={description} />
        <meta property="og:image:alt" content={description} />

        {!usesCustomOgImage && (
          <>
            <meta property="og:image" content={ogImageDefaultPath} />
            <meta property="og:image:url" content={ogImageDefaultPath} />
            <meta name="twitter:image" content={ogImageDefaultPath} />
            <meta
              property="og:image:type"
              content={`image/${getFileExtension(ogImageDefaultPath) ?? "png"}`}
            />
          </>
        )}

        {cfg.baseUrl && (
          <>
            <meta property="twitter:domain" content={cfg.baseUrl}></meta>
            <meta property="og:url" content={socialUrl}></meta>
            <meta property="twitter:url" content={socialUrl}></meta>
            {fileData.slug !== "404" && <link rel="canonical" href={socialUrl} />}
            {translations.map(([translationLanguage, href]) => (
              <link
                rel="alternate"
                hreflang={translationLanguage}
                href={absoluteTranslationUrl(href)}
              />
            ))}
            {translations.some(([translationLanguage]) => translationLanguage === "ru") && (
              <link
                rel="alternate"
                hreflang="x-default"
                href={absoluteTranslationUrl(
                  translations.find(([translationLanguage]) => translationLanguage === "ru")![1],
                )}
              />
            )}
            {openGraphLocale && <meta property="og:locale" content={openGraphLocale} />}
          </>
        )}

        <link rel="icon" href={iconPath} />
        <meta name="description" content={description} />
        <meta name="generator" content="Quartz" />

        {css.map((resource) => CSSResourceToStyleElement(resource, true))}
        {js
          .filter((resource) => resource.loadTime === "beforeDOMReady")
          .map((res) => JSResourceToScriptElement(res, true))}
        {additionalHead.map((resource) => {
          if (typeof resource === "function") {
            return resource(fileData)
          } else {
            return resource
          }
        })}
      </head>
    )
  }

  return Head
}) satisfies QuartzComponentConstructor
