import os
import sys
sys.path.insert(1,os.path.join(sys.path[0],'../../../'))
from imports import *



# загружайте изображения в светлом и темном режимах изображения
image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(65, 40))
large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
chat_image_1 = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "2.png")),dark_image=Image.open(os.path.join(image_path, "2.png")), size=(20, 20))
chat_image_2 = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "1.png")),dark_image=Image.open(os.path.join(image_path, "1.png")), size=(20, 20))
chat_image_3 = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "3.png")),dark_image=Image.open(os.path.join(image_path, "3.png")), size=(20, 20))
chat_image_4 = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "4.png")),dark_image=Image.open(os.path.join(image_path, "4.png")), size=(20, 20))
chat_image_5 = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "5.png")),dark_image=Image.open(os.path.join(image_path, "5.png")), size=(20, 20))
chat_image_6 = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "6.png")),dark_image=Image.open(os.path.join(image_path, "6.png")), size=(20, 20))
chat_image_7 = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "7.png")),dark_image=Image.open(os.path.join(image_path, "7.png")), size=(20, 20))
add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))
