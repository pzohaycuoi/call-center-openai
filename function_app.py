import azure.functions as func
import logging
import common


# Setup log config
common.logger_config()
logger = logging.getLogger("file")

# Functionapp initiate
app = func.FunctionApp()


@common.log_function_call
@app.function_name(name="BlobEvent")
def test_function(req: func.HttpRequest) -> func.HttpResponse:
    logger.debug(req)
    return func.HttpResponse(req, status_code=200)

    # name = req.params.get('name')
    # if not name:
    #     try:
    #         req_body = req.get_json()
    #     except ValueError:
    #         pass
    #     else:
    #         name = req_body.get('name')

    # if name:
    #     return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    # else:
    #     return func.HttpResponse(
    #         "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
    #         status_code=200
    #     )
