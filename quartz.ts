import { loadQuartzConfig, loadQuartzLayout } from "./quartz/plugins/loader/config-loader"
import * as ExternalPlugin from "./.quartz/plugins"
import type { ExplorerOptions } from "./.quartz/plugins"

ExternalPlugin.Explorer({
  filterFn: ((node) => {
    if (node.slugSegment === "tags") return false

    const firstSegment = node.slugSegments?.[0]
    const isEnglishPage = document.body.dataset.slug?.startsWith("en/") ?? false

    return isEnglishPage ? firstSegment === "en" : firstSegment !== "en"
  }) satisfies NonNullable<ExplorerOptions["filterFn"]>,
})

const config = await loadQuartzConfig()
export default config
export const layout = await loadQuartzLayout()
