from locationGenerator import LocationGenerator

labels = ["ASM324", "MLD013", "SHIPPING_DOCK", "ASM404-NOT_FOUND", "ASM322", "MLD013", "SHIPPING_DOCK", "ASM404-NOT_FOUND", "A"]

labels = labels * 1

generator = LocationGenerator()

generator.generatePDF(labels)
