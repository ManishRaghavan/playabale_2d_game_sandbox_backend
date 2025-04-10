from fastapi.responses import JSONResponse
from fastapi import Request
import traceback


def handle_exception(e: Exception, message: str = "An error occurred"):
    print("[Exception]", traceback.format_exc())

    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": message,
            "data": {
                "error": str(e)
            }
        }
    )
