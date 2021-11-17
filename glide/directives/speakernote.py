"""Speaker notes directive.

Adds a "speaker" directive for RevealJS speaker notes.

For example:

  Dictionaries are cool.

  .. speaker::

    Explain this part really well!

These are ignored in non-RevealJS builders.
"""

from docutils import nodes
from docutils.nodes import SkipNode
from docutils.parsers.rst import Directive

from glide import version


# noinspection PyPep8Naming
class speakernote(nodes.General, nodes.Element):
    """speaker note node."""


class SpeakernoteDirective(Directive):
    """The directive just adds a node for revealjs builder to find."""

    has_content = True

    def run(self):
        self.assert_has_content()
        text = '\n'.join(self.content)

        node = speakernote(text)
        self.add_name(node)
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


# noinspection PyUnusedLocal
def ignore_visit_speakernote(self, node):
    """All non-revealjs builders should use this."""
    raise SkipNode


# noinspection PyUnusedLocal
def revealjs_visit_speakernote(revealjs_translator, node):
    """Wrap contents in an aside element, which is used by revealjs JS."""
    revealjs_translator.body.append("<aside class='notes'>")


# noinspection PyUnusedLocal
def revealjs_depart_speakernote(revealjs_translator, node):
    """End the aside element we started."""
    revealjs_translator.body.append("</aside>")


def setup(app):
    app.add_node(
        speakernote,
        # Ignore on any builder except revealjs --- if there are newer builders,
        # these should be added here.
        epub=(ignore_visit_speakernote, None),
        html=(ignore_visit_speakernote, None),
        handouts=(ignore_visit_speakernote, None),
        latex=(ignore_visit_speakernote, None),
        revealjs=(revealjs_visit_speakernote, revealjs_depart_speakernote),
        text=(ignore_visit_speakernote, None),
        man=(ignore_visit_speakernote, None),
    )
    app.add_directive('speaker', SpeakernoteDirective)
    return {'version': version, 'parallel_read_safe': True}
