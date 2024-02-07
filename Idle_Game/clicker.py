#Imports
from replit import clear
from time import sleep as wait
import math

#Config
coins = 0
workers = 1
resets = 0
mega_resets = 0


worker_cost = 100
reset_cost = 1000000
mega_reset_cost = 4

shown_buy = False
first_buy = True

show_reset = False
first_reset = False

show_mega_reset = False
first_mega_reset = False

#Game code
while True:
  clear()
  print("You Have")
  print("Coins: {}".format(coins))
  if shown_buy:
    print("Workers: {}".format(workers))
  if show_reset:
    print("Resets: {}".format(resets))
  if show_mega_reset:
    print("Mega Resets: {}".format(mega_resets))

  if coins == 0:
    print("Type '/h' for help\nTo earn coins type 'c'")
  
  if coins >= worker_cost and shown_buy == False:
    clear()
    print("You now have {} coins!\nYou can now buy more workers to increase your productivity.\nTo open your buy menu run the command '/b'".format(coins))
    print("Closing in 5 seconds")
    wait(5)
    input("[ENTER]")
    shown_buy = True
    clear()
  
  if coins >= reset_cost and show_reset == False:
    clear()
    print("You now have {} coins!\nYou can now Reset\nThis will double your output, but will take away EVERYTHING!\nTo reset type '/r'".format(coins))
    print("Closing in 5 seconds")
    wait(5)
    input("[ENTER]")
    show_reset = True
    clear()
  
  if resets >= mega_reset_cost and show_mega_reset == False:
    clear()
    print("You have {} resets!\nYou can now MEGA RESET\nThis will double the amount of resets you get\nBut takes away all things under it\nTo mega reset type /mr".format(resets))
    print("Closing in 5 seconds")
    wait(5)
    input("[ENTER]")
    show_mega_reset = True
    clear()
  

  run_arg = input("? ")
  if run_arg == "/h":
    clear()
    print("Help menu is under development")
    input("Press [ENTER] to continue")
  elif run_arg == "/b" and shown_buy:
    ref = ""
    while True:
      clear()
      print("Welcome to the SHOP.\nPlease type in the id of the product you'd like to purchase!")
      if ref == "close":
        break
      print("[id: 1] Worker ({} coins)".format(worker_cost))
      if first_buy:
        print("Type '/e' to exit menu.")
        first_buy = False
      id = input("id: ")
      if id == "/e":
        break
      elif id == "1" and coins >= worker_cost:
        while True:
          clear()
          print("How many Workers would you like to purchase?")
          number = input("# ")
          if number == "max":
            number = math.floor(coins//worker_cost)
          else:
            try:
              number = int(number)
            except:
              print("That isn't a number!")
              input("Press [ENTER] to try again.")

          if number*worker_cost <= coins:
            coins -= number*worker_cost
            workers += number
            ref = "close"
            break
          else:
            print("Not enought coins.")
            input("Press [ENTER] to continue.")
            ref = ""
            break
  elif run_arg == "/r" and show_reset:
    clear()
    if coins < reset_cost:
      print("You are much to weak to reset!\nCome back when you are wealthy!")
      input("[ENTER] to continue.")
    elif coins >= reset_cost:
      print("You meet the requirments to reset.\nAre you sure\n(YOU WILL LOSE EVERYTHING)")
      sure = input("y/n ")
      if sure == "y":
        print("Wonderful!\nI you will now recieve {} coins per worker!".format(resets+1))
        coins = 0
        workers = 1
        resets += 1
        reset_cost *= 2
      else:
        clear()
        print("I understand.")
  elif run_arg == "/mr" and show_mega_reset:
    clear()
    if resets < mega_resets:
      print("You are not wealthy enough to gain a mega reset!\nYou need {} resets to mega reset!".format(mega_reset_cost))
    else:
      pass
  elif run_arg == "qbm" and shown_buy:
    number = math.floor(coins//worker_cost)
    coins -= number*worker_cost
    workers += number
  elif run_arg == "c":
    coins += workers*(resets+1)
  else:
    coins += workers*(resets+1)