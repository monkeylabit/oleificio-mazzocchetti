# Oleificio Mazzocchetti

Sito one-page dell'Oleificio Mazzocchetti: olio extravergine di oliva nuovo da Treciminiere, Atri (TE).

- `index.html`: tutto il sito (stili e script inclusi)
- `img/`: logo, foto, anteprime della hero, immagine di condivisione e icone
- `video/`: video della raccolta per la hero (verticale per i telefoni, orizzontale per gli schermi larghi)

## Pubblicazione

Su Vercel o Netlify basta collegare il repository: `build.mjs` parte da solo, riconosce l'indirizzo del sito e aggiunge canonical, anteprime con immagine per WhatsApp e social, `sitemap.xml` e `robots.txt`.

Su un altro hosting: `SITE_URL=https://tuodominio.it node build.mjs` e carica il contenuto di `dist/`.

## In locale (Mac)

Doppio clic su `Avvia sito.command` (oppure `python3 server.py`). Si apre da solo nel browser su `http://localhost:8080`.

Contatti: 377 229 3124
