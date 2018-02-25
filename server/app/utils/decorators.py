"""
Helpful decorators for the masses.
"""
from flask import render_template


def render(template):
    def decorator(f):
        def wrapped(*args, **kwargs):
            response = f(*args, **kwargs)
            if response is None:
                response = {}
            return render_template(template, **response)
        return wrapped
    return decorator
