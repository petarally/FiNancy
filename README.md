# FiNancy
FiNancy je web aplikacija koja prati režijske troškove.
Omogućava jednostavnu i učinkovitu evidenciju plaćenih računa, kao i unos računa koji trebaju biti podmireni.
Jedan od ključnih značajki FiNancy aplikacije je vizualizacija podataka. Aplikacija nudi grafički prikaz informacija putem pie charta (tortnog grafikona) i bar charta (stupčastog grafikona). Možete odabrati želite li pregled na mjesečnoj ili godišnjoj razini, pružajući vam cjelovitu sliku vaših financija.
Pored vizualizacije, FiNancy vam pruža i deskriptivnu statistiku dolaznih računa, pomažući vam da bolje razumijete svoje financijske obrasce. Također, aplikacija vam omogućuje praćenje promjena cijena u ovisnosti o prethodnim mjesecima, pružajući vam korisne uvide u trendove.
FiNancy ima i jedinstvenu značajku - optimizirani kalkulator plaćanja. Ovaj kalkulator je posebno dizajniran da vam pomogne maksimizirati isplatu računa s određenim iznosom. To znači da možete iskoristiti svaku kunu na najbolji mogući način, osiguravajući da platite što veći broj računa.

## Instalacija

Skidanje koda s GitHub-a:

    cd ~/Downloads
    git clone https://github.com/petarally/FiNancy
    cd financy

Docker tutorial:

    docker build -t financy .
    docker start financy
    docker ps
    docker run -p 8080:8080 financy
