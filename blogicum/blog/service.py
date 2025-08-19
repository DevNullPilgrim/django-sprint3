from .constants import STR_REPR_MAX_LENGTH


def _short(text: str):
    return text if len(text) <= STR_REPR_MAX_LENGTH else f'{
        text[:STR_REPR_MAX_LENGTH - 1]
    }…'
