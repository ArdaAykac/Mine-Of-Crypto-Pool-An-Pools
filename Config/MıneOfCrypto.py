import customtkinter as ctk
import tkinter as tk
import time
import random
import json
from PIL import Image
import os


#path
#variable
Level = 0


#Animations
#buttons
#label
colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF"]
color_index = 0


import customtkinter as ctk
import tkinter as tk
import os

# Path
# Variable
Level = 0
Dollars = 0

def open_inventory():
    user_profile = os.environ.get('USERPROFILE')
    inventory_path = os.path.join(user_profile, 'Documents', 'Mıne Of Crypto', 'Inventory')

    if not os.path.exists(inventory_path):
        print("Inventory klasörü bulunamadı.")
        return
    
    inventory_items = os.listdir(inventory_path)

    inventory_window = ctk.CTkToplevel()
    inventory_window.title("Inventory")
    inventory_window.geometry("200x200")

    label_ıtem = ctk.CTkLabel(inventory_window, text="Inventory Items:")
    label_ıtem.pack(pady=10)

    for item in inventory_items:
        item_label = ctk.CTkLabel(inventory_window, text=item)
        item_label.pack(anchor="w", padx=10)

def Shop_system():
    user_profile = os.environ.get('USERPROFILE')
    shop_paths = os.path.join(user_profile, 'Documents', 'Mıne Of Crypto', 'Mods', 'CryptoMınıng gane')
    json_path = os.path.join(shop_paths, 'ıtems.json')
    pixel_font = ctk.CTkFont(family="Press Start 2P", size=15)

    if not os.path.exists(json_path):
        print("Mağaza JSON dosyası bulunamadı.")
        return

    # JSON verisini okur
    with open(json_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    shop_items = data.get("items", [])

    shop_window = ctk.CTkToplevel()
    shop_window.title("Shop")
    shop_window.geometry("350x500")
    #Guı
    #Bar/Frame
    taskbar = ctk.CTkFrame(shop_window, height=30, corner_radius=0, fg_color="gray")
    taskbar.pack(fill="x", side="top")
    #label
    Dollars_label = ctk.CTkLabel(taskbar,text=f"Dollars:{Dollars}",text_color="Green",font=pixel_font)
    Dollars_label.pack(side="left")


    #Scroll Frame
    scroll_frame = ctk.CTkScrollableFrame(shop_window, width=330, height=400)
    scroll_frame.pack(padx=10, pady=5, fill="both", expand=True)

    def select_item(item_name):
        print(f"{item_name} seçildi!")  

    for item in shop_items:
        item_name = item.get("name", "Bilinmeyen Ürün")
        image_path = os.path.join(shop_paths, item.get("image", ""))
        #Frame
        item_frame = ctk.CTkFrame(scroll_frame)
        item_frame.pack(fill="x", padx=10, pady=5)

        if os.path.exists(image_path):  # Eğer görsel dosyası varsa gösterir
            #İmage
            img = ctk.CTkImage(Image.open(image_path), size=(50, 50))
            img_label = ctk.CTkLabel(item_frame, image=img, text="")
            img_label.pack(side="left", padx=5)
        #Button
        item_button = ctk.CTkButton(item_frame, text=item_name, command=lambda n=item_name: select_item(n),text_color="Black") #Burada lambda isimsiz itemler için kullanılıyor
        item_button.pack(side="left", padx=10)

def start_game_check_files_sys():
    user_profile = os.environ.get('USERPROFILE')
    path = os.path.join(user_profile, 'Documents', 'Mıne Of Crypto', 'Cache')
    
    if not os.path.exists(path):
        print("Cache klasörü bulunamadı.")
        return
    
    worlds = [f for f in os.listdir(path) if f.endswith(".dat")]
    
    if not worlds:
        print("Kayıtlı dünya bulunamadı.")
        return
    
    world_selection_win = ctk.CTkToplevel()
    world_selection_win.title("Dünya Seçimi")
    world_selection_win.geometry("300x200")
    pixel_font = ctk.CTkFont(family="Press Start 2P", size=15)

    def start_selected_game():
        selected_world = world_var.get()
        if selected_world:
            world_path = os.path.join(path, selected_world)
            global Level
            
            with open(world_path, 'r') as file:
                for line in file:
                    if line.startswith("Level:"):
                        Level = int(line.split(":")[1].strip())
                        break
            
            game_window = ctk.CTkToplevel()
            game_window.title(f"{selected_world} - Oyun")
            game_window.geometry("400x300")
            
            taskbar = ctk.CTkFrame(game_window, height=30, corner_radius=0, fg_color="gray")
            taskbar.pack(fill="x", side="top")
            

            inventory_button = tk.Button(taskbar, text="Inventory", command=open_inventory,background="Blue",fg="Red",font=pixel_font)
            inventory_button.pack(side="right",padx=10)
            Shop_Button = tk.Button(taskbar,text="Shop", command=Shop_system,background="Blue",fg="green",font=pixel_font)
            Shop_Button.pack(side="right",padx=11)

            level_label = ctk.CTkLabel(taskbar, text=f"Level: {Level}", text_color="white")
            level_label.pack(side="left", padx=10)
            Balance_label = ctk.CTkLabel(taskbar,text=f"Dollars: {Dollars}", text_color="Green")
            Balance_label.pack(side="left",padx=11)

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
    #gui
    #fonts
    pixel_font = ctk.CTkFont(family="Press Start 2P", size=15)
    #function
    def new_game_sys():
        new_game_win = ctk.CTkToplevel()
        new_game_win.title("İnfromations")
        new_game_win.geometry("200x200")
        global new_game_label
        #gui
        #function
        def get_game_name_entry_folder():
            game_name = game_name_entry.get().strip()   
            if not game_name:
                print("Lütfen geçerli bir oyun ismi girin.")
                return
            
            user_profile = os.environ.get('USERPROFILE')
            path = os.path.join(user_profile, 'Documents', 'Mıne Of Crypto')
            
            # Eğer dizin yoksa oluşturur
            if not os.path.exists(path):
                os.makedirs(path)
            
            # Cache klasörünü oluşturur
            cache_folder = os.path.join(path, 'Cache')
            if not os.path.exists(cache_folder):
                os.makedirs(cache_folder)
                print(f"Cache klasörü '{cache_folder}' oluşturuldu.")
            else:
                print("Cache klasörü zaten var.")
            
            # Oyun ismini .dat dosyasına kaydetme
            file_name = f"{game_name}.dat"
            file_path = os.path.join(cache_folder, file_name)
            
            # Aynı ada sahip bir dosya var mı kontrol et
            if os.path.exists(file_path):
                print(f"Hata: '{file_name}' dosyası zaten var.")
            else:
                # Dosyayı oluşturur
                with open(file_path, 'w') as f:
                    f.write(f"Game name: {game_name}\n")
                    f.write(f"Level: {Level}\n")
                    f.write(f"Balance: {Dollars}\n")

                print(f"{file_name} dosyası oluşturuldu ve 'Cache' klasörüne kaydedildi.")
                new_game_win.destroy()
        #anim
        #frame
        #entry
        game_name_entry=ctk.CTkEntry(new_game_win,placeholder_text="Game Name",placeholder_text_color="Blue")
        game_name_entry.pack(anchor="n",pady=10)
        #button
        build_game_button =ctk.CTkRadioButton(new_game_win,text="Build",command=get_game_name_entry_folder)
        build_game_button.pack()
        #label
        new_game_label=ctk.CTkLabel(new_game_win,text="Build New Game", text_color="Orange", font=pixel_font)
        new_game_label.pack(anchor="s",side="bottom")
    #frame
    on_top_frame = ctk.CTkFrame(main,width=80,height=40,corner_radius=0,bg_color="Grey")
    on_top_frame.pack(fill="x")
    #button
    New_game_button = tk.Button(on_top_frame,text="New Game", command=new_game_sys,background="Green",fg="Blue",font=pixel_font)
    New_game_button.pack(anchor="n",padx=10)
    start_game_button = tk.Button(main,text="Start Game", command=start_game_check_files_sys,background="Green",fg="Blue",font=pixel_font)
    start_game_button.pack(anchor="s",pady=10)
    #entry
    #label
    MoonDevelop_label = ctk.CTkLabel(main,text="MoonDevelop",text_color="Blue",font=pixel_font)
    MoonDevelop_label.pack(side="bottom", anchor="w",pady=10)
    #mainloop
    main.mainloop()


main()
