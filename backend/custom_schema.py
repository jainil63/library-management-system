from .metadata import Config


def modify_openapi_schema(openapi_schema):
    openapi_schema["info"]["license"] = Config.LICENSE_INFO

    if Config.FRONTEND_PATH:
        openapi_schema["paths"].update(Config.FRONTEND_PATH)
