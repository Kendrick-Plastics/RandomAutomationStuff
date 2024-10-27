from nicegui import ui, events
import pandas as pd
from io import StringIO
from .locationGenerator import LocationGenerator
import asyncio

async def fileUpload(file: events.UploadEventArguments):
    if file is not None:
        with StringIO(file.content.read().decode("utf-8")) as f:
            df = pd.read_csv(f)

            labels = []

            for index, row in df.iterrows():
                labels.append(row.iloc[0])

            labelGenerator = LocationGenerator()
            labelGenerator.generatePDF(labels)


def locationLabel(ui):
    ui.label("Upload an CSV file")
    ui.download("Labels.pdf", "Labels.pdf")
    ui.upload(on_upload=fileUpload).props("accept=.csv")
