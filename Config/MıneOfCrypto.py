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
power_types = "w"
Level = 0
Dollars = 900
electric_bill = 0
gas_bill = 0
total_power = 0
world_folder = ""
dat_file_path = ""
Dollars_labels = []  








def Rooms_system():
    global world_folder, total_power, power_types, Dollars_labels, dat_file_path
    
    rooms_window = ctk.CTkToplevel()
    rooms_window.title("Odalar")
    rooms_window.geometry("500x400")
    
    # Ana çerçeve
    main_frame = ctk.CTkFrame(rooms_window)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Sağdaki dikey görev çubuğu
    taskbar = ctk.CTkFrame(rooms_window, width=120, corner_radius=0, fg_color="gray")
    taskbar.pack(side="right", fill="y", padx=5, pady=5)
    pixel_font = ctk.CTkFont(family="Press Start 2P", size=12)
    
    # Yol tanımlamaları
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
    
    # Başlangıçta toplam gücü yükle veya hesapla
    def load_or_calculate_total_power():
        global total_power
        if os.path.exists(dat_file_path):
            with open(dat_file_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if line.startswith("Total Power:"):
                        total_power = int(line.split(":")[1].strip())
                        break
                else:
                    # .dat dosyasında Total Power yoksa PSU'lardan hesapla
                    total_power = 0
                    for item in os.listdir(psu_path):
                        if item.endswith(".json"):
                            try:
                                with open(os.path.join(psu_path, item), 'r') as f:
                                    item_data = json.load(f)
                                total_power += item_data.get("Power", 0)
                            except Exception as e:
                                print(f"PSU gücünü yüklerken hata: {e}")
                    update_total_power_in_dat_file(total_power)
        else:
            print("Veri dosyası bulunamadı, toplam güç sıfırdan başlatılıyor.")
            total_power = 0
    
    def update_total_power_in_dat_file(power_value):
        if not os.path.exists(dat_file_path):
            print("Veri dosyası bulunamadı!")
            return
        with open(dat_file_path, 'r') as file:
            lines = file.readlines()
        with open(dat_file_path, 'w') as file:
            found = False
            for line in lines:
                if line.startswith("Total Power:"):
                    file.write(f"Total Power: {power_value}\n")
                    found = True
                else:
                    file.write(line)
            if not found:
                file.write(f"Total Power: {power_value}\n")
    
    # İlk açılışta toplam gücü yükle
    load_or_calculate_total_power()
    
    # Odalardaki öğeleri gösterme alanı
    scroll_frame = ctk.CTkScrollableFrame(main_frame, width=300, height=300)
    scroll_frame.pack(fill="both", expand=True)
    
    # Güç etiketleri
    power_frame = ctk.CTkFrame(main_frame)
    power_frame.pack(fill="x", pady=5)
    total_power_label = ctk.CTkLabel(power_frame, text=f"Toplam Güç: {total_power} {power_types}")
    total_power_label.pack(side="left", padx=5)
    using_power = 0
    using_power_label = ctk.CTkLabel(power_frame, text=f"Kullanılan Güç: {using_power} W")
    using_power_label.pack(side="right", padx=5)
    
    mining_active = False
    start_mining_button = tk.Button(main_frame, text="Mining Başlat", background="Green", fg="White", font=pixel_font)
    start_mining_button.pack(side="bottom", pady=5)
    stop_mining_button = tk.Button(main_frame, text="Miningi Durdur", background="Red", fg="White", font=pixel_font, state="disabled")
    
    def animate_gif(img_label, frames, delay=200, frame_num=0):
        if not img_label.winfo_exists() or not rooms_window.winfo_exists():
            return
        try:
            frame = frames[frame_num % len(frames)]
            img_label.configure(image=frame)
            rooms_window.after(delay, animate_gif, img_label, frames, delay, frame_num + 1)
        except tk.TclError:
            return
    
    def update_rooms_display():
        for widget in scroll_frame.winfo_children():
            widget.destroy()
        
        for item in os.listdir(rooms_path):
            if item.endswith(".json") and not item.startswith(("PSU_", "Rack_")):
                try:
                    with open(os.path.join(rooms_path, item), 'r') as f:
                        item_data = json.load(f)
                    item_name = item_data.get("name", "Bilinmeyen GPU")
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
                    
                    item_label = ctk.CTkLabel(item_frame, text=f"GPU: {item_name}")
                    item_label.pack(side="left", padx=5)
                    
                    def remove_gpu(selected_item=item):
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
                    
                    tk.Button(item_frame, text="Kaldır", command=remove_gpu, background="Red", fg="White", font=pixel_font).pack(side="right", padx=5)
                except Exception as e:
                    print(f"GPU gösteriminde hata: {e}")
    
    def update_power_labels():
        total_power_label.configure(text=f"Toplam Güç: {total_power} {power_types}")
        using_power_label.configure(text=f"Kullanılan Güç: {using_power} W")
    
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
        nonlocal using_power
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
    
    def check_mining_status():
        nonlocal mining_active
        if mining_active and total_power < using_power:
            stop_mining()
            print("Toplam güç kullanılan güçten az, mining durduruldu.")
    
    def start_mining():
        nonlocal mining_active
        if not mining_active:
            gpu_count = count_current_gpus()
            if gpu_count == 0:
                print("Mining başlatılamaz, GPU bulunamadı.")
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
    
    def stop_mining():
        nonlocal mining_active, using_power
        if mining_active:
            mining_active = False
            print("Mining durduruldu.")
            using_power = 0
            calculate_using_power()
            start_mining_button.config(state="normal")
            stop_mining_button.config(state="disabled")
            stop_mining_button.pack_forget()
    
    start_mining_button.config(command=start_mining)
    stop_mining_button.config(command=stop_mining)
    
    def add_gpu():
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
                if item_data.get("Item Type", "Bilinmeyen Tür") == "GPU":
                    gpu_found = True
                    item_frame = ctk.CTkFrame(scroll_frame_gpu)
                    item_frame.pack(fill="x", pady=5)
                    
                    item_label = ctk.CTkLabel(item_frame, text=item_data.get("name", "Bilinmeyen GPU"))
                    item_label.pack(side="left", padx=5)
                    
                    def move_gpu(selected_item=item):
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
                    
                    tk.Button(item_frame, text="Ekle", command=move_gpu, background="Blue", fg="White", font=pixel_font).pack(side="right", padx=5)
            except Exception as e:
                print(f"GPU eklemede hata: {e}")
        
        if not gpu_found:
            ctk.CTkLabel(scroll_frame_gpu, text="GPU bulunamadı.").pack(pady=10)
    
    def psu_rooms():
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
                        global total_power
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
                        update_total_power_in_dat_file(total_power)  # Kalıcı kaydet
                        if mining_active:
                            check_mining_status()
                        item_frame.destroy()
                    
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
                            global total_power
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
                            update_total_power_in_dat_file(total_power)  # Kalıcı kaydet
                            if mining_active:
                                check_mining_status()
                        
                        tk.Button(item_frame, text="Kaldır", command=remove_psu, background="Red", fg="White", font=pixel_font).pack(side="right", padx=5)
                    except Exception as e:
                        print(f"PSU gösteriminde hata: {e}")
        
        update_psu_display(scroll_frame_psu)
        if not psu_found and not os.listdir(psu_path):
            ctk.CTkLabel(scroll_frame_add, text="Envanterde PSU bulunamadı.").pack(pady=10)
            ctk.CTkLabel(scroll_frame_psu, text="Eklenmiş PSU yok.").pack(pady=10)
    
    def racks_rooms():
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
                        
                        tk.Button(item_frame, text="Kaldır", command=remove_rack, background="Red", fg="White", font=pixel_font).pack(side="right", padx=5)
                    except Exception as e:
                        print(f"Rack gösteriminde hata: {e}")
        
        update_racks_display(scroll_frame_racks)
        if not rack_found and not os.listdir(racks_path):
            ctk.CTkLabel(scroll_frame_add, text="Envanterde Rack bulunamadı.").pack(pady=10)
            ctk.CTkLabel(scroll_frame_racks, text="Eklenmiş Rack yok.").pack(pady=10)
    
    # Görev çubuğu butonları
    tk.Button(taskbar, text="GPU Ekle", command=add_gpu, background="Blue", fg="Red", font=pixel_font).pack(side="top", pady=10, anchor="center")
    tk.Button(taskbar, text="PSU Odaları", command=psu_rooms, background="Blue", fg="Green", font=pixel_font).pack(side="top", pady=10, anchor="center")
    tk.Button(taskbar, text="Rack Odaları", command=racks_rooms, background="Blue", fg="Yellow", font=pixel_font).pack(side="top", pady=10, anchor="center")
    
    update_rooms_display()
    update_power_labels()




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
    shop_window.geometry("400x600")

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
                    elif line.startswith("Total Power:"):
                        total_power = int(line.split(":")[1].strip())

            game_window = ctk.CTkToplevel()
            game_window.title(f"{selected_world} - Oyun")
            game_window.geometry("400x300")
            
            taskbar = ctk.CTkFrame(game_window, height=30, corner_radius=0, fg_color="gray")
            taskbar.pack(fill="x", side="top")
            vertical_bar = ctk.CTkFrame(game_window, height=30, width=90, corner_radius=0, fg_color="grey")
            vertical_bar.pack(fill="y", side="right")
            under_panel=ctk.CTkFrame(game_window, height=30, corner_radius=0, fg_color="gray")
            under_panel.pack(fill="x",side="bottom")

            inventory_button = tk.Button(vertical_bar, text="Envanter", command=open_inventory, background="Blue", fg="Red", font=pixel_font)
            inventory_button.pack(side="top", padx=10, pady=10)
            Shop_Button = tk.Button(vertical_bar, text="Mağaza", command=Shop_system, background="Blue", fg="green", font=pixel_font)
            Shop_Button.pack(side="top", padx=5, pady=20)
            payment_bill_button = tk.Button(vertical_bar, text="Ödemeler", command=Payment_system, background="Red")
            payment_bill_button.pack(side="top", padx=5, pady=20)
            rooms_button = tk.Button(vertical_bar,text="Rooms",command=Rooms_system,background="Purple",fg="Black")
            rooms_button.pack(side="top",padx=5,pady=20)

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
                    f.write(f"Total Power:{total_power}\n")
                    f.write(f"PoweTypes:{power_types}")
                print(f"{file_name} dosyası oluşturuldu ve '{game_folder}' içine kaydedildi.")
                
                # Create Inventory folder
                inventory_folder = os.path.join(game_folder, 'Inventory')
                if not os.path.exists(inventory_folder):
                    os.makedirs(inventory_folder)
                    print(f"'Envanter' klasörü '{game_folder}' içinde oluşturuldu.")
                
                # Create Rooms folder
                rooms_folder = os.path.join(game_folder, 'Rooms')
                if not os.path.exists(rooms_folder):
                    os.makedirs(rooms_folder)
                    print(f"'Rooms' klasörü '{game_folder}' içinde oluşturuldu.")
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