# DAG 3
#### EKSAMENSDAGEN
-----
Jeg startet dagen med å få satt opp server pcen, og alt som skal være klart til eksamen.

Deretter fikk jeg clona hele repositoriet over på server maskinen min. Så måtte jeg også få over api keys og secret keys over på maskinen, som ikke kunne ligge i selve repositoriet.
|
|
Da brukte jeg en ekstern skjerm og åpna en terminal på den skjermen. Jeg brukte den terminalen til å secure shelle meg inn på server pcen, og kopierte keysa inn.
<img src="/mediadokumentasjon/DAGC.png" alt="Description" width="500"> 
Så manglet jeg noen moduler:
<img src="/mediadokumentasjon/Screenshot 2026-06-09 at 09.10.22.png" alt="Description" width="500"> 
Installerte alle requirements via requirements.txt:
<img src="/mediadokumentasjon/Screenshot 2026-06-09 at 09.23.03.png" alt="Description" width="500"> 

Også fikk jeg siden hosta opp på nettet igjennom-
http://172.31.1.4:9876/


Deretter startet jeg å jobbe med å sette opp en typ script som ville kjøre hver gang nettet går opp, for å starte opp hostingen av siden.
Etter litt research på stackoverflow og chatgpt kom jeg frem til en måte å gjøre dette på.

For dette lagde jeg to scripts, en til å sjekke om nettet er oppe, som kjører en annen script når det er oppe:
<img src="/mediadokumentasjon/Screenshot 2026-06-09 at 10.42.32.png" alt="Description" width="500"> 
<img src="/mediadokumentasjon/Screenshot 2026-06-09 at 10.41.13.png" alt="Description" width="500">

Da testa jeg scriptsa, og det fungerte fint.
<img src="/mediadokumentasjon/Screenshot 2026-06-09 at 10.40.37.png" alt="Description" width="500"> 

Nå skal jeg ordne noen databasekoblinger som ikke fungerer helt enda.