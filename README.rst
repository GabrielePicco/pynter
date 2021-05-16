Pynter
======

.. image:: https://img.shields.io/pypi/v/pynter.svg
    :target: https://pypi.python.org/pypi/pynter
    :alt: Latest PyPI version

Minimal utility for generating images with textual caption

Usage
-----

1. Download an image

    curl https://ichef.bbci.co.uk/news/1024/branded_news/46C9/production/_118512181_zhurong-china-mars-lander.jpg -o ./image.jpg

2. Download a font

    curl https://fonts.google.com/download?family=Roboto -o ./roboto.zip ; unzip ./roboto.zip -d ./Roboto

3. Provide a caption and Generate the image::

    font_path = './Roboto/Roboto-Regular.ttf'
    image_path = './image.jpg'
    im = generate_captioned('China lands rover on Mars'.upper(), image_path=image_path, size=(1080, 1350),
                            font_path=font_path, filter_color=(0, 0, 0, 40))
    im.show()
    im.convert('RGB').save('drawn_image.jpg')


Results will look like:

.. image:: https://i.imgur.com/fS6vPNm.jpg


Installation
------------

   pip install pynter
