function menu(title){
    document.write(`
        <ul id="lateralmenu">
            <li id="Title"><h4>`+ title +`</h4></li>
            <li><a href="/dashboard">Dashboard</a></li>
            <li><a href="/config">Configuration</a></li>
            <li><a href="/users">Users</a></li>
            <li><a href="/screens">Screens</a></li>
        </ul>
    `);
}