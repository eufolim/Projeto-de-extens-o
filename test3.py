import keyboard 

def key(value):
    if value.name == "up":
        print("Y+")
    elif value.name == "down":
        print("Y-")
    keyboard.unhook_all()
    global wait
    wait = False



wait = True
keyboard.on_press_key("up",key,True)
keyboard.on_press_key("down",key,True)
while wait == True:
    pass