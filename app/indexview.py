from flask_appbuilder.views import IndexView


class FABView(IndexView):
    """
        A simple view that implements the index for the site
    """
    index_template = 'index.html'
