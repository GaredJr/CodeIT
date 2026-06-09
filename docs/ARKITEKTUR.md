# Arkitektur

## Kort forklaring

CodeIT er en kodefokusert sosialplatform inspirert av reddit og stackoverflow, hvor brukere kan stille spørsmål, poste repositories, og hjelpe hverandre. Flask brukes for backend, Jinja templates for frontend, Supabase for database/auth, og Cloudflare for tunneling av prosjektet for å gjøre det tilgjengelig utenfor nettverket og for sikkerhet.


## Arkitekturdiagram

```text
Bruker
  |
  v
Browser
  |
  v
Flask app på Ubuntu-server
  |
  +--> Supabase Auth (GitHub login)
  |
  +--> Supabase Database
  |
  v
Cloudflare Tunnel
  |
  v
Domene / offentlig tilgang
```

## Komponenter

| Komponent | Rolle i prosjektet |
|---|---|
| Flask | Python Webserver |
| Jinja templates | Tar imot data fra flask render_template og lager en html |
| CSS / JS | Css-en er for styling av webpagen, gjøre den fin og ryddig. Javascripten er hovedsaklig for enkel funksjonalitet og auth. |
| Supabase Database | Webpagen sender HTTP forespørseler gjennom supabase APIen med supabase key og user token, til postgres databasen som ligger innenfor, for å endre eller hente informasjon fra tabeller. Sikker cloud-lagring av brukerdata. |
| Supabase Auth | Bruker supabase sin innebygde support for github innlogging, null passord lagres på selve siden, bare brukerinfo. |
| Ubuntu-server | Hoster på egen laptop boota med ubuntu server på lokalt nett. |
| Cloudflare Tunnel | Bruker cloudflare sin tunneling for å gjøre siden åpen utenfor nettet. |

## Viktige routes

| Route | Funksjon |
|---|---|
| `/` | Forside/feed |
| `/create` | Lage post |
| `/post/<id>` | Vise post og kommentarer |
| `/code/<name>` | Filtrere på teknologi/subcodeit |
| `/login` | Login-side |
| `/auth/github` | Starter GitHub OAuth |
| `/auth/callback` | Mottar auth callback |
| `/u/<username>` | Profilside |

## Designvalg

Designet er inspirert av en terminal, med bruk av mørk bakgrunn, varierende farget tekst, ascii characters, osv. Dette er for å passe målgruppen, og fordi jeg personlig synes designed er clean og relativt orginalt.

## Begrensninger

Håndtering av dårlig innhold mangler fortsatt, hvis dette skulle gått globalt hadde det også trengt moderatorer og administratorer, rapportering, sjuling og sletting av innhold, rate limiting, og spam beskyttelse.

## Videre arbeid

Moderasjon, mer avansert søking, brukersikkerhet, bedre kjærnearkitektur, osv.
