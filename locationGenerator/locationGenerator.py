from ppf.datamatrix import DataMatrix
import cairosvg
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


class LocationGenerator:
    def __init__(self):
        # Location Label Dimensions (inches)
        self.height = 3.25
        self.width = 3.75
        self.thickness = 0.05
        self.matrixSize = 2.5

        self.ppi = 120

        self.thicknessPPX = int(self.thickness * self.ppi)
        self.heightPPX = int(self.height * self.ppi)
        self.widthPPX = int(self.width * self.ppi)
        self.matrixPPX = int(self.matrixSize * self.ppi)

        self.quarter = int(0.05 * self.ppi)
        self.margin = int(.5 * self.ppi)

        self.pageWidthPPX = int((3 * self.quarter) + (2 * self.widthPPX)) + (2 * self.margin)
        self.pageHeightPPX = int((4 * self.quarter) + (3 * self.heightPPX)) + (2 * self.margin)
        
    # Return PIL object
    def generateLocation(self, message):
        if message == "":
            return None
        matrixSVGData = DataMatrix(message).svg()
        matrixPNGData = cairosvg.svg2png(bytestring=matrixSVGData.encode("utf-8"), output_height=self.matrixPPX, output_width=self.matrixPPX)
        barcodeData = BytesIO(matrixPNGData)
        barcodeImage = Image.open(barcodeData).convert("RGBA")

        whiteBG = Image.new("RGB", barcodeImage.size, "white")
        whiteBG.paste(barcodeImage, mask=barcodeImage.split()[3])

        canvas = Image.new("RGBA", (int(self.width * self.ppi), int(self.height * self.ppi)), "white")
        draw = ImageDraw.Draw(canvas)

        draw.rectangle(
            [0, 0, 
            self.widthPPX, self.heightPPX],
            outline="black", width=self.thicknessPPX
        )

        barX = (self.widthPPX - self.matrixPPX) // 2
        barY = int(0.0625 * self.ppi)

        canvas.paste(whiteBG, (barX, barY + int(.625 * self.ppi)))

        font = ImageFont.truetype("./arial.ttf", int(0.625 * self.ppi))

        maxWidthPPX = int(3.5 * self.ppi)
        fontPPX = font.getlength(message)

        if (maxWidthPPX < fontPPX):
            factor = fontPPX / maxWidthPPX
            font = ImageFont.truetype("./arial.ttf", int((0.625 * self.ppi) / factor))

        fontX = int((self.widthPPX - font.getlength(message)) / 2 )

        ascent, _ = font.getmetrics()
        (_, _), (_, offsetY) = font.font.getsize(message)
        fontY = int((2.0625 * self.ppi) + (((1.1875 * self.ppi) - (ascent - offsetY)) / 2))

        # textWidth, textHeight = draw.textlength(message, font=font)
        draw.text((fontX, fontY - self.matrixPPX), message, font=font, fill="black")

        return canvas

    # Returns PDF of all labels
    def generatePDF(self, labels):
        pdfPages = []

        # X (left/right), Y(up/down) Coords
        TLCoord = (self.margin + self.quarter, self.margin + self.quarter)
        TRCoord = (self.margin + 2 * self.quarter + self.widthPPX, self.margin + self.quarter)

        MLCoord = (self.margin + self.quarter,self.margin +  2 * self.quarter + self.heightPPX)
        MRCoord = (self.margin + 2 * self.quarter + self.widthPPX,self.margin +  2 * self.quarter + self.heightPPX)

        BLCoord = (self.margin + self.quarter,self.margin +  3 * self.quarter + 2 * self.heightPPX)
        BRCoord = (self.margin + 2 * self.quarter + self.widthPPX,self.margin +  3 * self.quarter + 2 * self.heightPPX)

        canvas = Image.new("RGBA", (self.pageWidthPPX, self.pageHeightPPX), "white")

        for tmpIndex, label in enumerate(labels):
            index = tmpIndex % 6

            if index == 0:
                canvas.paste(self.generateLocation(label), TLCoord)

            elif index == 1:
                canvas.paste(self.generateLocation(label), TRCoord)

            elif index == 2:
                canvas.paste(self.generateLocation(label), MLCoord)

            elif index == 3:
                canvas.paste(self.generateLocation(label), MRCoord)

            elif index == 4:
                canvas.paste(self.generateLocation(label), BLCoord)

            elif index == 5:
                canvas.paste(self.generateLocation(label), BRCoord)
                pdfPages.append(canvas)
                canvas = Image.new("RGBA", (self.pageWidthPPX, self.pageHeightPPX), "white")

        pdfPages.append(canvas)
        canvas = Image.new("RGBA", (self.pageWidthPPX, self.pageHeightPPX), "white")
            

        pdfPages[0].save("out.pdf", save_all=True, append_images=pdfPages[1:])
