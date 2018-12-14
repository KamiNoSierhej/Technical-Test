from requests import post, exceptions

from django.conf import settings


def credit_check(first_name, last_name):
    """Helper to get credit check from third party provider."""
    payload = {
        'first_name': 'Luke',  # 'first_name': first_name
        'last_name': 'Voldemort',  # 'last_name': last_name
    }

    try:
        return post(
            settings.DATA_SOURCE_FOR_CREDIT_INFORMATION,
            json=payload,
            timeout=10
        ).json()
    except exceptions.ConnectionError:
        return {
            'message': (
                'Connection error with 3rd party data provider '
                'occurred.'
            )
        }
