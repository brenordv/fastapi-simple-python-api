from fastapi import FastAPI

from endpoints.messaging_endpoints import configure_messaging_endpoints
from endpoints.pdf_endpoints import configure_pdf_endpoints
from endpoints.system_endpoints import configure_system_endpoints

app = FastAPI(
    title="RVerse API",
    version="1.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    summary="General purpose API for RVerse.")

api_prefix_v1 = "/api/v1"

# Some endpoints will only work with my setup, so I'll only include them if the environment is configured.
# Worst case scenario, you'll only have the PDF endpoints available.
system_endpoints = configure_system_endpoints(api_prefix_v1)
message_endpoints = configure_messaging_endpoints(api_prefix_v1)
pdf_endpoints = configure_pdf_endpoints(api_prefix_v1)


app.include_router(system_endpoints)
app.include_router(message_endpoints)
app.include_router(pdf_endpoints)
