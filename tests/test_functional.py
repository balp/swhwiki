def test_root(testapp):
    res = testapp.get("/", status=200)
    assert b"<title>HiQ Testing Wiki Thing</title>" in res.body


def test_add_page(testapp):
    res = testapp.get("/add", status=200)
    assert b"<h1>Wiki</h1>" in res.body


def test_edit_page(testapp):
    res = testapp.get("/w/1/edit", status=200)
    assert b"<h1>Wiki</h1>" in res.body


def test_post_wiki(testapp):
    post = testapp.post(
        "/add",
        {"title": "New Page", "body": "New Page", "submit": "submit"},
        status=302,
    )
    res = testapp.get("/w/2", status=200)
    assert b"<h1>New Page</h1>" in res.body
    assert b"New Page" in res.body


def test_edit_wiki(testapp):
    testapp.post(
        "/w/1/edit",
        {"title": "New Page", "body": "New Page", "submit": "submit"},
        status=302,
    )
    res = testapp.get("/w/1", status=200)
    assert b"<h1>New Page</h1>" in res.body
    assert b"New Page" in res.body
