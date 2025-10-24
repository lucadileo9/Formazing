## Analisi completa: "Event loop is closed" — cause, diagnosi e soluzione adottata

Questa pagina documenta a 360° la situazione che hai incontrato nel progetto Formazing: l'errore
`RuntimeError: Event loop is closed`, la diagnosi, la soluzione praticata (Soluzione 1 nel documento
`analisi_architettura_e_errore_async.md`) e le raccomandazioni operative per mantenere il sistema
robusto nel tempo.

## Sommario rapido

- Contesto: un'app Flask sincrona (`run.py`) e un processo bot Telegram asincrono (`run_bot.py`).
- Problema: riuso di un client Telegram asincrono legato a un event loop differente -> `Event loop is closed`.
- Soluzione applicata: separazione dei casi d'uso — client "one‑shot" per le route Flask e client persistente
  (Application) per il bot interattivo. Questo elimina la condivisione di un oggetto legato a loop diversi.

## Concetti base (per chi è nuovo a sync/async)

Questa sezione fornisce una spiegazione semplice e pratica dei concetti fondamentali usati nel documento,
pensata per chi non ha familiarità con la programmazione asincrona.

- Sincrono (sync): il codice viene eseguito una istruzione dopo l'altra. Ogni operazione deve finire prima
  che inizi la successiva. Esempio: leggere un file poi inviare una email; la seconda azione aspetta che la
  prima sia conclusa.

- Asincrono (async): il codice può dichiarare punti in cui può cedere il controllo (con `await`) e permettere
  ad altre attività di proseguire nel frattempo. Non significa necessariamente esecuzione parallela su più
  core, ma permette di evitare che il programma resti bloccato durante operazioni di I/O (rete, disco).

- Event loop: è il "motore" che orchestra l'esecuzione delle attività asincrone. Un event loop gestisce quando
  far riprendere ogni attività (coroutine) quando l'I/O è pronto. In Python `asyncio` fornisce l'event loop.

- Coroutine: funzioni definite con `async def` che possono usare `await` per attendere il risultato di altre
  coroutine o operazioni I/O senza bloccare l'intero thread.

- `await` e `async`: `async def` dichiara una coroutine; `await` sospende quella coroutine e passa il controllo
  all'event loop finché l'operazione non è pronta.

- `asyncio.run()`: funzione di alto livello che crea un nuovo event loop, esegue la coroutine principale e poi
  chiude l'event loop al termine. Questo comportamento è importante: se un oggetto async viene creato legato a
  quel loop e poi riutilizzato dopo la chiusura, provocherà errori.

- Differenza tra concorrenza e parallelismo: l'async fornisce concorrenza (gestione di molte attività apparentemente
  sovrapposte) usando un solo thread; il parallelismo usa più thread/processi per eseguire veramente le cose in
  parallelo.

Esempio pratico semplice:

```py
import asyncio

async def slow_io():
    await asyncio.sleep(2)  # simula I/O non bloccante
    return 'done'

async def main():
    result = await slow_io()
    print(result)

# crea un loop, esegue main e lo chiude
asyncio.run(main())
```

Se invece istanziassi un client di rete (es. `Bot`) dentro questo loop e poi provassi a riusarlo dopo che
`asyncio.run()` ha chiuso il loop, riceveresti `RuntimeError: Event loop is closed`.


## Componenti coinvolti (riferimenti file)

- Web app (Flask): `run.py`, `app/__init__.py`, `app/routes.py` — avvio con `app.run(...)` (processo sincronizzato)
- Bot Telegram persistente: `run_bot.py` — avvia processo dedicato con loop persistente
- Servizio di orchestrazione: `app/services/training_service.py` (singleton per processo)
- Telegram service: `app/services/telegram_service.py` — implementa invii one‑shot e avvio polling
- Documentazione analitica: `analisi_architettura_e_errore_async.md` (spiega le soluzioni)

## Cos'è successo — sequenza che porta all'errore

1. Il bot interattivo viene lanciato con `run_bot.py` e crea un event loop persistente che gestisce una
   `telegram.ext.Application` (o un `telegram.Bot`) per tutta la vita del processo.
2. La web app Flask (processo separato) crea occasionalmente event loop temporanei per eseguire
   operazioni async (tipicamente tramite `asyncio.run()` dentro le route o servizi).
3. Se lo stesso oggetto client Telegram (o l'Application) viene creato in un loop e poi riutilizzato in
   un altro loop (o dopo che un loop temporaneo è stato chiuso), il client può tentare operazioni I/O
   su un event loop chiuso → `RuntimeError('Event loop is closed')`.

Questo problema in genere emerge quando la stessa istanza (singleton) di `TelegramService` o del
`telegram.Bot` è condivisa tra contesti di esecuzione diversi.

## Root cause tecnica

- Oggetti asyncio (e molte librerie async) tengono riferimenti all'event loop corrente quando vengono
  istanziati o avviati. Se un oggetto è creato legato a un loop A e poi usato in un loop B o dopo che
  A è stato chiuso, le chiamate I/O falliranno.
- Condivisione di client tra processi non è possibile (memoria separata), ma condivisione tra thread o
  tra contesti di event loop nello stesso processo è pericolosa.

## Soluzione adottata (Soluzione 1) — Overview

Principio: non riutilizzare la stessa istanza del client Telegram tra due contesti di event loop diversi.

Implementazione pratica nel progetto:

- Il bot interattivo (`run_bot.py`) avvia una istanza persistente del client (Application) che vive
  nello stesso processo e usa il suo loop persistente. Questo è il solo posto in cui l'Application
  persistente esiste.
- Le route della web app (Flask) non accedono al client persistente del bot. Al contrario, per ogni
  invio "one‑shot" (notifiche, feedback, ecc.) il `TelegramService` crea un client temporaneo, lo usa con un `async with` o in un contesto creato ad hoc, e lo chiude pulitamente allo scopo.

Vantaggio: l'oggetto client è sempre legato al loop che lo usa, non c'è riuso tra loop e quindi non si verifica l'errore "Event loop is closed".

## Dettagli di implementazione consigliati e pattern usati

1) One‑shot pattern (usato da Flask routes)

Pseudocodice pattern (semplificato):

```py
async def _send_one_shot(token, chat_id, message):
    # crea e usa un bot legato al loop corrente
    async with telegram.Bot(token=token) as bot:
        await bot.send_message(chat_id=chat_id, text=message)

# chiamato dal servizio: asyncio.run(_send_one_shot(...))
```

Benefici:
- Nessun oggetto persistente rimane legato ad altri loop.
- Chiusura deterministica delle risorse.

2) Persistent bot (usato da `run_bot.py`)

Il codice che avvia il bot mantiene un'Application/polling in un processo dedicato (es. `run_bot.py`):

```py
def run_bot_sync():
    # crea e avvia l'Application; non deve essere chiamato dalla web app
    application = Application.builder().token(TOKEN).build()
    application.run_polling()

# run_bot.py: chiamata a training_service.telegram_service.run_bot_sync()
```

Nota: quando si avvia il bot persistente, è corretto creare la Application nel contesto del suo loop.

3) Raccomandazione: non istanziare client async nel costruttore

Evitare di chiamare `telegram.Bot(...)` o `Application(...)` dentro `__init__` di `TelegramService`,
perché quel costruttore potrebbe essere eseguito in un contesto con loop diverso.
Invece, istanziare on‑demand o durante `run_bot_sync()`.

4) Helper contextmanager (consigliato)

Centralizza la logica one‑shot con un piccolo helper in `TelegramService`, ad esempio `_temporary_bot` che incapsula creare/usare/chiudere il bot. Questo riduce duplicazioni e rende i test più semplici.


## Casi limite ed edge case

- Threading: se la web app gira in modalità threaded (`app.run(threaded=True)`), il pattern one‑shot
  continua a funzionare finché non condividi istanze di bot tra thread.
- Reloader (dev): il reloader di Flask può avviare più processi; assicurati che il bot persistente non venga avviato accidentalmente in più processi. Tenere `run_bot.py` come processo separato evita questo rischio.
- Rate limiting: creare bot temporanei ripetutamente ha overhead; se hai altissimo throughput di invii valuta un meccanismo di pooling o un processo di dispatch dedicato (es. una coda con worker).

## Esempi di file rilevanti da aprire

- `app/services/telegram_service.py` — implementazione di invii one‑shot e `run_bot_sync`  
- `run.py` — entry point web app Flask (processo separato)  
- `run_bot.py` — entry point processo bot Telegram  
- `analisi_architettura_e_errore_async.md` — analisi originaria e opzioni di soluzione

## Conclusione 

Hai applicato la soluzione più pratica e a basso impatto: separare il client persistente del bot dal
client one‑shot usato dalle route. Questo risolve la causa tecnica dell'errore e mantiene il codice
semplice e comprensibile. Le raccomandazioni qui sopra ti aiutano a consolidare il pattern e prevenire
regressioni in futuri cambiamenti.

---