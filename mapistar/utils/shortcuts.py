# Third Party Libraries
from apistar.exceptions import NotFound
from django.db import models
from django.http import Http404
from django.shortcuts import get_object_or_404


def get_or_404(model: models, id: [str, int]):
    try:
        item = get_object_or_404(model, id=id)
    except Http404 as e:
        raise NotFound(str(e))
    return item
