import re

_CAMEL_TO_SNAKE_PATTERN = re.compile(r'(?<!^)(?=[A-Z])')


def camel_to_snake(name: str) -> str:  # TODO move to utils
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return _CAMEL_TO_SNAKE_PATTERN.sub('_', name).lower()


def snake_to_camel(name: str) -> str:  # TODO move to utils
    return ''.join(word.title() for word in name.split('_'))
