import sys, plistlib
from sys import argv
from PIL import Image

if len(sys.argv) < 3:
	sys.exit("Example usage: python SpriteExtractor.py sprites.plist sprites.png")

script, plistname, spritesheetname = argv

pl = plistlib.readPlist(plistname)
img = Image.open(spritesheetname)

for framename in pl['frames']:
	coordset = pl['frames'][framename]['frame'].replace("{", "").replace("}", "").split(",")
	sourceSizes = pl['frames'][framename]['sourceSize'].replace("{", "").replace("}", "").split(",")
	offsetSizes = pl['frames'][framename]['sourceColorRect'].replace("{", "").replace("}", "").split(",")
	rotated = pl['frames'][framename]['rotated']

	left = int(coordset[0])
	top = int(coordset[1])

	if rotated:
		width = int(coordset[3])
		height = int(coordset[2])
	else:
		width = int(coordset[2])
		height = int(coordset[3])

	box = (left, top, left+width, top+height)
	area = img.crop(box)
	
	if rotated:
		area = area.rotate(90)

	background = Image.new('RGBA',(int(sourceSizes[0]), int(sourceSizes[1])))
	offset = (int(offsetSizes[0]), int(offsetSizes[1]))
	background.paste(area, offset)
	
	background.save(framename)

print("Done")