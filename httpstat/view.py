from httpstat import app
from flask import (
    jsonify,
    request,
    make_response,
)


@app.route("/<path:path>")
def resp_status(path):
    req_headers = request.headers
    # Default is json response. Response text if assign accept: text/plain in headers.
    is_json = req_headers.get("Accept") != "text/plain"
    try:
        status_code = int(path)
        if status_code > 599:
            raise ValueError()

        data = {"status_code": status_code} if is_json else str(status_code)
        resp = handle_resp(data, is_json=is_json)
    except Exception:
        status_code = 500
        err_msg = f"Invalid status code '{path}'"
        errors = {"errors": err_msg} if is_json else err_msg
        resp = handle_resp(errors, is_json=is_json)

    return resp, status_code


def handle_resp(data, is_json=True):
    if is_json:
        resp = jsonify(data)
        resp.headers = {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        }
    else:
        resp = make_response(data)

    return resp
