from app import create_app
from config import Config
from flask import redirect, render_template, request, url_for
from werkzeug.exceptions import HTTPException

app = create_app()


# gestion des erreurs:
@app.route("/error")
def error():
    error_messages = {
        '400': 'Requête incorrecte.',
        '401': 'Non autorisé.',
        '403': 'Accès interdit.',
        '404': 'Page non trouvée.',
        '500': 'Erreur interne du serveur.',
    }
    code = request.args.get("code", "404")
    message = error_messages.get(code, "Une erreur inconnue s'est produite.")
    return render_template("error.html", code=code, message=message)


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Gérer toutes les erreurs HTTP"""
    return redirect(url_for("error", code=e.code))


if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
