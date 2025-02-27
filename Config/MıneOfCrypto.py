import customtkinter as ctk
import tkinter as tk
import time
import random
import json
from PIL import Image
import os

# Path
# Variable
close_electric_sys = True
close_gas_sys=True
Level = 0
Dollars = 0
#Bills
electric_bill = 0
gas_bill = 0







def open_inventory():
    user_profile = os.environ.get('USERPROFILE')
    inventory_path = os.path.join(user_profile, 'Documents', 'Mıne Of Crypto',world_folder,'Inventory' )

    if not os.path.exists(inventory_path):
        print("Inventory klasörü bulunamadı.")
        return
    
    inventory_items = os.listdir(inventory_path)

    inventory_window = ctk.CTkToplevel()
    inventory_window.title("Inventory")
    inventory_window.geometry("200x200")

    label_item = ctk.CTkLabel(inventory_window, text="Inventory Items:")
    label_item.pack(pady=10)

    for item in inventory_items:
        item_label = ctk.CTkLabel(inventory_window, text=item)
        item_label.pack(anchor="w", padx=10)

def Payment_system():
    payments_win = tk.Toplevel()
    payments_win.title("Payments")
    payments_win.geometry("200x300")
    user_home = os.path.expanduser("~")
    icon_path = os.path.join(user_home, "Documents", "Mıne Of Crypto", "Mods","Mine-Of-Crypto-Pool-An-Pools", "ICON","MıneOfCryptoicon1.ico")
    payments_win.iconbitmap(icon_path)

    #Guı
    #functions 
    #Frame
    def payment_system_for_pp():
        global Dollars, electric_bill, gas_bill, dat_file_path

        if not os.path.exists(dat_file_path):
            print("Veri dosyası bulunamadı!")
            return

        # .dat dosyasını oku ve verileri güncelle
        with open(dat_file_path, 'r') as file:
            lines = file.readlines()

        for line in lines:
            if line.startswith("Level:"):
                Level = int(line.split(":")[1].strip())
            elif line.startswith("Dollars:"):
                Dollars = int(line.split(":")[1].strip())
            elif line.startswith("Electric Bill:"):
                electric_bill = int(line.split(":")[1].strip())
            elif line.startswith("Gas Bill:"):
                gas_bill = int(line.split(":")[1].strip())

        # Ödemeyi gerçekleştir
        total_bills = electric_bill + gas_bill

        if Dollars >= total_bills:
            Dollars -= total_bills
            electric_bill = 0
            gas_bill = 0
            print("Faturalar ödendi!")
            level_label.configure(text=f"Level: {Level}")
            Dollars_label.configure(text=f"Dollars: {Dollars}")
            electric_bill_label.configure(text=f"Electric Bill: {electric_bill}")
            gas_bill_label.configure(text=f"Gas Bill: {gas_bill}")

            with open(dat_file_path, 'w') as file:
                for line in lines:
                    if line.startswith("Dollars:"):
                        file.write(f"Dollars: {Dollars}\n")
                    elif line.startswith("Electric Bill:"):
                        file.write("Electric Bill: 0\n")
                    elif line.startswith("Gas Bill:"):
                        file.write("Gas Bill: 0\n")
                    else:
                        file.write(line)
        else:
            print("Yetersiz bakiye! Faturaları ödemek için yeterli paranız yok.")
        if total_bills > Dollars:
            close_electric_sys = False
            close_gas_sys = False

            
        
    #label
    #Button
    pay_button=tk.Button(payments_win,text="Pay The Bills",command= payment_system_for_pp)
    pay_button.pack()
    #mainloop
    payments_win.mainloop()


def select_item(item_details):
    details_window = ctk.CTkToplevel()
    details_window.title(f"{item_details['name']} Detayları")
    
    # Label 
    detail_font = ctk.CTkFont(family="Arial", size=12)

    # Ürün detaylarını gösterecek taglar
    for key, value in item_details.items():
        label_text = f"{key}: {value}"
        detail_label = ctk.CTkLabel(details_window, text=label_text, font=detail_font)
        detail_label.pack(pady=5)

def Shop_system():
    user_profile = os.environ.get('USERPROFILE')
    shop_paths = os.path.join(user_profile, 'Documents', 'Mıne Of Crypto', 'Mods', 'CryptoMınıng gane')
    json_path = os.path.join(shop_paths, 'ıtems.json')
    pixel_font = ctk.CTkFont(family="Press Start 2P", size=15)

    global Dollars, electric_bill, gas_bill, dat_file_path

    if not os.path.exists(dat_file_path):
        print("Veri dosyası bulunamadı!")
        return

    # .dat dosyasını oku ve verileri günceller
    with open(dat_file_path, 'r') as file:
        lines = file.readlines()

        for line in lines:
            if line.startswith("Level:"):
                Level = int(line.split(":")[1].strip())
            elif line.startswith("Dollars:"):
                Dollars = int(line.split(":")[1].strip())
            elif line.startswith("Electric Bill:"):
                electric_bill = int(line.split(":")[1].strip())
            elif line.startswith("Gas Bill:"):
                gas_bill = int(line.split(":")[1].strip())

    if not os.path.exists(json_path):
        print("Mağaza JSON dosyası bulunamadı.")
        return

    # JSON verisini okur
    with open(json_path, "r", encoding="utf-8") as files:
        data = json.load(files)

    shop_items = data.get("items", [])

    shop_window = ctk.CTkToplevel()
    shop_window.title("Shop")
    shop_window.geometry("350x500")
    
    # GUI
    # Bar/Frame
    taskbar = ctk.CTkFrame(shop_window, height=30, corner_radius=0, fg_color="gray")
    taskbar.pack(fill="x", side="top")
    
    # Label
    Dollars_label = ctk.CTkLabel(taskbar, text=f"Dollars: {Dollars}", text_color="Green", font=pixel_font)
    Dollars_label.pack(side="left")

    # Scroll Frame
    scroll_frame = ctk.CTkScrollableFrame(shop_window, width=330, height=400)
    scroll_frame.pack(padx=10, pady=5, fill="both", expand=True)

    for item in shop_items:
        item_name = item.get("name", "Bilinmeyen Ürün")
        image_path = os.path.join(shop_paths, item.get("image", ""))
        
        # Frame
        item_frame = ctk.CTkFrame(scroll_frame)
        item_frame.pack(fill="x", padx=10, pady=5)

        if os.path.exists(image_path):  # Eğer görsel dosyası varsa gösterir
            # Image
            img = ctk.CTkImage(Image.open(image_path), size=(50, 50))
            img_label = ctk.CTkLabel(item_frame, image=img, text="")
            img_label.pack(side="left", padx=5)

        # Button
        item_button = ctk.CTkButton(item_frame, text=item_name, command=lambda details=item: select_item(details), text_color="Black")
        item_button.pack(side="left", padx=10)

def start_game_check_files_sys():
    user_profile = os.environ.get('USERPROFILE')
    path = os.path.join(user_profile, 'Documents', 'Mıne Of Crypto', 'Cache')
    
    if not os.path.exists(path):
        print("Cache klasörü bulunamadı.")
        return
    
    # Cache klasöründeki tüm klasörleri al
    worlds = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".dat"):
                worlds.append(os.path.splitext(file)[0])  # Uzantıyı kaldır ve dosya adını ekle

    if not worlds:
        print("Kayıtlı dünya bulunamadı.")
        return
    
    world_selection_win = ctk.CTkToplevel()
    world_selection_win.title("Dünya Seçimi")
    world_selection_win.geometry("300x200")
    pixel_font = ctk.CTkFont(family="Press Start 2P", size=15)

    def start_selected_game():
        global Dollars,gas_bill,electric_bill,dat_file_path,Dollars_label,level_label,gas_bill_label,electric_bill_label
        selected_world = world_var.get()
        global world_folder
        if selected_world:
            global Level
            
            # Seçilen dünyanın klasörünün tam yolunu bul
            world_folder = os.path.join(path, selected_world)  # Klasör yolunu al
            dat_file_path = os.path.join(world_folder, f"{selected_world}.dat")  # Klasör içindeki .dat dosyasının tam yolu

            # .dat dosyasını kontrol et
            print(f"Seçilen dosya yolu: {dat_file_path}")
            
            if not os.path.exists(dat_file_path):
                print("Seçilen dünya dosyası bulunamadı.")
                return
            
            # .dat dosyasını aç ve işlemleri gerçekleştir
            with open(dat_file_path, 'r') as file:
                for line in file:
                    if line.startswith("Level:"):
                        Level = int(line.split(":")[1].strip())
                    if line.startswith("Dollars"):
                        Dollars = int(line.split(":")[1].strip())
                    if line.startswith("Electric Bill"):
                        electric_bill = int(line.split(":")[1].strip())
                    if line.startswith("Gas Bill"):
                        gas_bill = int(line.split(":")[1].strip())
                        break
                
            game_window = ctk.CTkToplevel()
            game_window.title(f"{selected_world} - Oyun")
            game_window.geometry("400x300")
            
            taskbar = ctk.CTkFrame(game_window, height=30, corner_radius=0, fg_color="gray")
            taskbar.pack(fill="x", side="top")
            vertical_bar =ctk.CTkFrame(game_window,height=30,width=90,corner_radius=0,fg_color="grey")
            vertical_bar.pack(fill="y", side="right")

            inventory_button = tk.Button(vertical_bar, text="Inventory", command=open_inventory, background="Blue", fg="Red", font=pixel_font)
            inventory_button.pack(side="top", padx=10,pady=10)
            Shop_Button = tk.Button(vertical_bar, text="Shop", command=Shop_system, background="Blue", fg="green", font=pixel_font)
            Shop_Button.pack(side="top", padx=5,pady=20)
            payment_bill_button = tk.Button(vertical_bar,text="Payments",command=Payment_system,background="Red")
            payment_bill_button.pack(side="top",padx=5,pady=20)

            level_label = ctk.CTkLabel(taskbar, text=f"Level: {Level}", text_color="white")
            level_label.pack(side="left", padx=10)
            Dollars_label = ctk.CTkLabel(taskbar, text=f"Dollars: {Dollars}", text_color="Green")
            Dollars_label.pack(side="left", padx=11)
            electric_bill_label = ctk.CTkLabel(taskbar,text=f"Electric Bill: {electric_bill}",text_color="Blue")
            electric_bill_label.pack(side="left",padx=7)
            gas_bill_label=ctk.CTkLabel(taskbar,text=f"Gas Bill:{gas_bill}",text_color="Green")
            gas_bill_label.pack(side="right",padx=5)
            
            world_selection_win.destroy()
    
    world_var = tk.StringVar(value=worlds[0])

    label = ctk.CTkLabel(world_selection_win, text="Bir dünya seçin:")
    label.pack(pady=10)

    for world in worlds:
        rb = ctk.CTkRadioButton(world_selection_win, text=world, variable=world_var, value=world)
        rb.pack(anchor="w")
    
    start_button = ctk.CTkButton(world_selection_win, text="Başlat", command=start_selected_game)
    start_button.pack(pady=10)

def main():
    main=ctk.CTk()
    main.title("Mıne Of Crypto Menu")
    main.geometry("200x200")
    main._set_appearance_mode("Dark")
    user_home = os.path.expanduser("~")
    icon_path = os.path.join(user_home, "Documents", "Mıne Of Crypto", "Mods","Mine-Of-Crypto-Pool-An-Pools", "ICON","MınewOfCryptoIcon3.ico")
    main.iconbitmap(icon_path)
    # GUI
    # Fonts
    pixel_font = ctk.CTkFont(family="Press Start 2P", size=15)
    
    # Function
    def new_game_sys():
        new_game_win = ctk.CTkToplevel()
        new_game_win.title("İnfromations")
        new_game_win.geometry("200x200")
        global new_game_label
        
        # GUI
        # Function
        def get_game_name_entry_folder():
            game_name = game_name_entry.get().strip() 
            global games_name  
            if not game_name:
                print("Lütfen geçerli bir oyun ismi girin.")
                return
            
            user_profile = os.environ.get('USERPROFILE')
            base_path = os.path.join(user_profile, 'Documents', 'Mıne Of Crypto')

            # Eğer ana dizin yoksa oluştur
            if not os.path.exists(base_path):
                os.makedirs(base_path)
            
            # Cache klasörünü oluştur
            cache_folder = os.path.join(base_path, 'Cache')
            if not os.path.exists(cache_folder):
                os.makedirs(cache_folder)
                print(f"Cache klasörü '{cache_folder}' oluşturuldu.")
            else:
                print("Cache klasörü zaten var.")

            # Oyun için ayrı bir klasör oluştur (Cache'in içinde)
            game_folder = os.path.join(cache_folder, game_name)
            if not os.path.exists(game_folder):
                os.makedirs(game_folder)
                print(f"'{game_name}' klasörü Cache içinde oluşturuldu.")
            else:
                print(f"Hata: '{game_name}' klasörü zaten var.")
                return  # Aynı ada sahip bir klasör varsa işlemi sonlandır
            
            # Oyun ismiyle .dat dosyasını oluştur
            file_name = f"{game_name}.dat"
            file_path = os.path.join(game_folder, file_name)

            # Eğer dosya zaten varsa hata ver
            if os.path.exists(file_path):
                print(f"Hata: '{file_name}' dosyası zaten var.")
            else:
                with open(file_path, 'w') as f:
                    f.write(f"Game name: {game_name}\n")
                    f.write(f"Level: {Level}\n")
                    f.write(f"Dollars: {Dollars}\n")
                    f.write(f"Electric Bill:{electric_bill}\n")
                    f.write(f"Gas Bill: {gas_bill}\n")

                print(f"{file_name} dosyası oluşturuldu ve '{game_folder}' içine kaydedildi.")
                inventory_folder = os.path.join(game_folder, 'Inventory')
            if not os.path.exists(inventory_folder):
                os.makedirs(inventory_folder)
                print(f"'Inventory' klasörü '{game_folder}' içinde oluşturuldu.")
            else:
                print(f"Hata: 'Inventory' klasörü zaten var.")
            new_game_win.destroy()  # Yeni oyun penceresini kapat

        # Anim
        # Frame
        # Entry
        game_name_entry = ctk.CTkEntry(new_game_win, placeholder_text="Game Name", placeholder_text_color="Blue")
        game_name_entry.pack(anchor="n", pady=10)

        # Button
        build_game_button = ctk.CTkRadioButton(new_game_win, text="Build", command=get_game_name_entry_folder)
        build_game_button.pack()

        # Label
        new_game_label = ctk.CTkLabel(new_game_win, text="Build New Game", text_color="Orange", font=pixel_font)
        new_game_label.pack(anchor="s", side="bottom")

    # Frame
    on_top_frame = ctk.CTkFrame(main, width=80, height=40, corner_radius=0, bg_color="Grey")
    on_top_frame.pack(fill="x")
    
    # Button
    New_game_button = tk.Button(on_top_frame, text="New Game", command=new_game_sys, background="Green", fg="Blue", font=pixel_font)
    New_game_button.pack(anchor="n", padx=10)
    start_game_button = tk.Button(main, text="Start Game", command=start_game_check_files_sys, background="Green", fg="Blue", font=pixel_font)
    start_game_button.pack(anchor="s", pady=10)

    # Label
    MoonDevelop_label = ctk.CTkLabel(main, text="MoonDevelop", text_color="Blue", font=pixel_font)
    MoonDevelop_label.pack(side="bottom", anchor="w", pady=10)

    # Mainloop
    main.mainloop()

main()