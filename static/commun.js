function menu(){
    html = `
        <div id="sidebar" class="sidebar sidebar-collapsed">
        <div class="logo">
            <h2>{{config['title']}}</h2>
        </div>
        <ul>
            <li><a href="/dashboard">Accueil</a></li>
            <li><a href="/config">Paramètres</a></li>
            <li><a href="/photos">Photos (SoOn)</a></li>
            <li><a href="/logs">Logs (SoOn)</a></li>
        </ul>
    </div>
    `

    // write html
    document.write(html)
}