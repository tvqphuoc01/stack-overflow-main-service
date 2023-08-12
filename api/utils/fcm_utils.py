from typing import Any
from firebase_admin import messaging


class FcmUtils:
    def send_to_token(self, registration_token, title, body, data=None) -> Any:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data,
            token=registration_token
        )
        response = messaging.send(message)
        print(response)
        return response

    # send_to_token_multicast
    # Send a message to a specific tokens
    # registration_tokens: The tokens to send the message to
    # data: The data to send to the tokens
    def send_to_token_multicast(self, registration_tokens, title, body, data=None) -> Any:
        # registration_tokens has to be a list
        assert isinstance(registration_tokens, list)

        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data,
            tokens=registration_tokens
        )
        response = messaging.send_multicast(message)
        print(response)
        # See the BatchResponse reference documentation
        # for the contents of response.
        return response

    # send_to_topic
    # Send a message to a topic
    # topic: The topic to send the message to
    # data: The data to send to the topic
    # {
    #   'score': '850',
    #   'time': '2:45',
    # },
    # example
    def send_to_topic(self, topic, title, body, data=None) -> Any:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data,
            topic=topic
        )
        response = messaging.send(message)
        print(response)
        # Response is a message ID string.
        return response
