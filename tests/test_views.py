from swhwiki.views.default import WikiViews
from swhwiki.views.notfound import notfound_view


def test_notfound_view(app_request):
    info = notfound_view(app_request)
    assert app_request.response.status_int == 404
    assert info == {}


def test_home_view(app_request):
    inst = WikiViews(app_request)
    response = inst.wiki_view()
    assert len(list(response['pages'])) == 1