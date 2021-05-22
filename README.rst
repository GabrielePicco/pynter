Pynter
======

.. image:: https://img.shields.io/pypi/v/pynter.svg
    :target: https://pypi.python.org/pypi/pynter
    :alt: Latest PyPI version

Minimal utility for generating images with textual caption

Usage
-----

1. Download an image

    curl https://i.imgur.com/XQCKcC9.jpg -o ./image.jpg

2. Download a font

    curl https://fonts.google.com/download?family=Roboto -o ./roboto.zip ; unzip ./roboto.zip -d ./Roboto

3. Provide a caption and Generate the image::

    from pynter.pynter import generate_captioned
    font_path = './Roboto/Roboto-Regular.ttf'
    image_path = './image.jpg'
    im = generate_captioned('China lands rover on Mars'.upper(), image_path=image_path, size=(1080, 1350),
                            font_path=font_path, filter_color=(0, 0, 0, 40))
    im.show()
    im.convert('RGB').save('drawn_image.jpg')


Results will look like:

.. image:: https://i.imgur.com/fS6vPNm.jpg


Image Generation
-----


generate_captioned(    text: str,
                       image_path,
                       size: Optional[Tuple[int, int]] = None, 
                       font_path: str = None,
                       text_align: TextAlign = TextAlign.LEFT,
                       bottom_margin: Optional[float] = 0.07,
                       top_margin: Optional[float] = None,
                       left_margin: float = 0.2, 
                       right_margin: float = 0.2,
                       character_ratio: float = 0.07,
                       filter_color: Tuple[int, int, int, int] = (0, 0, 0, 0),
                       text_background_color: Tuple[int, int, int, int] = (0, 0, 0, 180),
                       text_background_padding: float = 0.2,
                       text_background_mode: TextBackgroundMode = TextBackgroundMode.STRIPE,
                       filters: [BuiltinFilter] = [],
                       color: Tuple[int, int, int, int] = (255, 255, 255, 255)) -> Image:


Installation
------------

   pip install pynter
