from PIL import Image
from io import BytesIO


def extract_frames(file_name):
    gif = Image.open(file_name)

    try:
        i = 0
        palette = None

        while True:
            gif.seek(i)
            frame = gif.copy()
            if i == 0:
                palette = frame.getpalette()
            else:
                frame.putpalette(palette)

            output = BytesIO()
            frame.save(output, format='GIF')
            yield output
            i += 1

    except EOFError:
        """End of File."""
    finally:
        gif.close()
