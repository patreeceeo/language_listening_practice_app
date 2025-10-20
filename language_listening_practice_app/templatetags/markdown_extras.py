from django import template
from django.utils.safestring import mark_safe
import markdown as md
import textwrap

register = template.Library()


class MarkdownNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        # Get the content between {% markdown %} and {% endmarkdown %}
        content = self.nodelist.render(context)
        # Remove common leading whitespace to allow for template indentation
        dedented = textwrap.dedent(content)
        # Strip leading/trailing whitespace
        cleaned = dedented.strip()
        # Convert to HTML
        html = md.markdown(cleaned, extensions=['toc'])
        return mark_safe(html)


@register.tag(name='markdown')
def do_markdown(parser, token):
    """
    Convert Markdown to HTML using a block-style tag.

    Usage:
        {% load markdown_extras %}

        {% markdown %}
        # My Heading

        This is **bold** and *italic*.

        - List item 1
        - List item 2
        {% endmarkdown %}
    """
    nodelist = parser.parse(('endmarkdown',))
    parser.delete_first_token()
    return MarkdownNode(nodelist)


# Also provide a filter for inline use
@register.filter(name='markdown')
def markdown_filter(content):
    """
    Convert Markdown to HTML using a filter.

    Usage:
        {{ my_variable|markdown }}
    """
    if not content:
        return ''
    html = md.markdown(str(content), extensions=['toc'])
    return mark_safe(html)
