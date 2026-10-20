
# CAP 931 - Competitor Research Agent

from research_agent import research_company


def research_competitors(competitor_urls):
    results = []

    for url in competitor_urls:
        url = url.strip()

        if not url:
            continue

        try:
            research = research_company(url)
            results.append(research)

        except Exception as error:
            results.append(
                f"Competitor URL: {url}\n"
                f"Research unavailable: {error}"
            )

    return "\n\n---\n\n".join(results)
