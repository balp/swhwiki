def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('wiki_view', '/')
    config.add_route('wikipage_add', '/add')
    config.add_route('wikipage_view', '/w/{uid}')
    config.add_route('wikipage_edit', '/w/{uid}/edit')
    config.add_static_view('deform_static', 'deform:static/')
