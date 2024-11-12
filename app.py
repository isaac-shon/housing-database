from shiny import App, ui, render_ui

# Define UI for each page
page_one_ui = ui.page_fluid(
    ui.h2("Page 1"),
    ui.p("This is the first page of the app.")
)

page_two_ui = ui.page_fluid(
    ui.h2("Page 2"),
    ui.p("This is the second page of the app.")
)

# Define the app UI with navigation bar
app_ui = ui.page_navbar(
    ui.nav_panel("Page 1", page_one_ui),
    ui.nav_panel("Page 2", page_two_ui),
    title="My Multipage App"
)

# Define the app server (optional)
def server(input, output, session):
    pass

# Create the Shiny app
app = App(app_ui, server)