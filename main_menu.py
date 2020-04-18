import tkinter as tk
# import pygame
# pygame.init()
# pygame.mixer.quit()
# from network import Network

# ToDo:
#   - add the description of the game (which fields are 
#     rquiered and the type of data) --> on the left side of
#     Frames
#   - add the list of existing games

# dictionary object which will be passed further down
# to the client for creating the Game object
game_init_data = \
      {"n"       : None,
       "m"       : None,
       "max_len" : None,
       "player"  : None,
       "game"    : None,
       "ip"      : None,
       "port"    : None,
       "new"     : None}

def set_new_game(master,e_list,err_msg):
    # here check if entered data is correct
    # if it is store the data and exit
    global good

    e1,e2,e3,e4,e5,eIP,ePort = e_list
    e1_text = e1.get()
    e2_text = e2.get()
    e3_text = e3.get()
    e4_text = e4.get()
    e5_text = e5.get()
    serverIP = eIP.get()
    serverPort = ePort.get()

    # checks if the grid width is integer and
    # has the value in range [10,30)
    try:
        game_init_data["n"] = int(e1_text)
        if (game_init_data["n"] <= 30) and (game_init_data["n"]>=10):
            n_check = True
        else:
            n_check = False
    except:
        n_check = False
   
    # checks if the grid height is integer and
    # has value in range [10,20)
    try:    
        game_init_data["m"] = int(e2_text)
        if (game_init_data["m"] <= 20) and (game_init_data["m"]>=10):
            m_check = True
        else:
            m_check = False
    except:
        m_check = False

    # checks if the array length is integer and
    # has value in range [4,8]
    try:
        game_init_data["max_len"] = int(e3_text)
        if (game_init_data["max_len"]<=8) and (game_init_data["max_len"]>=4):
            max_len_check = True
        else:
            max_len_check = False
    except:
        max_len_check = False

    # checks if the player name is at least one charater
    if (len(e4_text)>0) and (len(e4_text)<=10):
        game_init_data["player"] = e4_text
        player_name_check = True
    else:
        player_name_check = False

    # checks if the game name is at least one character
    if (len(e5_text)>0) and (len(e5_text)<=10):
        game_init_data["game"] = e5_text
        game_name_check = True
    else:
        game_name_check = False

    # checks if the port is integer
    try:
        game_init_data["port"] = int(serverPort)
        port_check = True
    except:
        port_check = False

    if (len(serverIP)>=7):
        game_init_data["ip"] = serverIP
        server_check = True
    else:
        server_check = False

    # if all input data is good --> exit the tkinter window
    if n_check and m_check and max_len_check \
        and player_name_check and game_name_check \
        and port_check and server_check:
        game_init_data["new"] = True
        good = True
        master.destroy()
        master.quit()
    else:
      err_msg.set("Game data initialization error")

def join_game(master, e_list,err_msg):
    global good
    e_pname, e_gname,eIP,ePort = e_list
    
    # checks if the game name is at least one character
    game_name = e_gname.get()
    if (len(game_name)>0) and (len(game_name)<=10):
      game_init_data["game"] = game_name
      game_name_check = True
    else:
      game_name_check = False
        
    # checks if the player name is longer than 1 character
    pname = e_pname.get()
    if (len(pname)>0) and (len(pname)<=10):
        game_init_data["player"] = pname
        player_name_check = True
    else:
        player_name_check = False

    # check server address length
    serverIP = eIP.get()
    if (len(serverIP)>=7):
        game_init_data["ip"] = serverIP
        server_check = True
    else:
        server_check = False

    # checks if the port is integer
    serverPort = ePort.get()
    try:
        game_init_data["port"] = int(serverPort)
        port_check = True
    except:
        port_check = False

    if game_name_check and player_name_check and server_check and port_check:
        game_init_data["new"] = False
        good = True
        master.destroy()
        master.quit()
    else:
      err_msg.set("Game data initialization error")

def MainMenu(msg):
    global game_init_data
    global good
    game_init_data = \
      {"n"       : None,
       "m"       : None,
       "max_len" : None,
       "player"  : None,
       "game"    : None,
       "ip"      : None,
       "port"    : None,
       "new"     : None}

    master = tk.Tk()
    good = False

    padx,pady,gap = 20,20,10
    obj_height = 25
    obj_width  = 110
    
    #===--- server data input fields ---===#
    connection_frame = tk.Frame(master, borderwidth=2, relief=tk.GROOVE)
    connection_frame_height = pady*3+gap*3+obj_height*2
    connection_frame.place(x=padx, y=pady,
                           width=3*obj_width,
                           height=connection_frame_height)

    l = tk.Label(connection_frame, text="Server IP*", font=(8), anchor="w")
    l.place(x=padx,
            y=pady,
            width=obj_width,
            height=obj_height)
    l = tk.Label(connection_frame, text="Server port*", font=(8), anchor="w")
    l.place(x=padx,
            y=pady+gap+obj_height,
            width=obj_width,
            height=obj_height)

    eIP = tk.Entry(connection_frame)
    eIP.insert(30, "192.168.178.24")
    eIP.place(x=padx+obj_width+gap,
              y=pady,
              width=obj_width,
              height=obj_height)

    ePort = tk.Entry(connection_frame)
    ePort.insert(5, "5555")
    ePort.place(x=padx+obj_width+gap,
                y=pady+gap+obj_height,
                width=obj_width,
                height=obj_height)

    err_msg = tk.StringVar()
    err_msg.set(msg)
    errl = tk.Label(connection_frame, textvariable=err_msg, font=(8), fg="red")
    errl.place(x=padx,
            y=pady+gap*2+obj_height*2,
            width=3*obj_width - 2*gap - 2*padx,
            height=obj_height)

    bottom_border = connection_frame_height
    #===--- end connection data frame ---===#


    #===--- data input fileds ---===#
    data_frame = tk.Frame(master, borderwidth=2, relief=tk.GROOVE)
    data_frame_height = obj_height*6 + pady*2 + gap*5
    data_frame.place(x=padx,
                     y=bottom_border + pady + gap,
                     width=3*obj_width,
                     height=data_frame_height)
    # field labels
    l1 = tk.Label(data_frame, text="Grid width", font=(8), anchor="w")
    l1.place(x=padx,
             y=pady,
             width=obj_width,
             height=obj_height)
    l2 = tk.Label(data_frame, text="Grid height", font=(8), anchor="w")
    l2.place(x=padx, 
             y=pady+gap+obj_height,
             width=obj_width,
             height=obj_height)
    l3 = tk.Label(data_frame, text="Max length", font=(8), anchor="w")
    l3.place(x=padx,
             y=pady+gap*2+obj_height*2, 
             width=obj_width, 
             height=obj_height)
    l4 = tk.Label(data_frame, text="Player name*", font=(8), anchor="w")
    l4.place(x=padx,
             y=pady+gap*3+obj_height*3, 
             width=obj_width, 
             height=obj_height)
    l5 = tk.Label(data_frame, text="Game name*", font=(8), anchor="w")
    l5.place(x=padx,
             y=pady+gap*4+obj_height*4, 
             width=obj_width, 
             height=obj_height)

    # text entries
    text_box_width = 75
    e1 = tk.Entry(data_frame)
    e1.insert(tk.END, "15")
    e1.place(x=padx+gap+obj_width,
             y=pady,
             width=text_box_width,
             height=obj_height)
    e2 = tk.Entry(data_frame)
    e2.insert(tk.END, "10")
    e2.place(x=padx+gap+obj_width,
             y=pady+gap+obj_height,
             width=text_box_width,
             height=obj_height)
    e3 = tk.Entry(data_frame)
    e3.insert(tk.END, "4")
    e3.place(x=padx+gap+obj_width,
             y=pady+gap*2+obj_height*2,
             width=text_box_width,
             height=obj_height)
    e4 = tk.Entry(data_frame)
    e4.place(x=padx+gap+obj_width,
             y=pady+gap*3+obj_height*3,
             width=text_box_width,
             height=obj_height)
    e5 = tk.Entry(data_frame)
    e5.place(x=padx+gap+obj_width,
             y=pady+gap*4+obj_height*4,
             width=text_box_width,
             height=obj_height)
    e_list = [e1,e2,e3,e4,e5,eIP,ePort]

    # max value labels
    l11 = tk.Label(data_frame, text="[10,30] int", anchor="w")
    l11.place(x=padx+gap+obj_width+text_box_width,
              y=pady,
              width=text_box_width,
              height=obj_height)
    l12 = tk.Label(data_frame, text="[10,20] int", anchor="w")
    l12.place(x=padx+gap+obj_width+text_box_width,
              y=pady+gap+obj_height,
              width=text_box_width,
              height=obj_height)
    l13 = tk.Label(data_frame, text="[4,8] int", anchor="w")
    l13.place(x=padx+gap+obj_width+text_box_width,
              y=pady+gap*2+obj_height*2,
              width=text_box_width,
              height=obj_height)
    l14 = tk.Label(data_frame, text="[1,10] char", anchor="w")
    l14.place(x=padx+gap+obj_width+text_box_width,
              y=pady+gap*3+obj_height*3,
              width=text_box_width,
              height=obj_height)
    l15 = tk.Label(data_frame, text="[1,10] char", anchor="w")
    l15.place(x=padx+gap+obj_width+text_box_width,
              y=pady+gap*4+obj_height*4,
              width=text_box_width,
              height=obj_height)

    btn = tk.Button(data_frame, 
                   text="Start the new game",
                   command=lambda: set_new_game(master,e_list,err_msg),
                   font=(8))
    btn.place(x=padx,
              y=pady+gap*5+obj_height*5,
              width=3*obj_width - 2*gap - 2*padx,
              height=obj_height)
    bottom_border += data_frame_height + pady + gap
    #===--- end data init frame ---===#

    #===--- join game frame ---===#
    join_frame = tk.Frame(master, borderwidth=2, relief=tk.GROOVE)
    join_frame_height = pady*3+gap + obj_height*3
    join_frame.place(x=padx,
                     y=bottom_border + gap,
                     width=3*obj_width,
                     height=join_frame_height)

    l = tk.Label(join_frame, text="Player name*", font=(8), anchor="w")
    l.place(x=padx,
            y=pady, 
            width=obj_width, 
            height=obj_height)

    l = tk.Label(join_frame, text="Game name*", font=(8), anchor="w")
    l.place(x=padx,
            y=pady+gap+obj_height, 
            width=obj_width, 
            height=obj_height)

    e_pname = tk.Entry(join_frame)
    e_pname.place(x=padx+gap+obj_width,
                 y=pady,
                 width=text_box_width,
                 height=obj_height)

    e_gname = tk.Entry(join_frame)
    e_gname.place(x=padx+gap+obj_width,
                 y=pady+gap+obj_height,
                 width=text_box_width,
                 height=obj_height)

    l = tk.Label(join_frame, text="[1,10] char", anchor="w")
    l.place(x=padx+gap+obj_width+text_box_width,
            y=pady,
            width=text_box_width,
            height=obj_height)

    l = tk.Label(join_frame, text="[1,10] char", anchor="w")
    l.place(x=padx+gap+obj_width+text_box_width,
            y=pady+gap+obj_height,
            width=text_box_width,
            height=obj_height)

    btn = tk.Button(join_frame, 
                   text="Join the game",
                   command=lambda: join_game(master,[e_pname,e_gname,eIP,ePort],err_msg),
                   font=(8))
    btn.place(x=padx,
              y=pady*2+gap+obj_height*2,
              width=3*obj_width - 2*gap - 2*padx,
              height=obj_height)
    bottom_border += join_frame_height + pady + gap
    #===--- end join game frame ---===#

    #===--- game description frame ---===#
    game_description = tk.Frame(master, borderwidth=2, relief=tk.GROOVE)
    game_description.place(x=3*obj_width + padx + gap, 
                           y=pady,
                           width=obj_width*3,
                           height=bottom_border-pady-gap*2)

    header = "XOX game"
    game_label  = "Rules of the game are the same \n" 
    game_label += "as in classical 3x3 board except\n"
    game_label += "here the maximum array of same \n"
    game_label += "symbols can be larger than 3 and\n"
    game_label += "user can set it's value in range [4,8]. \n\n"
    game_label += "Players can choose the grid size (nxm)\n"
    game_label += "and if they would like to create\n"
    game_label += "the new game or join the existing one.\n\n"
    game_label += "In case of violation of initial data\n"
    game_label += "or in case there is no game requested\n"
    game_label += "by given name or the game is full\n"
    game_label += "you will be returned to this window and\n"
    game_label += "could set new game data values.\n\n"
    game_label += "Have fun! :)"
    footer = "Requierd fields are marked\nwith asterix symbol (*)"

    l = tk.Label(game_description, text=header, font=(8), fg="red")
    l.place(x=padx, y=pady,
            width=obj_width*3 - padx*2,
            height=obj_height)

    l = tk.Label(game_description, text=game_label, anchor="n")
    l.place(x=padx, y=pady + obj_height + gap*2,
            width=obj_width*3 - padx*2, 
            height=bottom_border-pady*3-gap*2 - 3*obj_height )

    l = tk.Label(game_description, text=footer, fg="red")
    l.place(x=padx, y=bottom_border-pady*3-gap*2 - 2*obj_height,
            width=obj_width*3 - padx*2,
            height=obj_height*2)

    frame_width = obj_width*3
    #===--- end game description frame ---===#

    master.title("XOX - main menu")
    master_width = obj_width*3 + 2*padx + frame_width
    master_height = bottom_border
    master.geometry( str(master_width) + "x" + str(master_height))
    master.resizable(0,0) # block window resizing

    master.mainloop()

    return good

if __name__ == "__main__":
    MainMenu("Error message")
    print("Exiting the main menu!")