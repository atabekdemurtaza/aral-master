from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.utils.translation import ugettext_lazy as _
from django.utils.deconstruct import deconstructible


@deconstructible
class ImageDimensionsValidator:
    """ImageField dimensions validator."""

    def __init__(
            self,
            width=None,
            height=None,
            min_width=None,
            max_width=None,
            min_height=None,
            max_height=None
        ):
        """
        Constructor

        Args:
        width (int): exact width
        height (int): exact height
        min_width (int): minimum width
        min_height (int): minimum height
        max_width (int): maximum width
        max_height (int): maximum height
        """

        self.width = width
        self.height = height
        self.min_width = min_width
        self.max_width = max_width
        self.min_height = min_height
        self.max_height = max_height

    def __call__(self, image):
        image.open()
        w, h = get_image_dimensions(image)

        if self.width is not None and w != self.width:
            raise ValidationError(
                _('%s width must be %dpx.') % (
                    image.field.verbose_name.title(),
                    self.width,
                )
            )

        if self.height is not None and h != self.height:
            raise ValidationError(
                _('%s height must be %dpx.') % (
                    image.field.verbose_name.title(),
                    self.height,
                )
            )

        if self.min_width is not None and w < self.min_width:
            raise ValidationError(
                _('%s minimum width must be %dpx.') % (
                    image.field.verbose_name.title(), self.min_width,
                )
            )

        if self.min_height is not None and h < self.min_height:
            raise ValidationError(
                _('%s minimum height must be %dpx.') % (
                    image.field.verbose_name.title(), self.min_height,
                )
            )

        if self.max_width is not None and w > self.max_width:
            raise ValidationError(
                _('%s maximum width must be %dpx.') % (
                    image.field.verbose_name.title(),
                    self.max_width,
                )
            )

        if self.max_height is not None and h > self.max_height:
            raise ValidationError(
                _('%s maximum height must be %dpx.') % (
                    image.field.verbose_name.title(),
                    self.max_height,
                )
            )
