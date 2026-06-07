# DAG 1

### PLANLEGGING
Jeg startet dagen med å planlegge prosjektet og hvilke eventuelle teknologier jeg ville bruke til prosjektet.

### WIFI SETUP
Deretter, tenkte jeg å sette opp wifi på nytt på server pc-en min, siden passordet på nettverket her var endret siden sist jeg brukte den, dette tar litt tid siden det er en elgammel pc som helst vil jobbe mot deg i alle tilfeller, men jeg fikk det til å fungere etter ca. 30-40 minutter.

```bash
nmcli device wifi list
nmcli radio wifi off
nmcli radio wifi on
nmcli device wifi connect "Elvebakken-IM" password "placeholder (hemmelig)"

ip a
nmcli device status
systemctl status ssh
hostname -I
```

Deretter, lagde jeg en ssh kobling mellom mac-en og serveren for mer lettvindt utvikling senere.

### VIDERE

Så satt jeg opp en lett KANBAN på github for hva jeg har lyst til å gjøre fremover, spesielt i dag, dette kan jeg endre på senere.

Så startet jeg å jobbe med å lage en visuell profil for siden med hjelp av chatgpt, og fikk lagd en solid logo

**FLASK SETUP**
Nå var det på tide å sette opp noe ordentlig, og få prosjektet i gang.
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install flask
pip freeze > requirements.txt
```

Etter en stund hadde jeg en grei placeholder for nettsiden
Slik ser den ut nå, men har ikke noe ordentlig funksjonalitet:
<img src="/mediadokumentasjon/Home - CodeIT.jpeg" alt="Description" width="500"> 
  