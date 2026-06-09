# Testplan

## Målet med testing

TODO: Forklar hva du vil bevise med testingen.

Eksempel:
Testingen skal vise at de viktigste brukerflytene fungerer, at data lagres riktig, og at appen håndterer feil på en forståelig måte.

## Manuelle tester

| Test | Forventet resultat | Status |
|---|---|---|
| Åpne forsiden | Feed vises uten feil | TODO |
| Søke etter post | Relevante posts vises | TODO |
| Lage anonym post | Post lagres og vises | TODO |
| Legge ved GitHub repository | Repository-lenke vises på posten | TODO |
| Åpne login-side | GitHub login-knapp vises | TODO |
| Logge inn med GitHub | Bruker sendes til profilside | TODO |
| Lage post som innlogget bruker | Post kobles til riktig profil | TODO |
| Kommentere på post | Kommentar lagres og vises | TODO |
| Upvote post | Vote-teller endres | TODO |
| Åpne profilside | Profil og brukerens posts vises | TODO |

## Tekniske tester

| Test | Kommando/metode | Status |
|---|---|---|
| Python syntax check | `python -m py_compile app.py` | TODO |
| Installer dependencies | `pip install -r requirements.txt` | TODO |
| Start lokal server | `flask --app app run --port 5002` | TODO |
| Test databasekobling | TODO | TODO |
| Test auth callback uten token | TODO | TODO |

## Feiltilfeller

TODO: Fyll ut hvordan appen reagerer på:

- Tom tittel/body ved post creation.
- Ugyldig GitHub repository URL.
- Manglende Supabase config.
- Direkte besøk til `/auth/callback` uten login.
- Databasefeil eller nettverksfeil.

## Kjente begrensninger

TODO: Skriv hva som ikke er testet enda.

## Videre testing

TODO: Skriv hva du ville automatisert senere.
