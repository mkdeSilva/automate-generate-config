import os
from pathlib import Path
class Config:
  newPath = str(Path(os.getcwd()).parents[2]) + "/"
  addresses = []
  asNumbers = []
  prefixNumbers = []
  maxNumbers = []
  data = []
  success = False

  def __init__(self, type, filePath):
    self.type = type
    self.filePath = filePath
    print "Data to be read", filePath

  def get_data(self):
    with open(self.filePath, 'r') as file:
      for line in file:
        cleanedLine = line.strip()
        if cleanedLine:
          self.data.append(cleanedLine)

  def create_lists(self):
    if self.type == 4:
      for item in self.data:
        self.addresses.append(item.split()[0])
        self.asNumbers.append(item.split()[2])
        self.prefixNumbers.append(item.split()[-1])
    else:
      i = 0
      for item in self.data:
        newItem = item.split()[-1]
        if (i%2 == 0):
          self.addresses.append(newItem)
        else:
          self.asNumbers.append(item.split()[1])
          self.prefixNumbers.append(newItem)
        i += 1

  def getMaxPrefixNumbers(self, number):
    maxPrefix = 0
    if number >= 0 and number <= 900:
      maxPrefix = 1000
    elif number >= 901 and number <= 4500:
      maxPrefix = 5000
    elif number >= 4501 and number <= 9000:
      maxPrefix = 10000
    elif number >= 9001 and number <= 22500:
      maxPrefix = 25000
    elif number >= 22501 and number <= 45000:
      maxPrefix = 50000
    elif number >= 45000 and number <= 67500:
      maxPrefix = 75000
    elif number >= 67501 and number <= 90000:
      maxPrefix = 100000
    elif number >= 90001 and number <= 180000:
      maxPrefix = 200000
    elif number >= 180001 and number <= 270000:
      maxPrefix = 300000
    elif number >= 270001 and number <= 360000:
      maxPrefix = 400000
    elif number >= 360001 and number <= 450000:
      maxPrefix = 500000
    elif number >= 450001 and number <= 540000:
      maxPrefix = 600000
    elif number >= 540001 and number <= 630000:
      maxPrefix = 700000
    elif number >= 630001 and number <= 720000:
      maxPrefix = 800000
    self.maxNumbers.append(maxPrefix)

 
  def delete_files(self): # pass in locations of text files
    if self.type == 4:
      try:
        os.remove(self.newPath + "/files/4-idle-active.txt") # CHANGE THIS LATER
      except OSError:
        pass
      try:
        os.remove(self.newPath + "files/4-config.txt") # CHANGE THIS LATER
      except OSError:
        pass
    elif self.type == 6:
      try:
        os.remove(self.newPath + "files/6-idle-active.txt") # CHANGE THIS LATER
      except OSError:
        pass
      try:
        os.remove(self.newPath + "files/6-config.txt") # CHANGE THIS LATER
      except OSError:
        pass

  def get_prefixes(self):
    i = 0
    for index, eachNumber in enumerate(self.prefixNumbers):
      try:
        receivedPrefix = int(eachNumber)
      except ValueError:
        if self.type == 4:
          with open(self.newPath + "files/4-idle-active.txt", "a") as activeOrIdleFile:
            activeOrIdleFile.write("{} : {} : {}".format(eachNumber, self.asNumbers[i], self.addresses[i]))
            activeOrIdleFile.write("\n")
            successIdle = True
          receivedPrefix = 1  
        else:
          with open(self.newPath + "files/6-idle-active.txt", "a") as activeOrIdleFile:
            activeOrIdleFile.write("{} : {} : {}".format(eachNumber, self.asNumbers[i], self.addresses[i]))
            activeOrIdleFile.write("\n")
            successIdle = True
          receivedPrefix = 1  

      i += 1
      self.getMaxPrefixNumbers(receivedPrefix)

  def write_config(self):
    if self.type == 4:
      with open(self.newPath + "files/4-config.txt", 'w') as potato:
        potato.write("router bgp 4651\n")
      for index, address in enumerate(self.addresses):
        with open(self.newPath + "files/4-config.txt", "a") as potato:
          #potato.write("router bgp 4651\n")
          potato.write(" neighbor {}\n".format(address))
          potato.write("  address-family ipv4 unicast\n")
          potato.write("   maximum-prefix {} 90 restart 30\n".format(self.maxNumbers[index]))
          potato.write("\n")
          successConfig = True
      self.success = True
    else:
      with open(self.newPath + "files/6-config.txt", 'w') as potato:
        potato.write("router bgp 4651\n")
      for index, address in enumerate(self.addresses):
      #print address
        with open(self.newPath + "files/6-config.txt", "a") as potato:
          #potato.write("router bgp 4651\n")
          potato.write(" neighbor {}\n".format(address))
          potato.write("  address-family ipv6 unicast\n")
          potato.write("   maximum-prefix {} 90 restart 30\n".format(self.maxNumbers[index]))
          potato.write("\n")
          successConfig = True
      self.success = True

  # def clean_data(self):
  #   addresses = []
  #   asNumbers = []
  #   prefixNumbers = []
  #   maxNumbers = []
  #   data = ""

  def make_dir(self):
    try: 
        os.makedirs(self.newPath + "/files/")
    except OSError:
        if not os.path.isdir(self.newPath + "/files"):
            raise

  def get_path(self):
    return self.newPath

  def generate_config(self):
    self.get_data()
    self.create_lists()
    self.make_dir()
    self.delete_files()
    self.get_prefixes()
    self.write_config()
    







