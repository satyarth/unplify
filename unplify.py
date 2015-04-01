import Image, ImageDraw, ImageFilter
import argparse

p = argparse.ArgumentParser(description="Make an image look like the album art for 'Unknown Pleasures' by Joy Division")
p.add_argument("image", help="input image file")
p.add_argument("-o", "--output", default='out.png', help="output image file, defaults to 'out.png'")
p.add_argument("-y", "--line_separation", default=6, help="Default separation between horizontal lines")
p.add_argument("-x", "--sampling_frequency", default=1, help="How often the image is sampled (horizontally)")
p.add_argument("-s", "--scale", default=20, help="Scale of the offset")
p.add_argument("-m", "--monochrome", default='n', help="Draw lines as white?")
args = p.parse_args()

line_separation = int(args.line_separation)
sampling_frequency = int(args.sampling_frequency)
bg_color = (0, 0, 0)
scale = int(args.scale)

def offset((r, g, b)):
	lightness = r + g + b
	return lightness/scale

def invert((r, g, b)):
	return (255-r,255-g,255-b)

def draw_chain(chain):
	start_point = chain[0]
	for end_point in chain[1:]:
		draw.line(start_point[0] + end_point[0], fill = (255,255,255) if args.monochrome == 'y' else start_point[1])
		start_point = end_point

def get_chain(y):
	chain = []
	for x in range(0, img.size[0], sampling_frequency):
			chain.append([(x, y-offset(pixels[x,y])),pixels[x,y]])
			# chain.append([(x, y-offset(edgy_pixels[x,y])),pixels[x,y]])
	return chain

def get_chains():
	chains = []
	for y in range(0, img.size[1], line_separation):
		chains.append(get_chain(y))
	return chains

img = Image.open(args.image)
img = img.convert('RGB')
edges = img.filter(ImageFilter.FIND_EDGES)
pixels = img.load()
edgy_pixels = edges.load()
new = Image.new('RGBA', img.size, bg_color)

chains = get_chains()
draw = ImageDraw.Draw(new)
for chain in chains:
	draw_chain(chain)
del draw

new.save(args.output)