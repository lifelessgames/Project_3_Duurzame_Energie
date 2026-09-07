# Project_3_Duurzame_Energie — RHE Online (redesign concept)

Een moderne, frisse herontwerp-concept website voor een Nederlands
duurzame-energiebedrijf (windparkontwikkeling), gebouwd met alleen
HTML, CSS en vanilla JavaScript — geen frameworks, geen build-stap,
geen externe afhankelijkheden nodig om te draaien.

> **Let op:** de live site `rheonline.nl` was vanuit deze omgeving niet
> bereikbaar (netwerktoegang wordt geblokkeerd), dus de content hier is
> **niet 1-op-1 overgenomen** van de echte site. Dit is een origineel
> herontwerp geïnspireerd op de bestandsnamen/afbeeldingen in deze
> repository (windturbineparken, onderstation), met representatieve
> voorbeeldtekst en placeholder-contactgegevens.

## Bekijken

Open `index.html` direct in een browser, of start een lokale server:

```bash
python3 -m http.server 8080
# open http://localhost:8080
```

## Structuur

```
index.html         Homepage
over-ons.html       Over ons / missie / team / geschiedenis
projecten.html      Projectoverzicht met filter (wind / onderstation)
diensten.html       Dienstenoverzicht
contact.html        Contactformulier + info + kaart
css/style.css       Alle styling (licht + donker thema, responsive)
js/main.js          Navigatie, scroll-animaties, tellers, formuliervalidatie
images/             Aangeleverde projectfoto's
favicon.svg         Site-icoon
```

## Ontwerp

- Fris, modern kleurenpalet (donkergroen + lichtgroen accent) passend
  bij een duurzame-energiemerk.
- Volledig responsive (mobiel menu, vloeiende grids).
- Ondersteunt lichte en donkere modus via `prefers-color-scheme`.
- Zachte scroll-reveal animaties en geanimeerde statistieken
  (`IntersectionObserver`, met fallback en `prefers-reduced-motion`).
- Toegankelijkheid: skip-link, `aria-*` attributen, focus states,
  semantische HTML5-structuur.

## Veiligheid

- Geen externe scripts of trackers; alle CSS/JS is lokaal.
- `Content-Security-Policy` meta-tag op iedere pagina.
- Geen `innerHTML`/`eval` met ongefilterde input — formulierfeedback
  gebruikt uitsluitend `textContent`.
- Geen inline event handlers; alle interactiviteit via
  `addEventListener` in `js/main.js`.
- Contactformulier: client-side validatie, honeypot-veld tegen
  eenvoudige spambots, en duidelijke `autocomplete`-attributen. Er is
  geen backend aangesloten — in productie moet het formulier POSTen
  naar een server die invoer server-side valideert, CSRF-bescherming
  toepast en submissies rate-limit.
- Externe links (`target="_blank"`) gebruiken `rel="noopener noreferrer"`.
