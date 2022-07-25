from pydantic import BaseModel


def children(instance, filter=BaseModel):
    """Recursively yield all children that are subclasses of filter."""
    for fieldname, field in instance:
        if isinstance(field, list):
            for f in field:
                if filter in f.__class__.__mro__:
                    yield f
                    yield from children(f)
                else:
                    print(f"Ignoring {f.__class__.__name__}")
        elif filter in field.__class__.__mro__:
            yield field
            yield from children(field)
