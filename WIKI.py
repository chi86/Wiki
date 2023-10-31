#!/home/chi/pyvenv/bin/python
 
##   __        _____ _  _____    ##
##   \ \      / /_ _| |/ /_ _|   ##
##    \ \ /\ / / | || ' / | |    ##
##     \ V  V /  | || . \ | |    ##
##      \_/\_/  |___|_|\_\___|   ##
##                            

__title__   = 'WIKI'
__version__ = '0.1'
__author__  = 'christoph irrenfried'
__license__ = 'none'
__release__ = True

# prepare environment
import time,os,copy
import textwrap
import subprocess
import pyperclip

### Set environment variables
if os.environ['WIKI'] != "":
   prefix=os.environ['WIKI']
else:
   prefix=""
PDFviewer="evince "
Editor="emacs "

### repr(
### entry=next(filter(lambda obj: obj.get('doi'), self.BibContent), None)


#======== Fancy terminal print ==================

color=["black","red","green","blue","pink","yellow","peru"]

class Texti:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

#================================================

            
#===== Main routine definition ==================
def main():
   Logo()
   
   database,msg=ReadDatabase(prefix)
   # print(msg)

   if(__release__):
      cli(database,msg,prefix)
   else:
      arguments={"database":database,
                 "prefix":prefix,
                 "searchString":""
                 }

      CLI_ListProgs(arguments)

   

#===== LitEntry class ==================
class WikiEntry:
   """
   class for holding all relevent information of a literature entry
   """
   def __init__(self,file,prg,description,content):
      self.file=file

      self.prg=prg
      self.description=description
      self.content=content

      self.searchString=[self.prg,self.description,self.content]


#===== cli ==================
def cli(database,msg,prefix):
   # command line interface

   arguments={"database":database,
              "prefix":prefix,
              "msg":msg,
              "searchString":"",
              "export":[]
              }

   menuItems = [
      { "E(x)it": CLI_Exit },
      { "List Progs": CLI_ListProgs },
      { "Search": CLI_Search }
   ]
   	
   while True:
      os.system('clear')

      Logo()
      
      print(arguments["msg"])
                                            
      
      for item in menuItems:
         print("[" + str(menuItems.index(item)) + "] "+ list(item.keys())[0])

      choice = input("# or search >> ")
      try:
         if len(choice) > 1:
            arguments["searchString"]=choice
            choice=2
         if choice == 'x': choice=0
         if int(choice) < 0 : raise ValueError
         list(menuItems[int(choice)].values())[0](arguments)
         arguments["searchString"]=""
      except (ValueError, IndexError):
         pass


#===== Utility functions for cli ==================
def Logo():
   """
   Routine for plotting the logo
   """
   
   print(Texti.GREEN+"  __        _____ _  _____ "+Texti.END)
   print(Texti.GREEN+"  \ \      / /_ _| |/ /_ _|"+Texti.END)
   print(Texti.GREEN+"   \ \ /\ / / | || ' / | | "+Texti.END)
   print(Texti.GREEN+"    \ V  V /  | || . \ | | "+Texti.END)
   print(Texti.GREEN+"     \_/\_/  |___|_|\_\___|"+Texti.END)
   print(Texti.GREEN+"                           "+Texti.END)

   print("       "+Texti.GREEN+"WIKI"+Texti.END)
   print("          "+Texti.GREEN+"chi86"+Texti.END)
   print()

#===== literature database functions ==================
def CLI_ReloadDatabase(arguments):
   """
   Reload databese
   """
   prefix=arguments["prefix"]
   database,msg=ReadDatabase(prefix)
   arguments["database"]=database
   arguments["msg"]=msg
   

#===== general literature database stuff ==================
def OutputFormat(idx,val):
   """
   helper: fancy output of literature entry
   """
   print(Texti.BLUE+val.prg+Texti.END)
   print(Texti.RED+val.description+Texti.END)

   # # truncent lines
   # entry=""
   # for line in val.content:
   #    entry+=line
      
   # entry=(str(idx)+' : '+entry)
   # entry=textwrap.wrap(entry, 72)
      
   # print(entry[0])
   # for i in entry[1:]:
   #    print('\t'+i)

   for line in val.content:
      dat=line.replace("\n","")

      if dat[0:2] == "##":
         print(Texti.GREEN+dat+Texti.END)
      elif dat[0:2] == "#c": # copy to clipboard
         print(Texti.YELLOW+dat+Texti.END)
         cc=dat.strip("#c")
         pyperclip.copy(cc)
      else:
         print(dat)

         
def CLI_ListProgs(arguments):
   """
   CLI entry **ListAuthors**
   """
   database=arguments["database"]
   prefix  =arguments["prefix"]
   
   datapoint0={}
   for idx,dat in enumerate(database):
      entry=dat.prg
      if(entry==None): continue
      if(not entry in datapoint0):
         datapoint0[entry]=[dat]
      else:
         datapoint0[entry].append(dat)

   #print(datapoint)

   datapoint={}
   for key, value in sorted(datapoint0.items()):
      datapoint[key]=value

   # for key,value in datapoint.items():
   #    print("{:3} : {}".format(key,value))

   for idx,dat in enumerate(datapoint):
      print("{:3} : {}".format(idx,dat))

   print('number / X')
   choice = input(">> ")


   if int(choice) >= 0:
      #print(datapoint.values()[int(choice)])
      for idx,val in enumerate(list(datapoint.values())[int(choice)]):
         OutputFormat(idx,val)
      
      choiceDat = input(">> ")
        

 
def CLI_Search(arguments):
   """
   CLI entry **Search**
   """
   database=arguments["database"]
   prefix  =arguments["prefix"]
   
   datapoint=[]

   if(arguments["searchString"] != ""):
      keyw=arguments["searchString"]
   else:
      keyw=input("keyword : ")
      
   idx=0
   for id,dat in enumerate(database):
      for dat_keyw in dat.searchString:
         if keyw in dat_keyw:
            datapoint.append(dat)
            # OutputFormat(idx,dat)

            print(idx,
                  " : ",
                  Texti.BLUE+dat.prg+Texti.END,
                  " ",
                  Texti.RED+dat.description+Texti.END)
               
            idx+=1
            break

   print('select (number)')
   choiceDat = input(">> ")


   if( int(choiceDat) >= 0 ):
      OutputFormat(int(choiceDat),datapoint[int(choiceDat)])
      choiceDat = input(">> ")
   

def CLI_Exit(arguments):
   """
   CLI entry **Exit**
   """
   exit()


#===== Database related functions ==================
def ReadDatabase(prefix):
   """
   Read database given by prefix

   example file "ffmpeg/chopTime.txt"

   ```
   # ffmpeg
   # chop time

   ffmpeg -ss 00:00:00.0 -i INPUT.mkv -c copy -t 00:13:17.0 OUTPUT.mk

   ## ss start
   ## t duration
   ```

   1. line: program or language
   2. line: description

   3-end line: code and explanation (must start with "##")

   """
   msg=""
   database=[]

   # loop directories
   out, err = subprocess.Popen(['ls '+prefix], stdout=subprocess.PIPE,shell=True).communicate()
   dirs = out.splitlines()

   for dir in dirs:
      dir=dir.decode()
      if(not "." in dir):
         # print(repr(dir))

         # loop files
         out, err = subprocess.Popen(['ls '+prefix+dir], stdout=subprocess.PIPE,shell=True).communicate()
         files = out.splitlines()
         for file in files:
            file=file.decode()
            if(not "~" in file):
               
               # print("\t",file)
   
               path=dir+"/"+file
               file_h=open(prefix+path,"r")

               prg=file_h.readline().strip("\n")[2:]
               description=file_h.readline().strip("\n")[2:]
   
               content=[]
               
               for line in file_h:
                  content.append(line)

               point=WikiEntry(path,prg,description,content)
               database.append(point)
      
   return database,msg
         



#===== execute MAIN ==================
if __name__ == '__main__':
   #===== Main routine execute =============
   #start = time.time()
   main()
   #end = time.time()
   #print('\n\nTime:',end - start,'sec')
   #========================================
