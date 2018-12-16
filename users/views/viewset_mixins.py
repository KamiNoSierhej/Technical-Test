from django.http import Http404


class GetObjectMixin:
    def get_object(self):
        obj = self.filter_queryset(self.get_queryset()).first()

        if obj:
            return obj

        raise Http404
