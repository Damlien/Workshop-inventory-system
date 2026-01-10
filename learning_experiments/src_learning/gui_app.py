import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from lager_tjeneste import hent_lager, ny_vare, søk_vare, endre_beholdning

# --- 1. OPPSETT AV HOVEDVINDUET ---
root = tk.Tk()
root.title("Lagerstyring v1.0")
root.geometry("600x500") # Litt større vindu nå

# Vi lager en beholder (frame) som skal holde på innholdet vårt
# Denne endrer vi på når vi bytter "side"
innhold_frame = tk.Frame(root)
innhold_frame.pack(fill="both", expand=True, padx=20, pady=20)


# --- 2. HJELPEFUNKSJON FOR Å BYTTE SIDE ---
def bytt_innhold(ny_funksjon):
    """
    Denne sletter alt som er i vinduet nå, og kjører den nye funksjonen
    for å tegne opp det nye innholdet.
    """
    # Slett alt som er i innhold_frame (gamle knapper osv)
    for widget in innhold_frame.winfo_children():
        widget.destroy()
    
    # Kjør funksjonen som tegner det nye innholdet
    ny_funksjon()


# --- 3. SIDE: HOVEDMENY ---
def vis_meny():
    # Overskrift
    lbl = tk.Label(innhold_frame, text="Hovedmeny", font=("Arial", 20, "bold"))
    lbl.pack(pady=20)

    # Knappene (Nå bruker vi lambda for å fortelle 'bytt_innhold' hvor vi skal)
    
    k1 = tk.Button(innhold_frame, text="1. Vis oversikt", 
                   command=lambda: bytt_innhold(vis_oversikt_side), height=2)
    k1.pack(fill="x", pady=5)

    k2 = tk.Button(innhold_frame, text="2. Uttak av vare", height=2,
                   command=lambda: bytt_innhold(lambda: vis_transaksjon_side("uttak")))
    k2.pack(fill="x", pady=5)

    k3 = tk.Button(innhold_frame, text="3. Påfyll av vare", height=2,
                   command=lambda: bytt_innhold(lambda: vis_transaksjon_side("pafyll")))
    k3.pack(fill="x", pady=5)

    k4 = tk.Button(innhold_frame, text="4. Registrer ny vare", height=2,
                   command=lambda: bytt_innhold(vis_registrering_side))
    k4.pack(fill="x", pady=5)

    skille = tk.Frame(innhold_frame, height=2, bd=1, relief="sunken")
    skille.pack(fill="x", pady=20)

    k5 = tk.Button(innhold_frame, text="Avslutt", command=root.destroy, bg="#ffcccc")
    k5.pack(pady=5)


# --- 4. SIDE: OVERSIKT (TABELL) ---
def vis_oversikt_side():
    # Overskrift
    tk.Label(innhold_frame, text="Lagerbeholdning", font=("Arial", 16)).pack(pady=10)

    # Oppsett av tabell
    kolonner = ("id", "navn", "antall", "hylle")
    tabell = ttk.Treeview(innhold_frame, columns=kolonner, show="headings", height=15)
    
    tabell.heading("id", text="ID")
    tabell.heading("navn", text="Navn")
    tabell.heading("antall", text="Antall")
    tabell.heading("hylle", text="Hylle")

    tabell.column("id", width=50, anchor="center")
    tabell.column("navn", width=200)
    tabell.column("antall", width=80, anchor="center")
    tabell.column("hylle", width=80)

    # Scrollbar er kjekt å ha hvis listen blir lang
    scrollbar = ttk.Scrollbar(innhold_frame, orient="vertical", command=tabell.yview)
    tabell.configure(yscroll=scrollbar.set)
    
    # Pakk tabell og scrollbar
    scrollbar.pack(side="right", fill="y")
    tabell.pack(fill="both", expand=True)

    # Fyll inn data
    varer = hent_lager()
    for vare in varer:
        tabell.insert("", tk.END, values=(
            vare.get("id"),
            vare.get("navn"),
            vare.get("antall"),
            vare.get("hylle")
        ))

    # TILBAKE-KNAPP
    btn_tilbake = tk.Button(innhold_frame, text="⬅ Tilbake til meny", 
                            command=lambda: bytt_innhold(vis_meny))
    btn_tilbake.pack(pady=15)





def vis_registrering_side():
    # Overskrift
    tk.Label(innhold_frame, text="Registrer Ny Vare", font=("Arial", 16)).pack(pady=10)

    # --- SKJEMA (Labels og Entries) ---
    
    # Navn
    tk.Label(innhold_frame, text="Navn:").pack(anchor="w", padx=100)
    entry_navn = tk.Entry(innhold_frame)
    entry_navn.pack(fill="x", padx=100)

    # ID
    tk.Label(innhold_frame, text="ID (Tall):").pack(anchor="w", padx=100)
    entry_id = tk.Entry(innhold_frame)
    entry_id.pack(fill="x", padx=100)

    # Antall
    tk.Label(innhold_frame, text="Antall (Tall):").pack(anchor="w", padx=100)
    entry_antall = tk.Entry(innhold_frame)
    entry_antall.pack(fill="x", padx=100)

    # Hylle
    tk.Label(innhold_frame, text="Hylleplassering:").pack(anchor="w", padx=100)
    entry_hylle = tk.Entry(innhold_frame)
    entry_hylle.pack(fill="x", padx=100)

    # --- LAGRE-LOGIKK ---
    def sjekk_og_lagre():
        # 1. Hent tekst fra feltene
        n = entry_navn.get()
        i_tekst = entry_id.get()
        a_tekst = entry_antall.get()
        h = entry_hylle.get()

        # 2. Enkel sjekk at feltene ikke er tomme
        if not n or not i_tekst or not a_tekst:
            messagebox.showwarning("Mangler info", "Du må fylle ut navn, ID og antall!")
            return

        # 3. Prøv å konvertere tall (Dette erstatter try/except fra terminalen)
        try:
            i = int(i_tekst)
            a = int(a_tekst)
            
            # 4. Send til backend (Tjenesten din)
            ny_vare(n, i, a, h)
            
            messagebox.showinfo("Suksess", f"{n} er lagret!")
            
            # Tøm feltene så man kan registrere mer
            entry_navn.delete(0, tk.END)
            entry_id.delete(0, tk.END)
            entry_antall.delete(0, tk.END)
            entry_hylle.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Feil", "ID og Antall må være hele tall!")

    # --- KNAPPER ---
    
    btn_lagre = tk.Button(innhold_frame, text="💾 Lagre vare", 
                          command=sjekk_og_lagre, bg="#ccffcc", height=2)
    btn_lagre.pack(pady=20, fill="x", padx=100)

    btn_tilbake = tk.Button(innhold_frame, text="⬅ Tilbake til meny", 
                            command=lambda: bytt_innhold(vis_meny))
    btn_tilbake.pack(pady=5)



def vis_transaksjon_side(modus):
    # modus er enten "uttak" eller "pafyll"
    tittel = "Uttak av vare" if modus == "uttak" else "Påfyll av vare"
    farge = "#ffcccc" if modus == "uttak" else "#ccffcc" 
    
    tk.Label(innhold_frame, text=tittel, font=("Arial", 16)).pack(pady=10)

    # --- SØKEFELT ---
    sok_frame = tk.Frame(innhold_frame)
    sok_frame.pack(pady=5)
    
    tk.Label(sok_frame, text="Søk: ").pack(side="left")
    entry_sok = tk.Entry(sok_frame)
    entry_sok.pack(side="left", padx=5)

    # --- TABELL ---
    kolonner = ("id", "navn", "antall", "hylle")
    tabell = ttk.Treeview(innhold_frame, columns=kolonner, show="headings", height=8)
    
    for kol in kolonner:
        tabell.heading(kol, text=kol.capitalize())
        tabell.column(kol, width=80)
    tabell.column("navn", width=150)
    
    tabell.pack(pady=10)

    # --- LOGIKK ---

    def kjor_sok(event=None): # <--- Tips: La til 'event=None' så vi kan bruke Enter-tasten senere
        # 1. Tøm tabellen
        for rad in tabell.get_children():
            tabell.delete(rad)
            
        # 2. Hent søkeord (hvis tomt, finner den alt!)
        tekst = entry_sok.get().lower()
        resultater = søk_vare(tekst) 
        
        # 3. Fyll tabellen
        for vare in resultater:
            tabell.insert("", tk.END, values=(
                vare["id"], vare["navn"], vare["antall"], vare.get("hylle", "-")
            ))

    # Knapp for søk
    btn_sok = tk.Button(sok_frame, text="🔍 Søk", command=kjor_sok)
    btn_sok.pack(side="left")
    
    # BONUS: Gjør at søket kjører når du trykker Enter i søkefeltet
    entry_sok.bind("<Return>", kjor_sok) 

    # --- HANDLING (UTTAK/PÅFYLL) ---
    handling_frame = tk.Frame(innhold_frame)
    handling_frame.pack(pady=20)

    tk.Label(handling_frame, text="Antall:").pack(side="left")
    entry_antall = tk.Entry(handling_frame, width=5)
    entry_antall.pack(side="left", padx=5)

    def utfor_handling():
        valgt_item = tabell.selection() 
        if not valgt_item:
            messagebox.showwarning("Ops", "Du må klikke på en vare i listen over!")
            return

        verdier = tabell.item(valgt_item)['values']
        valgt_id = verdier[0]
        valgt_navn = verdier[1]

        try:
            antall = int(entry_antall.get())
            endring = antall * -1 if modus == "uttak" else antall
            
            if endre_beholdning(valgt_id, endring):
                messagebox.showinfo("Suksess", f"Oppdaterte {valgt_navn}!")
                
                # Oppdater tabellen for å vise nytt tall (uten å miste søket)
                kjor_sok() 
                entry_antall.delete(0, tk.END)
            else:
                messagebox.showerror("Feil", "Noe gikk galt med lagringen.")

        except ValueError:
            messagebox.showerror("Feil", "Antall må være et tall!")

    btn_lagre = tk.Button(handling_frame, text="Utfør", command=utfor_handling, bg=farge)
    btn_lagre.pack(side="left", padx=10)

    tk.Button(innhold_frame, text="Tilbake", command=lambda: bytt_innhold(vis_meny)).pack(side="bottom", pady=10)

    # --- HER ER FIXEN ---
    # Vi kjører søkefunksjonen én gang med tom tekstboks når siden lastes.
    # Da fylles tabellen med ALT innholdet fra start.
    kjor_sok()




# --- START APPEN ---
# Vi starter med å vise menyen
vis_meny()

root.mainloop()