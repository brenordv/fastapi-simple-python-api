from fastapi import APIRouter

from data_fetcher.news_fetcher import fetch_news_article


def configure_news_articles_endpoints(prefix):
    news_endpoints = APIRouter(prefix=f"{prefix}/news", tags=["News"])

    @news_endpoints.get("/", status_code=200,
                      summary="The latest news headlines for Canada.")
    async def latest_glucose_value_endpoint():
        """
        The latest news headlines for Canada.
        """

        news = fetch_news_article()
        return news

    return news_endpoints
