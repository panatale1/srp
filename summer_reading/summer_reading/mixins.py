from django.core.paginator import Paginator
from django.http import Http404

class PaginationMixin(object):

    def build_page(self, results, results_per_page=25, page_no=0):
        if page_no == 0:
            try:
                page_no = int(self.request.GET.get('page', 1))
            except (TypeError, ValueError):
                raise Http404("Not a valid number for a page")

        if page_no < 1:
            raise Http404("No such page!")
        paginator = Paginator(results, results_per_page)
        try:
            page = paginator.page(page_no)
        except InvalidPage:
            raise Http404("No such page!")
        return paginator, page
