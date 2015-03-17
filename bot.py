import ch

#!/usr/bin/python
# vim: set fileencoding=utf-8 :

class Bot(ch.RoomManager):
	def onConnect(self,room):
		if( Handle.__rQueHs__ >= 1 ):
			return
		else:
			try: print("[" + Settings.colour("yellow","conn".upper()) + "] Connection established with " + Settings.colour("blue", room.name.upper()) )
			except Exception as e:
				print(str(e))
				Handle.__errors__ += 1
				pass
			Handle.__joined__ += 1

	def onDisconnect(self,room):
		if( Handle.__rQueHs__ >= 1 ):
			return
		else:
			try: print("[" + Settings.colour("red","conn".upper()) + "] Connection terminated with " + Settings.colour("blue", room.name.upper()) )
			except Exception as e:
				print(str(e))
				Handle.__errors__ += 1
				pass
			Handle.__joined__ -= 1

	def onInit(self):
		if Settings.__chatcolour__ == True:
			self.setNameColor( Data.__colours__[int( Data.__col_dict__["name"] - 1 )] )
			self.setFontColor( Data.__colours__[int( Data.__col_dict__["msg"] - 1 )] )
			self.setFontFace( Data.__colours__[int( Data.__col_dict__["face"] - 1 )] )
			self.setFontSize( int(Data.__colours__[int( Data.__col_dict__["size"] - 1 )]) )
			self.enableBg()

	def onFloodWarning(self, room):
		Handle.__overflow__.append(str(room.name))
		Handle.relay(2)
		Handle.level(3)
		self.reconnect(room.name)

	def onPMMessage(self, pm, user, body):
		if Settings.__PMs__ == True:
			data = body
			pm.message( user , Handle.parsePM( data = data ))
		else:
			pm.message( ch.User("duubz") , "Message [FORWARDED] - From %s - %s" % ( user.name , body )  )

		print("[" + Settings.colour("red","user".upper()) + "] (" +
			Settings.colour("blue","PMs") +
			") " + Settings.colour("white",user.name.upper()) + " (" + Settings.colour("yellow", Group.title(user.name.lower()).upper() ) + "): " + Settings.colour("green",body))

	def parseCmd(self, room, data, user):
		import time
		cmd  = data[0][0]
		args = data[0][1]

		if cmd == "anc":
			if Group.ID( user ) == 4:
				for group in Settings.groups:
					self.getRoom(group).message( "Message from {0} at {1}:\r {2}".format(user.title(), time.strftime("%H:%M:%S"), args ) )
			else:
				room.message("No, bad.")

		if cmd == "pm":
			__user__ = args.split()[0].lower()
			__mssg__ = " ".join(args.split()[1:])
			self.pm.message( ch.User( __user__ ) , "Message from {0} at {1}: {2}".format(user.title(), time.strftime("%H:%M:%S"), __mssg__) )

		if cmd == "rm":
			__room__ = args.split()[0].lower()
			__mssg__ = " ".join( args.split()[1:] )
			self.getRoom(__room__).message("Message from {0} at {1} ({2}): {3}".format( user.title(), time.strftime("%H:%M:%S"), room.name.title(), __mssg__ ))

		if cmd == "rooms":
			rData = []
			for group in Settings.groups:
				val  = str(self.getRoom(group).usercount)
				rData.append( "<a href='http://{0}.chatango.com/'>{0}</a> ({1} users)".format( group.title(), val ) )
			fData = "I am in " + ", ".join( rData[:int(len(rData) - 1)] ) + ", and " + rData[-1]
			room.message( fData , True )

		if cmd == "whois":
			import whois
			if args.split()[0]=="purge":
				if Group.ID( user ) == 4:
					whois.clearWhois(room, args.split()[1])
				else:
					room.message("No, bad.")
			else:
				whois.getWhois(room, args)

		if cmd == "join":
			try:
				self.joinRoom( args.lower() )
				Settings.groups.append( args.lower() )
			except Exception as e:
				Handle.__errors__ += 1

		if cmd == "leave":
			try:
				self.leaveRoom( args.lower() )
				Settings.groups.append( args.lower() )
			except Exception as e:
				Handle.__errors__ += 1

		if cmd == "find":
			if not ch.User(args).roomnames:
				room.message("Unable to find " + args.title())
			else:
				room.message( args.title() + " has been found in the following chatrooms; " +
					", ".join(ch.User(args).roomnames[:int(len(ch.User(args).roomnames) - 1)]) + ", and " + ch.User(args).roomnames[-1] )

		if cmd == "ship":
			import random
			args = args.lower()
			uwatm8 = room.usernames
			try:
				uwatm8.remove( self.user )
			except: pass
			if args:
				if args not in uwatm8:
					room.message( "Can't find " + args.title() + "." )
				else:
					try: uwatm8.remove( args.lower() )
					except: pass
					sel = random.choice( uwatm8 )
					room.message( args.title() + " x " + sel.title() )
			else:
				try:
					try:
						uwatm8.remove( user )
					except: pass
					__sel__1 = random.choice(uwatm8)
					__sel__2 = random.choice(uwatm8)
					if __sel__1 == __sel__2:
						__sel__2 = random.choice(uwatm8)
					room.message( str( "%s x %s" % (__sel__1.title(),__sel__2.title()) ) )
				except Exception as e:
					room.message(str(e))

		if cmd == "endcmd":
			if args == "omn":
				Handle.XMO(cmd = "setEnd")
				self.stop()
			if args == "silent":
				self.stop()
			if args == "xmo":
				Handle.XMO(cmd = "res")
				self.stop()

		if cmd == "chan":
			import urllib2,json
			try:
				req  = " ".join(args.split()[1:])
				args = args.split()[0].split("-")[1]
				args_present = True
			except:
				room.message( "Missing arguments! D:" )
			if args_present == True:
				if args == "c":
					try:
						if req.lower() not in room.usernames:
							room.message("I can't find {0}! D:".format(req.capitalize()))
						else:
							dataurl= str(urllib2.urlopen("http://{0}.chatango.com".format(user)).read())
							requrl = str(urllib2.urlopen("http://{0}.chatango.com".format(req)).read())
							age__1 = Data.rgx( string = dataurl, objects = ["""<strong>Age:</strong></span></td><td><span class="profile_text">""","<br />"] )
							age__2 = Data.rgx( string = requrl , objects = ["""<strong>Age:</strong></span></td><td><span class="profile_text">""","<br />"] )
							if age__1 == "?":
								room.message("You cannot claim an underling until you have set your age.")
							else:
								if age__2 == "?":
									age__2 = 1
								if( int(age__1) > int(age__2) ):
									if Data.parseSenpai(req) == "":
										chan,user = user.lower(),req.lower()
										Data.__senpais__[user] = json.dumps(chan)
										room.message("You are now %s's senpai! ^^" % (req.capitalize()))
									else:
										if Data.parseSenpai(req) != req:
											if Data.parseSenpai(req) == user:
												ring = " Poor " + req.capitalize() + "."
												chan,user = user.lower(),req.lower()
												Data.__senpais__[chan] = json.dumps(chan)
												room.message("You are now %s's senpai!%s ^^" % (req.capitalize(),ring))
											else:
												room.message("{0} already has a senpai! :o ".format( req.capitalize() ))
										else:
											room.message("You are already the senpai of {0}!".format(req.capitalize()))
								else:
									room.message("You're not older than " + req.capitalize() + ", so you're not the senpai, silly. ^^")
					except Exception as e:
						Handle.__errors__ += 1
				if args == "o":
					if Data.parseSenpai(req) !="":
						room.message("{0}'s senpai is {1}".format(req.capitalize(), Data.parseSenpai(req).capitalize()))
					else:
						room.message("{0} doesn't have a senpai!".format(req.capitalize()))
				if args == "help":
					room.message("This command is similar to Botteh's \"Claim\" command, you will be the senpai of anyone you choose who is in the same room as you (when you choose to be their senpai), and you must be older than them. You can only have one underling at a time, so choose wisely.")

	def onMessage(self, room, user, message):

		import whois

		if( self.user == user ):
			return
		if( Group.ID( user.name.lower() ) == 1 ):
			return

		try:
			import time
			Handle.__msglog__.append("(%s) %s @ %s : %s  " % ( room.name.title(), user.name.title(), time.strftime("%Y/%m/%d %H:%M:%S"), message.body ) )
		except Exception as e:
			Handle.__errors__ += 1
			print str(e)

		try:
			whois.addWhois(user,message)
		except Exception as e:
			print( "[" + Settings.colour("white","err".upper()) + "] " + str(e))

		print("[" + Settings.colour("red","user".upper()) + "] (" +
			Settings.colour("blue",room.name.upper()) +
			") " + Settings.colour("white",user.name.upper()) + " (" + Settings.colour("yellow", Group.title(user.name.lower()).upper() ) + "): " + Settings.colour("green",message.body))

		if( Settings.__relay__ != 0 ):
			import time
			time.sleep( Settings.__relay__ / Settings.__level__ )

		if( Settings.__multicolour__ == True ):
			import random
			colours = Data.__multicolour__
			self.setNameColor( random.choice( colours ) )
			self.setFontColor( random.choice( colours ) )

		if( Data.hasnotes(user.name.lower()) ) and (user.name.lower() not in Data.__notified__):
			room.message( Data.getnotelength(user.name.lower(),"rml") )
			Data.__notified__.append(user.name.lower())

		if( Handle.parseMessage(message.body)==True ):
			parsed = Handle.parse( Settings.prefix, message.body )
			parsed.append(user.name.lower())
			parcmd = Handle.parseCmd( parsed, room )
			if parcmd[1] == "partial":
				try:
					self.parseCmd(room, parcmd, user.name.lower())
				except Exception as e:
					room.message(str(e))
					Handle.__errors__ += 1
			else: return

		if user.name.lower() in Group.whitelist:
			short = message.body.split(" ",1)[0].lower()
			if( short == "micro" ):
				try:
					room.message( "Yes, " + Data.parseAlias(user.name.lower()) + "?" )
				except Exception as e:
					room.message(str(e))

			if( short[0:3] == "*h*" ):
				room.message("<3")

			if(short == "marco"):
				room.message("POLO!")


class Settings(object):
	username       = "Microprocessor"
	password       = "password"
	groups         = None #sorted(["microprocesses","newdle","antimerica","animeyum","freakskingdom1234","betaintellectual","tgarr2","theeeveeclan"])#,"testingcodingroom","cloeys"])
	prefix         = "/"
	version        = "3.3c9"
	__relay__      = 0
	__level__      = 0
	__chatcolour__ = False
	__overflow__   = []
	__PMs__        = False
	__multicolour__= False

	@staticmethod
	def pop(dta):
		if dta == "relay":
			Pop.relay()
		if dta == "level":
			Pop.level()
		else:
			return

	@staticmethod
	def relay(timing):
		global __relay__
		__relay__ = int(timing)

	@staticmethod
	def level(lvl):
		global __level__
		__level__ = int(lvl)

	@staticmethod
	def colour(c,string):
		base   = '\033['
		end    = '\033[0m'
		if c == "red":
			return base + '0;31m' +  string + end
		if c == "white":
			return base + '1;37m' + string + end
		if c == "yellow":
			return base + '0;33m' + string + end
		if c == "blue":
			return base + '0;34m' + string + end
		if c == "green":
			return base + '1;32m' + string + end

class Pop(object):
	@staticmethod
	def onInit(level,relay,colour):
		Settings.level(level)
		Settings.relay(relay)

		if colour == 1:
			Settings.__chatcolour__ = True

	@staticmethod
	def onEnd(md):
		import time

		try:
			__fle__ = open( Handle.directory + "log.txt","r")
			__tmp__ = __fle__.readlines()
			__fle__ = open( Handle.directory + "log.txt","w")
			for construct in Handle.__msglog__ + __tmp__:
				__fle__.write( construct + "\n" )
			__fle__.close()
		except Exception as e:
			print("Unable to save (LOG).\n"+str(e))
			pass
		try:
			__fle__ = open( Handle.directory + "aliases.txt","w")
			for user in Data.__aliases__:
				__fle__.write( json.dumps([user,(json.loads(Data.__aliases__[user]))]) + "\n" )
			__fle__.close()
			__fle__ = open( Handle.directory + "senpais.txt","w")
			for user in Data.__senpais__:
				__fle__.write(json.dumps([user,(json.loads(Data.__senpais__[user]))]) + "\n")
			__fle__.close()

		except Exception as e:
			print("Unable to save (ALIASES/SENPAIS).\n"+str(e))
			pass

		try:
			data = [ ":".join(Settings.groups) , ":".join(Group.administrators) , ":".join(Group.__banned__) , ":".join(Group.__bots__) , ":".join(Group.trusted) , ":".join(Group.whitelist) ]
			__fle__ = open(Handle.directory + "data.txt","w")
			__fle__.write( "\n".join(data) )
			__fle__.close()
		except Exception as e:
			print("Unable to save (DATA).\n"+str(e))
			pass

		if(md==True):
			print("[" + Settings.colour("white","INIT") + "] BOT ended => %s " % (
				time.strftime("%H:%M:%S")
				)
			)
		else:
			return

	@staticmethod
	def setTime(time):
		import time
		if(time==0):
			setTime = time.strftime("%H:%M:%S")
		else:
			if( time == 1 ):
				setTime = time.strftime("%H:%M:%S", gmtime())
			if( time > 1 ):
				setTime = time.strftime("%H:%M:%S") #Resets the time variable since we only need two times in this case.
		print("[" + Settings.colour("white","INIT") + "] BOT started with LEVEL='%s', RELAY='%s'  => %s " % (
				str(Settings.__level__),
				str(Settings.__relay__),
				str(
					setTime
					)
				)
			)

	@staticmethod
	def Assert():
		Handle.__rQueue__ = False

	@staticmethod
	def level():
		Settings.level(0)

	@staticmethod
	def relay():
		Settings.relay(0)

	@staticmethod
	def enableAutoMessaging(setting):
		if setting == 1:
			Settings.__PMs__ = True
		if setting == 0:
			return
		if setting != 1 and setting != 0:
			Pop.enableAutoMessaging(1)

	@staticmethod
	def multicolour(setting):
		if setting == 1:
			Settings.__multicolour__ = True
		if setting == 0:
			return
		if setting != 1 and setting != 0:
			Pop.multicolour(1)

	@staticmethod
	def appendData(lm):
		if lm:
			datax = []
			for line in open( Handle.directory + "data.txt" , "r" ).readlines():
				datax.append( line.replace("\n","") )
			Settings.groups      = sorted(str(datax[0]).split(":"))
			Group.administrators = sorted(str(datax[1]).split(":"))
			Group.__banned__     = sorted(str(datax[2]).split(":"))
			Group.__bots__       = sorted(str(datax[3]).split(":"))
			Group.trusted        = sorted(str(datax[4]).split(":"))
			Group.banned         = Group.__banned__ + Group.__bots__
			Group.whitelist      = sorted(str(datax[5]).split(":"))

	@staticmethod
	def getHelp():
		import random
		sa    = random.choice( ["Clearly intellectual","Unable to process...","B-B-B-B-B... BONFIRE!","The lewdest of them all"] )
		lel   = random.choice( ["Duubz: volkner is first bith","Duubz: Name my dick \"The South\" so it can rise again.","Duubz: "] )
		ga    = "\r".join([ "Version %s" % (Settings.version) , lel , "Programmed by Duubz" ])
		build = "\r\r[%s]\r\r%s" % ( sa , ga )
		return build

class Group(object):
	administrators = None
	trusted        = None
	__bots__       = None
	__banned__     = None
	banned         = None
	whitelist      = None

	@staticmethod
	def ID(username):
		username = str(username).lower()
		if username in Group.administrators:
			return 4
		if username in Group.trusted:
			return 3
		if username in Group.banned:
			return 1
		if username in Group.whitelist:
			return 2
		else:
			return 0

	@staticmethod
	def title(username):
		username = str(username).lower()
		if username in Group.administrators:
			return "Administrator"
		if username in Group.trusted:
			return "Trusted"
		if username in Group.banned:
			return "Banned"
		if username in Group.whitelist:
			return "Whitelisted"
		else:
			return "Unwhitelisted"

class Data(object):
	__commands__ = sorted(["help","whois","pm","rooms","rm","cmds","profile","bg","find","sds","google","image","alias","ship","youtube","deep","say","senpai","note"])
	__ACommands__= sorted(["e","sta","anc","leave","join","proc"])
	__aliases__  = dict()
	__senpais__  = dict()

	__colours__  = ["ff004f","ff004f","Ariel",9]
	__col_dict__ = {"name":1,"msg":2,"face":3,"size":4}

	__notified__ = []

	__multicolour__ = ["FF004F","7630D9","99CC00","00FFFF","DADADA","FFFFFF","800000","3333FF","9900CC","CC0099"]

	@staticmethod
	def dex(query,slx,string=True):
		import sqlite3
		database = sqlite3.connect("/home/equinox/Desktop/Python/Bots/Chatango/new/databases.db", isolation_level = None)
		cursor = database.cursor()
		try:
			if(slx == "array"):
				data = [x for x in cursor.execute(query)]
				return data if string else data
			if(slx == ""):
				data = [x for x in cursor.execute(query)]
				return str(data) if string else data
			if(slx == "retup"):
				data = list([list(x) for x in cursor.execute(query)])
				return data[0] if string else data
			if(slx == "commit"):
				cursor.execute(query)
				database.commit()
		except Exception as e:
			return str(e)
			Handle.__errors__ += 1

	@staticmethod
	def list(query):
		return Data.dex(query,"array",string=False)

	@staticmethod
	def rgx(string,objects):
		import re
		try:
			__Obj__1 = objects[0]
			__Obj__2 = objects[1]
			return re.search('%s(.*)%s' % (__Obj__1,__Obj__2), string).group(1)
		except Exception as e:
			Handle.__errors__ += 1
			return str(e)

	#Alternative to the RGX function
	@staticmethod
	def split(string, objects):
		return string.split( str(objects[0]) , 2 )[1].split( str(objects[1]) , 1 )[0]

	@staticmethod
	def parseAlias(user):
		import json
		user = user.lower()
		if user in Data.__aliases__:
			return json.loads(Data.__aliases__[user])
		else:
			return user

	@staticmethod
	def parseSenpai(user):
		import json
		user = user.lower()
		if user in Data.__senpais__:
			return json.loads(Data.__senpais__[user])
		else:
			return ""

	@staticmethod
	def sendnote(_to,_f,_time,_m):
		import random
		_c = random.randrange( 2 ** 15, 3 ** 16 )
		print str(_c)
		Data.dex("INSERT INTO notes VALUES ('%s','%s','%s','%s','%s')" % (_to,_f,_time,_m,str(_c)),"",string=True)

	@staticmethod
	def readnote(user):
		import time
		user  = user.lower()
		notes = Data.dex("SELECT * FROM notes WHERE _to='%s'" % (user), "retup", string=False)
		if len(notes) >= 1:
			new   = str(notes[0][3]).encode("ascii")
			Data.dex("DELETE FROM notes WHERE _c='%s'" % (notes[0][4]), "commit", string=False )
			return "Note from %s at %s:\r%s" % ( str(notes[0][1]).encode("ascii") , time.strftime("%H:%M:%S on %d/%m/%y", time.localtime(float(notes[0][2]))), new )
		else:
			return "You have no notes! ^^"

	@staticmethod
	def hasnotes(user):
		user = user.lower()
		notes = Data.dex("SELECT * FROM notes WHERE _to='%s'" % (user), "retup", string=False)
		if( len(notes) > 0 ):
			return True
		else:
			return False

	@staticmethod
	def getnotelength(user,ty):
		user = user.lower()
		notes = Data.dex("SELECT * FROM notes WHERE _to='%s'" % (user), "retup", string=False)
		if ty == "":
			if (len(notes)>=2):
				ring = "s"
			else:
				ring = ""
		if ty == "rml":
			if (len(notes)>=2):
				ring = "s, " + user.capitalize()
			else:
				ring = ", " + user.capitalize()
		return "You have {0} unread note{1}.".format(str(len(notes)), ring)

class Handle(object):
	__joined__ = 0
	__errors__ = 0
	__msglog__ = []
	__errlog__ = []
	__rQueue__ = False
	__Ending__ = False
	__rQueHs__ = 0
	directory  = ""

	@staticmethod
	def __quickCall__(function, arguments):
		if function == "start":

			Handle.start(
				arguments[0],
				arguments[1],
				arguments[2]
				)

		if function == "parse":

			Handle.parse(
				arguments[0],
				arguments[1]
				)

		else:
			return

	@staticmethod
	def start(username, password, groups):
		Bot.easy_start(
			rooms = groups,
			name = username,
			password = password
			)

	@staticmethod
	def XMO(cmd):
		if(cmd == "res"):
			Handle.__rQueue__ = True
			Handle.__rQueHs__ += 1
		if(cmd == "get"):
			return Handle.__rQueue__
		if(cmd == "setEnd"):
			Handle.__Ending__ = True
		if(cmd == "getEnd"):
			return Handle.__Ending__

	@staticmethod
	def parse(prefix, data):
		data = data.split(" ",1)
		if(len(data)>1):
			command   = data[0]
			arguments = data[1]
		else:
			command   = data[0]
			arguments = ""

		command = command.lower()

		if(command[0] == prefix):
			prefixed  = True
			command   = command[1:]
		else:
			prefixed  = False
			command   = command

		return [prefixed, command, arguments]

	@staticmethod
	def parseCmd( data , room ):

		import random,urllib,urllib2,json

		if data[0] == True:
			prefix = True
		else:
			prefix = False

		cmd  = data[1]
		args = data[2]
		user = data[3]

		if Group.ID(user.lower()) == 0:
			if prefix and cmd == "help":
				ret = Pop.getHelp()
				Group.whitelist.append(user.lower())
				sta = True
			else: return

		if prefix and cmd == "help":
			ret = Pop.getHelp()
			sta = True

		if prefix and cmd == "whois":
			try:
				ret = ["whois",args]
				sta = "partial"
			except Exception as e:
				Handle.__errlog__.append(str(e))
				Handle.__errors__ += 1

		if prefix and cmd == "e":
			if Group.ID( user ) == 4:
				try:
					ret = eval(args)
					sta = True
				except Exception as e:
					Handle.__errlog__.append(str(e))
					Handle.__errors__ += 1

		if prefix and cmd == "sta":
			if Group.ID( user ) == 4:
				try:
					ret = str( Handle.returnDetails() )
					sta = True
				except Exception as e:
					Handle.__errlog__.append(str(e))
					Handle.__errors__ += 1

		if prefix and cmd == "anc":
				try:
					if Group.ID( user ) == 4:
						ret = ["anc",args]
						sta = "partial"
					else:
						ret = "No, bad."
						sta = True
				except Exception as e:
					Handle.__errlog__.append(str(e))
					Handle.__errors__ += 1

		if prefix and cmd == "pm":
			try:
				ret = ["pm",args]
				sta = "partial"
			except Exception as e:
				Handle.__errlog__.append(str(e))
				Handle.__errors__ += 1

		if prefix and cmd == "rm":
			try:
				ret = ["rm",args]
				sta = "partial"
			except Exception as e:
				Handle.__errlog__.append(str(e))
				Handle.__errors__ += 1

		if prefix and cmd == "rooms":
			try:
				ret = ["rooms",args]
				sta = "partial"
			except Exception as e:
				Handle.__errlog__.append(str(e))
				Handle.__errors__ += 1

		if prefix and cmd == "cmds":
			try:
				if( Group.ID(user)==4):
					exf = ", ".join( (Data.__commands__+Data.__ACommands__)[0:int(len((Data.__commands__+Data.__ACommands__)) - 1)] ) + ", and " + (Data.__commands__+Data.__ACommands__)[-1]
					ring = ""
				else:
					exf = ", ".join( Data.__commands__[0:int(len(Data.__commands__) - 1)] ) + ", and " + Data.__commands__[-1]
					ring= ", however, you only have access to {0} of them".format( len(Data.__commands__) )
				ret = "I have {0} commands, using \"{1}\" as the prefix{2}. The commands are {3}".format(
					str( len( Data.__commands__ + Data.__ACommands__ ) ),
					Settings.prefix,
					ring,
					exf
					)
				sta = True
			except Exception as e:
				Handle.__errlog__.append(str(e))
				Handle.__errors__ += 1

		if prefix and cmd == "join":
			try:
				if Group.ID( user ) == 4:
					ret = ["join",args]
					sta = "partial"
				else:
					room.message("No, bad.")
			except Exception as e:
				Handle.__errlog__.append(str(e))
				Handle.__errors__ += 1

		if prefix and cmd == "leave":
			try:
				if Group.ID( user ) == 4:
					ret = ["leave",args]
					sta = "partial"
				else:
					room.message("No, bad.")
			except Exception as e:
				Handle.__errlog__.append(str(e))
				Handle.__errors__ += 1

		if prefix and cmd == "profile":
			if(len(args)>0):
				data = str( urllib2.urlopen( "http://chatango.com/fpix?"+args.lower() ).read() )
				age  = Data.rgx( string = data, objects = ["""<strong>Age:</strong></span></td><td><span class="profile_text">""","<br />"] )
				loc  = Data.rgx( string = data, objects = ["""<strong>Location:</strong></span></td><td><span class="profile_text">"""," <br />"] )
				sex  = Data.rgx( string = data, objects = ["""<strong>Gender:</strong></span></td><td><span class="profile_text">"""," <br />"] )

				img  = " http://fp.chatango.com/profileimg/{0}/{1}/{2}/full.jpg ".format(
					str(args.lower())[0:1],
					str(args.lower())[1:2],
					str(args.lower())[0:]
					)

				#Don't feel like adding encodings to Python for profiles such as Microprocessor's that use special encoded characters

				#__profile_Text__ = urllib2.urlopen("http://st.chatango.com/profileimg/{0}/{1}/{2}/mod1.xml".format( str(args.lower())[0:1],str(args.lower())[1:2],str(args.lower())[0:] )).read()
				#profileText      = urllib.unquote( Data.rgx( string = __profile_Text__ , objects = ["<body>","</body>"] ) )

				try:
					xData = [age, sex, loc]
					rData = "<b>{0}</b>, {1}, {2}, {3}".format( args.title() , xData[1] , xData[0] , xData[2] )
					ret   = rData + "{0}".format( img ) #, profileText )
					sta   = True
				except Exception as e:
					Handle.__errlog__.append(str(e))
					Handle.__errors__ += 1
			else:
				ret = "Improper use of command; /profile [user]"
				sta = True

		if prefix and cmd == "bg":
			import time,urllib2
			if args:
				user = args
				try:
					img = " http://st.chatango.com/profileimg/{0}/{1}/{2}/msgbg.jpg ".format( str(args.lower())[0:1],str(args.lower())[1:2],str(args.lower())[0:] )
					url = urllib2.urlopen("http://st.chatango.com/profileimg/{0}/{1}/{2}/mod1.xml".format( str(args.lower())[0:1],str(args.lower())[1:2],str(args.lower())[0:] )).read()
					unx = Data.rgx( string = url , objects = ["<d>","</d>"] )
					ret = "{0} {1}'s BG ends on {2}".format( img , args.title() , time.ctime( float(unx) ) )
					sta = True
				except Exception as e:
					Handle.__errlog__.append(str(e))
					Handle.__errors__ += 1
			else:
				args = user
				try:
					img = " http://st.chatango.com/profileimg/{0}/{1}/{2}/msgbg.jpg ".format( str(args.lower())[0:1],str(args.lower())[1:2],str(args.lower())[0:] )
					url = urllib2.urlopen("http://st.chatango.com/profileimg/{0}/{1}/{2}/mod1.xml".format( str(args.lower())[0:1],str(args.lower())[1:2],str(args.lower())[0:] )).read()
					unx = Data.rgx( string = url , objects = ["<d>","</d>"] )
					ret = "{0} {1}'s BG ends on {2}".format( img , args.title() , time.ctime( float(unx) ) )
					sta = True
				except Exception as e:
					Handle.__errlog__.append(str(e))
					Handle.__errors__ += 1

		if prefix and cmd == "find":
			try:
				ret = ["find",args]
				sta = "partial"
			except Exception as e:
				Handle.__errlog__.append(str(e))
				Handle.__errors__ += 1

		if prefix and cmd == "sds":
			xList = ["http://i.imgur.com/uL7LQU4.png","http://i.imgur.com/3xL77OZ.jpg","http://oi58.tinypic.com/zl2lc3.jpg"]
			try:
				ret = random.choice(xList)
				sta = True
			except Exception as e:
				Handle.__errlog__.append(str(e))
				Handle.__errors__ += 1

		if prefix and cmd == "google":
			try:
				dataExt = json.loads( urllib2.urlopen( "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=" + (urllib.quote(args)) ).read() )
				dat     = dataExt['responseData']
				xRes    = []
				for res in dat['results']:
					xRes.append( res['url'] )
				rRet    = "\r".join( xRes[0:3] )
				xRet    = "{0} estimated results in {1} seconds. Here is the first <b>{2}</b> results.\r".format(
					dat['cursor']['estimatedResultCount'],
					dat['cursor']['searchResultTime'],
					str(3),
					str(urllib.unquote( args ))
					)
				ret     = xRet + rRet
				sta     = True
			except Exception as e:
				Handle.__errlog__.append(str(e))
				Handle.__errors__ += 1

		if prefix and cmd == "image":
			try:
				args = urllib.quote( args )
				i    = 1
				xRes = []
				dataExt = json.loads(urllib2.urlopen("https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q="+args).read().decode("utf-8"))
				for res in dataExt['responseData']['results']:
					xRes.append( res['unescapedUrl'] )
				ret = str(random.choice(xRes))
				sta = True
			except Exception as e:
				Handle.__errlog__.append(str(e))
				Handle.__errors__ += 1

		if prefix and cmd == "alias":
			try:
				if( len(args)>0 ):
					if( args.split()[0] == "-s" ):
						args = " ".join(args.split()[1:])
						alias, user = args, user
						Data.__aliases__[user] = json.dumps(alias)
						ret = "Alias set successfully, I shall now refer to you as \"{0}\", {1}.".format(alias,user)
						sta = True
					if( args.split()[0] == "-o" ):
						args = " ".join(args.split()[1:])
						ret  = "{0}'s alias is {1}.".format( args.title() , Data.parseAlias( args ) )
						sta  = True
					if( args.split()[0] == "-c" ):
						args = " ".join(args.split()[1:])
						if(Group.ID(user)==4):
							alias, user = " ".join(args.split()[1:]),args.split()[0]
							Data.__aliases__[user] = json.dumps(alias)
							ret = "Alias changed."
							sta = True
						else:
							ret = "No, bad."
							sta = True
				else:
					ret = "Improper use of command; /alias -[s/o/c] [IF:C/O;user] [alias]"
					sta = True
			except Exception as e:
				Handle.__errlog__.append(str(e))
				Handle.__errors__ += 1

		if prefix and cmd == "deep":
			ret = random.choice( [ "http://i.imgur.com/TwAAv6V.png" , "http://i.imgur.com/fhqnuUW.png" ] )
			sta = True

		if prefix and cmd == "ship":
			try:
				ret = ["ship",args]
				sta = "partial"
			except Exception as e:
				Handle.__errlog__.append(str(e))
				Handle.__errors__ += 1

		if prefix and cmd == "proc":
			import subprocess as sub
			if Group.ID( user ) == 4:
				if args.split()[0] == "-help":
					ret = "/proc -[CMD] -[IF-ANY:ARGS]"
					sta = True
				if args.split()[0] == "-end":
					if args.split()[1] == "-s":
						ret = ["endcmd","silent"]
						sta = "partial"
					if args.split()[1] == "-o":
						ret = ["endcmd","omn"]
						sta = "partial"
				if args.split()[0] == "-restart":
						ret = ["endcmd","xmo"]
						sta = "partial"
				if args.split()[0] == "-term":
					if args.split()[1] != "":
						x = sub.Popen( " ".join(args.split()[1:]) , shell = True , stderr = sub.PIPE , stdout = sub.PIPE )
						ret, err = x.communicate()
						__err__  = x.returncode
						sta = True
				if not args:
					room.message("Improper use of command; do /proc -help")

		if prefix and cmd == "youtube":
			try:
				__inf__  = str( urllib2.urlopen( "http://gdata.youtube.com/feeds/api/videos?vq=" + urllib.quote( args ) ).read() )
				__link__ = Data.split(string = __inf__ , objects =["<media:player url='http://www.youtube.com/watch?v=","&amp;"])
				__inf__  = str( urllib2.urlopen("http://gdata.youtube.com/feeds/api/videos/"+__link__).read() )
				Auth     = Data.split(string = __inf__ , objects = ["/><author><name>","</name>"])
				Title    = Data.split(string = __inf__ , objects = ["<media:title type='plain'>","</media:title>"])
				Uploaded = Data.split(string = __inf__ , objects = ["<published>","T"])
				Views    = Data.split(string = __inf__ , objects = ["viewCount='","'/>"])
				Category = Data.split(string = __inf__ , objects = ["<media:category label='","'"])
				ret = "<b>%s</b>, uploaded by <b>%s</b> on <b>%s</b>.\rThis video has <i>%s views</i>, and is under the <i>%s category</i>.\r %s" % ( Title , Auth , Uploaded ,Views , Category , "http://www.youtube.com/watch?v="+__link__ )
				sta = True
			except Exception as e:
				Handle.__errlog__.append(str(e))
				Handle.__errors__ += 1

		if prefix and cmd == "inf":
			if Group.ID(user) == 4:
				import os,getpass,socket
				if not args:
					ret = "Improper use of command; /inf -[args]"
					sta = True
				else:
					if args.split("-")[1] == "dxl":
						try:
							ret = str(os.getloadavg())
							sta = True
						except Exception as e:
							ret = str(e)
							sta = True
					if args.split("-")[1] == "mcd":
						try:
							import types
							xlmUSER = "%s@%s" % (getpass.getuser(),socket.gethostname())
							loadavg = str(os.getloadavg())
							clss = [n for n,v in globals().items()]
							ret = "\r\r[ S Y S T E M _ I N F O R M A T I O N ]\r\rGlobal items: " + str(clss) + "\rRunning on {0} with a load average of {1}".format(
								xlmUSER,
								loadavg
								) + "\r" + Handle.returnDetails() + "\rError log: " + str(Handle.__errlog__)
							print ret
							sta = True
						except Exception as e:
							Handle.__errlog__.append(str(e))
							Handle.__errors__ += 1

		if prefix and cmd == "say":
			ret = args
			sta = True

		if prefix and cmd == "senpai":
			if args != "":
				ret = ["chan",args]
				sta = "partial"
			else:
				ret = "Missing arguments, do \"/senpai -help\" for extra help."
				sta = True

		if prefix and cmd == "note":
			import time
			try:
				if not args:
					ret = str(Data.getnotelength(user.lower(),""))
					sta = True
				else:
					argus = args.split()[0]
					if argus == "-send":
						__to__ = str(args.split()[1]).split("-")[1]
						if __to__ in Group.__banned__:
							ret = ("I can't send a note to a banned member, sorry! ^^ ")
							sta = True
						else:
							__from__ = user.lower()
							__time__ = time.time()
							__message__ = " ".join(args.split()[2:])
							try:
								Data.sendnote(__to__,__from__,__time__,__message__)
								ret = ("Note sent to %s! ^^ " % ( __to__.capitalize() ) )
								sta = True
							except Exception as e:
								ret = ("There was an error when sending this message! D:")
								sta = True
								Handle.__errlog__.append(str(e))
								Handle.__errors__ += 1
					if argus == "-read":
						ret = str(Data.readnote(user.lower()))
						sta = True
					if argus == "-help":
						ret = "Send people notes through the bot! You can only send notes to users who are not banned from usage of me, but don't worry, I check if they're banned first! ^^ (usage; /note -[SEND:READ:HELP:] -[IF:SEND; USERNAME] [IF:SEND; MESSAGE])"
						sta = True
			except Exception as e:
				Handle.__errlog__.append(str(e))
				Handle.__errors__ += 1

		if(sta == True):
			room.message(ret,True)
		if(sta == "partial"):
			return [ret, sta]
		else:
			return

	@staticmethod
	def parseMessage(data):
		if data.split(" ",1)[0][0] == "/":
			return True
		else:
			return False

	@staticmethod
	def parsePM(data):
		import subprocess as sub
		term = sub.Popen( "python3 /home/equinox/Desktop/Python/Bots/Chatango/new/pms.py " + data , shell = True , stderr = sub.PIPE , stdout = sub.PIPE )
		ret, err = term.communicate()
		code     = term.returncode
		print str(ret)
		return str(ret)

	@staticmethod
	def returnDetails():
		try:
			return ("{0} Errors parsed; Currently connected to {1} room(s).".format( str(Handle.__errors__), str(Handle.__joined__) ))
		except Exception as e:
			return (str(e))
			Handle.__errors__ += 1 #LOL

if __name__ == "__main__":
	try:
		import json
		__alias__file__ = open("/home/equinox/Desktop/Python/Bots/Chatango/new/aliases.txt")
		for line in __alias__file__.readlines():
			user, alias            = json.loads( line.strip() )
			Data.__aliases__[user] = json.dumps(alias)
		__alias__file__.close()
		__senpai__file__= open("/home/equinox/Desktop/Python/Bots/Chatango/new/senpais.txt")
		for line in __senpai__file__.readlines():
			user, senpai           = json.loads( line.strip() )
			Data.__senpais__[user] = json.dumps(senpai)
		__senpai__file__.close()
		Handle.directory = "/home/equinox/Desktop/Python/Bots/Chatango/new/"
		Pop.appendData(1)
		Pop.Assert() #Resets the __rQueue__ variable in the Handle class (for restarting the bot)
		Pop.onInit(0,0,1) #Resets the bot's LEVEL and RELAY if they were modified, third variable is to enable colours/font styling or not.
		Pop.setTime(0) #Returns the exact timestamp the bot was started
		Pop.enableAutoMessaging(0)
		Pop.multicolour(1)
		Handle.__quickCall__(
			function = "start",
			arguments = [Settings.username, Settings.password, Settings.groups]
			)
		if(Handle.XMO(cmd = "get") == True ):
			Pop.Assert()
			Handle.__quickCall__(
				function = "start",
				arguments = [Settings.username, Settings.password, Settings.groups]
				)
		else:
			if(Handle.XMO(cmd = "getEnd")==True):
				Pop.onEnd(True)
			else:
				Pop.onEnd(False)
	except KeyboardInterrupt:
		Pop.onEnd(False)
