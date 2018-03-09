# Third Party Libraries
from apistar.exceptions import BadRequest, Forbidden
from apistar.interfaces import Auth
from django.utils import timezone
from utils.shortcuts import get_or_404


class ActesWritePermission():

    def __init__(self, actesviews):
        self.actesviews = actesviews

    def has_permission(self, obj_id: int, auth: Auth):

        obj = get_or_404(self.actesviews.model, obj_id)

        if obj.created.date() != timezone.localdate():
            raise BadRequest("Observation can't be edited another day")

        if auth.user != obj.owner:
            raise Forbidden('Only owner can edit an Observation')

        return True
