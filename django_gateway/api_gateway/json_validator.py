import json

from django.core.handlers.wsgi import WSGIRequest

from api_gateway.models import InternalException
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
        "users_register": ["mailbox_address", "password", "username"]
    }

    def __init__(self, request: WSGIRequest, name: str):
        self.request: WSGIRequest = request
        self.name: str = name

    def check_keys(self, result):
        missing_fields = []
        for required_key in self.validation_vocabulary[self.name]:
            value = result.get(required_key, "field doesn't exist")
            if value == "field doesn't exist":
                missing_fields.append(required_key)
                continue
        return missing_fields

    def validate(self) -> dict:
        # Check and parse request body
        try:
            result = JSONParser().parse(self.request)
        except json.decoder.JSONDecodeError:
            raise InternalException({"status": 0, "error": "Some data is wrong."}, 422)

        # Check if all needed keys is present in request body
        missing_fields = self.check_keys(result)
        if missing_fields:
            raise InternalException({"status": 0, "error": f"Missing required fields: {', '.join(missing_fields)}"},
                                    422)

        # Recreate a dict with only needed fields
        validated_dict = {item: result[item] for item in self.validation_vocabulary[self.name]}

        return validated_dict
