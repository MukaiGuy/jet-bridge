from collections import OrderedDict

import math
import tornado.web

from paginators.pagination import Pagination
from responses.base import Response


class PageNumberPagination(Pagination):
    page_size = 20
    page_query_param = 'page'
    page_size_query_param = None
    max_page_size = None

    def paginate_queryset(self, queryset, handler):
        page_number = self.get_page_number(handler)
        if not page_number:
            return None

        page_size = self.get_page_size(handler)
        if not page_size:
            return None

        self.count = queryset.count()
        self.page_size = page_size

        queryset = queryset.offset((page_number - 1) * page_size).limit(page_size)

        return list(queryset)

    def get_pages_count(self):
        return math.ceil(self.count / self.page_size)

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
            ('num_pages', self.get_pages_count()),
            ('per_page', self.page_size),
        ]))

    def get_page_number(self, handler):
        try:
            result = int(handler.get_argument(self.page_query_param))
            return max(result, 1)
        except (tornado.web.MissingArgumentError, ValueError):
            return 1

    def get_page_size(self, handler):
        if self.page_size_query_param:
            try:
                result = int(handler.get_argument(self.page_size_query_param))
                result = max(result, 1)

                if self.max_page_size:
                    result = min(result, self.max_page_size)

                return result
            except (tornado.web.MissingArgumentError, ValueError):
                pass

        return self.page_size

    def get_next_link(self):
        pass
        # if not self.page.has_next():
        #     return None
        # url = self.request.build_absolute_uri()
        # page_number = self.page.next_page_number()
        # return replace_query_param(url, self.page_query_param, page_number)

    def get_previous_link(self):
        pass
        # if not self.page.has_previous():
        #     return None
        # url = self.request.build_absolute_uri()
        # page_number = self.page.previous_page_number()
        # if page_number == 1:
        #     return remove_query_param(url, self.page_query_param)
        # return replace_query_param(url, self.page_query_param, page_number)
