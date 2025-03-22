import customtkinter as ctk
import tkinter as tk
import time
import json
from PIL import Image, ImageSequence,ImageTk
import os
import shutil
import threading
import random
import pygame

# Global değişkenler
close_electric_sys = True
close_gas_sys = True
power_types = "W"
set_timer_stat =False #core loader main loader gibi deflerin yükleme bittiyse devam et durumu
Level = 0
xp = 0.000
Dollars = 900
gas_bill = 0
electric_bill = 0
total_power = 0
world_folder = ""
dat_file_path = ""
Dollars_labels = []  
moc_coins = 0.0
room_temperature = 2  
active_windows = {}  
using_power = 0  
musics_stats = True
user_profile = os.environ.get('USERPROFILE')
sounds_path = os.path.join(user_profile, 'Documents', 'Mıne Of Crypto', 'Mods', 'Sounds')
shop_music = os.path.join(sounds_path, 'İnSlowMotionsMenuSound.mp3')
main_music_path = os.path.join(sounds_path, 'GameSoundALone.mp3')







def main_loader():
    global loader_screen_win
    loader_screen_win = tk.Tk()
    loader_screen_win.title("MoonDevelopGame")
    loader_screen_win.geometry("300x300")
    loader_screen_win.attributes("-toolwindow",True)
    loader_screen_win.resizable(False, False)
    loader_screen_win.overrideredirect(False) 
    #path
    screen_png_path = os.path.join(user_profile,'Documents', 'Mıne Of Crypto', 'Mods',"ICON")
    screen_png = os.path.join(screen_png_path, "MoonDevelopGame.png")
    #Load Sys
    image = Image.open(screen_png)
    image = image.resize((300, 300), Image.LANCZOS)
    logo = ImageTk.PhotoImage(image)

    label = tk.Label(loader_screen_win, image=logo)
    label.place(x=0, y=0, relwidth=1, relheight=1) 

    #updater
    loader_screen_win.update_idletasks()
    screen_width = loader_screen_win.winfo_screenwidth()
    screen_height  = loader_screen_win.winfo_screenheight()
    x = (screen_width - 800) // 2
    y = (screen_height - 600) // 2
    loader_screen_win.geometry(f"300x300+{x}+{y}")
    loader_screen_win.after(2000, lambda:[loader_screen_win.destroy(),main()])


    loader_screen_win.mainloop()


def loader_screen():
    loader_screen_win = tk.Tk()
    loader_screen_win.title("MoonDevelopGame")
    loader_screen_win.geometry("300x300")
    loader_screen_win.attributes("-toolwindow", True)
    loader_screen_win.resizable(False, False)
    loader_screen_win.overrideredirect(True)

    # Path to GIF file
    screen_gif_path = os.path.join(user_profile, 'Documents', 'Mıne Of Crypto', 'Mods', 'ICON')
    screen_gif = os.path.join(screen_gif_path, "MoonDevelopGame.gif")

    # Open GIF and get all frames
    gif_image = Image.open(screen_gif)
    frames = []
    try:
        while True:
            frames.append(gif_image.copy())  # Save the raw frame images
            gif_image.seek(gif_image.tell() + 1)
    except EOFError:
        pass

    # Create label to display GIF
    label = tk.Label(loader_screen_win)
    label.pack(fill=tk.BOTH, expand=True)  # Makes the label fill the entire window

    # Function to update the GIF
    def update_frame(frame_index):
        frame = frames[frame_index]

        # Resize the frame to fill the window size
        width = loader_screen_win.winfo_width()
        height = loader_screen_win.winfo_height()

        # Resize the frame to match the window size using better quality resampling
        resized_frame = frame.resize((width, height), Image.Resampling.LANCZOS)

        # Convert resized frame to PhotoImage
        resized_frame_tk = ImageTk.PhotoImage(resized_frame)
        label.config(image=resized_frame_tk)
        label.image = resized_frame_tk  # Keep a reference to avoid garbage collection

        loader_screen_win.after(100, update_frame, (frame_index + 1) % len(frames))  # Update every 100ms

    # Start the animation
    update_frame(0)

    # Center the window on the screen
    loader_screen_win.update_idletasks()
    screen_width = loader_screen_win.winfo_screenwidth()
    screen_height = loader_screen_win.winfo_screenheight()
    x = (screen_width - 300) // 2
    y = (screen_height - 300) // 2
    loader_screen_win.geometry(f"300x300+{x}+{y}")

    loader_screen_win.mainloop()












# Tüm dataları .dat dosyasında günceller
def update_all_values_in_dat_file():
    global Dollars, gas_bill, electric_bill, total_power, moc_coins, room_temperature, using_power
    if not os.path.exists(dat_file_path):
        print("Veri dosyası bulunamadı!")
        return
    with open(dat_file_path, 'r') as file:
        lines = file.readlines()
    with open(dat_file_path, 'w') as file:
        for line in lines:
            if line.startswith("Dollars:"):
                file.write(f"Dollars: {Dollars}\n")
            elif line.startswith("Gas Bill:"):
                file.write(f"Gas Bill: {gas_bill}\n")
            elif line.startswith("Electric Bill:"):
                file.write(f"Electric Bill: {electric_bill}\n")
            elif line.startswith("Total Power:"):
                file.write(f"Total Power: {total_power}\n")
            elif line.startswith("MOC Coins:"):
                file.write(f"MOC Coins: {moc_coins}\n")
            elif line.startswith("Room Temperature:"):
                file.write(f"Room Temperature: {room_temperature}\n")
            elif line.startswith("Using Power:"):  # Yeni eklenen alan
                file.write(f"Using Power: {using_power}\n")
            else:
                file.write(line)
        if not any(line.startswith("Electric Bill:") for line in lines):
            file.write(f"Electric Bill: {electric_bill}\n")
        if not any(line.startswith("MOC Coins:") for line in lines):
            file.write(f"MOC Coins: {moc_coins}\n")
        if not any(line.startswith("Room Temperature:") for line in lines):
            file.write(f"Room Temperature: {room_temperature}\n")
        if not any(line.startswith("Using Power:") for line in lines):  
            file.write(f"Using Power: {using_power}\n")
    refresh_all_windows()  # Her güncellemede pencereleri yeniler

# Refresher for windows
def refresh_all_windows():
    global using_power
    for window_name, widgets in active_windows.items():
        if widgets['window'].winfo_exists():
            for key, widget in widgets.items():
                if key != 'window' and widget.winfo_exists():
                    if key == 'Dollars_label':
                        widget.configure(text=f"Dollars: {Dollars}")
                    elif key == 'gas_bill_label':
                        widget.configure(text=f"Gaz Faturası: ${gas_bill}")
                    elif key == 'electric_bill_label':
                        widget.configure(text=f"Elektrik Faturası: ${electric_bill}")
                    elif key == 'total_power_label':
                        widget.configure(text=f"Toplam Güç: {total_power} {power_types}")
                    elif key == 'moc_coins_label':
                        widget.configure(text=f"MOC Coins: {moc_coins:.3f}")
                    elif key == 'temp_label':
                        widget.configure(text=f"Oda Sıcaklığı: {room_temperature}°C")
                    elif key == 'using_power_label':
                        widget.configure(text=f"Kullanılan Güç: {using_power} W")

# Ayarları kaydetme fonksiyonu
def save_settings_to_file(music_on, volume_level):
    settings_file_path = os.path.join(world_folder, "settings.dat")
    with open(settings_file_path, 'w') as f:
        f.write(f"Music: {music_on}\n")
        f.write(f"Volume: {volume_level}\n")
    print(f"Ayarlar {settings_file_path} dosyasına kaydedildi.")

# Load Settings sys
def load_settings_from_file():
    global musics_stats
    settings_file_path = os.path.join(world_folder, "settings.dat")
    music_on = True  
    volume_level = 0.5  
    
    if os.path.exists(settings_file_path):
        with open(settings_file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("Music:"):
                    music_on = line.split(":")[1].strip() == "True"
                elif line.startswith("Volume:"):
                    volume_level = float(line.split(":")[1].strip())
    
    # Applying settings
    musics_stats = music_on
    pygame.mixer.music.set_volume(volume_level)
    if music_on and pygame.mixer.music.get_busy():
        pygame.mixer.music.unpause()
    elif not music_on:
        pygame.mixer.music.pause()
    return music_on, volume_level

# Settings sys
def Settings_system():
    global musics_stats
    settings_window = ctk.CTkToplevel()
    settings_window.title("Ayarlar")
    settings_window.geometry("300x200")
    pixel_font = ctk.CTkFont(family="Press Start 2P", size=12)

    # Mevcut ayarları yükle
    music_on, volume_level = load_settings_from_file()

    # Ses seviyesini güncelleme fonksiyonu (önce tanımlıyoruz)
    def update_volume(value):
        pygame.mixer.music.set_volume(value)
        volume_label.configure(text=f"Ses Seviyesi: {int(value * 100)}%")
        save_settings_to_file(musics_stats, value)

    # Müziği açma/kapama fonksiyonu (önce tanımlıyoruz)
    def toggle_music(state):
        global musics_stats
        musics_stats = state
        if state:
            pygame.mixer.music.unpause()
            print("Müzik açıldı.")
        else:
            pygame.mixer.music.pause()
            print("Müzik kapatıldı.")
        save_settings_to_file(musics_stats, volume_slider.get())

    # Müzik aç/kapa
    music_var = tk.BooleanVar(value=music_on)
    music_check = ctk.CTkCheckBox(settings_window, text="Müzik Açık", variable=music_var, font=pixel_font,
                                  command=lambda: toggle_music(music_var.get()))
    music_check.pack(pady=10)

    # Ses seviyesi kaydırıcısı
    volume_label = ctk.CTkLabel(settings_window, text=f"Ses Seviyesi: {int(volume_level * 100)}%", font=pixel_font)
    volume_label.pack(pady=5)
    volume_slider = ctk.CTkSlider(settings_window, from_=0, to=1, number_of_steps=100, command=update_volume)
    volume_slider.set(volume_level)
    volume_slider.pack(pady=10)

    # Kapatma işlemi
    def on_close():
        settings_window.destroy()

    settings_window.protocol("WM_DELETE_WINDOW", on_close)

# ROom Sys
def Rooms_system():
    global world_folder, total_power, power_types, Dollars_labels, dat_file_path, electric_bill, moc_coins, room_temperature, using_power
    
    rooms_window = ctk.CTkToplevel()
    rooms_window.title("Odalar")
    rooms_window.geometry("600x800")
    
    main_frame = ctk.CTkFrame(rooms_window)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    taskbar = ctk.CTkFrame(rooms_window, width=120, corner_radius=0, fg_color="gray")
    taskbar.pack(side="right", fill="x", padx=5, pady=5)
    pixel_font = ctk.CTkFont(family="Press Start 2P", size=12)
    
    inventory_path = os.path.join(os.environ.get('USERPROFILE'), 'Documents', 'Mıne Of Crypto', world_folder, 'Inventory')
    rooms_path = os.path.join(os.environ.get('USERPROFILE'), 'Documents', 'Mıne Of Crypto', world_folder, 'Rooms')
    psu_path = os.path.join(rooms_path, 'PSU')
    racks_path = os.path.join(rooms_path, 'Racks')
    
    if not os.path.exists(rooms_path):
        os.makedirs(rooms_path)
    if not os.path.exists(psu_path):
        os.makedirs(psu_path)
    if not os.path.exists(racks_path):
        os.makedirs(racks_path)
    
    def load_or_calculate_total_power():
        global total_power, electric_bill, moc_coins, room_temperature, using_power
        if os.path.exists(dat_file_path):
            with open(dat_file_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if line.startswith("Total Power:"):
                        total_power = int(line.split(":")[1].strip())
                    elif line.startswith("Electric Bill:"):
                        electric_bill = float(line.split(":")[1].strip())
                    elif line.startswith("MOC Coins:"):
                        moc_coins = float(line.split(":")[1].strip())
                    elif line.startswith("Room Temperature:"):
                        room_temperature = float(line.split(":")[1].strip())
                    elif line.startswith("Using Power:"):
                        using_power = int(line.split(":")[1].strip())
                else:
                    total_power = 0
                    for item in os.listdir(psu_path):
                        if item.endswith(".json"):
                            try:
                                with open(os.path.join(psu_path, item), 'r') as f:
                                    item_data = json.load(f)
                                total_power += item_data.get("Power", 0)
                            except Exception as e:
                                print(f"PSU gücünü yüklerken hata: {e}")
                    update_all_values_in_dat_file()
        else:
            print("Veri dosyası bulunamadı, toplam güç sıfırdan başlatılıyor.")
            total_power = 0
    
    load_or_calculate_total_power()
    
    scroll_frame = ctk.CTkScrollableFrame(main_frame, width=400, height=400)
    scroll_frame.pack(fill="both", expand=True)
    
    power_frame = ctk.CTkFrame(main_frame)
    power_frame.pack(fill="x", pady=5)
    total_power_label = ctk.CTkLabel(power_frame, text=f"Toplam Güç: {total_power} {power_types}")
    total_power_label.pack(side="left", padx=5)
    using_power_label = ctk.CTkLabel(power_frame, text=f"Kullanılan Güç: {using_power} W")
    using_power_label.pack(side="right", padx=5)
    
    electric_bill_label = ctk.CTkLabel(main_frame, text=f"Elektrik Faturası: ${electric_bill:.2f}")
    electric_bill_label.pack(pady=5)
    moc_coins_label = ctk.CTkLabel(main_frame, text=f"MOC Coins: {moc_coins:.3f}")
    moc_coins_label.pack(pady=5)
    temp_label = ctk.CTkLabel(main_frame, text=f"Oda Sıcaklığı: {room_temperature}°C")
    temp_label.pack(pady=5)
    
    # WindowS Activer
    active_windows['rooms'] = {
        'window': rooms_window,
        'total_power_label': total_power_label,
        'using_power_label': using_power_label,
        'electric_bill_label': electric_bill_label,
        'moc_coins_label': moc_coins_label,
        'temp_label': temp_label
    }
    
    mining_active = False
    mining_thread = None
    start_mining_button = tk.Button(main_frame, text="Mining Başlat", background="Green", fg="White", font=pixel_font)
    start_mining_button.pack(side="bottom", pady=5)
    stop_mining_button = tk.Button(main_frame, text="Miningi Durdur", background="Red", fg="White", font=pixel_font, state="disabled")
    
    def animate_gif(img_label, frames, delay=200, frame_num=0):
        if not img_label.winfo_exists() or not rooms_window.winfo_exists():
            return
        try:
            frame = frames[frame_num % len(frames)]
            img_label.configure(image=frame)
            if rooms_window.winfo_exists():
                rooms_window.after(delay, animate_gif, img_label, frames, delay, frame_num + 1)
        except tk.TclError:
            return
    
    def update_rooms_display():
        if not rooms_window.winfo_exists():
            return
        for widget in scroll_frame.winfo_children():
            widget.destroy()
        
        for item in os.listdir(rooms_path):
            if item.endswith(".json") and not item.startswith(("PSU_", "Rack_")):
                try:
                    with open(os.path.join(rooms_path, item), 'r') as f:
                        item_data = json.load(f)
                    item_name = item_data.get("name", "Bilinmeyen GPU")
                    damage = item_data.get("Damage", 0)
                    item_frame = ctk.CTkFrame(scroll_frame)
                    item_frame.pack(fill="x", pady=2)
                    
                    image_extensions = [".png", ".jpg", ".gif"]
                    image_file = None
                    for ext in image_extensions:
                        potential_image = os.path.join(rooms_path, item.replace(".json", ext))
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
                    
                    item_label = ctk.CTkLabel(item_frame, text=f"GPU: {item_name} (Hasar: {damage}%)")
                    item_label.pack(side="left", padx=5)
                    
                    def remove_gpu(selected_item=item):
                        global using_power
                        shutil.move(os.path.join(rooms_path, selected_item), os.path.join(inventory_path, selected_item))
                        for ext in image_extensions:
                            img_path = os.path.join(rooms_path, selected_item.replace(".json", ext))
                            if os.path.exists(img_path):
                                shutil.move(img_path, os.path.join(inventory_path, selected_item.replace(".json", ext)))
                        print(f"{item_name} envantere geri taşındı.")
                        update_rooms_display()
                        calculate_using_power()
                        update_power_labels()
                        if mining_active:
                            check_mining_status()
                        refresh_all_windows()  # Yenile
                    
                    tk.Button(item_frame, text="Kaldır", command=remove_gpu, background="Red", fg="White", font=pixel_font).pack(side="right", padx=5)
                except Exception as e:
                    print(f"GPU gösteriminde hata: {e}")
    
    def update_power_labels():
        if not rooms_window.winfo_exists():
            return
        total_power_label.configure(text=f"Toplam Güç: {total_power} {power_types}")
        using_power_label.configure(text=f"Kullanılan Güç: {using_power} W")
        electric_bill_label.configure(text=f"Elektrik Faturası: ${electric_bill:.2f}")
        moc_coins_label.configure(text=f"MOC Coins: {moc_coins:.3f}")
        temp_label.configure(text=f"Oda Sıcaklığı: {room_temperature}°C")
    
    def get_max_gpu_capacity():
        max_gpu_capacity = 0
        for item in os.listdir(racks_path):
            if item.endswith(".json"):
                try:
                    with open(os.path.join(racks_path, item), 'r') as f:
                        item_data = json.load(f)
                    max_gpu_capacity += item_data.get("Max Gpu", 0)
                except Exception as e:
                    print(f"Rack kapasite hesaplamada hata: {e}")
        return max_gpu_capacity
    
    def count_current_gpus():
        return len([f for f in os.listdir(rooms_path) if f.endswith(".json") and not f.startswith(("PSU_", "Rack_"))])
    
    def calculate_using_power():
        global using_power
        using_power = 0
        for item in os.listdir(rooms_path):
            if item.endswith(".json") and not item.startswith(("PSU_", "Rack_")):
                try:
                    with open(os.path.join(rooms_path, item), 'r') as f:
                        item_data = json.load(f)
                    using_power += item_data.get("Needed Power", 0)
                except Exception as e:
                    print(f"GPU gücünü hesaplarken hata: {e}")
        update_power_labels()
        refresh_all_windows()  # Yenile
    
    def check_mining_status():
        nonlocal mining_active
        if mining_active:
            if total_power < using_power:
                stop_mining()
                print("Toplam güç kullanılan güçten az, mining durduruldu.")
            elif electric_bill >= 200:
                stop_mining()
                print("Elektrik faturası $200 veya daha fazla, mining durduruldu. Lütfen faturayı ödeyin!")
    
    def mining_loop():
        global electric_bill, moc_coins, room_temperature, using_power
        while mining_active and rooms_window.winfo_exists():
            mining_interval = random.randint(5, 6)
            print(mining_interval)
            time.sleep(mining_interval)
            if mining_active:
                moc_coins += 0.001
                electric_bill += 0.50
                temp_increase = random.uniform(2, 4)
                room_temperature += temp_increase
                print(f"Mining: +0.001 MOC, Elektrik Faturası: ${electric_bill:.2f}, Oda Sıcaklığı: {room_temperature:.1f}°C")
                
                if room_temperature >= 10:
                    for item in os.listdir(rooms_path):
                        if item.endswith(".json") and not item.startswith(("PSU_", "Rack_")):
                            try:
                                item_path = os.path.join(rooms_path, item)
                                with open(item_path, 'r') as f:
                                    item_data = json.load(f)
                                damage = item_data.get("Damage", 0)
                                if damage < 100:
                                    item_data["Damage"] = min(100, damage + 1)
                                    with open(item_path, 'w') as f:
                                        json.dump(item_data, f)
                                    print(f"{item_data['name']} hasarı %1 arttı: {item_data['Damage']}%")
                                    if item_data["Damage"] >= 100:
                                        shutil.move(item_path, os.path.join(inventory_path, item))
                                        for ext in [".png", ".jpg", ".gif"]:
                                            img_path = os.path.join(rooms_path, item.replace(".json", ext))
                                            if os.path.exists(img_path):
                                                shutil.move(img_path, os.path.join(inventory_path, item.replace(".json", ext)))
                                        print(f"{item_data['name']} %100 hasar aldı ve envantere taşındı.")
                            except Exception as e:
                                print(f"GPU hasar güncellemesinde hata: {e}")
                    room_temperature = 2
                    update_rooms_display()
                
                update_power_labels()
                update_all_values_in_dat_file()
                check_mining_status()
        if not rooms_window.winfo_exists():
            stop_mining()
    
    def start_mining():
        nonlocal mining_active, mining_thread
        if not mining_active:
            gpu_count = count_current_gpus()
            if gpu_count == 0:
                print("Mining başlatılamaz, GPU bulunamadı.")
                return
            if electric_bill >= 200:
                print("Elektrik faturası $200 veya daha fazla, mining başlatılamaz. Lütfen faturayı ödeyin!")
                return
            mining_active = True
            print("Mining başladı.")
            calculate_using_power()
            if total_power < using_power:
                mining_active = False
                print("Toplam güç kullanılan güçten az, mining durduruldu.")
                stop_mining_button.config(state="disabled")
                stop_mining_button.pack_forget()
                update_power_labels()
            else:
                start_mining_button.config(state="disabled")
                stop_mining_button.config(state="normal")
                stop_mining_button.pack(side="bottom", pady=5)
                mining_thread = threading.Thread(target=mining_loop, daemon=True)
                mining_thread.start()
            refresh_all_windows()  # Yenile
    
    def stop_mining():
        nonlocal mining_active
        global using_power
        if mining_active:
            mining_active = False
            print("Mining durduruldu.")
            using_power = 0
            calculate_using_power()
            if rooms_window.winfo_exists():
                start_mining_button.config(state="normal")
                stop_mining_button.config(state="disabled")
                stop_mining_button.pack_forget()
            update_all_values_in_dat_file()
            refresh_all_windows()  # Yenile
    
    start_mining_button.config(command=start_mining)
    stop_mining_button.config(command=stop_mining)
    
    def add_gpu():
        if not rooms_window.winfo_exists():
            return
        inventory_items = [f for f in os.listdir(inventory_path) if f.endswith(".json")]
        if not inventory_items:
            print("Envanterde .json dosyası bulunamadı.")
            return
        
        gpu_window = ctk.CTkToplevel()
        gpu_window.title("GPU Ekle")
        gpu_window.geometry("300x300")
        
        scroll_frame_gpu = ctk.CTkScrollableFrame(gpu_window, width=260, height=260)
        scroll_frame_gpu.pack(padx=10, pady=10, fill="both", expand=True)
        
        gpu_found = False
        for item in inventory_items:
            try:
                with open(os.path.join(inventory_path, item), 'r') as f:
                    item_data = json.load(f)
                if item_data.get("Item Type", "Bilinmeyen Tür") == "GPU" and item_data.get("Damage", 0) < 100:
                    gpu_found = True
                    item_frame = ctk.CTkFrame(scroll_frame_gpu)
                    item_frame.pack(fill="x", pady=5)
                    
                    item_label = ctk.CTkLabel(item_frame, text=item_data.get("name", "Bilinmeyen GPU"))
                    item_label.pack(side="left", padx=5)
                    
                    def move_gpu(selected_item=item):
                        global using_power
                        max_capacity = get_max_gpu_capacity()
                        current_gpus = count_current_gpus()
                        if current_gpus >= max_capacity:
                            print("Rack kapasitesi dolu! Daha fazla GPU eklenemez.")
                            return
                        
                        shutil.move(os.path.join(inventory_path, selected_item), os.path.join(rooms_path, selected_item))
                        image_ext = [".png", ".jpg", ".gif"]
                        for ext in image_ext:
                            img_path = os.path.join(inventory_path, selected_item.replace(".json", ext))
                            if os.path.exists(img_path):
                                shutil.move(img_path, os.path.join(rooms_path, selected_item.replace(".json", ext)))
                        print(f"{item_data['name']} Rooms'a eklendi ve envanterden kaldırıldı.")
                        update_rooms_display()
                        calculate_using_power()
                        update_power_labels()
                        if mining_active:
                            check_mining_status()
                        item_frame.destroy()
                        refresh_all_windows()  
                    
                    tk.Button(item_frame, text="Ekle", command=move_gpu, background="Blue", fg="White", font=pixel_font).pack(side="right", padx=5)
            except Exception as e:
                print(f"GPU eklemede hata: {e}")
        
        if not gpu_found:
            ctk.CTkLabel(scroll_frame_gpu, text="GPU bulunamadı veya tüm GPU'lar hasarlı.").pack(pady=10)
    
    def psu_rooms():
        if not rooms_window.winfo_exists():
            return
        psu_window = ctk.CTkToplevel()
        psu_window.title("PSU Odaları")
        psu_window.geometry("400x400")
        
        add_frame = ctk.CTkFrame(psu_window)
        add_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(add_frame, text="Envanterdeki PSU'lar").pack(pady=2)
        scroll_frame_add = ctk.CTkScrollableFrame(add_frame, width=360, height=150)
        scroll_frame_add.pack(fill="both", expand=True)
        
        remove_frame = ctk.CTkFrame(psu_window)
        remove_frame.pack(fill="both", expand=True, padx=10, pady=5)
        ctk.CTkLabel(remove_frame, text="Eklenmiş PSU'lar").pack(pady=2)
        scroll_frame_psu = ctk.CTkScrollableFrame(remove_frame, width=360, height=150)
        scroll_frame_psu.pack(fill="both", expand=True)
        
        inventory_items = [f for f in os.listdir(inventory_path) if f.endswith(".json")]
        psu_found = False
        for item in inventory_items:
            try:
                with open(os.path.join(inventory_path, item), 'r') as f:
                    item_data = json.load(f)
                if item_data.get("Item Type", "Bilinmeyen Tür") == "PSU":
                    psu_found = True
                    item_frame = ctk.CTkFrame(scroll_frame_add)
                    item_frame.pack(fill="x", pady=5)
                    
                    item_label = ctk.CTkLabel(item_frame, text=item_data.get("name", "Bilinmeyen PSU"))
                    item_label.pack(side="left", padx=5)
                    
                    def move_psu(selected_item=item):
                        global total_power, using_power
                        shutil.move(os.path.join(inventory_path, selected_item), os.path.join(psu_path, selected_item))
                        image_ext = [".png", ".jpg", ".gif"]
                        for ext in image_ext:
                            img_path = os.path.join(inventory_path, selected_item.replace(".json", ext))
                            if os.path.exists(img_path):
                                shutil.move(img_path, os.path.join(psu_path, selected_item.replace(".json", ext)))
                        power_added = item_data.get("Power", 0)
                        total_power = max(0, total_power + power_added)
                        print(f"{item_data['name']} PSU Odalarına eklendi ve envanterden kaldırıldı.")
                        update_psu_display(scroll_frame_psu)
                        update_power_labels()
                        update_all_values_in_dat_file()
                        if mining_active:
                            check_mining_status()
                        item_frame.destroy()
                        refresh_all_windows()  
                    
                    tk.Button(item_frame, text="Ekle", command=move_psu, background="Blue", fg="White", font=pixel_font).pack(side="right", padx=5)
            except Exception as e:
                print(f"PSU eklemede hata: {e}")
        
        def update_psu_display(frame):
            for widget in frame.winfo_children():
                widget.destroy()
            for item in os.listdir(psu_path):
                if item.endswith(".json"):
                    try:
                        with open(os.path.join(psu_path, item), 'r') as f:
                            item_data = json.load(f)
                        item_name = item_data.get("name", "Bilinmeyen PSU")
                        item_frame = ctk.CTkFrame(frame)
                        item_frame.pack(fill="x", pady=2)
                        
                        item_label = ctk.CTkLabel(item_frame, text=f"PSU: {item_name}")
                        item_label.pack(side="left", padx=5)
                        
                        def remove_psu(selected_item=item):
                            global total_power, using_power
                            shutil.move(os.path.join(psu_path, selected_item), os.path.join(inventory_path, selected_item))
                            image_ext = [".png", ".jpg", ".gif"]
                            for ext in image_ext:
                                img_path = os.path.join(psu_path, selected_item.replace(".json", ext))
                                if os.path.exists(img_path):
                                    shutil.move(img_path, os.path.join(inventory_path, selected_item.replace(".json", ext)))
                            power_removed = item_data.get("Power", 0)
                            total_power = max(0, total_power - power_removed)
                            print(f"{item_name} envantere geri taşındı.")
                            update_psu_display(frame)
                            update_power_labels()
                            update_all_values_in_dat_file()
                            if mining_active:
                                check_mining_status()
                            refresh_all_windows()  # Yenile
                        
                        tk.Button(item_frame, text="Kaldır", command=remove_psu, background="Red", fg="White", font=pixel_font).pack(side="right", padx=5)
                    except Exception as e:
                        print(f"PSU gösteriminde hata: {e}")
        
        update_psu_display(scroll_frame_psu)
        if not psu_found and not os.listdir(psu_path):
            ctk.CTkLabel(scroll_frame_add, text="Envanterde PSU bulunamadı.").pack(pady=10)
            ctk.CTkLabel(scroll_frame_psu, text="Eklenmiş PSU yok.").pack(pady=10)
    
    def racks_rooms():
        if not rooms_window.winfo_exists():
            return
        racks_window = ctk.CTkToplevel()
        racks_window.title("Rack Odaları")
        racks_window.geometry("400x400")
        
        add_frame = ctk.CTkFrame(racks_window)
        add_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(add_frame, text="Envanterdeki Rack'ler").pack(pady=2)
        scroll_frame_add = ctk.CTkScrollableFrame(add_frame, width=360, height=150)
        scroll_frame_add.pack(fill="both", expand=True)
        
        remove_frame = ctk.CTkFrame(racks_window)
        remove_frame.pack(fill="both", expand=True, padx=10, pady=5)
        ctk.CTkLabel(remove_frame, text="Eklenmiş Rack'ler").pack(pady=2)
        scroll_frame_racks = ctk.CTkScrollableFrame(remove_frame, width=360, height=150)
        scroll_frame_racks.pack(fill="both", expand=True)
        
        inventory_items = [f for f in os.listdir(inventory_path) if f.endswith(".json")]
        rack_found = False
        for item in inventory_items:
            try:
                with open(os.path.join(inventory_path, item), 'r') as f:
                    item_data = json.load(f)
                if item_data.get("Item Type", "Bilinmeyen Tür") == "Racks":
                    rack_found = True
                    item_frame = ctk.CTkFrame(scroll_frame_add)
                    item_frame.pack(fill="x", pady=5)
                    
                    item_label = ctk.CTkLabel(item_frame, text=item_data.get("name", "Bilinmeyen Rack"))
                    item_label.pack(side="left", padx=5)
                    
                    def move_rack(selected_item=item):
                        global using_power
                        shutil.move(os.path.join(inventory_path, selected_item), os.path.join(racks_path, selected_item))
                        image_ext = [".png", ".jpg", ".gif"]
                        for ext in image_ext:
                            img_path = os.path.join(inventory_path, selected_item.replace(".json", ext))
                            if os.path.exists(img_path):
                                shutil.move(img_path, os.path.join(racks_path, selected_item.replace(".json", ext)))
                        print(f"{item_data['name']} Rack Odalarına eklendi ve envanterden kaldırıldı.")
                        update_racks_display(scroll_frame_racks)
                        update_rooms_display()
                        item_frame.destroy()
                        refresh_all_windows()  # Yenile
                    
                    tk.Button(item_frame, text="Ekle", command=move_rack, background="Blue", fg="White", font=pixel_font).pack(side="right", padx=5)
            except Exception as e:
                print(f"Rack eklemede hata: {e}")
        
        def update_racks_display(frame):
            for widget in frame.winfo_children():
                widget.destroy()
            for item in os.listdir(racks_path):
                if item.endswith(".json"):
                    try:
                        with open(os.path.join(racks_path, item), 'r') as f:
                            item_data = json.load(f)
                        item_name = item_data.get("name", "Bilinmeyen Rack")
                        item_frame = ctk.CTkFrame(frame)
                        item_frame.pack(fill="x", pady=2)
                        
                        item_label = ctk.CTkLabel(item_frame, text=f"Rack: {item_name}")
                        item_label.pack(side="left", padx=5)
                        
                        def remove_rack(selected_item=item):
                            global using_power
                            gpu_items = [f for f in os.listdir(rooms_path) if f.endswith(".json") and not f.startswith(("PSU_", "Rack_"))]
                            image_ext = [".png", ".jpg", ".gif"]
                            for gpu in gpu_items:
                                shutil.move(os.path.join(rooms_path, gpu), os.path.join(inventory_path, gpu))
                                for ext in image_ext:
                                    img_path = os.path.join(rooms_path, gpu.replace(".json", ext))
                                    if os.path.exists(img_path):
                                        shutil.move(img_path, os.path.join(inventory_path, gpu.replace(".json", ext)))
                            print(f"Tüm GPU'lar envantere geri taşındı çünkü {item_name} kaldırıldı.")
                            
                            shutil.move(os.path.join(racks_path, selected_item), os.path.join(inventory_path, selected_item))
                            for ext in image_ext:
                                img_path = os.path.join(racks_path, selected_item.replace(".json", ext))
                                if os.path.exists(img_path):
                                    shutil.move(img_path, os.path.join(inventory_path, selected_item.replace(".json", ext)))
                            print(f"{item_name} envantere geri taşındı.")
                            update_racks_display(frame)
                            update_rooms_display()
                            calculate_using_power()
                            update_power_labels()
                            if mining_active:
                                check_mining_status()
                            refresh_all_windows()  # Yenile
                        
                        tk.Button(item_frame, text="Kaldır", command=remove_rack, background="Red", fg="White", font=pixel_font).pack(side="right", padx=5)
                    except Exception as e:
                        print(f"Rack gösteriminde hata: {e}")
        
        update_racks_display(scroll_frame_racks)
        if not rack_found and not os.listdir(racks_path):
            ctk.CTkLabel(scroll_frame_add, text="Envanterde Rack bulunamadı.").pack(pady=10)
            ctk.CTkLabel(scroll_frame_racks, text="Eklenmiş Rack yok.").pack(pady=10)
    
    tk.Button(taskbar, text="GPU Ekle", command=add_gpu, background="Blue", fg="Red", font=pixel_font).pack(side="top", pady=10, anchor="center")
    tk.Button(taskbar, text="PSU Odaları", command=psu_rooms, background="Blue", fg="Green", font=pixel_font).pack(side="top", pady=10, anchor="center")
    tk.Button(taskbar, text="Rack Odaları", command=racks_rooms, background="Blue", fg="Yellow", font=pixel_font).pack(side="top", pady=10, anchor="center")
    tk.Button(taskbar, text="Coolers", command=None, background="Blue", fg="Cyan", font=pixel_font).pack(side="top", pady=10, anchor="center")
    
    update_rooms_display()
    update_power_labels()

# Envanter açma
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
        if not img_label.winfo_exists() or not inventory_window.winfo_exists():
            return
        frame = frames[frame_num % len(frames)]
        img_label.configure(image=frame)
        if inventory_window.winfo_exists():
            inventory_window.after(delay, animate_gif, img_label, frames, delay, frame_num + 1)

    for item in inventory_items:
        if item.endswith(".json"):
            item_frame = ctk.CTkFrame(scroll_frame)
            item_frame.pack(fill="x", padx=5, pady=5)

            with open(os.path.join(inventory_path, item), 'r') as f:
                item_data = json.load(f)
            item_name = item_data.get("name", "Bilinmeyen Ürün")
            damage = item_data.get("Damage", 0)

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

            item_label = ctk.CTkLabel(item_frame, text=f"{item_name} (Hasar: {damage}%)")
            item_label.pack(side="left", padx=5)

# Dolarları .dat dosyasında güncelle
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
    refresh_all_windows()  # Yenile

# Ödeme sistemi
def Payment_system():
    global Dollars, gas_bill, electric_bill, dat_file_path, Dollars_labels

    payments_win = tk.Toplevel()
    payments_win.title("Ödemeler")
    payments_win.geometry("200x300")
    user_home = os.path.expanduser("~")
    icon_path = os.path.join(user_home, "Documents", "Mıne Of Crypto", "Mods", "Mine-Of-Crypto-Pool-An-Pools", "ICON", "MıneOfCryptoicon1.ico")
    payments_win.iconbitmap(icon_path)

    pixel_font = ctk.CTkFont(family="Press Start 2P", size=15)
    Dollars_label_local = ctk.CTkLabel(payments_win, text=f"Dolar: {Dollars}", text_color="Green", font=pixel_font)
    Dollars_label_local.pack(pady=10)
    Dollars_labels.append(Dollars_label_local)
    
    gas_bill_label = ctk.CTkLabel(payments_win, text=f"Gaz Faturası: ${gas_bill}", text_color="Green", font=pixel_font)
    gas_bill_label.pack(pady=10)
    
    electric_bill_label = ctk.CTkLabel(payments_win, text=f"Elektrik Faturası: ${electric_bill}", text_color="Green", font=pixel_font)
    electric_bill_label.pack(pady=10)

    active_windows['payments'] = {
        'window': payments_win,
        'Dollars_label': Dollars_label_local,
        'gas_bill_label': gas_bill_label,
        'electric_bill_label': electric_bill_label
    }

    def payment_system_for_pp():
        global Dollars, gas_bill, electric_bill
        if not os.path.exists(dat_file_path):
            print("Veri dosyası bulunamadı!")
            return

        with open(dat_file_path, 'r') as file:
            lines = file.readlines()

        for line in lines:
            if line.startswith("Dollars:"):
                Dollars = float(line.split(":")[1].strip())
            elif line.startswith("Gas Bill:"):
                gas_bill = float(line.split(":")[1].strip())
            elif line.startswith("Electric Bill:"):
                electric_bill = float(line.split(":")[1].strip())

        total_bills = gas_bill + electric_bill
        if Dollars >= total_bills:
            Dollars -= total_bills
            gas_bill = 0
            electric_bill = 0
            print("Faturalar ödendi!")
            gas_bill_label.configure(text=f"Gaz Faturası: ${gas_bill}")
            electric_bill_label.configure(text=f"Elektrik Faturası: ${electric_bill}")
            update_all_values_in_dat_file()
            refresh_all_windows()  
        else:
            print("Yetersiz bakiye! Faturaları ödemek için yeterli paranız yok.")

    pay_button = tk.Button(payments_win, text="Faturaları Öde", command=payment_system_for_pp)
    pay_button.pack(pady=20)

    payments_win.mainloop()

# Ürün satın alma
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
        
        item["Damage"] = 0
        item_details = json.dumps(item)
        with open(item_file, 'w') as f:
            f.write(item_details)
        
        shop_paths = os.path.join(user_profile, 'Documents', 'Mıne Of Crypto', 'Mods', 'CryptoMınıng gane')
        image_path = os.path.join(shop_paths, item.get("image", ""))
        if os.path.exists(image_path):
            image_dest = os.path.join(inventory_path, f"{item_name}_{timestamp}{os.path.splitext(image_path)[1]}")
            shutil.copy(image_path, image_dest)
        
        print(f"{item_name} başarıyla alındı ve envantere eklendi.")
        refresh_all_windows() 
    else:
        print("Yetersiz bakiye! Ürün satın alınamadı.")

# Shop sys
def Shop_system():
    global Dollars, Dollars_labels
    user_profile = os.environ.get('USERPROFILE')
    shop_paths = os.path.join(user_profile, 'Documents', 'Mıne Of Crypto', 'Mods', 'CryptoMınıng gane')
    json_path = os.path.join(shop_paths, 'ıtems.json')
    pixel_font = ctk.CTkFont(family="Press Start 2P", size=15)
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(shop_music)  
    pygame.mixer.music.play(-1)
    #Funcitons
    def on_close():
        pygame.mixer.music.stop()  
        shop_window.destroy()  
        time.sleep(1)
        pygame.mixer.music.load(main_music_path)  
        pygame.mixer.music.play(-1)

    if not os.path.exists(dat_file_path):
        print("Veri dosyası bulunamadı!")
        return

    with open(dat_file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("Dollars:"):
                Dollars = float(line.split(":")[1].strip())

    if not os.path.exists(json_path):
        print("Mağaza JSON dosyası bulunamadı.")
        return

    with open(json_path, "r", encoding="utf-8") as files:
        data = json.load(files)
    shop_items = data.get("items", [])
    shop_window = ctk.CTkToplevel()
    shop_window.title("Mağaza")
    shop_window.geometry("600x600")
    shop_window.attributes("-topmost", True)

    taskbar = ctk.CTkFrame(shop_window, height=30, corner_radius=0, fg_color="gray")
    taskbar.pack(fill="x", side="top")
    
    Dollars_label = ctk.CTkLabel(taskbar, text=f"Dollars: {Dollars}", text_color="Green", font=pixel_font)
    Dollars_label.pack(side="left")
    Dollars_labels.append(Dollars_label)

    active_windows['shop'] = {
        'window': shop_window,
        'Dollars_label': Dollars_label
    }

    scroll_frame = ctk.CTkScrollableFrame(shop_window, width=330, height=400)
    scroll_frame.pack(padx=10, pady=5, fill="both", expand=True)

    def animate_gif(img_label, frames, delay=200, frame_num=0):
        if not img_label.winfo_exists() or not shop_window.winfo_exists():
            return
        frame = frames[frame_num % len(frames)]
        img_label.configure(image=frame)
        if shop_window.winfo_exists():
            shop_window.after(delay, animate_gif, img_label, frames, delay, frame_num + 1)

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
        shop_window.protocol("WM_DELETE_WINDOW", on_close)
# Show ıtem detaıls
def select_item(item_details):
    details_window = ctk.CTkToplevel()
    details_window.title(f"{item_details['name']} Detayları")
    
    detail_font = ctk.CTkFont(family="Arial", size=12)
    for key, value in item_details.items():
        label_text = f"{key}: {value}"
        detail_label = ctk.CTkLabel(details_window, text=label_text, font=detail_font)
        detail_label.pack(pady=5)



#Game Checker
def start_game_check_files_sys():
    global world_folder, dat_file_path, Dollars, gas_bill, electric_bill, Level, Dollars_labels, moc_coins, room_temperature, using_power
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
        global world_folder, dat_file_path, Dollars, gas_bill, electric_bill, Level, Dollars_labels, moc_coins, room_temperature, using_power,main_music_path
        selected_world = world_var.get()
        main_music_path = os.path.join(sounds_path, 'GameSoundALone.mp3')
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
                    elif line.startswith("Xp:"):
                        xp = float(line.split(":")[1].strip())
                    elif line.startswith("Dollars:"):
                        Dollars = float(line.split(":")[1].strip())
                    elif line.startswith("Gas Bill:"):
                        gas_bill = float(line.split(":")[1].strip())
                    elif line.startswith("Electric Bill:"):
                        electric_bill = float(line.split(":")[1].strip())
                    elif line.startswith("Total Power:"):
                        total_power = int(line.split(":")[1].strip())
                    elif line.startswith("MOC Coins:"):
                        moc_coins = float(line.split(":")[1].strip())
                    elif line.startswith("Room Temperature:"):
                        room_temperature = float(line.split(":")[1].strip())
                    elif line.startswith("Using Power:"):
                        using_power = int(line.split(":")[1].strip())
                    elif line.startswith("Musics:"):
                        global musics_stats
                        musics_stats = line.split(":")[1].strip() == "True"
        
            # Load settings
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.load(main_music_path)
            load_settings_from_file()  # Ayarları yükle
            pygame.mixer.music.play(-1)

            game_window = ctk.CTkToplevel()
            game_window.title(f"{selected_world} - Oyun")
            game_window.geometry("500x300")
            #Funcitons
            def on_close():
                pygame.mixer.music.stop()  # Müzik durdur
                game_window.destroy()  # Pencereyi kapat

            game_window.protocol("WM_DELETE_WINDOW", on_close)

            #fRAME
            taskbar = ctk.CTkFrame(game_window, height=30, corner_radius=0, fg_color="gray")
            taskbar.pack(fill="x", side="top")
            vertical_bar = ctk.CTkFrame(game_window, height=30, width=90, corner_radius=0, fg_color="grey")
            vertical_bar.pack(fill="y", side="right")
            under_panel = ctk.CTkFrame(game_window, height=30, corner_radius=0, fg_color="gray")
            under_panel.pack(fill="x", side="bottom")
            #bUTTON
            inventory_button = tk.Button(vertical_bar, text="Envanter", command=open_inventory, background="Blue", fg="Red", font=pixel_font)
            inventory_button.pack(side="top", padx=10, pady=10)
            Shop_Button = tk.Button(vertical_bar, text="Mağaza", command=Shop_system, background="Blue", fg="green", font=pixel_font)
            Shop_Button.pack(side="top", padx=5, pady=10)
            payment_bill_button = tk.Button(vertical_bar, text="Ödemeler", command=Payment_system, background="Red", font=pixel_font)
            payment_bill_button.pack(side="top", padx=5, pady=10)
            rooms_button = tk.Button(vertical_bar, text="Rooms", command=Rooms_system, background="Purple", fg="Black", font=pixel_font)
            rooms_button.pack(side="top", padx=5, pady=10)
            settings_button = tk.Button(vertical_bar, text="Ayarlar", command=Settings_system, background="Gray", fg="White", font=pixel_font)
            settings_button.pack(side="top", padx=5, pady=10)

            #lABEL
            level_label = ctk.CTkLabel(taskbar, text=f"Seviye: {Level}", text_color="white")
            level_label.pack(side="left", padx=10)
            xp_label = ctk.CTkLabel(vertical_bar, text=f"Xp:{xp}", text_color="Green")
            xp_label.pack()
            Dollars_label = ctk.CTkLabel(taskbar, text=f"Dollars: {Dollars}", text_color="Green")
            Dollars_label.pack(side="left", padx=11)
            Dollars_labels.append(Dollars_label)
            gas_bill_label = ctk.CTkLabel(taskbar, text=f"Gaz Faturası: ${gas_bill}", text_color="Green")
            gas_bill_label.pack(side="right", padx=5)
            electric_bill_label = ctk.CTkLabel(taskbar, text=f"Elektrik Faturası: ${electric_bill}", text_color="Green")
            electric_bill_label.pack(side="right", padx=5)
            
            active_windows['game'] = {
                'window': game_window,
                'Dollars_label': Dollars_label,
                'gas_bill_label': gas_bill_label,
                'electric_bill_label': electric_bill_label
            }
            
            world_selection_win.destroy()
            refresh_all_windows()  # Yenile
    
    world_var = tk.StringVar(value=worlds[0])
    label = ctk.CTkLabel(world_selection_win, text="Bir dünya seçin:")
    label.pack(pady=10)

    for world in worlds:
        rb = ctk.CTkRadioButton(world_selection_win, text=world, variable=world_var, value=world)
        rb.pack(anchor="w")
    
    start_button = ctk.CTkButton(world_selection_win, text="Başlat", command=start_selected_game)
    start_button.pack(pady=10)



def gameselecter_core_loader():
    global loader_screen_win
    loader_screen_win = tk.Toplevel()
    loader_screen_win.title("MoonDevelopGame")
    loader_screen_win.geometry("300x300")
    loader_screen_win.attributes("-toolwindow",True)
    loader_screen_win.resizable(False, False)
    loader_screen_win.overrideredirect(False) 
    #path
    screen_png_path = os.path.join(user_profile,'Documents', 'Mıne Of Crypto', 'Mods',"ICON")
    screen_png = os.path.join(screen_png_path, "MoonDevelopGame.png")
    #Load Sys
    image = Image.open(screen_png)
    image = image.resize((300, 300), Image.LANCZOS)
    logo = ImageTk.PhotoImage(image)

    label = tk.Label(loader_screen_win, image=logo)
    label.place(x=0, y=0, relwidth=1, relheight=1) 

    #updater
    loader_screen_win.update_idletasks()
    screen_width = loader_screen_win.winfo_screenwidth()
    screen_height  = loader_screen_win.winfo_screenheight()
    x = (screen_width - 800) // 2
    y = (screen_height - 600) // 2
    loader_screen_win.geometry(f"300x300+{x}+{y}")
    loader_screen_win.after(2000, lambda:[loader_screen_win.destroy(),start_game_check_files_sys()])


    loader_screen_win.mainloop()





#Main
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
        global new_game_win
        new_game_win = ctk.CTkToplevel()
        new_game_win.title("Bilgiler")
        new_game_win.geometry("200x200")

        def get_game_name_entry_folder():
            global using_power
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
                    f.write(f"Xp:{xp}\n")
                    f.write(f"Dollars: {Dollars}\n")
                    f.write(f"Gas Bill: {gas_bill}\n")
                    f.write(f"Electric Bill: {electric_bill}\n")
                    f.write(f"Total Power:{total_power}\n")
                    f.write(f"PoweTypes:{power_types}\n")
                    f.write(f"MOC Coins:{moc_coins}\n")
                    f.write(f"Room Temperature:{room_temperature}\n")
                    f.write(f"Using Power:{using_power}\n")
                    f.write(f"Musics:{musics_stats}\n")
                print(f"{file_name} dosyası oluşturuldu ve '{game_folder}' içine kaydedildi.")
                
                inventory_folder = os.path.join(game_folder, 'Inventory')
                if not os.path.exists(inventory_folder):
                    os.makedirs(inventory_folder)
                    print(f"'Envanter' klasörü '{game_folder}' içinde oluşturuldu.")
                
                rooms_folder = os.path.join(game_folder, 'Rooms')
                if not os.path.exists(rooms_folder):
                    os.makedirs(rooms_folder)
                    print(f"'Rooms' klasörü '{game_folder}' içinde oluşturuldu.")
                
                # Varsayılan ayarları kaydet
                settings_file_path = os.path.join(game_folder, "settings.dat")
                with open(settings_file_path, 'w') as f:
                    f.write("Music: True\n")
                    f.write("Volume: 0.5\n")
                print(f"Varsayılan ayarlar '{settings_file_path}' dosyasına kaydedildi.")
                
                new_game_win.destroy()
            refresh_all_windows()  

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
    start_game_button = tk.Button(main, text="Oyunu Başlat", command=gameselecter_core_loader, background="orange", fg="Blue", font=pixel_font)
    start_game_button.pack(anchor="s", pady=10)

    MoonDevelop_label = ctk.CTkLabel(main, text="MoonDevelop", text_color="Blue", font=pixel_font)
    MoonDevelop_label.pack(side="bottom", anchor="w", pady=10)

    main.mainloop()

if __name__ == "__main__":
    main_loader()