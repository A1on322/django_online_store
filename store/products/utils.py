class DataMixxin:
    title_page = None
    cat_selected = None
    paginate_by = 6
    extra_context = {}

    def __init__(self):
        if self.title_page:
           self.extra_context['title'] = self.title_page

        if self.cat_selected is not None:
            self.extra_context['cat_selected'] = self.cat_selected