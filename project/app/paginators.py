from django.core.paginator import Paginator

class NegativeLabelPaginator(Paginator):

    def get_negative_page_range(self):
        mid = (self.num_pages // 2) + 1
        return [(i, i - mid) for i in range(1, self.num_pages + 1)]
