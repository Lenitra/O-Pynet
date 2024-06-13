import json


def format_size(size):
    # Convertir la taille en octets en kilo-octets, méga-octets, etc.
    power = 2**10
    n = 0
    power_labels = {0: 'o', 1: 'Ko', 2: 'Mo', 3: 'Go', 4: 'To'}
    while size > power:
        size /= power
        n += 1
    return f'{size:.2f} {power_labels[n]}'

# ecrit le fichier commun.js pour les éléments de navigation
def wirteCommonJS():
    with open("config.json") as f:
        config = json.load(f)
        
    toregister = """
    function writeHTMLNav() {
        var htmlCode = `
        <style>
            .navbar-nav {
                display: flex;
                flex-direction: row;
                justify-content: flex-end;
                width: 100%;
            }
            .nav-item {
                margin-left: 20px;
            }
        </style>
        <nav class="navbar navbar-dark bg-dark">
            <div class="navbar-nav">
                <a class="nav-item nav-link" href="/"><i class="fas fa-home"></i></a>
        """
        
    if config["modules"]["spotify"]:
        toregister += '<a class="nav-item nav-link" href="/musique"><i class="fas fa-music"></i></a>'
            
    if config["modules"]["files"]:
        toregister += '<a class="nav-item nav-link" href="/files"><i class="fas fa-file-alt"></i></a>'
            
    toregister += """
                <a class="nav-item nav-link" href="/cam"><i class="fas fa-camera"></i></a>
                <a class="nav-item nav-link" href="/login"><i class="fas fa-sign-out-alt"></i></a>
            </div>
        </nav>
        `;
        document.write(htmlCode);
    }
    """
    
    with open("app/static/js/communs.js", "w") as f:
        f.write(toregister)
        
        
    