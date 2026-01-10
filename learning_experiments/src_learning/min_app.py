from lager_tjeneste import hent_lager, lagre_lager, print_tabell, ny_vare, søk_vare, endre_beholdning


def hovedmeny():

    print("\n" + "="*30)
    print("  LAGERSTYRING V1.0  ")
    print("="*30)


    while True:
        print("\n--- Hovedmeny ---")
        print("1. Vis oversikt")
        print("2. Uttak av komponent")
        print("3. Fylle på komponent")
        print("4. Registrer ny vare")
        print("5. Avslutt")

        valg = input("Hva skal du gjøre?")

        if valg == "1":
            print_tabell(hent_lager())
        elif valg == "2":
            print("\n --Uttak av vare--")
            søkeord = input("Hvilken komponent skal du ha?").lower()
            
            resultater = søk_vare(søkeord)

            if len(resultater) == 0:
                print("Fant ingen resultater")
            else:
                print(f"Fant {len(resultater)} resultater")
                print_tabell(resultater)

                try:
                    vare_id = int(input("Skriv ID på vare du vil ta ut"))
                    endring = int(input("Hvor mange vil du ta ut?"))

                    antall_uttak = endring*(-1)

                    if endre_beholdning(vare_id, antall_uttak):
                        print("Lager oppdatert")
                    else:
                        print("Fant ikke ID. Avbrutt")
                except ValueError:
                    print("Ugyldig verdi")
                
            
        elif valg == "3":
            print("\n --Fylle på vare--")
            
            søkeord = input("Hvilken komponent skal du fylle på?").lower()
            
            resultater = søk_vare(søkeord)

            if len(resultater) == 0:
                print("Fant ingen resultater")
            else:
                print(f"Fant {len(resultater)} resultater")
                print_tabell(resultater)

                try:
                    vare_id = int(input("Skriv ID på vare du vil fylle på"))
                    endring = int(input("Hvor mange legger du til?"))

                    antall_påfyll = endring

                    if endre_beholdning(vare_id, antall_påfyll):
                        print("Lager oppdatert")
                    else:
                        print("Fant ikke ID. Avbrutt")
                except ValueError:
                    print("Ugyldig verdi")
            
        elif valg == "4":
            print("\n --Ny Vare--")
            

            nytt_navn= input("Hva er navn på ny komponent?")
            ny_id = int(input("Hva er id på ny komponent?"))
            nytt_antall = int( input("Hva er antall av komponenten?") )
            ny_lokasjon = input("hva er lokasjonen på komponenten?") 

            ny_vare(nytt_navn, ny_id, nytt_antall, ny_lokasjon)
            print("lagret")


        elif valg == "5":
            break

hovedmeny()
        


