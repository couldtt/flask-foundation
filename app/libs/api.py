import difflib
import sys

import re
from celery import current_app
from flask import got_request_exception, request
from flask_restful import Api, http_status_message
from werkzeug.datastructures import Headers
from werkzeug.exceptions import HTTPException


class CustomApi(Api):
    def handle_error(self, e):
        got_request_exception.send(current_app._get_current_object(), exception=e)

        if not isinstance(e, HTTPException) and current_app.propagate_exceptions:
            exc_type, exc_value, tb = sys.exc_info()
            if exc_value is e:
                raise
            else:
                raise e

        headers = Headers()
        if isinstance(e, HTTPException):
            code = e.code
            default_data = {
                'message': getattr(e, 'description', http_status_message(code))
            }
            headers = e.get_response().headers

        else:
            code = 500
            default_data = {
                'message': http_status_message(code),
            }

        # Werkzeug exceptions generate a content-length header which is added
        # to the response in addition to the actual content-length header
        # https://github.com/flask-restful/flask-restful/issues/534
        remove_headers = ('Content-Length',)

        for header in remove_headers:
            headers.pop(header, None)

        data = getattr(e, 'data', default_data)

        if code >= 500:
            exc_info = sys.exc_info()
            if exc_info[1] is None:
                exc_info = None
            current_app.log_exception(exc_info)

        help_on_404 = current_app.config.get("ERROR_404_HELP", True)
        if code == 404 and help_on_404:
            rules = dict([(re.sub('(<.*>)', '', rule.rule), rule.rule)
                          for rule in current_app.url_map.iter_rules()])
            close_matches = difflib.get_close_matches(request.path, rules.keys())
            if close_matches:
                # If we already have a message, add punctuation and continue it.
                if "message" in data:
                    data["message"] = data["message"].rstrip('.') + '. '
                else:
                    data["message"] = ""

                data['message'] += 'You have requested this URI [' + request.path + \
                                   '] but did you mean ' + \
                                   ' or '.join((
                                       rules[match] for match in close_matches)
                                   ) + ' ?'

        error_cls_name = type(e).__name__
        if error_cls_name in self.errors:
            custom_data = self.errors.get(error_cls_name, {})
            code = custom_data.get('status', 500)
            data.update(custom_data)

        if code == 406 and self.default_mediatype is None:
            # if we are handling NotAcceptable (406), make sure that
            # make_response uses a representation we support as the
            # default mediatype (so that make_response doesn't throw
            # another NotAcceptable error).
            supported_mediatypes = list(self.representations.keys())
            fallback_mediatype = supported_mediatypes[0] if supported_mediatypes else "text/plain"
            resp = self.make_response(
                data,
                code,
                headers,
                fallback_mediatype=fallback_mediatype
            )
        else:
            resp = self.make_response(data, code, headers)

        if code == 401:
            resp = self.unauthorized(resp)
        return resp
