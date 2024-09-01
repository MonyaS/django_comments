import json
import re

from api_gateway.models import InternalException
from django.core.handlers.wsgi import WSGIRequest
from rest_framework.parsers import JSONParser


class JsonValidator:
    """
        A class to check if the request body is valid and if all the required fields for the request are present.

        validation_vocabulary - A dictionary representing a structure:
            - key is the internal name of the endpoint
            - value is a list of fields that must be present in the query

        Usage example:
            user_data = JsonValidator(request, "users_login").validate()

        Example explanation:
            Create an object of JsonValidator and give two parameters:
                request: WSGIRequest - incoming request
                name: str - name og internal endpoint

            If there are missing fields, an InternalException will be called specifying the fields that are missing.
            Alternatively, if the request body is not found or is corrupted, an InternalException error
                with HTTP status 422 will be raised.
            If the validation is successful, the .validate() method will return the dictionary
                from the fields specified in the required fields.
    """
    validation_vocabulary = {
        "users_login": ["mailbox_address", "password"],
        "users_register": ["mailbox_address", "password", "username"],
        "add_comment": ["home_page", "captcha", "text"]
    }

    def __init__(self, name: str, dict_data: dict = None, request: WSGIRequest = None):
        self.request: WSGIRequest = request
        self.data: dict = dict_data
        self.name: str = name

    def _check_keys(self, result):
        missing_fields = []
        for required_key in self.validation_vocabulary[self.name]:
            value = result.get(required_key, "field doesn't exist")
            if value == "field doesn't exist":
                missing_fields.append(required_key)
                continue
        return missing_fields

    def _check_json(self, json_data):
        # Check if all needed keys is present in request body
        missing_fields = self._check_keys(json_data)
        if missing_fields:
            raise InternalException({"status": 0, "error": f"Missing required fields: {', '.join(missing_fields)}"},
                                    422)

        # Recreate a dict with only needed fields
        validated_dict = {item: json_data[item] for item in self.validation_vocabulary[self.name]}

        return validated_dict

    def validate(self) -> dict:
        # Check and parse request body
        try:
            result = JSONParser().parse(self.request)
        except json.decoder.JSONDecodeError:
            raise InternalException({"status": 0, "error": "Some data is wrong."}, 422)

        return self._check_json(result)

    def validate_comment(self):
        self.data["home_page"] = self.data.get("home_page", "/")
        validated_data = self._check_json(self.data)

        # All allowed HTML tegs
        allowed_tags_pattern = r'''
                (
                    <a\s+href="[^"]*"\s+title="[^"]*">.*?</a> |
                    <code>.*?</code> |
                    <i>.*?</i> |
                    <strong>.*?</strong>
                )
            '''
        html_tags_pattern = r'<[^>]+>'

        # Find all HTML tags in the text
        all_tags = re.findall(html_tags_pattern, validated_data["text"])

        # Validate each tag
        for tag in all_tags:
            if not re.match(allowed_tags_pattern, tag, re.VERBOSE):
                raise InternalException({"status": 0, "error": "User text contains illegal tags."}, 422)

        return validated_data
