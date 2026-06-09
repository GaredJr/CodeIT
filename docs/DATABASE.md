# Database

## Kort forklaring

TODO: Forklar hvorfor prosjektet trenger database.

Eksempel:
Databasen brukes for å lagre brukere, innlegg, kommentarer og stemmer. Supabase er valgt fordi det gir PostgreSQL, autentisering og sikkerhetsregler i samme plattform.

## Tabeller

| Tabell | Formål |
|---|---|
| `profiles` | TODO: Lagrer brukerprofil koblet til Supabase Auth |
| `posts` | TODO: Lagrer innlegg, kode, tags og GitHub repository-lenker |
| `comments` | TODO: Lagrer kommentarer på innlegg |
| `post_votes` | TODO: Lagrer upvotes/avstemninger |

## Relasjoner

```text
profiles
  |
  +-- posts
  |
  +-- comments

posts
  |
  +-- comments
  |
  +-- post_votes
```

## Felt som bør forklares

| Felt | Hvorfor det finnes |
|---|---|
| `author_id` | TODO: Kobler innhold til innlogget bruker |
| `anonymous_author` | TODO: Gjør det mulig å poste uten login |
| `repository_url` | TODO: Lenker en post til et GitHub repository |
| `tags` | TODO: Gjør innhold lettere å søke/filtrere |
| `created_at` | TODO: Sortering og historikk |

## Row Level Security

TODO: Forklar RLS med egne ord.

Punkter å fylle ut:

- Hvem kan lese data?
- Hvem kan opprette posts?
- Hvem kan opprette kommentarer?
- Hvordan hindres brukere fra å skrive som andre brukere?
- Hva er forskjellen på anonym bruker og innlogget bruker?

## Eksempeldata

TODO: Beskriv demo-postene som ligger i databasen.

## Kjente begrensninger

TODO: Skriv hva databasen ikke håndterer enda, for eksempel moderering, sletting, rapportering eller avansert søk.
