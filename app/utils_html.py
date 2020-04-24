
import pandas as pd


class HtmlElem:
    def __init__(self, tag, css_class=None, text=None, inner_html=None, href=None):
        self.tag = tag
        self.css_classes = []
        self.children = []
        if css_class is not None:
            self.css_classes.append(css_class)
        self.text = text
        self.inner_html = inner_html
        self.href = href

    def set_grid_layout(self, m, l):
        self.css_classes.append("w3-col m{} l{}".format(m, l))
        return self

    def add_child(self, item):
        self.children.append(item)
        return item

    def html(self):
        data = ""
        if self.tag is not None:
            css_class = " ".join(self.css_classes)
            href = " href=\"{}\"".format(self.href) if self.href is not None else ""
            data += "<{} class=\"{}\"{}>\n".format(self.tag, css_class, href)
        if self.text is not None:
            data += self.text
        if self.inner_html is not None:
            data += self.inner_html
        for child in self.children:
            data += child.html()
        if self.tag is not None:
            data += "</{}>\n".format(self.tag)
        return data


class HtmlGridRow(HtmlElem):
    def __init__(self, css_class=""):
        super().__init__(tag="div", css_class="w3-row " + css_class)


class HtmlContainer(HtmlElem):
    def __init__(self, css_class="w3-container", **kwargs):
        super().__init__(tag="div", css_class=css_class, **kwargs)


class HtmlTable(HtmlElem):
    def __init__(self, css_class=""):
        super().__init__(tag="table", css_class="w3-table-all w3-hoverable " + css_class)
        self.headers = []
        self.rows = []

    def build_from_df(self, df: pd.DataFrame):
        self.headers.append("")
        for col in df.columns:
            self.headers.append(col)
        for index, row in df.iterrows():
            new_row = [index]
            for col in row:
                new_row.append(col)
            self.rows.append(new_row)
        return self

    def build_from_table_dict(self, headers, data):
        for h in headers:
            self.headers.append(h[1])
        for row in data:
            new_row = []
            for h in headers:
                if h[0] in row:
                    new_row.append(row[h[0]])
                else:
                    new_row.append("")
            self.rows.append(new_row)
        return self

    def build_from_dict(self, data):
        for key, value in data.items():
            self.rows.append([key, value])
        return self

    def html(self):
        css_class = " ".join(self.css_classes)
        data = "<table class=\"{}\">\n".format(css_class)
        if len(self.headers) > 0:
            data += "<tr>"
            for col in self.headers:
                data += "<th>{}</th>".format(col)
            data += "</tr>\n"
        for row in self.rows:
            data += "<tr>"
            for col in row:
                if not isinstance(col, dict):
                    data += "<td>{}</td>".format(col)
                else:
                    text = col["text"]
                    css_class = " class=\"{}\"".format(col["css_class"]) if "css_class" in col else ""
                    if "href" in col:
                        text = "<a href=\"{}\">{}</a>".format(col["href"], text)
                    data += "<td{}>{}</td>".format(css_class, text)
            data += "</tr>\n"
        data += "</table>\n"
        return data



class Navigation:
    def __init__(self, cur_page):
        self._data = []
        self._pages = {}
        self.cur_page = cur_page
        self.setup()

    def setup(self):
        pass

    def add_page(self, name, href, title):
        page = {
            "name": name,
            "href": href,
            "title": title,
            "css_class": ""
        }
        self._data.append(page)
        self._pages[name] = page

    def update(self):
        self._pages[self.cur_page]["css_class"] += " w3-blue"

    def get(self):
        self.update()
        return self._data



def build_html_from_df(df: pd.DataFrame) -> str:
    data = "<table class=\"w3-table-all w3-hoverable\">\n<tr>\n"
    data += "<th></th>"
    for col in df.columns:
        data += "<th>{}</th>".format(col)
    data += "</tr>\n"
    for index, row in df.iterrows():
        data += "<tr><td>{}</td>".format(index)
        for col in row:
            data += "<td>{}</td>".format(col)
        data += "</tr>\n"
    data += "</table>\n"
    return data


def build_html_from_dict(data: dict) -> str:
    html = "<table class=\"w3-table-all w3-hoverable\">\n"
    for key, value in data.items():
        html += "<tr><td>{}</td><td>{}</td></tr>\n".format(key, value)
    html += "</table>\n"
    return html
