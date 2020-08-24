import window
import tkinter

with open('adress.txt', 'r') as ip_file:
    ip = ip_file.readlines()

w = window.Win(ip[0][0:-1], ip[1])

