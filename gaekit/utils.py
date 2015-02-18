import os


def is_hosted():
    if 'SERVER_SOFTWARE' in os.environ \
            and not os.environ['SERVER_SOFTWARE'].startswith("Development"):
        return True
    return False
