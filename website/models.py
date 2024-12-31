"""
Create or customize your page models here.
"""

from coderedcms.blocks import NAVIGATION_STREAMBLOCKS, BaseBlock
from coderedcms.fields import CoderedStreamField
from django import forms
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from modelcluster.fields import ParentalKey
from coderedcms.forms import CoderedFormField
from coderedcms.models import (
    CoderedArticlePage,
    CoderedArticleIndexPage,
    CoderedEmail,
    CoderedFormPage,
    CoderedWebPage,
)
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import StreamField, RichTextField
from wagtail.images import get_image_model_string, get_image_model
from wagtail.models import TranslatableMixin, Orderable
from wagtail.snippets.models import register_snippet

from website.blocks import CUSTOM_CONTENT_STREAMBLOCKS, CUSTOM_LAYOUT_STREAMBLOCKS


class ArticlePage(CoderedArticlePage):
    """
    Article, suitable for news or blog content.
    """

    class Meta:
        verbose_name = "Article"
        ordering = ["-first_published_at"]

    # Only allow this page to be created beneath an ArticleIndexPage.
    parent_page_types = ["website.ArticleIndexPage"]

    template = "coderedcms/pages/article_page.html"
    search_template = "coderedcms/pages/article_page.search.html"

    body = StreamField(
        CUSTOM_CONTENT_STREAMBLOCKS,
        null=True,
        blank=True,
        use_json_field=True,
    )


class ArticleIndexPage(CoderedArticleIndexPage):
    """
    Shows a list of article sub-pages.
    """

    class Meta:
        verbose_name = "Article Landing Page"

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = "website.ArticlePage"

    # Only allow ArticlePages beneath this page.
    subpage_types = ["website.ArticlePage"]

    template = "coderedcms/pages/article_index_page.html"

    body = StreamField(
        CUSTOM_LAYOUT_STREAMBLOCKS,
        null=True,
        blank=True,
        use_json_field=True,
    )


class LocationPage(CoderedArticlePage):
    class Meta:
        verbose_name = "Location"
        ordering = ["-first_published_at"]

    parent_page_types = ["website.LocationIndexPage"]
    template = "coderedcms/pages/location_page.html"
    search_template = "coderedcms/pages/location_page.search.html"

    body = StreamField(
        CUSTOM_LAYOUT_STREAMBLOCKS,
        null=True,
        blank=True,
        use_json_field=True,
    )

    address = models.CharField(max_length=255, blank=True, null=True)
    tel = models.CharField(max_length=20, blank=True, null=True)
    thumbnail = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Thumbnail image",
    )

    content_panels = CoderedArticlePage.content_panels + [
        FieldPanel("address"),
        FieldPanel("tel"),
        FieldPanel("thumbnail"),
    ]


class LocationIndexPage(CoderedArticleIndexPage):
    class Meta:
        verbose_name = "Location Landing Page"

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = "website.LocationPage"

    # Only allow ArticlePages beneath this page.
    subpage_types = ["website.LocationPage"]

    template = "coderedcms/pages/location_index_page.html"

    body = StreamField(
        CUSTOM_LAYOUT_STREAMBLOCKS,
        null=True,
        blank=True,
        use_json_field=True,
    )


class FormPage(CoderedFormPage):
    """
    A page with an html <form>.
    """

    class Meta:
        verbose_name = "Form"

    template = "coderedcms/pages/form_page.html"


class FormPageField(CoderedFormField):
    """
    A field that links to a FormPage.
    """

    class Meta:
        ordering = ["sort_order"]

    page = ParentalKey("FormPage", related_name="form_fields")


class FormConfirmEmail(CoderedEmail):
    """
    Sends a confirmation email after submitting a FormPage.
    """

    page = ParentalKey("FormPage", related_name="confirmation_emails")


class WebPage(CoderedWebPage):
    """
    General use page with featureful streamfield and SEO attributes.
    """

    class Meta:
        verbose_name = "Web Page"

    template = "coderedcms/pages/web_page.html"

    body = StreamField(
        CUSTOM_LAYOUT_STREAMBLOCKS,
        null=True,
        blank=True,
        use_json_field=True,
    )


@register_snippet
class TranslateNavbar(TranslatableMixin, models.Model):
    """
    Snippet for site navigation bars (header, main menu, etc.)
    """
    name = models.CharField(
        max_length=255,
        verbose_name="Name",
    )
    custom_css_class = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Custom CSS Class",
    )
    custom_id = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Custom ID",
    )
    menu_items = CoderedStreamField(
        NAVIGATION_STREAMBLOCKS,
        verbose_name="Navigation links",
        blank=True,
        use_json_field=True,
    )

    panels = [
        FieldPanel("name"),
        MultiFieldPanel(
            [
                FieldPanel("custom_css_class"),
                FieldPanel("custom_id"),
            ],
            heading="Attributes",
        ),
        FieldPanel("menu_items"),
    ]

    def __str__(self):
        return self.name


@register_setting(icon="cr-desktop")
class CustomSetting(ClusterableModel, BaseSiteSetting):
    """
    Tracking and Google Analytics.
    """

    class Meta:
        verbose_name = "Custom Settings"

    captcha = models.CharField(
        blank=True,
        max_length=255,
        verbose_name="Captcha key",
        help_text='Your captcha site key'
        ,
    )
    language_menu = models.BooleanField(
        default=True,
        verbose_name="Language menu item",
        help_text="Show/hide language menu item"
    )
    content_margin_top = models.IntegerField(
        default=0,
        verbose_name="Content margin top (px)",
        help_text="Margin top for content, use with fixed navbar settings"
    )
    footer_bg_color = models.CharField(
        null=True, blank=True, max_length=500,
        verbose_name="Footer background color",
        help_text="Footer background color value"
    )
    footer_text_color = models.CharField(
        null=True, blank=True, max_length=500,
        verbose_name="Footer text color",
        help_text="Footer text color value"
    )
    nav_bg_color = models.CharField(
        null=True, blank=True, max_length=500,
        verbose_name="Navbar background color",
        help_text="Navbar background color value"
    )

    facebook_page_id = models.CharField(
        blank=True,
        max_length=255,
        verbose_name="Facebook page ID",
        help_text='Your Facebook page ID',
    )

    using_messenger = models.BooleanField(
        default=True,
        verbose_name="Using Facebook Messenger chat support",
        help_text="Show/hide Facebook Messenger chat support"
    )

    whatsapp_id = models.CharField(
        blank=True,
        max_length=255,
        verbose_name="Whatsapp ID",
        help_text='Your Whatsapp ID',
    )

    using_whatsapp = models.BooleanField(
        default=True,
        verbose_name="Using whatsapp chat support",
        help_text="Show/hide whatsapp chat support"
    )
    owner_mail = models.EmailField(
        null=True,
        verbose_name="Owner mail",
        help_text="Enter the email address of the account owner or administrator."
    )

    custom_css = models.TextField(
        null=True,
        verbose_name="Custom CSS",
        help_text="Custom CSS"
    )
    panels = [
        FieldPanel("captcha"),
        MultiFieldPanel(
            children=[

            FieldPanel("language_menu"),
            FieldPanel("content_margin_top"),
            FieldPanel("nav_bg_color"),
            FieldPanel("footer_bg_color"),
            FieldPanel("footer_text_color"),
            ],
            heading="UI Settings",
        ),
        MultiFieldPanel(
            children=[
                FieldPanel("facebook_page_id"),
                FieldPanel("using_messenger"),
                FieldPanel("whatsapp_id"),
                FieldPanel("using_whatsapp"),
            ],
            heading="Social Media Settings",
        ),
        FieldPanel("owner_mail"),
        InlinePanel(
            "site_navbartrans",
            help_text="Choose one or more navbars for your site.",
            heading="Site Navbars",
        ),
        FieldPanel("custom_css"),
    ]


class TransNavbarOrderable(Orderable, models.Model):
    navbar_chooser = ParentalKey(
        CustomSetting,
        related_name="site_navbartrans",
        verbose_name="Site Navbars",
    )
    navbar = models.ForeignKey(
        TranslateNavbar,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    panels = [FieldPanel("navbar")]


@register_snippet
class LocationMarker(models.Model):
    location = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    tel = models.CharField(max_length=20, help_text="Enter phone number in the format +1234567890")
    description = models.CharField(max_length=255, default='', verbose_name="Address")
    link = models.URLField(blank=True, null=True, help_text="Enter a link associated with this location")

    panels = [
        FieldPanel('location'),
        FieldPanel('latitude'),
        FieldPanel('longitude'),
        FieldPanel('tel'),
        FieldPanel('description'),
        FieldPanel('link'),
    ]

    def __str__(self):
        return self.location

    class Meta:
        verbose_name = "Location Marker"


IMAGE_ORDER_TYPES = (
    (1, "Image title"),
    (2, "Newest image first"),
)

class GalleryIndexPage(CoderedWebPage):
    """
    Shows a list of article sub-pages.
    """

    class Meta:
        verbose_name = "Gallery Page"

    template = "gallery/gallery_page.html"

    intro_title = models.CharField(
        verbose_name=_("Intro title"),
        max_length=250,
        blank=True,
        help_text=_("Optional H1 title for the gallery page."),
    )
    intro_text = RichTextField(
        blank=True, verbose_name=_("Intro text"), help_text=_("Optional text to go with the intro text.")
    )
    collection = models.ForeignKey(
        "wagtailcore.Collection",
        verbose_name=_("Collection"),
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text=_("Show images in this collection in the gallery view."),
    )
    images_per_page = models.IntegerField(
        default=24, verbose_name=_("Images per page"), help_text=_("How many images there should be on one page.")
    )
    use_lightbox = models.BooleanField(
        verbose_name=_("Use lightbox"),
        default=True,
        help_text=_("Use lightbox to view larger images when clicking the thumbnail."),
    )
    order_images_by = models.IntegerField(choices=IMAGE_ORDER_TYPES, default=1,
                                          help_text=_("If 'Image title' is selected, you can manually sort images by adding a four-digit number in brackets to the beginning of the title (e.g., '[0004] Cute cat')"))

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel("intro_title"),
        FieldPanel("intro_text"),
        FieldPanel("collection"),
        FieldPanel("images_per_page"),
        FieldPanel("use_lightbox"),
        FieldPanel("order_images_by"),
    ]

    # No body content panels
    body_content_panels = []

    @property
    def images(self, tags=None):
        return get_gallery_images(self.collection.name, self)

    def get_context(self, request, *args, **kwargs):
        images = self.images
        context = super(GalleryIndexPage, self).get_context(request)
        page = request.GET.get("page")

        paginator = Paginator(images, self.images_per_page)
        try:
            images = paginator.page(page)
        except PageNotAnInteger:
            images = paginator.page(1)
        except EmptyPage:
            images = paginator.page(paginator.num_pages)
        context["gallery_images"] = images
        return context

    class Meta:
        verbose_name = _("Gallery Page")



def get_gallery_images(collection, page=None):
    images = None
    try:
        images = get_image_model().objects.filter(collection__name=collection)
        if page:
            if page.order_images_by == 1:
                images = images.order_by("-title")
            elif page.order_images_by == 2:
                images = images.order_by("-created_at")
    except Exception as e:
        pass

    return images



