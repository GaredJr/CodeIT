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