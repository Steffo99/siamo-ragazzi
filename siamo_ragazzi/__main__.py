import textwrap
import random
import click
import pathlib
import sys
import PIL
import PIL.Image
import PIL.ImageColor
import PIL.ImageFont
import PIL.ImageDraw


MALE = ["i", "ragazzi", "siamo ragazzi", "siamo ragazzi.", "male", "maschio"]
FEMALE = ["e", "ragazze", "siamo ragazze", "siamo ragazze.", "female", "femmina"]


@click.command()
@click.option("-k", "--kind", help="The meme variation. If not specified, picks a random variation.", default=None, type=str)
@click.option("-t", "--top-text", help="Path to the file containing text appearing at the top of the meme. Defaults to stdin.", default=sys.stdin, type=click.File("r"))
@click.option("-b", "--bottom-text", help="Overrides the text appearing at the bottom of the meme.", default=None, type=str)
@click.option("-c", "--background-color", help="Overrides the background color of the meme.", default=None, type=str)
@click.option("-f", "--foreground-color", help="Overrides the foreground color of the meme.", default=None, type=str)
@click.option("-f", "--font", help="Path to the TrueType font to be used in the meme.", default=None, type=click.Path(exists=True, dir_okay=False))
@click.option("-s", "--seed", help="Set the random seed.", default=None, type=str)
@click.option("-v", "--variation", help="Pixel variation for sizes and positions.", default=40, type=int)
@click.option("-o", "--output", help="Path to save the png output to. Defaults to stdout.", default=sys.stdout, type=click.File(mode="wb"))
def main(top_text, output, bottom_text=None, background_color=None, foreground_color=None, kind=None, font=None, seed=None, variation=40):
    if seed:
        random.seed(seed)

    if not kind:
        kind = random.sample(["male", "female"], 1)[0]

    if kind in MALE:
        bg = (63, 71, 204)
        fg = (0, 0, 0)
        bot = "Siamo Ragazzi."
    elif kind in FEMALE:
        bg = (163, 73, 163)
        fg = (0, 0, 0)
        bot = "Siamo Ragazze."
    else:
        raise click.ClickException(
            f"Unknown kind: {kind!r}\n"
            f"\n"
            f"Available kinds:\n"
            f"{' | '.join(MALE)}\n"
            f"{' | '.join(FEMALE)}\n"
        )

    if background_color:
        try:
            bg = PIL.ImageColor.getrgb(background_color)
        except ValueError:
            raise click.ClickException(f"Unknown background color: {background_color!r}")

    if foreground_color:
        try:
            fg = PIL.ImageColor.getrgb(foreground_color)
        except ValueError:
            raise click.ClickException(f"Unknown foreground color: {foreground_color!r}")

    top = top_text.read()

    if bottom_text:
        bot = bottom_text

    if font:
        fp = font
    else:
        fp = pathlib.Path(__file__).parent.joinpath("fonts").joinpath("Roboto-Regular.ttf")
    with open(fp, "rb") as file:
        font_obj = PIL.ImageFont.truetype(file, size=48)

    def variate(x, y):
        x += random.randint(-variation, variation)
        y += random.randint(-variation, variation)
        return x, y

    img = PIL.Image.new("RGB", variate(1200, 700), bg)
    draw = PIL.ImageDraw.Draw(img)
    draw.line(xy=((0, 550), (img.size[0], 550)), fill=fg, width=10)
    draw.multiline_text(xy=variate(150, 100), text="\n".join(textwrap.wrap(top, width=40)), fill=fg, font=font_obj)
    draw.text(xy=variate(320, 600), text=bot, fill=fg, font=font_obj)

    img.save(output, format="png")


if __name__ == "__main__":
    main()
