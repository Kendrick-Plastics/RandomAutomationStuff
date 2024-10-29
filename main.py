from nicegui import ui
from pages.labels.locationGen import locationLabel
import asyncio

with ui.header().classes(replace="row items-center bg-black") as header:
    with ui.tabs() as tabs:
        ui.tab("Home")
        ui.tab("Location")

with ui.tab_panels(tabs, value="Home").classes("w-full"):
    # Home Page
    with ui.tab_panel("Home"):
        ui.label("Kendrick Plastics Utilities").classes("text-4xl")
        ui.label("If anything doesn't work, don't contact IT")

    # Location Label Generator
    with ui.tab_panel("Location") as locationDiv:
        locationLabel(ui)

ui.run()
