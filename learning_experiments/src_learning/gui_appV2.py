import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Verktøy for faner og moderne knapper
from lager_tjeneste import hent_lager, ny_vare, søk_vare, endre_beholdning, oppdater_vare 

# --- HOVEDOPPSETT ---
root = tk.Tk()
root.title("Verksted Lagerstyring Pro")
root.geometry("800x600") # Større vindu for dashboard-følelse

# Vi bruker Notebook for å lage faner
faner = ttk.Notebook(root)
faner.pack(fill="both", expand=True)

# --- FANE 1: DASHBOARD (Oversikt + Handling) ---
tab_dashboard = tk.Frame(faner)
faner.add(tab_dashboard, text="📦 Lagerkontroll")

# 1. TOPPEN: SØKEFELT
top_frame = tk.Frame(tab_dashboard, bg="#f0f0f0", pady=10)
top_frame.pack(fill="x")

tk.Label(top_frame, text="Søk i lager:", bg="#f0f0f0", font=("Arial", 12)).pack(side="left", padx=10)
entry_sok = tk.Entry(top_frame, font=("Arial", 12), width=30)
entry_sok.pack(side="left", padx=5)

# 2. MIDTEN: TABELLEN
tree_frame = tk.Frame(tab_dashboard)
tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

kolonner = ("id", "navn", "antall", "hylle")
tabell = ttk.Treeview(tree_frame, columns=kolonner, show="headings")

# Konfigurer kolonner
tabell.heading("id", text="ID")
tabell.column("id", width=60, anchor="center")
tabell.heading("navn", text="Varenavn")
tabell.column("navn", width=300, anchor = "center")
tabell.heading("antall", text="Antall")
tabell.column("antall", width=100, anchor="center")
tabell.heading("hylle", text="Hylle", anchor="center")
tabell.column("hylle", width=100, anchor = "center")

scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tabell.yview)
tabell.configure(yscroll=scrollbar.set)

tabell.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# 3. BUNNEN: HANDLINGSPANELET (Action Panel)
action_frame = tk.Frame(tab_dashboard, bg="#e6e6e6", height=150, bd=1, relief="raised")
action_frame.pack(fill="x", side="bottom")

# Overskrift i handlingspanelet
lbl_action_title = tk.Label(action_frame, text="Velg en vare i listen over for å gjøre endringer", 
                            bg="#e6e6e6", font=("Arial", 10, "italic"))
lbl_action_title.pack(pady=10)

# Input og knapper (skjult til man velger noe? Nei, vi bare disabler dem kanskje, eller lar dem stå)
btn_frame = tk.Frame(action_frame, bg="#e6e6e6")
btn_frame.pack(pady=5)

tk.Label(btn_frame, text="Antall:", bg="#e6e6e6").pack(side="left")
entry_antall = tk.Entry(btn_frame, width=5, font=("Arial", 12))
entry_antall.pack(side="left", padx=5)

# --- LOGIKK FOR DASHBOARD ---

def oppdater_tabell(event=None):
    # Tømmer tabell
    for rad in tabell.get_children():
        tabell.delete(rad)
    
    # Søker (hvis tomt søkefelt -> henter alt)
    tekst = entry_sok.get().lower()
    varer = søk_vare(tekst)

    for v in varer:
        # Fargelegg rader med lite beholdning (valgfritt triks!)
        tag = "normal"
        if v['antall'] < 5:
            tag = "lav_beholdning"

        tabell.insert("", "end", values=(
            v['id'], v['navn'], v['antall'], v.get("hylle", "-")
        ), tags=(tag,))

# Gjør at vi ser rød tekst hvis det er lite igjen
tabell.tag_configure("lav_beholdning", foreground="red") 

def utfør_transaksjon(type_handling):
    # Sjekk valgt vare
    valgt = tabell.selection()
    if not valgt:
        messagebox.showwarning("Ops", "Velg en vare i listen først!")
        return
    
    # Hent data
    item = tabell.item(valgt)
    vare_id = item['values'][0]
    navn = item['values'][1]

    try:
        antall = int(entry_antall.get())
        
        # Logikk: Uttak er minus, Påfyll er pluss
        if type_handling == "uttak":
            endring = antall * -1
            bekreftelse = f"Tok ut {antall} stk av {navn}"
        else:
            endring = antall
            bekreftelse = f"Fylte på {antall} stk til {navn}"

        if endre_beholdning(vare_id, endring):
            # Suksess!
            oppdater_tabell() # Refresh listen
            entry_antall.delete(0, "end") # Tøm felt
            
            # I stedet for popup, oppdaterer vi teksten i bunnen
            lbl_action_title.config(text=f"✅ Suksess: {bekreftelse}", fg="green")
            
            # Resett teksten til svart etter 3 sekunder (kult triks)
            root.after(3000, lambda: lbl_action_title.config(text="Velg en vare...", fg="black"))
        
        else:
            messagebox.showerror("Feil", "Fant ikke varen i systemet.")

    except ValueError:
        messagebox.showerror("Feil", "Skriv inn et gyldig tall i antall-feltet.")




def rediger_valgt_vare():
    # 1. Sjekk at man har valgt noe
    valgt = tabell.selection()
    if not valgt:
        messagebox.showwarning("Ops", "Velg en vare i listen først!")
        return

    # 2. Hent data fra den valgte linjen
    item = tabell.item(valgt)
    verdier = item['values']
    
    # Lagre den gamle ID-en (nøkkelen vår)
    gammel_id = verdier[0] 
    nåværende_navn = verdier[1]
    nåværende_antall = verdier[2]
    nåværende_hylle = verdier[3]

    # 3. Lag et nytt vindu (Pop-up)
    edit_window = tk.Toplevel(root)
    edit_window.title(f"Rediger: {nåværende_navn}")
    edit_window.geometry("300x350")

    # --- SKJEMA ---
    tk.Label(edit_window, text="Navn:").pack(anchor="w", padx=20, pady=(10,0))
    e_navn = tk.Entry(edit_window)
    e_navn.pack(fill="x", padx=20)
    e_navn.insert(0, nåværende_navn) # Fyll inn gammel verdi

    tk.Label(edit_window, text="ID:").pack(anchor="w", padx=20, pady=(10,0))
    e_id = tk.Entry(edit_window)
    e_id.pack(fill="x", padx=20)
    e_id.insert(0, gammel_id)

    tk.Label(edit_window, text="Antall:").pack(anchor="w", padx=20, pady=(10,0))
    e_antall = tk.Entry(edit_window)
    e_antall.pack(fill="x", padx=20)
    e_antall.insert(0, nåværende_antall)

    tk.Label(edit_window, text="Hylle:").pack(anchor="w", padx=20, pady=(10,0))
    e_hylle = tk.Entry(edit_window)
    e_hylle.pack(fill="x", padx=20)
    e_hylle.insert(0, nåværende_hylle)

    # --- LAGRE-KNAPP INNI POP-UP ---
    def lagre_endringer():
        try:
            # Hent de nye verdiene fra feltene
            n_navn = e_navn.get()
            n_id = int(e_id.get())
            n_antall = int(e_antall.get())
            n_hylle = e_hylle.get()

            # Kall backend-funksjonen vi lagde i Steg 1
            if oppdater_vare(gammel_id, n_navn, n_id, n_antall, n_hylle):
                messagebox.showinfo("Suksess", "Varen er oppdatert!")
                edit_window.destroy() # Lukk popup-vinduet
                oppdater_tabell()     # Oppdater listen i hovedvinduet
            else:
                messagebox.showerror("Feil", "Klarte ikke oppdatere varen.")
        
        except ValueError:
            messagebox.showerror("Feil", "ID og Antall må være tall.")

    tk.Button(edit_window, text="💾 Lagre Endringer", command=lagre_endringer, bg="#ccffcc", height=2).pack(pady=20, fill="x", padx=20)




# Knapper
btn_uttak = tk.Button(btn_frame, text="📉 TA UT", bg="#ffcccc", width=15, 
                      command=lambda: utfør_transaksjon("uttak"))
btn_uttak.pack(side="left", padx=20)

btn_pafyll = tk.Button(btn_frame, text="📈 FYLL PÅ", bg="#ccffcc", width=15, 
                       command=lambda: utfør_transaksjon("pafyll"))
btn_pafyll.pack(side="left", padx=20)

btn_rediger = tk.Button(btn_frame, text="✏️ REDIGER", bg="#ffffcc", width=15, 
                        command=rediger_valgt_vare)
btn_rediger.pack(side="left", padx=20) 

# Koble Enter-tasten til søk
entry_sok.bind("<Return>", oppdater_tabell)
# Koble "klikk på tabell" til å oppdatere teksten nede
def ved_klikk(event):
    valgt = tabell.selection()
    if valgt:
        item = tabell.item(valgt)
        navn = item['values'][1]
        lbl_action_title.config(text=f"Valgt vare: {navn} - Hva vil du gjøre?", fg="blue")

tabell.bind("<<TreeviewSelect>>", ved_klikk)


# --- FANE 2: REGISTRERING ---
tab_reg = tk.Frame(faner)
faner.add(tab_reg, text="➕ Ny Vare")

# (Gjenbruk av din gamle registrerings-kode, men forenklet layout)
tk.Label(tab_reg, text="Registrer ny komponent", font=("Arial", 16)).pack(pady=20)

reg_frame = tk.Frame(tab_reg)
reg_frame.pack()

tk.Label(reg_frame, text="Navn:").grid(row=0, column=0, sticky="e", pady=5)
e_navn = tk.Entry(reg_frame); e_navn.grid(row=0, column=1, pady=5)

tk.Label(reg_frame, text="ID:").grid(row=1, column=0, sticky="e", pady=5)
e_id = tk.Entry(reg_frame); e_id.grid(row=1, column=1, pady=5)

tk.Label(reg_frame, text="Antall:").grid(row=2, column=0, sticky="e", pady=5)
e_antall = tk.Entry(reg_frame); e_antall.grid(row=2, column=1, pady=5)

tk.Label(reg_frame, text="Hylle:").grid(row=3, column=0, sticky="e", pady=5)
e_hylle = tk.Entry(reg_frame); e_hylle.grid(row=3, column=1, pady=5)

def lagre_ny():
    try:
        ny_vare(e_navn.get(), int(e_id.get()), int(e_antall.get()), e_hylle.get())
        messagebox.showinfo("Suksess", "Vare lagret!")
        # Tøm feltene
        e_navn.delete(0,"end"); e_id.delete(0,"end"); e_antall.delete(0,"end"); e_hylle.delete(0,"end")
        # Oppdater den andre fanen også!
        oppdater_tabell()
    except ValueError:
        messagebox.showerror("Feil", "Sjekk at ID og Antall er tall.")

tk.Button(tab_reg, text="Lagre Vare", bg="#ccffcc", command=lagre_ny).pack(pady=20)







# --- START ---
oppdater_tabell() # Last inn data med en gang
root.mainloop()