try:
	import Image
except ImportError:
	from PIL import Image
import argparse
import svgwrite

def offset(pixels):
	r, g, b = pixels[0], pixels[1], pixels[2]
	lightness = r + g + b
	return lightness*args.peakiness

def get_line(y):
	line = []
	for x in range(0, img.size[0], args.sampling_frequency):
			line.append([(x, y-offset(pixels[x,y])),pixels[x,y]])
	return line

p = argparse.ArgumentParser(description="Make an image look like the album art for 'Unknown Pleasures' by Joy Division")
p.add_argument("image", help="input image file")
p.add_argument("-o", "--output", default='out.svg', help="output image file, defaults to 'out.png'")
p.add_argument("-s", "--scale", type=float, default='1', help="scale the output with respect to the input")
p.add_argument("-v", "--vspace", type=int, default='20', help="vertical spacing between lines (in pixels)")
p.add_argument("-f", "--sampling_frequency", type=int, default='1', help="how frequently the imput image is sampled (in pixels)")
p.add_argument("-p", "--peakiness", type=float, default='0.08', help="scale the 'peaks' in the output image")
p.add_argument("-b", "--bg_color", type=str, default='#222', help="background color in #rrggbb format")
args = p.parse_args()

img = Image.open(args.image)
img.convert('RGBA')
pixels = img.load()

lines = []
for y in range(0, img.size[1], args.vspace):
	lines.append(get_line(y))

dwg = svgwrite.Drawing(args.output, profile='full',
									size=(int(img.size[0]*args.scale), int(img.size[1]*args.scale)))

dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill=args.bg_color))
for line in lines:
	start_point = line[0]
	for end_point in line[1:]:
		dwg.add(dwg.line(start = (start_point[0][0]*args.scale, start_point[0][1]*args.scale),
						 end = (end_point[0][0]*args.scale, end_point[0][1]*args.scale),
						 stroke='rgb' + str(start_point[1]) ))
		start_point = end_point
dwg.save()
