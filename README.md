# FiNancy
FiNancy je web aplikacija koja prati režijske troškove.
Aplikacija omugućava evidenciju plaćenih računa kao i unos računa koje je potrebno platiti.
Nadalje, ova web aplikacija nudi grafički prikaz podataka u obliku pie charta (tortni grafikon) i bar charta (stupčasti grafikon).
Ovisno o odabiru grafa, prikaz može biti na mjesečnoj i godišnjoj razini.

Skidanje koda s GitHub-a:

    cd ~/Downloads
    git clone https://github.com/petarally/FiNancy
    cd financy

Docker tutorial:

    docker build -t financy .
    docker-compose up
