from PIL import Image, ImageDraw, ImageFont


def draw_text(text, image_path):

    # create Image object with the input image
    image = Image.open(image_path)

    # initialise the drawing context with
    # the image object as background
    draw = ImageDraw.Draw(image)

    # create font object with the font file and specify
    # desired size
    font = ImageFont.truetype('../data/Roboto-Bold.ttf', size=20)

    # starting position of the message
    (x, y) = (0, 0)
    color = 'rgb(255, 0, 0)'  # black color

    # draw the message on the background
    draw.text((x, y), text, fill=color, font=font)

    # save the edited image
    image.save(image_path)


text = 'my name is krishna'
image_path  = '/Users/gopalmali/Projects_Office/BitBucket/linehtr/HTR/data/merge_test.png'
draw_text(text, image_path)