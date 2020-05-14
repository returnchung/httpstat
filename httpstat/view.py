import json
from httpstat import app
from flask import (
    jsonify,
    request,
    make_response,
)


# Ignore to sorted response json with jsonify
app.config["JSON_SORT_KEYS"] = False


@app.route("/<path:path>")
def resp_status(path):
    req_headers = request.headers
    # Default is json response. Response text if assign accept: text/plain in headers.
    is_json = req_headers.get("Accept") != "text/plain"
    try:
        status_code = int(path)
        if status_code > 599:
            raise ValueError()

        data = (
            {"statusCode": status_code} if is_json else f"statusCode: {status_code}"
        )
        resp = handle_resp(data, is_json=is_json)
    except Exception:
        status_code = 500
        err_msg = f"Invalid statusCode '{path}'"
        errors = {"errors": err_msg} if is_json else err_msg
        resp = handle_resp(errors, is_json=is_json)

    return resp, status_code


@app.route("/detail", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
def resp_detail():
    data = dict()
    data["method"] = request.method
    data["headers"] = {k: v for k, v in request.headers}
    data["body"] = get_request_body(request)
    data["args"] = {k: v for k, v in request.args.items()}
    resp = handle_resp(data)
    return resp, 200


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


def get_request_body(request, is_json=True):
    if request.content_type == "application/x-www-form-urlencoded":
        body = request.form.to_dict()
        return body

    body = request.get_data()
    if is_json:
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            body = body.decode("UTF-8")
    else:
        body = body.decode("UTF-8")

    return body
