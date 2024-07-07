
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
        <a class="nav-item nav-link" href="/musique"><i class="fas fa-music"></i></a><a class="nav-item nav-link" href="/files"><i class="fas fa-file-alt"></i></a>
                <a class="nav-item nav-link" href="/config"><i class="fas fa-cog"></i></a>
                <a class="nav-item nav-link" href="/login"><i class="fas fa-sign-out-alt"></i></a>
            </div>
        </nav>
        `;
        document.write(htmlCode);
    }
    