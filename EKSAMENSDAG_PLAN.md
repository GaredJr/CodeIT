# Plan for eksamensdag

*Tirsdag 09.06.2026*

Denne filen er en arbeidsplan for hva jeg skal gjøre på selve eksamensdagen. Målet er å få CodeIT fra lokal prototype til en mer komplett demonstrerbar løsning med GitHub-login, Supabase, serveroppsett og Cloudflare Tunnel.

---

## Hovedmål

```text
CodeIT skal kunne kjøres på server-PC-en, kobles til Supabase, bruke GitHub-login
og være tilgjengelig gjennom Cloudflare Tunnel.
```

Prioritet:

1. Få GitHub-login til å fungere.
2. Flytte riktig `.env`-oppsett til Ubuntu-serveren.
3. Kjøre Flask-appen stabilt på server-PC-en.
4. Sette opp Cloudflare Tunnel mot serveren.
5. Teste hele brukerflyten fra offentlig URL.
6. Dokumentere hva som fungerer og hva som gjenstår.

---

## 1. Første sjekk lokalt

Start med å sjekke at prosjektet fortsatt fungerer lokalt på Mac.

```bash
cd CodeIT
source .venv/bin/activate
python -m py_compile app.py
flask --app app run --port 5002
```

Åpne:

```text
http://127.0.0.1:5002
```

Sjekkliste:

- [x] Forsiden laster.
- [x] Posts vises fra Supabase.
- [x] Create-siden fungerer.
- [x] Login-siden vises.
- [x] `/auth/callback` viser en ryddig feilmelding hvis man besøker den direkte.

---

## 2. Sette opp GitHub-login i Supabase

GitHub-login består av tre deler:

```text
GitHub OAuth App
  -> Supabase Auth Provider
  -> Flask callback route
```

### 2.1 Lag GitHub OAuth App

Gå til:

```text
https://github.com/settings/developers
```

Velg:

```text
OAuth Apps -> New OAuth App
```

Fyll inn:

```text
Application name:
CodeIT

Homepage URL:
http://127.0.0.1:5002

Authorization callback URL:
https://ghhcfzdkklvfpzxqevwh.supabase.co/auth/v1/callback
```

Viktig:

```text
GitHub sin Authorization callback URL skal være Supabase sin callback,
ikke Flask sin /auth/callback.
```

Etterpå:

- [ ] Kopier `Client ID`.
- [ ] Trykk `Generate a new client secret`.
- [ ] Kopier `Client Secret`.
- [ ] Ikke legg secret inn i GitHub eller dokumentasjon.

### 2.2 Aktiver GitHub provider i Supabase

Gå til Supabase:

```text
CodeIT project -> Authentication -> Sign In / Providers -> GitHub
```

Sett:

```text
GitHub Enabled:
ON

Client ID:
<GitHub Client ID>

Client Secret:
<GitHub Client Secret>
```

Trykk `Save`.

### 2.3 Sett Supabase URL Configuration

Gå til:

```text
Authentication -> URL Configuration
```

For lokal testing:

```text
Site URL:
http://127.0.0.1:5002

Redirect URL:
http://127.0.0.1:5002/auth/callback
```

Når Cloudflare-domene er klart, legg også til:

```text
Site URL:
https://<ditt-domene>

Redirect URL:
https://<ditt-domene>/auth/callback
```

Hvis Supabase bare tillater én Site URL, bruk produksjonsdomenet som Site URL og legg lokal URL inn som ekstra redirect URL.

---

## 3. Test GitHub-login lokalt

Start Flask:

```bash
source .venv/bin/activate
flask --app app run --port 5002
```

Åpne:

```text
http://127.0.0.1:5002/login
```

Test:

- [ ] Trykk `continue with GitHub`.
- [ ] Du blir sendt til GitHub.
- [ ] Du blir sendt tilbake til `/auth/callback`.
- [ ] Du ender på egen profilside.
- [ ] Navbar viser `~brukernavn`.
- [ ] Det blir laget en rad i `profiles` i Supabase.

Hvis det feiler:

- Sjekk at GitHub callback URL er Supabase sin callback.
- Sjekk at Supabase redirect URL inneholder Flask sin `/auth/callback`.
- Sjekk at GitHub provider faktisk er aktivert i Supabase.
- Sjekk Flask-terminalen for feilmelding.

---

## 4. Kopiere Supabase keys og env til server-PC

På Mac har prosjektet en `.env` lokalt. Den skal ikke pushes til GitHub, men serveren trenger samme type verdier.

På server-PC-en, lag eller oppdater:

```bash
nano .env
```

Innhold:

```env
SECRET_KEY=<lag-en-lang-random-secret>
FLASK_DEBUG=0

SUPABASE_URL=https://ghhcfzdkklvfpzxqevwh.supabase.co
SUPABASE_PUBLISHABLE_KEY=<supabase-publishable-key>
```

Viktig:

- [ ] Ikke bruk `dev-only-change-me` i produksjon.
- [ ] Ikke push `.env`.
- [ ] Ikke bruk Supabase service-role/secret key i frontend eller repo.
- [ ] Publishable key er grei å bruke i appen, men RLS må beskytte databasen.

Lag en secret key hvis nødvendig:

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

---

## 5. Klargjøre Ubuntu-serveren

SSH inn på server-PC-en:

```bash
ssh <bruker>@<server-ip>
```

Gå til prosjektmappen:

```bash
cd CodeIT
```

Hent siste versjon:

```bash
git pull
```

Sett opp Python hvis nødvendig:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Test appen på serveren:

```bash
flask --app app run --host 127.0.0.1 --port 5002
```

Sjekk fra serveren:

```bash
curl http://127.0.0.1:5002
```

Sjekkliste:

- [ ] Serveren har riktig `.env`.
- [ ] Dependencies installeres.
- [ ] Flask starter uten error.
- [ ] Forsiden returnerer HTML.
- [ ] Supabase-data vises.

---

## 6. Cloudflare Tunnel

Målet er at Cloudflare peker offentlig trafikk til Flask-appen på serveren.

```text
Internett
  |
  v
Cloudflare
  |
  v
cloudflared på Ubuntu-server
  |
  v
http://127.0.0.1:5002
```

### Alternativ A: Dashboard-managed tunnel

Dette er ofte lettest på eksamen.

I Cloudflare Zero Trust:

```text
Networks -> Tunnels -> Create tunnel
```

Velg `cloudflared`, lag tunnel, og følg kommandoen Cloudflare gir for Ubuntu/Debian.

Den ser omtrent slik ut:

```bash
sudo cloudflared service install <TUNNEL_TOKEN>
```

Legg til Public Hostname:

```text
Subdomain:
codeit

Domain:
<ditt-domene>

Service:
http://127.0.0.1:5002
```

### Alternativ B: Lokalt administrert tunnel

Hvis jeg bruker CLI-oppsett:

```bash
cloudflared tunnel login
cloudflared tunnel create codeit
cloudflared tunnel route dns codeit codeit.<ditt-domene>
```

Lag config:

```bash
nano ~/.cloudflared/config.yml
```

Eksempel:

```yaml
tunnel: <tunnel-id>
credentials-file: /home/<bruker>/.cloudflared/<tunnel-id>.json

ingress:
  - hostname: codeit.<ditt-domene>
    service: http://127.0.0.1:5002
  - service: http_status:404
```

Kjør:

```bash
cloudflared tunnel run codeit
```

Installer som service når det fungerer:

```bash
sudo cloudflared service install
sudo systemctl enable cloudflared
sudo systemctl start cloudflared
sudo systemctl status cloudflared
```

---

## 7. Oppdatere Supabase og GitHub for produksjonsdomene

Når Cloudflare URL-en fungerer, må OAuth også vite om domenet.

Eksempel:

```text
https://codeit.<ditt-domene>
```

I Supabase:

```text
Authentication -> URL Configuration
```

Legg til:

```text
https://codeit.<ditt-domene>/auth/callback
```

I GitHub OAuth App:

```text
Homepage URL:
https://codeit.<ditt-domene>

Authorization callback URL:
https://ghhcfzdkklvfpzxqevwh.supabase.co/auth/v1/callback
```

Merk:

```text
GitHub callback URL forblir Supabase sin callback.
Det er Supabase som sender brukeren videre til Flask sin /auth/callback.
```

---

## 8. Produksjonskjøring av Flask

For eksamensdemo kan Flask dev-server fungere, men i dokumentasjonen bør jeg forklare at produksjon burde bruke en WSGI-server.

Minimum for demo:

```bash
flask --app app run --host 127.0.0.1 --port 5002
```

Mer produksjonsriktig videre arbeid:

```text
Gunicorn + systemd service + Cloudflare Tunnel
```

TODO etter eksamen hvis tid:

- [ ] Lage `systemd` service for Flask/Gunicorn.
- [ ] Automatisk restart ved crash.
- [ ] Loggfiler.
- [ ] Backup-rutine.

---

## 9. Full testrekkefølge

Når alt er satt opp:

1. Åpne offentlig Cloudflare URL.
2. Sjekk at forsiden laster.
3. Søk etter en post.
4. Lag en anonym post.
5. Lag en post med GitHub repository-lenke.
6. Logg inn med GitHub.
7. Sjekk profilside.
8. Lag post som innlogget bruker.
9. Kommenter på en post.
10. Upvote en post.
11. Sjekk i Supabase at data faktisk er lagret.

Sjekkliste:

- [ ] Appen fungerer lokalt.
- [ ] Appen fungerer på server-PC.
- [ ] Appen fungerer via Cloudflare.
- [ ] GitHub-login fungerer lokalt.
- [ ] GitHub-login fungerer via Cloudflare URL.
- [ ] Supabase viser nye `profiles`.
- [ ] Supabase viser nye `posts`.
- [ ] Supabase viser nye `comments`.
- [ ] Upvotes lagres.

---

## 10. Hva jeg skal dokumentere underveis

Skriv korte notater mens jeg jobber:

```text
Hva gjorde jeg?
Hvorfor gjorde jeg det?
Hva fungerte?
Hva feilet?
Hvordan løste jeg det?
Hva ville jeg gjort bedre med mer tid?
```

Filer som bør oppdateres:

- `DAG2.md` eller ny daglogg for eksamensdagen
- `docs/ARKITEKTUR.md`
- `docs/DATABASE.md`
- `docs/SIKKERHET_OG_DRIFT.md`
- `docs/TESTPLAN.md`

---

## 11. Ting jeg kan forklare muntlig

Gode faglige poeng:

- Flask håndterer routes og serverlogikk.
- Jinja templates bygger HTML basert på data fra Flask.
- Supabase er PostgreSQL database, Auth og REST API.
- GitHub-login gjør at jeg slipper å lagre passord selv.
- RLS beskytter databasen selv om API-et er tilgjengelig.
- `.env` holder secrets utenfor GitHub.
- Cloudflare Tunnel gjør siden tilgjengelig uten port forwarding.
- Prosjektet er en prototype, og produksjonsklar drift krever mer testing, logging og prosesshåndtering.

---

## 12. Hvis noe går galt

### GitHub-login feiler

- Sjekk GitHub OAuth callback.
- Sjekk Supabase provider.
- Sjekk Supabase redirect URLs.
- Sjekk Flask callback route.
- Sjekk at URL-en er enten lokal eller Cloudflare URL, ikke en blanding.

### Supabase-data vises ikke

- Sjekk `.env`.
- Sjekk `SUPABASE_URL`.
- Sjekk `SUPABASE_PUBLISHABLE_KEY`.
- Sjekk RLS policies.
- Sjekk Flask-terminalen.

### Cloudflare virker ikke

- Sjekk at Flask kjører på `127.0.0.1:5002`.
- Sjekk `cloudflared` status.
- Sjekk public hostname i Cloudflare.
- Sjekk at service peker til `http://127.0.0.1:5002`.

### Serveren stopper

- Start Flask på nytt.
- Hvis tid: sett opp systemd/Gunicorn.

---

## Kilder jeg brukte til oppsettet

- Supabase GitHub-login: https://supabase.com/docs/guides/auth/social-login/auth-github
- Supabase redirect URLs: https://supabase.com/docs/guides/auth/redirect-urls
- Cloudflare Tunnel setup: https://developers.cloudflare.com/tunnel/setup/
- Cloudflare Tunnel som Linux service: https://developers.cloudflare.com/tunnel/advanced/local-management/as-a-service/linux/
