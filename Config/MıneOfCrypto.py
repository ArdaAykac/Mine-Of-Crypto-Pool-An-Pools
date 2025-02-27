import customtkinter as ctk
import tkinter as tk
import time
import random
import json
from PIL import Image, ImageSequence
import os
import shutil

# Değişkenler
close_electric_sys = True
close_gas_sys = True
Level = 0
Dollars = 0
electric_bill = 0
gas_bill = 0
world_folder = ""
dat_file_path = ""
Dollars_labels = []  # Tüm pencerelerdeki Dollars_label’ları takip etmek için liste

def open_inventory():
    user_profile = os.environ.get('USERPROFILE')
    inventory_path = os.path.join(user_profile, 'Documents', 'Mıne Of Crypto', world_folder, 'Inventory')

    if not os.path.exists(inventory_path):
        print("Envanter klasörü bulunamadı.")
        return
    
    inventory_items = os.listdir(inventory_path)

    inventory_window = ctk.CTkToplevel()
    inventory_window.title("Envanter")
    inventory_window.geometry("300x400")

    scroll_frame = ctk.CTkScrollableFrame(inventory_window, width=280, height=360)
    scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)

    def animate_gif(img_label, frames, delay=200, frame_num=0):
        frame = frames[frame_num]
        img_label.configure(image=frame)
        inventory_window.after(delay, animate_gif, img_label, frames, delay, (frame_num + 1) % len(frames))

    for item in inventory_items:
        if item.endswith(".json"):
            item_frame = ctk.CTkFrame(scroll_frame)
            item_frame.pack(fill="x", padx=5, pady=5)

            with open(os.path.join(inventory_path, item), 'r') as f:
                item_data = json.load(f)
            item_name = item_data.get("name", "Bilinmeyen Ürün")

            image_extensions = [".png", ".jpg", ".gif"]
            image_file = None
            for ext in image_extensions:
                potential_image = os.path.join(inventory_path, item.replace(".json", ext))
                if os.path.exists(potential_image):
                    image_file = potential_image
                    break

            if image_file:
                if image_file.endswith(".gif"):
                    gif_image = Image.open(image_file)
                    frames = [ctk.CTkImage(frame.copy(), size=(30, 30)) for frame in ImageSequence.Iterator(gif_image)]
                    img_label = ctk.CTkLabel(item_frame, image=frames[0], text="")
                    img_label.pack(side="left", padx=5)
                    animate_gif(img_label, frames)
                else:
                    img = ctk.CTkImage(Image.open(image_file), size=(30, 30))
                    img_label = ctk.CTkLabel(item_frame, image=img, text="")
                    img_label.pack(side="left", padx=5)

            item_label = ctk.CTkLabel(item_frame, text=item_name)
            item_label.pack(side="left", padx=5)

def update_dollars_in_dat_file(new_dollars):
    global dat_file_path
    if not os.path.exists(dat_file_path):
        print("Veri dosyası bulunamadı!")
        return

    with open(dat_file_path, 'r') as file:
        lines = file.readlines()

    with open(dat_file_path, 'w') as file:
        for line in lines:
            if line.startswith("Dollars:"):
                file.write(f"Dollars: {new_dollars}\n")
            else:
                file.write(line)

def update_all_dollars():
    global Dollars, Dollars_labels
    for label in Dollars_labels:
        if label.winfo_exists():  # Etiketin hala geçerli olup olmadığını kontrol et
            label.configure(text=f"Dollars: {Dollars}")

def purchase_item(item, price):
    global Dollars
    if Dollars >= price:
        Dollars -= price
        update_dollars_in_dat_file(Dollars)
        
        user_profile = os.environ.get('USERPROFILE')
        inventory_path = os.path.join(user_profile, 'Documents', 'Mıne Of Crypto', world_folder, 'Inventory')
        
        if not os.path.exists(inventory_path):
            os.makedirs(inventory_path)

        item_name = item.get("name", "Unknown Item")
        timestamp = int(time.time())
        item_file = os.path.join(inventory_path, f"{item_name}_{timestamp}.json")
        
        item_details = json.dumps(item)
        with open(item_file, 'w') as f:
            f.write(item_details)
        
        shop_paths = os.path.join(user_profile, 'Documents', 'Mıne Of Crypto', 'Mods', 'CryptoMınıng gane')
        image_path = os.path.join(shop_paths, item.get("image", ""))
        if os.path.exists(image_path):
            image_dest = os.path.join(inventory_path, f"{item_name}_{timestamp}{os.path.splitext(image_path)[1]}")
            shutil.copy(image_path, image_dest)
        
        print(f"{item_name} başarıyla alındı ve envantere eklendi.")
        update_all_dollars()
    else:
        print("Yetersiz bakiye! Ürün satın alınamadı.")

def Payment_system():
    global Dollars, electric_bill, gas_bill, dat_file_path, Dollars_labels

    payments_win = tk.Toplevel()
    payments_win.title("Ödemeler")
    payments_win.geometry("200x300")
    user_home = os.path.expanduser("~")
    icon_path = os.path.join(user_home, "Documents", "Mıne Of Crypto", "Mods", "Mine-Of-Crypto-Pool-An-Pools", "ICON", "MıneOfCryptoicon1.ico")
    payments_win.iconbitmap(icon_path)

    # Etiketleri tanımla
    pixel_font = ctk.CTkFont(family="Press Start 2P", size=15)
    Dollars_label_local = ctk.CTkLabel(payments_win, text=f"Dollars: {Dollars}", text_color="Green", font=pixel_font)
    Dollars_label_local.pack(pady=10)
    Dollars_labels.append(Dollars_label_local)
    
    electric_bill_label = ctk.CTkLabel(payments_win, text=f"Elektrik Faturası: {electric_bill}", text_color="Blue", font=pixel_font)
    electric_bill_label.pack(pady=10)
    
    gas_bill_label = ctk.CTkLabel(payments_win, text=f"Gaz Faturası: {gas_bill}", text_color="Green", font=pixel_font)
    gas_bill_label.pack(pady=10)

    def payment_system_for_pp():
        global Dollars, electric_bill, gas_bill
        if not os.path.exists(dat_file_path):
            print("Veri dosyası bulunamadı!")
            return

        with open(dat_file_path, 'r') as file:
            lines = file.readlines()

        for line in lines:
            if line.startswith("Dollars:"):
                Dollars = int(line.split(":")[1].strip())
            elif line.startswith("Electric Bill:"):
                electric_bill = int(line.split(":")[1].strip())
            elif line.startswith("Gas Bill:"):
                gas_bill = int(line.split(":")[1].strip())

        total_bills = electric_bill + gas_bill
        if Dollars >= total_bills:
            Dollars -= total_bills
            electric_bill = 0
            gas_bill = 0
            print("Faturalar ödendi!")
            update_all_dollars()
            electric_bill_label.configure(text=f"Elektrik Faturası: {electric_bill}")
            gas_bill_label.configure(text=f"Gaz Faturası: {gas_bill}")

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

    pay_button = tk.Button(payments_win, text="Faturaları Öde", command=payment_system_for_pp)
    pay_button.pack(pady=20)

    payments_win.mainloop()

def select_item(item_details):
    details_window = ctk.CTkToplevel()
    details_window.title(f"{item_details['name']} Detayları")
    
    detail_font = ctk.CTkFont(family="Arial", size=12)
    for key, value in item_details.items():
        label_text = f"{key}: {value}"
        detail_label = ctk.CTkLabel(details_window, text=label_text, font=detail_font)
        detail_label.pack(pady=5)

def Shop_system():
    global Dollars, Dollars_labels
    user_profile = os.environ.get('USERPROFILE')
    shop_paths = os.path.join(user_profile, 'Documents', 'Mıne Of Crypto', 'Mods', 'CryptoMınıng gane')
    json_path = os.path.join(shop_paths, 'ıtems.json')
    pixel_font = ctk.CTkFont(family="Press Start 2P", size=15)

    if not os.path.exists(dat_file_path):
        print("Veri dosyası bulunamadı!")
        return

    with open(dat_file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("Dollars:"):
                Dollars = int(line.split(":")[1].strip())

    if not os.path.exists(json_path):
        print("Mağaza JSON dosyası bulunamadı.")
        return

    with open(json_path, "r", encoding="utf-8") as files:
        data = json.load(files)

    shop_items = data.get("items", [])
    shop_window = ctk.CTkToplevel()
    shop_window.title("Mağaza")
    shop_window.geometry("350x500")

    taskbar = ctk.CTkFrame(shop_window, height=30, corner_radius=0, fg_color="gray")
    taskbar.pack(fill="x", side="top")
    
    Dollars_label = ctk.CTkLabel(taskbar, text=f"Dollars: {Dollars}", text_color="Green", font=pixel_font)
    Dollars_label.pack(side="left")
    Dollars_labels.append(Dollars_label)

    scroll_frame = ctk.CTkScrollableFrame(shop_window, width=330, height=400)
    scroll_frame.pack(padx=10, pady=5, fill="both", expand=True)

    def animate_gif(img_label, frames, delay=200, frame_num=0):
        frame = frames[frame_num]
        img_label.configure(image=frame)
        shop_window.after(delay, animate_gif, img_label, frames, delay, (frame_num + 1) % len(frames))

    def buy_item(item):
        item_price = item.get("price", 0)
        purchase_item(item, item_price)

    for item in shop_items:
        item_name = item.get("name", "Bilinmeyen Ürün")
        image_path = os.path.join(shop_paths, item.get("image", ""))

        item_frame = ctk.CTkFrame(scroll_frame)
        item_frame.pack(fill="x", padx=10, pady=5)

        if os.path.exists(image_path):
            if image_path.lower().endswith(".gif"):
                gif_image = Image.open(image_path)
                frames = [ctk.CTkImage(frame.copy(), size=(50, 50)) for frame in ImageSequence.Iterator(gif_image)]
                img_label = ctk.CTkLabel(item_frame, image=frames[0], text="")
                img_label.pack(side="left", padx=5)
                animate_gif(img_label, frames)
            else:
                img = ctk.CTkImage(Image.open(image_path), size=(50, 50))
                img_label = ctk.CTkLabel(item_frame, image=img, text="")
                img_label.pack(side="left", padx=5)

        item_button = ctk.CTkButton(item_frame, text=f"Detaylar: {item_name}", command=lambda details=item: select_item(details), text_color="Black")
        item_button.pack(side="left", padx=10)

        buy_button = ctk.CTkButton(item_frame, text=f"Satın Al: {item.get('price', 0)}$", command=lambda item=item: buy_item(item))
        buy_button.pack(side="left", padx=10)

def start_game_check_files_sys():
    global world_folder, dat_file_path, Dollars, electric_bill, gas_bill, Level, Dollars_labels
    user_profile = os.environ.get('USERPROFILE')
    path = os.path.join(user_profile, 'Documents', 'Mıne Of Crypto', 'Cache')
    
    if not os.path.exists(path):
        print("Cache klasörü bulunamadı.")
        return
    
    worlds = [os.path.splitext(file)[0] for root, dirs, files in os.walk(path) for file in files if file.endswith(".dat")]
    if not worlds:
        print("Kayıtlı dünya bulunamadı.")
        return
    
    world_selection_win = ctk.CTkToplevel()
    world_selection_win.title("Dünya Seçimi")
    world_selection_win.geometry("300x200")
    pixel_font = ctk.CTkFont(family="Press Start 2P", size=15)

    def start_selected_game():
        global world_folder, dat_file_path, Dollars, electric_bill, gas_bill, Level, Dollars_labels
        selected_world = world_var.get()
        if selected_world:
            world_folder = os.path.join(path, selected_world)
            dat_file_path = os.path.join(world_folder, f"{selected_world}.dat")

            if not os.path.exists(dat_file_path):
                print("Seçilen dünya dosyası bulunamadı.")
                return

            with open(dat_file_path, 'r') as file:
                for line in file:
                    if line.startswith("Level:"):
                        Level = int(line.split(":")[1].strip())
                    elif line.startswith("Dollars:"):
                        Dollars = int(line.split(":")[1].strip())
                    elif line.startswith("Electric Bill:"):
                        electric_bill = int(line.split(":")[1].strip())
                    elif line.startswith("Gas Bill:"):
                        gas_bill = int(line.split(":")[1].strip())

            game_window = ctk.CTkToplevel()
            game_window.title(f"{selected_world} - Oyun")
            game_window.geometry("400x300")
            
            taskbar = ctk.CTkFrame(game_window, height=30, corner_radius=0, fg_color="gray")
            taskbar.pack(fill="x", side="top")
            vertical_bar = ctk.CTkFrame(game_window, height=30, width=90, corner_radius=0, fg_color="grey")
            vertical_bar.pack(fill="y", side="right")

            inventory_button = tk.Button(vertical_bar, text="Envanter", command=open_inventory, background="Blue", fg="Red", font=pixel_font)
            inventory_button.pack(side="top", padx=10, pady=10)
            Shop_Button = tk.Button(vertical_bar, text="Mağaza", command=Shop_system, background="Blue", fg="green", font=pixel_font)
            Shop_Button.pack(side="top", padx=5, pady=20)
            payment_bill_button = tk.Button(vertical_bar, text="Ödemeler", command=Payment_system, background="Red")
            payment_bill_button.pack(side="top", padx=5, pady=20)

            level_label = ctk.CTkLabel(taskbar, text=f"Seviye: {Level}", text_color="white")
            level_label.pack(side="left", padx=10)
            Dollars_label = ctk.CTkLabel(taskbar, text=f"Dollars: {Dollars}", text_color="Green")
            Dollars_label.pack(side="left", padx=11)
            Dollars_labels.append(Dollars_label)
            electric_bill_label = ctk.CTkLabel(taskbar, text=f"Elektrik Faturası: {electric_bill}", text_color="Blue")
            electric_bill_label.pack(side="left", padx=7)
            gas_bill_label = ctk.CTkLabel(taskbar, text=f"Gaz Faturası: {gas_bill}", text_color="Green")
            gas_bill_label.pack(side="right", padx=5)
            
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
    main = ctk.CTk()
    main.title("Mıne Of Crypto Menü")
    main.geometry("200x200")
    main._set_appearance_mode("Dark")
    user_home = os.path.expanduser("~")
    icon_path = os.path.join(user_home, "Documents", "Mıne Of Crypto", "Mods", "Mine-Of-Crypto-Pool-An-Pools", "ICON", "MınewOfCryptoIcon3.ico")
    main.iconbitmap(icon_path)

    pixel_font = ctk.CTkFont(family="Press Start 2P", size=15)
    
    def new_game_sys():
        new_game_win = ctk.CTkToplevel()
        new_game_win.title("Bilgiler")
        new_game_win.geometry("200x200")

        def get_game_name_entry_folder():
            game_name = game_name_entry.get().strip()
            if not game_name:
                print("Lütfen geçerli bir oyun ismi girin.")
                return
            
            user_profile = os.environ.get('USERPROFILE')
            base_path = os.path.join(user_profile, 'Documents', 'Mıne Of Crypto')
            if not os.path.exists(base_path):
                os.makedirs(base_path)
            
            cache_folder = os.path.join(base_path, 'Cache')
            if not os.path.exists(cache_folder):
                os.makedirs(cache_folder)
                print(f"Cache klasörü '{cache_folder}' oluşturuldu.")

            game_folder = os.path.join(cache_folder, game_name)
            if not os.path.exists(game_folder):
                os.makedirs(game_folder)
                print(f"'{game_name}' klasörü Cache içinde oluşturuldu.")
            else:
                print(f"Hata: '{game_name}' klasörü zaten var.")
                return
            
            file_name = f"{game_name}.dat"
            file_path = os.path.join(game_folder, file_name)
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    f.write(f"Game name: {game_name}\n")
                    f.write(f"Level: {Level}\n")
                    f.write(f"Dollars: {Dollars}\n")
                    f.write(f"Electric Bill: {electric_bill}\n")
                    f.write(f"Gas Bill: {gas_bill}\n")
                print(f"{file_name} dosyası oluşturuldu ve '{game_folder}' içine kaydedildi.")
                inventory_folder = os.path.join(game_folder, 'Inventory')
                if not os.path.exists(inventory_folder):
                    os.makedirs(inventory_folder)
                    print(f"'Envanter' klasörü '{game_folder}' içinde oluşturuldu.")
            new_game_win.destroy()

        game_name_entry = ctk.CTkEntry(new_game_win, placeholder_text="Oyun Adı", placeholder_text_color="Blue")
        game_name_entry.pack(anchor="n", pady=10)

        build_game_button = ctk.CTkButton(new_game_win, text="Oluştur", command=get_game_name_entry_folder)
        build_game_button.pack()

        new_game_label = ctk.CTkLabel(new_game_win, text="Yeni Oyun Oluştur", text_color="Orange", font=pixel_font)
        new_game_label.pack(anchor="s", side="bottom")

    on_top_frame = ctk.CTkFrame(main, width=80, height=40, corner_radius=0, bg_color="Grey")
    on_top_frame.pack(fill="x")
    
    New_game_button = tk.Button(on_top_frame, text="Yeni Oyun", command=new_game_sys, background="Green", fg="Blue", font=pixel_font)
    New_game_button.pack(anchor="n", padx=10)
    start_game_button = tk.Button(main, text="Oyunu Başlat", command=start_game_check_files_sys, background="Green", fg="Blue", font=pixel_font)
    start_game_button.pack(anchor="s", pady=10)

    MoonDevelop_label = ctk.CTkLabel(main, text="MoonDevelop", text_color="Blue", font=pixel_font)
    MoonDevelop_label.pack(side="bottom", anchor="w", pady=10)

    main.mainloop()

main()