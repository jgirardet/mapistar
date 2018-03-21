# Third Party Libraries
from apistar.exceptions import NotFound
from pony import orm


def get_or_404(model, id: [str, int]):
    try:
        item = model[id]
    except orm.ObjectNotFound as e:
        raise NotFound
    return item
