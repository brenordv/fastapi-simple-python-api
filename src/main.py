from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from endpoints.glucose_monitor_endpoints import configure_glucose_monitor_endpoints
from endpoints.messaging_endpoints import configure_messaging_endpoints
from endpoints.news_endpoints import configure_news_articles_endpoints
from endpoints.pdf_endpoints import configure_pdf_endpoints
from endpoints.system_endpoints import configure_system_endpoints
from utils.env import CORS_ALLOWED_ORIGINS

app = FastAPI(
    title="RVerse API",
    version="1.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    summary="General purpose API for RVerse.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],    # Allows all HTTP methods
    allow_headers=["*"],    # Allows all headers
)

api_prefix_v1 = "/api/v1"

# Some endpoints depend on environment variables, so they will only be available if the required configuration is done.
# Worst case scenario, you'll only have the PDF endpoints available.
endpoints = [
    configure_system_endpoints(api_prefix_v1),
    configure_messaging_endpoints(api_prefix_v1),
    configure_pdf_endpoints(api_prefix_v1),
    configure_glucose_monitor_endpoints(api_prefix_v1),
    configure_news_articles_endpoints(api_prefix_v1)
]

for endpoint in endpoints:
    if endpoint is None:
        continue
    app.include_router(endpoint)
