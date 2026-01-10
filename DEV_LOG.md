# Utviklingslogg

**Dato: [10/01/26]**

Opprettet repository i GitHub `Verksted-Lager-system`

installerte Git på pc

klonet repository til egen mappe på min pc
	
- guide:
  - 1) åpne mappe der repository skal lagres på egen pc
  - 2) høyre klikk i mappe og velg `åpne i terminal`
  - 3) hent repository clone link fra github, grønn knapp med `<>code`
	i dette tilfelle: https://github.com/Damlien/Verksted-Lager-system.git
  - 4) i terminal skriv git clone [url]
	i dette tilfelle: git clone https://github.com/Damlien/Verksted-Lager-system.git
  - 5) resulterer i ny mappe med samme navn som repository `Verksted-Lager-system`

la til ekstra mapper i `Verksted-lager-system` på min pc: 
- `learning_experiments` for prosjekter der man lærer kode
- `src` for source code

lagde tekstfilen `DEV_LOG.md` for loggføring

github må nå oppdateres med endringer på pc. 

- her brukes tre kommandoer:	

  - git add . 
    - kommandoen forteller git om hvilke endringer som er gjort og hva som skal være med i neste
    - oppdatering. I kommandoen indikerer punktum alle endringer gjort i prosjketmappen
  
  - git commit -m `beskjed`
    - For dokumentasjon. Låser endringer og gir et unikt ID-nummer. `-m` står fo r message. 				
    - Forklar hva som er gjort i bedskjed merket med  " "

  - git push
    - sender alle endringer og dokumentasjonen til GitHub

I `learning_experiments` mappen ble det opprettet mappen `data_lagring_test` 
- Testing av json for lagring av data med python
- lagde script data_lagring_test.py 

	kode som ble brukt:

		import json

		liste av dioctionaries for lagring av data for komponenter i lager:
			eks:
				komponenter = [
					{"id":1  , "navn": "motstand 10kohm" , "antall": 100, "hyll": 1 },
					{"id":2  , "navn": "Arduino Nano" , "antall": 8 , "hyll": 2  },
					{"id": 3 , "navn": "kondensator", "antall": 20, "hyll": 3 }
				]
		with open(filnavn, operation): 

			formålet med `with` er automatisk håndtering av fil. Filen er åpen for indent blokk under. 
			Etter blokk lukkes filen. 

		json.dump(variabel, filnavn)

		json.load(filnavn)

learning_experiments - script data_lagring_test.py oppdatering
- Gjorde endring i scriptet data_lagring_test.py inne i mappen data_lagring_test 
  - benytter nå library path fra pathlib for moderne og ryddig håndtering av filstier

	kode: 

		from pathlib import path

		BASE_DIR = Path(__file__).resolve().parent 
			første del "Path(__file__)" henter path til python scriptet, 
			.resolve() finner den nøyaktige, absoluttet stien til filen eller mappen.
			.parent finner mappen som filen er i.
			resultate er da full sti til mappen som filen er i.
		
		FIL_STI = BASE_DIR / "lager.json"
			her får man sti til selve filen

Lagde mappen søk og filen søk_i_lager.py 
- scriptet gjør at man kan søke etter komponenter i filen lager.json. 
- Bruker enkel input for søkeord og bruker det for å sammenligne med navn i lager listen

- bruker path library for å finne lokasjon til lager.json som ligger i en annen mappe enn scriptet

Lagde mappen `lager_endring` og scriptene: `vare_pafyll.py`, `vare_registrering.py` og `vare_uttak.py`

- vare_pafyll.py: søke opp vare og legge til flere antall
- vare_uttak.py: søke opp vare og redusere antall
- vare_registrering.py: legge til helt ny komponent


Restrukturering av prosjektet ("Refactoring")
- Innså at å ha separate filer for hver handling (`vare_uttak.py`, `vare_pafyll.py`) ble rotete og førte til mye duplisert kode.
- Opprettet mappen `src_learning` for å samle koden på en mer strukturert måte.
- Delte koden opp i to hoveddeler (Modularisering):
  - `lager_tjeneste.py`: En "backend"-fil som inneholder alle funksjonene (logikken) for å snakke med databasen (`hent_lager`, `lagre`, `søk`, `ny_vare`). Denne filen har ingen `input()` eller `print()`, den håndterer kun data.
  - `min_app.py`: En "frontend"-fil (CLI - Command Line Interface) som styrer menyen og kommuniserer med brukeren. Denne importerer funksjonene fra `lager_tjeneste.py`.

Prototyping av GUI (Grafisk Brukergrensesnitt)
- Ønsket å utforske mulighetene for et visuelt program fremfor tekstbasert terminal.
- Opprettet `gui_appV3.py` i `src_learning`.
- **Note:** Denne filen er i stor grad generert ved hjelp av AI for å demonstrere potensialet i biblioteket `tkinter`.
  - **Formål:** Å ha en fungerende prototype ("Gold Standard") å navigere etter.
  - **Læringspunkt:** Oppdaget at GUI-programmering krever en annen tankegang ("Event-driven") enn de lineære scriptene jeg har skrevet tidligere. Programmet venter på hendelser (klikk) i stedet for å kjøre fra topp til bunn.
- Programmet fungerer og bruker samme logikk fra `lager_tjeneste.py`, men koden er foreløpig for kompleks til å brukes som direkte læringsmateriell.

Plan videre:
- Bruke `lager_tjeneste.py` som grunnmur for videre utvikling.
- Lage små, isolerte GUI-scripts (f.eks. `min_gui_start.py`) for å lære `tkinter` fra bunnen av, steg-for-steg, i stedet for å kopiere store, genererte kodeblokker.