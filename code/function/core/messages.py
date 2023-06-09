from pydantic import BaseSettings


class Messages(BaseSettings):
    # Base messages
    NO_API_KEY = "No API key provided."
    AUTH_REQ = "Authentication required."
    HTTP_500_DETAIL = "Internal server error."

    # Templates
    NO_VALID_PAYLOAD = "{} is not a valid payload."


messages = Messages()
