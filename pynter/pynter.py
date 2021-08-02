import math
from enum import Enum
from typing import Callable, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFilter import BuiltinFilter


class TextBackgroundMode(str, Enum):
    NONE = 'none',
    ATTACH_TO_BOTTOM = 'attach_to_bottom',
    ATTACH_TO_TOP = 'attach_to_top',
    STRIPE = 'stripe',


class TextAlign(str, Enum):
    LEFT = 'left',
    RIGHT = 'right',
    CENTER = 'center',


class ImageMode(str, Enum):
    OVERLAY = 'overlay',
    NOT_OVERLAY = 'not_overlay',


def split_text_on_width_size(text: str, max_width: float, fn_text_to_width: Callable) -> str:
    """
    Split a text given a maximum width
    :param text: Text to be split
    :param max_width: The maximum width that the text should fit
    :param fn_text_to_width: Function to compute the width size given a text
    :return: The text split in order to fit the max_width
    """
    text_words = text.replace("\n", "").split()
    missing_start_index = 0
    text_pieces = []
    while missing_start_index < len(text_words):
        missing_end_index = len(text_words)
        while fn_text_to_width(" ".join(text_words[missing_start_index:missing_end_index])) > max_width:
            missing_end_index -= 1
        if missing_start_index == missing_end_index:
            raise ValueError("Unable to find a split. Most likely the character size is too big.")
        text_pieces.append(" ".join(text_words[missing_start_index:missing_end_index]))
        missing_start_index = missing_end_index
    return "\n".join(text_pieces)


def generate_captioned(text: str, image_path, size: Optional[Tuple[int, int]] = None, image_mode=ImageMode.OVERLAY,
                       font_path: str = None,
                       text_align: TextAlign = TextAlign.LEFT,
                       text_min_height: Optional[float] = None,
                       bottom_margin: Optional[float] = 0.07, top_margin: Optional[float] = None,
                       left_margin: float = 0.2, right_margin: float = 0.2,
                       character_ratio: float = 0.07,
                       filter_color: Tuple[int, int, int, int] = (0, 0, 0, 0),
                       text_background_color: Tuple[int, int, int, int] = (0, 0, 0, 180),
                       text_background_padding: float = 0.2,
                       text_background_mode: TextBackgroundMode = TextBackgroundMode.STRIPE,
                       filters: [BuiltinFilter] = [],
                       color: Tuple[int, int, int, int] = (255, 255, 255, 255)) -> Image:
    """
    Generate an image with a textual caption
    :param text: the text
    :param image_path: image path
    :param size: image tuple, if None size of the image_path are taken
    :param image_mode: OVERLAY (text and background cover the image) or NOT_OVERLAY
    :param font_path: font path
    :param text_align: text alignment
    :param text_min_height: minimum text height percentage (of total image height)
    :param bottom_margin: text bottom margin percentage
    :param top_margin: text top margin percentage
    :param left_margin: text left margin percentage
    :param right_margin: text right margin percentage
    :param character_ratio: character ratio of the ImageWidth
    :param filter_color: color of the filter applied on the image
    :param text_background_color: color of the textual background
    :param text_background_padding: background padding
    :param text_background_mode: text background type
    :param filters: filters that can be applied to the image
    :param color: text color
    :return: the generated image
    """
    # Adapt and paste provided image
    post_im = Image.open(image_path).convert('RGBA')
    W, H = size if size else post_im.size
    im = Image.new(mode='RGBA', size=(W, H))
    # Compute text size and position
    font = ImageFont.truetype(font_path, round(W * character_ratio))
    draw = ImageDraw.Draw(im)
    text = split_text_on_width_size(text, W - left_margin * W - right_margin * W,
                                    lambda x: draw.multiline_textsize(x, font=font)[0])
    w, h = draw.multiline_textsize(text, font=font)
    if text_min_height and h < text_min_height*H:
        h = text_min_height*H
    # Calculate text background dimension
    text_background_width = W
    if text_background_mode in (TextBackgroundMode.ATTACH_TO_BOTTOM, TextBackgroundMode.ATTACH_TO_TOP):
        text_background_height = h + H * bottom_margin * 2 if bottom_margin else h + H * top_margin * 2
    else:
        text_background_height = h + h * text_background_padding * 2
    # Adapt and paste provided image
    post_img_w, post_img_h = post_im.size
    img_height = H - text_background_height if image_mode == ImageMode.NOT_OVERLAY else H
    resize_ratio = max(W / post_img_w, img_height / post_img_h)
    post_img_w, post_img_h = math.ceil(post_img_w * resize_ratio), math.ceil(post_img_h * resize_ratio)
    post_im = post_im.resize((post_img_w, post_img_h), Image.ANTIALIAS)
    if text_background_mode != TextBackgroundMode.ATTACH_TO_BOTTOM \
            and text_background_mode != TextBackgroundMode.ATTACH_TO_TOP\
            and image_mode == ImageMode.NOT_OVERLAY:
        raise ValueError("NOT_OVERLAY option only supported with ATTACH_TO_TOP ot ATTACH_TO_BOTTOM")
    offset_x = round((W - post_img_w) / 2)
    if text_background_mode == TextBackgroundMode.ATTACH_TO_TOP and image_mode == ImageMode.NOT_OVERLAY:
        offset_y = round((H - post_img_h) / 2 + text_background_height/2)
    elif text_background_mode == TextBackgroundMode.ATTACH_TO_BOTTOM and image_mode == ImageMode.NOT_OVERLAY:
        offset_y = round((H - post_img_h) / 2 - text_background_height/2)
    else:
        offset_y = round((H - post_img_h) / 2)
    im.paste(post_im, (offset_x, offset_y))
    # Add Color Filter
    if filter_color:
        filter_im = Image.new(mode='RGBA', size=(W, H), color=filter_color)
        im.paste(filter_im, (0, 0), filter_im)
    # Apply Filter
    for f in filters:
        im = im.filter(f)
    # Write Text
    if bottom_margin and top_margin or (not bottom_margin and not top_margin):
        raise ValueError("Provide either bottom or top margin")
    if bottom_margin:
        text_w_anchor, text_h_anchor = W * left_margin, H - (H * bottom_margin + h)
    else:
        text_w_anchor, text_h_anchor = W * left_margin, H * top_margin
    # Write text background
    if not text_background_mode == TextBackgroundMode.NONE:
        text_background_im = Image.new(mode='RGBA',
                                       size=(math.ceil(text_background_width), math.ceil(text_background_height)),
                                       color=text_background_color)
        im.paste(text_background_im, (0, 0 if text_background_mode == TextBackgroundMode.ATTACH_TO_TOP else
                                      round(text_h_anchor - h * text_background_padding / 2)), text_background_im)
    draw.multiline_text((text_w_anchor, text_h_anchor), text, color, font, align=text_align)
    return im
