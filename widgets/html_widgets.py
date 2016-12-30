from pyasm.web import HtmlElement


def get_label_widget(label_text):
    """
    Given a label string, return a DivWdg containing the label

    :param label_text: String
    :return: HtmlElement.label
    """

    return HtmlElement.label(label_text)


def get_page_header(string):
    """
    Given a string, return a DivWdg containing the string in an H2 tag

    :param string: String
    :return: HtmlElement.label
    """

    return HtmlElement.h2(string)


def get_paragraph_widget(string):
    return HtmlElement.p(string)


def get_pre_widget(string):
    return  HtmlElement.pre(string)
