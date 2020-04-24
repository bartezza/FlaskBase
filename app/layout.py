
import traceback
from flask import Blueprint, render_template, request, flash
from .utils_html import HtmlElem, HtmlGridRow, HtmlContainer, HtmlTable, Navigation


class Layout:

    block: HtmlContainer
    title: str

    flash_colors = {
        "error": "w3-pale-red",
        "success": "w3-pale-green"
    }

    container_class = "w3-panel w3-border w3-margin-top w3-padding-small"

    def __init__(self, navigation, title=None):
        self.navigation = navigation  # MyNavigation("opt_strats")

        self.block = HtmlContainer(css_class=None)

        if title is not None:
            self.title = title
            self.block.add_child(HtmlElem(tag="h2", text="{}".format(title)))
        else:
            self.title = "Test"

    def new_container(self, **kwargs):
        row = self.block.add_child(HtmlGridRow())
        cont = row.add_child(HtmlContainer(css_class=self.container_class, **kwargs))
        return cont

    def add_table(self, data, headers):
        block_row = self.block.add_child(HtmlGridRow())
        table = block_row.add_child(HtmlTable()) \
                         .build_from_table_dict(headers=headers, data=data)

    def add_link(self, href, text):
        cont = self.new_container()
        # cont.add_child(HtmlElem(tag="hr"))
        cont.add_child(HtmlElem(tag="p")).add_child(HtmlElem(tag="a", href=href, text=text))

    def add_html(self, html, container=False):
        if container:
            cont = self.new_container()
            cont.add_child(HtmlElem(tag=None, inner_html=html))
        else:
            self.block.add_child(HtmlElem(tag=None, inner_html=html))

    def add_template(self, template_name, **kwargs):
        html = render_template(template_name, **kwargs)
        self.add_html(html)

    def add_pre(self, content):
        cont = self.new_container()
        cont.add_child(HtmlElem(tag="pre", inner_html=content))

    def add_toolbar(self, buttons):
        block = ""
        for button in buttons:
            block += "<a href=\"{href}\"><button class=\"w3-button w3-teal\">{text}</button></a>\n"\
                     .format(**button)

        container_class = "w3-panel w3-border w3-margin-top w3-padding-small"
        row = self.block.add_child(HtmlGridRow())
        cont = row.add_child(HtmlContainer(css_class=container_class, inner_html=block))

    def add_exception(self):
        var = traceback.format_exc()
        self.add_pre(var)
    
    def add_form(self, html, action=""):
        form_html = "<form action=\"{action}\" method=\"post\" novalidate>".format(action=action)
        form_html += html
        form_html += "</form>"
        cont = self.new_container(inner_html=form_html)

        print(cont.html())

    def finish(self, add_template=None, **kwargs):
        params = {}
        if add_template is not None:
            params["add_template"] = add_template
        return render_template("index_layout.html", title=self.title, navigation=self.navigation.get(),
                               block=self.block.html(), flash_colors=self.flash_colors, **params, **kwargs)
