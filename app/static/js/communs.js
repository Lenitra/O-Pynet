function writeHTMLNav() {
    var htmlCode = `
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ml-auto">
                    <li class="nav-item"><a class="nav-link" href="/">Accueil</a></li>
                    <li class="nav-item"><a class="nav-link" href="/musique">Musique</a></li>
                    <li class="nav-item"><a class="nav-link" href="/files">Fichiers</a></li>
                    <li class="nav-item"><a class="nav-link" href="/login">Déconnexion</a></li>
                </ul>
            </div>
        </nav>
    `;
    document.write(htmlCode);
}





// Importer les éléments communs dans le fichier HTML
// Pour importer ces éléments dans un fichier HTML, vous devez inclure le fichier JavaScript contenant cette fonction dans votre balise <script>.
// Assurez-vous d'inclure le chemin correct vers le fichier JavaScript dans l'attribut src de la balise <script>.
// Par exemple, si votre fichier JavaScript est situé à "/static/js/communs.js", vous pouvez inclure le code suivant dans votre fichier HTML :

// <script src="/static/js/communs.js"></script>
// Vous pouvez placer cette balise <script> à la fin du corps de votre fichier HTML pour vous assurer que le DOM est entièrement chargé avant d'exécuter le code JavaScript.