import typer

from .scrape import retrieve_scores

app = typer.Typer()
app.command()(retrieve_scores)

if __name__ == "__main__":
    app()