from PIL import Image, ImageDraw


def calculateTint(RGBA):
    red_tint = RGBA[0] + (0.25 * (255 - RGBA[0]))
    green_tint = RGBA[1] + (0.25 * (255 - RGBA[1]))
    blue_tint = RGBA[2] + (0.25 * (255 - RGBA[2]))
    return (int(red_tint), int(green_tint), int(blue_tint), 0)


def calculateAverage(color1, color2):
    avg = tuple(int(sum(x)/2) for x in zip(color1, color2))
    return avg

def calculateInverse(color):
    inv_all = tuple(255-x for x in color)
    #make sure we don't invert the alpha
    inv = (inv_all[0], inv_all[1], inv_all[2], 0)
    return inv


def draw_colors(outfile, colors, numcolors=5, swatchsize=20):
    pal = Image.new('RGB', (swatchsize*numcolors, swatchsize))
    draw = ImageDraw.Draw(pal)
    posx = 0
    for col in colors:
        # print col
        draw.rectangle([posx, 0, posx+swatchsize, swatchsize], fill=col)
        posx = posx + swatchsize

    del draw
    pal.save(outfile, "PNG")

def print_hex(colors):
    for color in colors:
        #get the hex value of the RGB
        r = str(hex(color[0]))[2:]
        g = str(hex(color[1]))[2:]
        b = str(hex(color[2]))[2:]
        #make it html friendly
        print '#' + r+g+b

    #TODO: return the html values in a list?

def get_colors(infile, outfile, resize=150):

    image = Image.open(infile)
    image = image.resize((resize, resize))
    #grab 10 colors from the image
    result = image.convert('P', palette=Image.ADAPTIVE, colors=10)
    result.putalpha(0)
    colors = result.getcolors(resize*resize)
    #sort colors from largest number of occurences to smallest
    colors.sort(key=lambda tup: tup[0], reverse=True)
    #grab the RGBA values for the primaries
    primary1 = colors[0][1]
    primary2 = colors[1][1]
    #calculate accent tints
    accent1 = calculateTint(primary1)
    accent2 = calculateTint(primary2)
    #contrast color is the inverse of the average of the two primaries
    contrast = calculateInverse(calculateAverage(primary1, primary2))
    #tuple of colors
    pal_colors = (primary1, primary2, accent1, accent2, contrast)
    
    # Save colors to file
    draw_colors(outfile, pal_colors)

    #print hex values of colors
    print_hex(pal_colors)


if __name__ == '__main__':
    get_colors('infile.jpg', 'outfile.png')
