from requests import post, exceptions

from django.conf import settings


def credit_check_call(first_name, last_name):
    """Helper to get credit check from third party provider."""
    try:
        return post(
            settings.DATA_SOURCE_FOR_CREDIT_INFORMATION,
            json={'first_name': first_name, 'last_name': last_name},
            timeout=10
        ).json()
    except exceptions.ConnectionError:
        return {
            'Message': (
                'Connection error with 3rd party data provider '
                'occurred.'
            )
        }
    except ValueError:
        return {
            'Message': (
                'Wrong data supplied by 3rd party provider.'
            )
        }
