import colander
import deform.widget
from pyramid.httpexceptions import HTTPFound
from pyramid.security import forget, remember
from pyramid.view import forbidden_view_config, view_config

from ..models import DBSession, Page
from ..security import USERS, check_password


class WikiPage(colander.MappingSchema):
    title = colander.SchemaNode(colander.String())
    body = colander.SchemaNode(colander.String(), widget=deform.widget.RichTextWidget())


class WikiViews:
    def __init__(self, request):
        self.request = request
        self.logged_in = request.authenticated_userid

    @property
    def wiki_form(self):
        schema = WikiPage()
        return deform.Form(schema, buttons=("submit",))

    @property
    def reqts(self):
        return self.wiki_form.get_widget_resources()

    @view_config(route_name="wiki_view", renderer="swhwiki:templates/wiki_view.jinja2")
    def wiki_view(self):
        pages = DBSession.query(Page).order_by(Page.title)
        return dict(title="Wiki View", pages=pages)

    @view_config(
        route_name="wikipage_add",
        renderer="swhwiki:templates/wikipage_addedit.jinja2",
        permission="edit",
    )
    def wikipage_add(self):
        form = self.wiki_form.render()

        if "submit" in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = self.wiki_form.validate(controls)
            except deform.ValidationFailure as e:
                # Form is NOT valid
                return dict(form=e.render())

            # Form is valid, Add in DB
            new_title = appstruct["title"]
            new_body = appstruct["title"]
            DBSession.add(Page(title=new_title, body=new_body))

            # Now visit new page
            page = DBSession.query(Page).filter_by(title=new_title).one()
            new_uid = page.uid
            url = self.request.route_url("wikipage_view", uid=new_uid)
            return HTTPFound(url)

        return dict(form=form)

    @view_config(
        route_name="wikipage_view", renderer="swhwiki:templates/wikipage_view.jinja2"
    )
    def wikipage_view(self):
        uid = int(self.request.matchdict["uid"])
        page = DBSession.query(Page).filter_by(uid=uid).one()
        return dict(page=page)

    @view_config(
        route_name="wikipage_edit",
        renderer="swhwiki:templates/wikipage_addedit.jinja2",
        permission="edit",
    )
    def wikipage_edit(self):
        uid = int(self.request.matchdict["uid"])
        page = DBSession.query(Page).filter_by(uid=uid).one()

        wiki_form = self.wiki_form

        if "submit" in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = wiki_form.validate(controls)
            except deform.ValidationFailure as e:
                return dict(page=page, form=e.render())

            # Change the content and redirect to the view
            page.title = appstruct["title"]
            page.body = appstruct["body"]
            url = self.request.route_url("wikipage_view", uid=uid)
            return HTTPFound(url)

        form = self.wiki_form.render(
            dict(uid=page.uid, title=page.title, body=page.body)
        )

        return dict(page=page, form=form)

    @view_config(route_name="login", renderer="swhwiki:templates/login.jinja2")
    @forbidden_view_config(renderer="swhwiki:templates/login.jinja2")
    def login(self):
        request = self.request
        login_url = request.route_url("login")
        referrer = request.url
        if referrer == login_url:
            referrer = "/"  # never use login form itself as came_from
        came_from = request.params.get("came_from", referrer)
        message = ""
        login = ""
        password = ""
        if "form.submitted" in request.params:
            login = request.params["login"]
            password = request.params["password"]
            hashed_pw = USERS.get(login)
            if hashed_pw and check_password(password, hashed_pw):
                headers = remember(request, login)
                return HTTPFound(location=came_from, headers=headers)
            message = "Failed login"

        return dict(
            name="Login",
            message=message,
            url=request.application_url + "/login",
            came_from=came_from,
            login=login,
            password=password,
        )

    @view_config(route_name="logout")
    def logout(self):
        request = self.request
        headers = forget(request)
        url = request.route_url("wiki_view")
        return HTTPFound(location=url, headers=headers)
