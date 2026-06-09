# Sikkerhet og drift

## Kort forklaring

TODO: Forklar hvordan prosjektet håndterer sikkerhet og hosting.

## Secrets og miljøvariabler

| Variabel | Bruk |
|---|---|
| `SECRET_KEY` | TODO: Flask session-sikkerhet |
| `SUPABASE_URL` | TODO: URL til Supabase-prosjektet |
| `SUPABASE_PUBLISHABLE_KEY` | TODO: Offentlig klientnøkkel til Supabase |

Viktig:

- TODO: Forklar hvorfor `.env` ikke skal pushes til GitHub.
- TODO: Forklar hvorfor `.env.example` kan pushes.
- TODO: Forklar hva som må endres før produksjon.

## Autentisering

TODO: Forklar GitHub OAuth via Supabase Auth.

Flyt:

```text
Bruker klikker GitHub login
  |
  v
Supabase sender bruker til GitHub
  |
  v
GitHub bekrefter bruker
  |
  v
Supabase sender bruker tilbake til /auth/callback
  |
  v
Flask lagrer bruker i session
```

## Hosting

TODO: Forklar hvordan appen skal kjøres på Ubuntu-laptopen.

Punkter:

- Python virtual environment
- Flask / eventuell WSGI-server
- SSH fra Mac til server
- Git pull på server
- Cloudflare Tunnel
- Domene

## Cloudflare Tunnel

TODO: Forklar hvorfor Cloudflare Tunnel brukes i stedet for port forwarding.

## Risikoer

| Risiko | Tiltak |
|---|---|
| Secrets blir lekket | TODO |
| Feil redirect URL i OAuth | TODO |
| Server stopper | TODO |
| Database-regler er for åpne | TODO |
| Misbruk/spam | TODO |

## Produksjonsklarhet

TODO: Skriv hva som må gjøres før prosjektet kan regnes som produksjonsklart.
