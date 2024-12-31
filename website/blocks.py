from wagtail import blocks
from coderedcms.blocks import CONTENT_STREAMBLOCKS, HeroBlock, GridBlock, CardGridBlock, CardBlock, BaseBlock
from django.utils.translation import gettext_lazy as _


class CustomTextBlock(BaseBlock):
    """
    An embedded Google map in an <iframe>.
    """
    color = blocks.CharBlock(
        max_length=255,
        label="Text Color",
        required=False
    )
    font_size = blocks.IntegerBlock(
        required=False,
        label="Font Size (px)",
    )
    content = blocks.RichTextBlock(
        max_length=255,
        label="Text"
    )

    class Meta:
        template = "coderedcms/blocks/custom_rich_text_block.html"
        icon = "doc-full"
        label = "Custom Text"


class CustomMapBlock(BaseBlock):
    longitude = blocks.FloatBlock(
        required=True,
        help_text="First open longitude"
    )
    latitude = blocks.FloatBlock(
        required=True,
        help_text="First open latitude"
    )
    zoom_default_level = blocks.IntegerBlock(
        default=10,
        min_value=1,
        max_value=18,
        help_text="Zoom default level"
    )
    zoom_maker_level = blocks.IntegerBlock(
        default=15,
        min_value=1,
        max_value=18,
        help_text="Zoom marker level"
    )
    location_header = blocks.CharBlock(
        max_length=255,
        required=True,
        default='Location',
        help_text='Enter the location header.'
    )

    class Meta:
        template = "coderedcms/blocks/custom_map.html"
        icon = "doc-full"
        label = "Custom Map"


class CustomHeroBlock(HeroBlock):
    background_image_gradient = blocks.CharBlock(required=False, default="linear-gradient(to left, rgba(255, 255, 255, 0.0), rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.9))")
    show_form = blocks.BooleanBlock(required=False, label="show form")
    form_background_color = blocks.CharBlock(
        max_length=255,
        label="Form Background Color",
        required=False
    )
    form_width = blocks.IntegerBlock(
        label="Form width(in %)",
        default=50
    )
    form_left = blocks.IntegerBlock(
        label="Form position left(in %)",
        default=50
    )
    form_top = blocks.IntegerBlock(
        label="Form position top(in pixel)",
        default=0
    )
    form_mobile_show = blocks.BooleanBlock(
        label="Form show on mobile",
        default=False,
        required=False
    )

    form_url = blocks.CharBlock(
        label="Form page url",
        default=False,
        help_text="Copy form page url paste here"
    )

    class Meta:
        template = "coderedcms/blocks/hero_block.html"
        icon = "cr-newspaper-o"
        label = "Hero Unit"


CUSTOM_CONTENT_STREAMBLOCKS = CONTENT_STREAMBLOCKS + [("custom_text", CustomTextBlock()), ] + [
    ("custom_map", CustomMapBlock()), ]

CUSTOM_LAYOUT_STREAMBLOCKS = [
    (
        "hero",
        CustomHeroBlock(
            [
                ("row", GridBlock(CUSTOM_CONTENT_STREAMBLOCKS)),
                (
                    "cardgrid",
                    CardGridBlock(
                        [
                            ("card", CardBlock()),
                        ]
                    ),
                ),
                (
                    "html",
                    blocks.RawHTMLBlock(
                        icon="code", form_classname="monospace", label=_("HTML")
                    ),
                ),
            ]
        ),
    ),
    ("row", GridBlock(CUSTOM_CONTENT_STREAMBLOCKS)),
    (
        "cardgrid",
        CardGridBlock(
            [
                ("card", CardBlock()),
            ]
        ),
    ),
    (
        "html",
        blocks.RawHTMLBlock(
            icon="code", form_classname="monospace", label=_("HTML")
        ),
    ),
]
