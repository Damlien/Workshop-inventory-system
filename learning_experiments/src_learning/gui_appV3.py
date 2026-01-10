import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
from lager_tjeneste import hent_lager, ny_vare, søk_vare, endre_beholdning, oppdater_vare

class LagerApp:
    def __init__(self, root):
        self.root = root
        self.root.withdraw() # Skjul hovedvinduet mens vi logger inn

        # --- STEG 1: LOGIN (Hvem er du?) ---
        self.er_admin = False
        if not self.vis_login_skjerm():
            root.destroy() # Avslutt hvis man trykker avbryt/kryss
            return
        
        # Hvis vi kom hit, er vi logget inn! Vis hovedvinduet.
        self.root.deiconify() 
        self.root.title(f"Lagerstyring Modern - {'ADMINISTRATOR' if self.er_admin else 'Lagerarbeider'}")
        self.root.geometry("1000x600")
        
        # Styling
        style = ttk.Style()
        style.theme_use('clam') 
        style.configure("Treeview", rowheight=30, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
        
        # Split View
        self.split_view = tk.PanedWindow(root, orient="horizontal", sashrelief="ridge", sashwidth=4)
        self.split_view.pack(fill="both", expand=True)

        # --- VENSTRE SIDE ---
        self.frame_list = tk.Frame(self.split_view, bg="#f0f0f0")
        self.split_view.add(self.frame_list, minsize=400)

        # Søk
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.kjør_søk_auto)
        
        lbl_sok = tk.Label(self.frame_list, text="🔍 Søk i lager:", bg="#f0f0f0", font=("Segoe UI", 10))
        lbl_sok.pack(pady=(10, 0), padx=10, anchor="w")
        
        entry_sok = ttk.Entry(self.frame_list, textvariable=self.search_var)
        entry_sok.pack(fill="x", padx=10, pady=5)

        # Tabell
        kolonner = ("id", "navn", "antall", "hylle") 
        self.tree = ttk.Treeview(self.frame_list, columns=kolonner, show="headings", selectmode="browse")
        
        self.tree.heading("id", text="ID")
        self.tree.column("id", width=50, anchor="center")
        
        self.tree.heading("navn", text="Varenavn")
        self.tree.column("navn", width=200)
        
        self.tree.heading("antall", text="#")
        self.tree.column("antall", width=50, anchor="center")

        # NY KOLONNE
        self.tree.heading("hylle", text="Lokasjon")
        self.tree.column("hylle", width=80, anchor="center")
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.vis_detaljer)
        
        # --- SIKKERHETSSJEKK 1: Kun Admin får se "Ny Vare" knappen ---
        if self.er_admin:
            btn_ny = ttk.Button(self.frame_list, text="+ Registrer Ny Vare", command=self.vis_ny_vare_skjema)
            btn_ny.pack(fill="x", padx=10, pady=10)
        else:
            lbl_info = tk.Label(self.frame_list, text="Du er logget inn som vanlig bruker.\nKontakt admin for å opprette varer.", bg="#f0f0f0", fg="gray")
            lbl_info.pack(pady=10)

        # --- HØYRE SIDE ---
        self.frame_detail = tk.Frame(self.split_view, bg="white")
        self.split_view.add(self.frame_detail, minsize=400)

        self.detail_container = tk.Frame(self.frame_detail, bg="white")
        self.detail_container.pack(fill="both", expand=True, padx=40, pady=40)
        
        lbl_intro = tk.Label(self.detail_container, text="👈 Velg en vare i listen for å se detaljer", 
                             bg="white", fg="gray", font=("Segoe UI", 14))
        lbl_intro.pack(expand=True)

        self.oppdater_liste()

    # ---------------------------------------------------------
    # LOGIN LOGIKK
    # ---------------------------------------------------------
    def vis_login_skjerm(self):
        """Enkelt vindu som spør hvem du er"""
        login_win = tk.Toplevel(self.root)
        login_win.title("Logg inn")
        login_win.geometry("300x200")
        login_win.resizable(False, False)
        
        # Gjør vinduet "modalt" (man MÅ svare på det)
        login_win.grab_set()
        
        tk.Label(login_win, text="Velg Profil", font=("Arial", 14, "bold")).pack(pady=20)

        resultat = tk.BooleanVar(value=False) # Holder styr på om innlogging var OK
        
        def velg_admin():
            # Her kan du legge inn passordsjekk hvis du vil
            passord = simpledialog.askstring("Passord", "Skriv admin passord (tips: 1234)", parent=login_win)
            if passord == "1234":
                self.er_admin = True
                resultat.set(True)
                login_win.destroy()
            elif passord is not None:
                messagebox.showerror("Feil", "Feil passord!")

        def velg_bruker():
            self.er_admin = False
            resultat.set(True)
            login_win.destroy()

        tk.Button(login_win, text="👤 Lagerarbeider (Vanlig)", command=velg_bruker, height=2, width=25).pack(pady=5)
        tk.Button(login_win, text="🔑 Administrator (Full tilgang)", command=velg_admin, height=2, width=25).pack(pady=5)

        # Vent til vinduet lukkes
        self.root.wait_window(login_win)
        return resultat.get()

    # ---------------------------------------------------------
    # MAIN APP LOGIKK
    # ---------------------------------------------------------

    def kjør_søk_auto(self, *args):
        query = self.search_var.get().lower()
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        resultater = søk_vare(query)
        for vare in resultater:
            # Pass på å ta med vare["hylle"] her, og bruk .get() i tilfelle feltet mangler
            self.tree.insert("", "end", iid=str(vare["id"]), values=(
                vare["id"], 
                vare["navn"], 
                vare["antall"], 
                vare.get("hylle", "")  # Henter hylle, eller tom streng hvis mangler
            ))
    def oppdater_liste(self):
        self.kjør_søk_auto()

    def vis_detaljer(self, event):
        # 1. Sikre at vi har en variabel for lagringsmeldinger
        if not hasattr(self, "lagre_melding"):
            self.lagre_melding = ""

        valgt = self.tree.selection()
        if not valgt: return
        
        item = self.tree.item(valgt)
        try:
            valgt_id_fra_liste = int(item['values'][0])
        except ValueError:
            return

        alle_varer = hent_lager()
        vare = next((v for v in alle_varer if v["id"] == valgt_id_fra_liste), None)
        if not vare: return

        # Tøm høyre side
        for widget in self.detail_container.winfo_children():
            widget.destroy()

        # --- VARIABLER ---
        original_id = vare['id'] 
        var_navn = tk.StringVar(value=vare['navn'])
        var_id = tk.StringVar(value=str(vare['id']))
        var_hylle = tk.StringVar(value=vare.get('hylle', '-'))

        # --- NAVN ---
        if self.er_admin:
            tk.Label(self.detail_container, text="Varenavn:", bg="white", fg="gray").pack(anchor="w")
            ent_navn = tk.Entry(self.detail_container, textvariable=var_navn, font=("Segoe UI", 18, "bold"), bg="#ffffe0", relief="solid")
            ent_navn.pack(anchor="w", fill="x", pady=(0, 20))
        else:
            lbl_tittel = tk.Label(self.detail_container, text=vare['navn'], bg="white", font=("Segoe UI", 24, "bold"))
            lbl_tittel.pack(anchor="w", pady=(0, 20))

        # --- INFO TABELL ---
        info_frame = tk.Frame(self.detail_container, bg="white")
        info_frame.pack(fill="x", pady=10)

        # ID
        tk.Label(info_frame, text="ID:", bg="white", fg="gray").grid(row=0, column=0, sticky="w")
        if self.er_admin:
            tk.Entry(info_frame, textvariable=var_id, width=10, bg="#ffffe0").grid(row=1, column=0, sticky="w", padx=(0, 30))
        else:
            tk.Label(info_frame, text=str(vare['id']), bg="white", font=("Segoe UI", 12)).grid(row=1, column=0, sticky="w", padx=(0, 30))

        # Lokasjon
        tk.Label(info_frame, text="LOKASJON:", bg="white", fg="gray").grid(row=0, column=1, sticky="w")
        if self.er_admin:
            tk.Entry(info_frame, textvariable=var_hylle, width=15, bg="#ffffe0").grid(row=1, column=1, sticky="w")
        else:
            tk.Label(info_frame, text=var_hylle.get(), bg="white", font=("Segoe UI", 12)).grid(row=1, column=1, sticky="w")

        # --- LAGRE KNAPP OG STATUS (Kun Admin) ---
        if self.er_admin:
            lbl_status = tk.Label(info_frame, text="", bg="white", font=("Segoe UI", 9, "bold"))
            lbl_status.grid(row=3, column=0, columnspan=2, sticky="w")

            if self.lagre_melding:
                lbl_status.config(text=self.lagre_melding, fg="green")
                self.lagre_melding = "" 
                
                def fjern_tekst():
                    try:
                        lbl_status.config(text="")
                    except tk.TclError:
                        pass
                self.root.after(3000, fjern_tekst)

            def lagre_endringer():
                try:
                    ny_id_int = int(var_id.get())
                except ValueError:
                    lbl_status.config(text="ID ma vaere et tall!", fg="red")
                    return

                suksess = oppdater_vare(
                    gammel_id=original_id,
                    ny_id=ny_id_int,
                    nytt_navn=var_navn.get(),
                    nytt_antall=vare['antall'],
                    ny_hylle=var_hylle.get()
                )

                if suksess:
                    self.lagre_melding = "Endringer lagret"
                    self.oppdater_liste() 
                    
                    if original_id == ny_id_int:
                        try:
                            self.tree.selection_set(str(ny_id_int))
                        except: pass
                else:
                    lbl_status.config(text="Kunne ikke lagre (ID opptatt?)", fg="red")

            btn_save = tk.Button(info_frame, text="LAGRE ENDRINGER", command=lagre_endringer, bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold"))
            btn_save.grid(row=2, column=0, columnspan=2, sticky="w", pady=(15, 5))

        # --- BEHOLDNING (Nå kun én gang!) ---
        tk.Frame(self.detail_container, height=2, bg="#f0f0f0").pack(fill="x", pady=20)
        tk.Label(self.detail_container, text="BEHOLDNING", bg="white", fg="gray", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        
        stock_frame = tk.Frame(self.detail_container, bg="white")
        stock_frame.pack(pady=10, anchor="w")

        tk.Button(stock_frame, text="-", font=("Arial", 20), width=3, bg="#ffcccc", relief="flat",
                  command=lambda: self.endre_antall(vare['id'], -1)).pack(side="left", padx=10)

        tk.Label(stock_frame, text=str(vare['antall']), font=("Segoe UI", 40), bg="white", width=4).pack(side="left", padx=10)

        tk.Button(stock_frame, text="+", font=("Arial", 20), width=3, bg="#ccffcc", relief="flat",
                  command=lambda: self.endre_antall(vare['id'], 1)).pack(side="left", padx=10)
        
        # Manuell
        manuell_frame = tk.Frame(self.detail_container, bg="white")
        manuell_frame.pack(anchor="w", pady=10)
        var_manuell = tk.IntVar(value=0)
        ttk.Entry(manuell_frame, textvariable=var_manuell, width=8).pack(side="left")
        
        def manuell_endring(retning):
            try:
                ant = var_manuell.get()
                if ant > 0: self.endre_antall(vare['id'], ant * retning)
            except: pass

        tk.Button(manuell_frame, text="TA UT", bg="#ffcccc", command=lambda: manuell_endring(-1)).pack(side="left", padx=5)
        tk.Button(manuell_frame, text="FYLL PA", bg="#ccffcc", command=lambda: manuell_endring(1)).pack(side="left", padx=5)
    def endre_antall(self, vare_id, endring):
        endre_beholdning(vare_id, endring)
        self.oppdater_liste()
        try:
            self.tree.selection_set(str(vare_id))
            self.vis_detaljer(None)
        except tk.TclError:
            pass 

    def vis_ny_vare_skjema(self):
        # Dobbeltsjekk i tilfelle noen hacker GUI-et (valgfritt, men god praksis)
        if not self.er_admin:
            messagebox.showerror("Nektet", "Du har ikke tilgang.")
            return

        for widget in self.detail_container.winfo_children():
            widget.destroy()

        tk.Label(self.detail_container, text="Registrer Ny Vare", bg="white", font=("Segoe UI", 20)).pack(pady=20)
        form_frame = tk.Frame(self.detail_container, bg="white")
        form_frame.pack()

        def lag_rad(tekst, rad):
            tk.Label(form_frame, text=tekst, bg="white", font=("Segoe UI", 10)).grid(row=rad, column=0, sticky="w", pady=10)
            e = ttk.Entry(form_frame, width=30)
            e.grid(row=rad, column=1, padx=10, pady=10)
            return e

        e_navn = lag_rad("Navn:", 0)
        e_id = lag_rad("ID (Tall):", 1)
        e_antall = lag_rad("Startantall:", 2)
        e_hylle = lag_rad("Hylle:", 3)

        def lagre():
            try:
                ny_vare(e_navn.get(), int(e_id.get()), int(e_antall.get()), e_hylle.get())
                messagebox.showinfo("Suksess", "Vare opprettet!")
                self.oppdater_liste()
                e_navn.delete(0, "end"); e_id.delete(0, "end")
            except ValueError:
                messagebox.showerror("Feil", "ID og Antall må være tall.")

        ttk.Button(form_frame, text="LAGRE VARE", command=lagre).grid(row=4, column=1, sticky="e", pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = LagerApp(root)
    root.mainloop()