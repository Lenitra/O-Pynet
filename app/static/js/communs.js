function writeHTMLNav() {
    var htmlCode = `
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="navbar-nav ml-auto">
            <a class="nav-item nav-link" href="/"><i class="fas fa-home"></i></a>
            <a class="nav-item nav-link" href="/musique"><i class="fas fa-music"></i></a>
            <a class="nav-item nav-link" href="/files"><i class="fas fa-file-alt"></i></a>
            <a class="nav-item nav-link" href="/login"><i class="fas fa-sign-out-alt"></i></a>
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