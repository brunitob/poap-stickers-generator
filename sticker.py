
import qrcode
import csv
import sys

# https://pillow.readthedocs.io/en/3.1.x/reference/Image.html
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def create_qr(data, path, title):
	print "New QR for: " + title

	# We use POAP Font
	fnt = ImageFont.truetype("/Library/Fonts/Arial.ttf", 50)

	#QR Settings
	qr = qrcode.QRCode(
	    version = 1,
	    error_correction = qrcode.constants.ERROR_CORRECT_H,
	    box_size = 8,
	    border = 4,
	)

	img_bg = Image.open('sticker_modelo.png')

	#Some magic number to adjust the position
	x = (img_bg.size[0] / 4) - 15
  	y = -7

	# Add data to the QR
	qr_string = "https://poap.xyz/claim/" + data
	qr.add_data(qr_string)
	qr.make(fit=True)

	# Create an image from the QR Code instance
	img = qr.make_image()
	#Now paste the QR on the original template
	img_bg.paste(img, (x, y ))

	#Just draw the code
	draw = ImageDraw.Draw(img_bg)
	draw.text((295, 578), data, (0, 0, 0), font=fnt)

	# Save it somewhere
	img_bg.save(path + "/" + title)

def process_csv(csv_location, export_location, start_row=False, end_row=False):
	with open(csv_location, 'r') as csvfile:

		current_row = -1
		csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in csv_reader:

			current_row += 1

			if start_row or end_row:
				if current_row < start_row:
					continue
				if current_row >= end_row:
					break
			else:
				# Create the QR Code and save to the export location
				create_qr(row[0], export_location, row[0] + ".png")

if __name__ == "__main__":
	if len(sys.argv) > 2:
		print("CSV Location     : %s" % sys.argv[1])
		print("Export Location  : %s" % sys.argv[2])

		start_row = False
		if len(sys.argv) > 3:
			print("Start Row: %s" % sys.argv[3])
			start_row = sys.argv[3]

		end_row = False
		if len(sys.argv) > 4:
			print("End Row: %s" % sys.argv[4])
			end_row = sys.argv[4]

		process_csv(sys.argv[1], sys.argv[2], start_row=start_row, end_row=end_row)
	else:
		print("Please provide a path to your csv and an export location.")