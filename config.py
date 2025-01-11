import os

class Config:
    BASE_URL = "https://citstudentportal.org"
    API_TITLE = "cit-results-api"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.1.1"
    OPENAPI_JSON_PATH = "api-spec.json"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    API_SPEC_OPTIONS = {
        "security": [{"bearerAuth": []}],
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                    "description": "Enter your bearer token in the format: Bearer <token>"
                }
            }
        }
    }

    JWT_SECRET_KEY = os.getenv("SECRET_KEY", "luvuinfx") 
