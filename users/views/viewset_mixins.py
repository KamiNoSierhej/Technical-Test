from django.http import Http404


class GetObjectMixin:
    """
    Get first object filtered out by backend filters from queryset or raise 404
    """

    def get_object(self):
        obj = self.filter_queryset(self.get_queryset()).first()

        if obj:
            return obj

        raise Http404
