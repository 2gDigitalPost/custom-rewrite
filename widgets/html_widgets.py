from pyasm.web import HtmlElement


def get_label_widget(label_text):
    """
    Given a label string, return a DivWdg containing the label

    :param label_text: String
    :return: HtmlElement.label
    """

    return HtmlElement.label(label_text)
