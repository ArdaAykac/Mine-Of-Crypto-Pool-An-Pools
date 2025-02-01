import customtkinter as ctk
import tkinter as tk
import time
import random
import os


#path


#Animations
#buttons
#label
colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF"]
color_index = 0



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
            game_name = game_name_entry.get().strip()  # Kullanıcıdan oyun ismini al
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
                # Dosyayı oluştur
                with open(file_path, 'w') as f:
                    f.write(f"Game name: {game_name}\n")
                print(f"{file_name} dosyası oluşturuldu ve 'Cache' klasörüne kaydedildi.")
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
    #entry
    #label
    MoonDevelop_label = ctk.CTkLabel(main,text="MoonDevelop",text_color="Blue",font=pixel_font)
    MoonDevelop_label.pack(side="bottom", anchor="w",pady=10)
    #mainloop
    main.mainloop()


main()
