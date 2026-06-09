```text
   ______          __     __________
  / ____/___  ____/ /__  /  _/_  __/
 / /   / __ \/ __  / _ \ / /  / /   
/ /___/ /_/ / /_/ /  __// /  / /    
\____/\____/\____/\___/___/ /_/     
                                    
```

# Eksamensprosjekt 05. - 09.06.2026

<div align="center">

## CODEIT

**Lett tilgjengelig og lettvindt Reddit typ sosial platform spesifikt for koding.**

</div>

---

## IDE

**Navn:** ***CODEIT***

Lett tilgjengelig og lettvindt Reddit typ sosial platform spesifikt for koding.

"Subreddits" for forskjellige typer kodespråk og teknologier.

Kan legge ved kodesnippets, github repositories, osv.

---

## TEKNOLOGIER

| Teknologi | Bruk |
|---|---|
| Gammel laptop med Ubuntu Server | Hoste nettsiden og ulike teknologier |
| Cloudflare | Tunneling av siden for å gjøre den tilgjengelig på et domene, og utenfor det lokale nettverket |
| Supabase | Databaser og brukerlagring |
| HTML / CSS | Frontend design |
| JS | Enkel backend |
| Flask | Koblinger |
| GIT + SSH | Syncing av siden mellom Mac og server |
| GITHUB + KANBAN | Planlegging og backup |
| Adobe Photoshop / Illustrator | Design av logo *(Ikke relevant lol)* |
| CHATGPT | Hjelp med planlegging og enkle elementer for raskere utvikling |

> Cloudflare brukes også for sikker kobling til siden, uten lekkasje av hemmelige keys osv.

---

## FORMÅL

Gjøre det mye lettere for uviklere å dele kunnskap og hjelpe hverandre, uten krav for pålogging, men muligheten til det.

Alle kan poste spørsmål, dele repositories og kode, og bli kjent med nye utviklere som er interresserte i samme ting som deg.

---

## HOVEDIDÉ

```text
CODEIT = Reddit typ sosial platform + koding + subreddits for teknologi
```

---

## MULIGHETER

- Poste spørsmål
- Dele kode
- Legge ved kodesnippets
- Legge ved github repositories
- Lage "subreddits" for kodespråk og teknologier
- Bruke siden uten krav for pålogging
- Ha mulighet til pålogging

---

## PROSJEKTSTACK

```text
Mac  ->  Git / SSH  ->  Ubuntu Server  ->  Flask / JS / Supabase
                           |
                           v
                     Cloudflare Tunnel
                           |
                           v
                         Domene
```

---

## STATUS

```text
[x] Planlegging
[x] Design
[x] Frontend
[-] Backend
[-] Database
[-] Hosting
[ ] Testing
[ ] Ferdigstilling
```

---

## EKSAMENSDOKUMENTASJON

Disse filene brukes som placeholders for å vise teknisk kompetanse, refleksjon og arbeidsprosess i prosjektet:

| Dokument | Hva det skal vise |
|---|---|
| [docs/ARKITEKTUR.md](docs/ARKITEKTUR.md) | Hvordan frontend, Flask, Supabase, GitHub Auth, Ubuntu-server og Cloudflare henger sammen |
| [docs/DATABASE.md](docs/DATABASE.md) | Databasemodell, tabeller, relasjoner, RLS og hvordan data lagres |
| [docs/SIKKERHET_OG_DRIFT.md](docs/SIKKERHET_OG_DRIFT.md) | Miljøvariabler, secrets, OAuth, hosting, tunnel og produksjonsvurderinger |
| [docs/TESTPLAN.md](docs/TESTPLAN.md) | Hva som skal testes, hvordan det testes, og kjente begrensninger |

### Kompetanse jeg vil vise

- Fullstack-utvikling med Flask, HTML, CSS, JavaScript og Supabase.
- Databasedesign med profiler, posts, kommentarer og votes.
- Autentisering via GitHub OAuth gjennom Supabase Auth.
- Sikker bruk av miljøvariabler og hemmelige nøkler.
- Hosting på egen Ubuntu-server med Cloudflare Tunnel.
- Iterativ utviklingsprosess dokumentert i dagloggene.
- Refleksjon rundt begrensninger, sikkerhet, brukervennlighet og videre arbeid.
