from nicegui import ui, events
import pandas as pd
from io import StringIO
from .locationGenerator import LocationGenerator
import asyncio
import os

async def genPDF(labels, completed):
    labelGenerator = LocationGenerator()
   
    await asyncio.to_thread(labelGenerator.generatePDF, labels)
    completed.set()

async def fileUpload(file: events.UploadEventArguments):
    if file is not None:
        with StringIO(file.content.read().decode("utf-8")) as f:
            df = pd.read_csv(f)

            labels = []

            for index, row in df.iterrows():
                labels.append(row.iloc[0])

            completed = asyncio.Event()
            asyncio.create_task(genPDF(labels, completed))

            spinner = ui.spinner().props("size=50")
            
            spinner.visible = True

            await completed.wait()
            ui.download("Labels.pdf", "Labels.pdf")

            spinner.visible = False

def locationLabel(ui):
    ui.label("Upload a CSV file")
    ui.upload(on_upload=fileUpload).props("accept=.csv")
