from Tkinter import * 
from ttk import Frame, Button, Style
from collections import defaultdict
#
#import os
#import sys

dictionary = {1:187, 2:189, 3:191, 4:193, 5:195, 6:197, 7:199, 8:201, 9:203, 10:205, 11:207, 12:209, 13:211, 14:213, 15:215, 16:217, 17:219, 18:221, 19:223, 20:225, 21:227, 22:229, 23:231, 24:233, 25:235, 26:237, 27:239, 28:241} #
links = []  
hosts = []
switches = []
sw = []
ho = []
s = 0

#coordinates of the hosts
v=[[248,20],[108,545],[108,570],[108,595],[108,620],[178,545],[178,570], [178,595], [178,620],[248,545],[248,570], [248,595], [248,620], [318,545],[318,570],[318,595],[318,620],[600,545]]

#coordinates of the switches
#w=[[108,470], [178,470], [248,470], [318,470], [460,470], [530,470], [600,470], [670,470], [178,90], [248,90], [530,90], [600,90], [178,333], [248,333], [530,333], [600,333], [108,204], [178,204], [248,204], [318,204], [460,204], [530,204], [600,204], [670,204]]
         
w = [[178,90], [248,90], [530,90], [600,90],[108,204], [178,204], [248,204], [318,204], [460,204], [530,204], [600,204], [670,204],[108,333],[178,333], [248,333], [318,333],[460,333],[530,333], [600,333], [670,333], 
[108,470], [178,470], [248,470], [318,470], [460,470], [530,470], [600,470], [670,470] ]   

paintlink = defaultdict(lambda:defaultdict(lambda:None))
hosts_list = []

class GraphicInterface(Frame):
        global s 
        
        s = 30
        s/=2
    
    	
        def __init__(self, master=None):
		    # create main frame
		    master = Tk()
		    #master.attributes('-zoomed', True)
		    #master.overrideredirect(True)
		    Frame.__init__(self, master)
		    self.master.title("Topology")
		    self.master.style = Style()
		    self.master.resizable(width = True, height = True)   
		    # configure the geometry
		    self.grid(padx = 10, pady = 10)
		    # call the funtions
		    self.createWidgets()                                  
		    self.paint_active_links()
		    self.paint_idle_links()

	def paint_idle_links(self):
		global paintlink
		for src,dict in paintlink.iteritems():
			for dst, workload in dict.iteritems():					
				for pos, l in enumerate(links):
					if l["typ"] == "sh":
						continue
					if workload == 0 and src == int(l["fro"]) and dst == int(l["to"]):
						for h in hosts_list:
							for path in h.path_list:
								for node in path.path:
									if src == node or dst == node:
										if h.workload > 0:
											return
						self.idle_link(l["l"])

		self.after(500,self.paint_idle_links)

	def paint_active_links(self):	
		global paintlink
		for src,dict in paintlink.iteritems():
			for dst, workload in dict.iteritems():					
				for pos, l in enumerate(links):
					if l["typ"] == "sh":
						continue
					if workload >=1 and workload <= 10.0:
						if src == int(l["fro"]) and dst == int(l["to"]) and str(l["typ"]) == "10":
							self.use_link(l["l"])
							'''for lnk in links:
								if lnk["typ"] == "sh":
									continue
								if src == int(lnk["fro"]) and dst == int(lnk["to"]) and str(lnk["typ"]) == "30":
									self.idle_link(l["l"])'''
					else:
						if src == int(l["fro"]) and dst == int(l["to"]) and str(l["typ"]) == "30" and workload > 10.0:
							self.use_link(l["l"])
							'''for lnk in links:
								if lnk["typ"] == "sh":
									continue
								if src == int(lnk["fro"]) and dst == int(lnk["to"]) and str(lnk["typ"]) == "10":
									self.idle_link(l["l"])'''
		self.after(500,self.paint_active_links)

        def createWidgets(self):
                global links, w, v, s, ho, sw
                self.hosts = ["Sink 1", "Source 1","Source 2","Source 3","Source 4", "Source 5", "Source 6","Source 7","Source 8","Source 9","Source 10","Source 11","Source 12","Source 13","Source 14","Source 15","Source 16", "Sink 2"]
                self.switches = ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11", "s12", "s13", "s14", "s15", "s16", "s17", "s18", "s19", "s20", "s21", "s22", "s23", "s24", "s25", "s26", "s27", "s28"]
                self.canvas = Canvas(self,width=870, height=680)
                self.canvas.grid(row=0, column=0, padx = 10)
                self.canvas.create_rectangle(1, 1, 870, 680, fill="white", )
                #self.canvas.create_rectangle(730,25,850,65, outline="light slate gray")
                #self.canvas.create_line(750,35,760,35, fill="red")
                #self.canvas.create_text(810,35, text="30Mbps", fill="navy")
                #self.canvas.create_line(750,55,760,55, fill="gray", dash=(4,3))
                #self.canvas.create_text(810,55, text="< 10 Mbps", fill="navy")
                self.canvas.create_rectangle(20,15, 80, 45, fill="white") 
                self.time = self.canvas.create_text(50, 30, text="hh:mm", fill="black", tag="time")
                self.canvas.pack(fill=BOTH, expand= YES)
	
                for i in range(178):
                        links.append({})                        
              
                links[0]={"l":self.createLinkSwH(w[1],v[0]), "fro":"2", "to":"h18", "typ":"sh"}
                links[1]={"l":self.createLinkSwH(w[20],v[1]), "fro":"21", "to":"h1", "typ":"sh"}
                links[2]={"l":self.createLinkSwH(w[20],v[2]), "fro":"21", "to":"h2", "typ":"sh"}
                links[3]={"l":self.createLinkSwH(w[20],v[3]), "fro":"21", "to":"h3", "typ":"sh"}
                links[4]={"l":self.createLinkSwH(w[20],v[4]), "fro":"21", "to":"h4", "typ":"sh"}
                links[5]={"l":self.createLinkSwH(w[21],v[5]), "fro":"22", "to":"h5", "typ":"sh"}
                links[6]={"l":self.createLinkSwH(w[21],v[6]), "fro":"22", "to":"h6", "typ":"sh"}
                links[7]={"l":self.createLinkSwH(w[21],v[7]), "fro":"22", "to":"h7", "typ":"sh"}
                links[8]={"l":self.createLinkSwH(w[21],v[8]), "fro":"22", "to":"h8", "typ":"sh"}
                links[9]={"l":self.createLinkSwH(w[22],v[9]), "fro":"23", "to":"h9", "typ":"sh"}
                links[10]={"l":self.createLinkSwH(w[22],v[10]), "fro":"23", "to":"h10", "typ":"sh"}
                links[11]={"l":self.createLinkSwH(w[22],v[11]), "fro":"23", "to":"h11", "typ":"sh"}
                links[12]={"l":self.createLinkSwH(w[22],v[12]), "fro":"23", "to":"h12", "typ":"sh"}
                links[13]={"l":self.createLinkSwH(w[23],v[13]), "fro":"24", "to":"h13", "typ":"sh"}
                links[14]={"l":self.createLinkSwH(w[23],v[14]), "fro":"24", "to":"h14", "typ":"sh"}
                links[15]={"l":self.createLinkSwH(w[23],v[15]), "fro":"24", "to":"h15", "typ":"sh"}
                links[16]={"l":self.createLinkSwH(w[23],v[16]), "fro":"24", "to":"h16", "typ":"sh"}
                links[17]={"l":self.createLinkSwH(w[26],v[17]), "fro":"27", "to":"h17", "typ":"sh"}
               
                links[18]={"l":self.createLink30(w[0],w[4]), "fro":"1", "to":"5", "typ":"30"}
                links[19]={"l":self.createLink30(w[0],w[5]), "fro":"1", "to":"6", "typ":"30"}
                links[20]={"l":self.createLink30(w[0],w[6]), "fro":"1", "to":"7", "typ":"30"}
                links[21]={"l":self.createLink30(w[0],w[7]), "fro":"1", "to":"8", "typ":"30"}
                links[22]={"l":self.createLink30(w[1],w[4]), "fro":"2", "to":"5", "typ":"30"}
                links[23]={"l":self.createLink30(w[1],w[5]), "fro":"2", "to":"6", "typ":"30"}
                links[24]={"l":self.createLink30(w[1],w[6]), "fro":"2", "to":"7", "typ":"30"}
                links[25]={"l":self.createLink30(w[1],w[7]), "fro":"2", "to":"8", "typ":"30"}
                links[26]={"l":self.createLink30(w[2],w[8]), "fro":"3", "to":"9", "typ":"30"}
                links[27]={"l":self.createLink30(w[2],w[9]), "fro":"3", "to":"10", "typ":"30"}
                links[28]={"l":self.createLink30(w[2],w[10]), "fro":"3", "to":"11", "typ":"30"}
                links[29]={"l":self.createLink30(w[2],w[11]), "fro":"3", "to":"12", "typ":"30"}
                links[30]={"l":self.createLink30(w[3],w[8]), "fro":"4", "to":"9", "typ":"30"}
                links[31]={"l":self.createLink30(w[3],w[9]), "fro":"4", "to":"10", "typ":"30"}
                links[32]={"l":self.createLink30(w[3],w[10]), "fro":"4", "to":"11", "typ":"30"}
                links[33]={"l":self.createLink30(w[3],w[11]), "fro":"4", "to":"12", "typ":"30"}
                links[34]={"l":self.createLink30(w[4],w[12]), "fro":"5", "to":"13", "typ":"30"}
                links[35]={"l":self.createLink30(w[4],w[13]), "fro":"5", "to":"14", "typ":"30"}
                links[36]={"l":self.createLink30(w[4],w[16]), "fro":"5", "to":"17", "typ":"30"}
                links[37]={"l":self.createLink30(w[4],w[17]), "fro":"5", "to":"18", "typ":"30"}
                links[38]={"l":self.createLink30(w[5],w[12]), "fro":"6", "to":"13", "typ":"30"}
                links[39]={"l":self.createLink30(w[5],w[13]), "fro":"6", "to":"14", "typ":"30"}
                links[40]={"l":self.createLink30(w[5],w[16]), "fro":"6", "to":"17", "typ":"30"}
                links[41]={"l":self.createLink30(w[5],w[17]), "fro":"6", "to":"18", "typ":"30"}
                links[42]={"l":self.createLink30(w[6],w[12]), "fro":"7", "to":"13", "typ":"30"}
                links[43]={"l":self.createLink30(w[6],w[13]), "fro":"7", "to":"14", "typ":"30"}
                links[44]={"l":self.createLink30(w[6],w[16]), "fro":"7", "to":"17", "typ":"30"}
                links[45]={"l":self.createLink30(w[6],w[17]), "fro":"7", "to":"18", "typ":"30"}
                links[46]={"l":self.createLink30(w[7],w[12]), "fro":"8", "to":"13", "typ":"30"}
                links[47]={"l":self.createLink30(w[7],w[13]), "fro":"8", "to":"14", "typ":"30"}
                links[48]={"l":self.createLink30(w[7],w[16]), "fro":"8", "to":"17", "typ":"30"}
                links[49]={"l":self.createLink30(w[7],w[17]), "fro":"8", "to":"18", "typ":"30"}
                links[50]={"l":self.createLink30(w[8],w[14]), "fro":"9", "to":"15", "typ":"30"}
                links[51]={"l":self.createLink30(w[8],w[15]), "fro":"9", "to":"16", "typ":"30"}
                links[52]={"l":self.createLink30(w[8],w[18]), "fro":"9", "to":"19", "typ":"30"}
                links[53]={"l":self.createLink30(w[8],w[19]), "fro":"9", "to":"20", "typ":"30"}
                links[54]={"l":self.createLink30(w[9],w[14]), "fro":"10", "to":"15", "typ":"30"}
                links[55]={"l":self.createLink30(w[9],w[15]), "fro":"10", "to":"16", "typ":"30"}
                links[56]={"l":self.createLink30(w[9],w[18]), "fro":"10", "to":"19", "typ":"30"}
                links[57]={"l":self.createLink30(w[9],w[19]), "fro":"10", "to":"20", "typ":"30"}
                links[58]={"l":self.createLink30(w[10],w[14]), "fro":"11", "to":"15", "typ":"30"}
                links[59]={"l":self.createLink30(w[10],w[15]), "fro":"11", "to":"16", "typ":"30"}
                links[60]={"l":self.createLink30(w[10],w[18]), "fro":"11", "to":"19", "typ":"30"}
                links[61]={"l":self.createLink30(w[10],w[19]), "fro":"11", "to":"20", "typ":"30"}
                links[62]={"l":self.createLink30(w[11],w[14]), "fro":"12", "to":"15", "typ":"30"}
                links[63]={"l":self.createLink30(w[11],w[15]), "fro":"12", "to":"16", "typ":"30"}
                links[64]={"l":self.createLink30(w[11],w[18]), "fro":"12", "to":"19", "typ":"30"}
                links[65]={"l":self.createLink30(w[11],w[19]), "fro":"12", "to":"20", "typ":"30"}
                links[66]={"l":self.createLink30(w[12],w[20]), "fro":"13", "to":"21", "typ":"30"}
                links[67]={"l":self.createLink30(w[12],w[21]), "fro":"13", "to":"22", "typ":"30"}
                links[68]={"l":self.createLink30(w[12],w[22]), "fro":"13", "to":"23", "typ":"30"}
                links[69]={"l":self.createLink30(w[12],w[23]), "fro":"13", "to":"24", "typ":"30"}
                links[70]={"l":self.createLink30(w[13],w[20]), "fro":"14", "to":"21", "typ":"30"}
                links[71]={"l":self.createLink30(w[13],w[21]), "fro":"14", "to":"22", "typ":"30"}
                links[72]={"l":self.createLink30(w[13],w[22]), "fro":"14", "to":"23", "typ":"30"}
                links[73]={"l":self.createLink30(w[13],w[23]), "fro":"14", "to":"24", "typ":"30"}
                links[74]={"l":self.createLink30(w[14],w[20]), "fro":"15", "to":"21", "typ":"30"}
                links[75]={"l":self.createLink30(w[14],w[21]), "fro":"15", "to":"22", "typ":"30"}
                links[76]={"l":self.createLink30(w[14],w[22]), "fro":"15", "to":"23", "typ":"30"}
                links[77]={"l":self.createLink30(w[14],w[23]), "fro":"15", "to":"24", "typ":"30"}
                links[78]={"l":self.createLink30(w[15],w[20]), "fro":"16", "to":"21", "typ":"30"}
                links[79]={"l":self.createLink30(w[15],w[21]), "fro":"16", "to":"22", "typ":"30"}
                links[80]={"l":self.createLink30(w[15],w[22]), "fro":"16", "to":"23", "typ":"30"}
                links[81]={"l":self.createLink30(w[15],w[23]), "fro":"16", "to":"24", "typ":"30"}
                links[82]={"l":self.createLink30(w[16],w[24]), "fro":"17", "to":"25", "typ":"30"}
                links[83]={"l":self.createLink30(w[16],w[25]), "fro":"17", "to":"26", "typ":"30"}
                links[84]={"l":self.createLink30(w[16],w[26]), "fro":"17", "to":"27", "typ":"30"}
                links[85]={"l":self.createLink30(w[16],w[27]), "fro":"17", "to":"28", "typ":"30"}
                links[86]={"l":self.createLink30(w[17],w[24]), "fro":"18", "to":"25", "typ":"30"}
                links[87]={"l":self.createLink30(w[17],w[25]), "fro":"18", "to":"26", "typ":"30"}
                links[88]={"l":self.createLink30(w[17],w[26]), "fro":"18", "to":"27", "typ":"30"}
                links[89]={"l":self.createLink30(w[17],w[27]), "fro":"18", "to":"28", "typ":"30"}
                links[90]={"l":self.createLink30(w[18],w[24]), "fro":"19", "to":"25", "typ":"30"}
                links[91]={"l":self.createLink30(w[18],w[25]), "fro":"19", "to":"26", "typ":"30"}
                links[92]={"l":self.createLink30(w[18],w[26]), "fro":"19", "to":"27", "typ":"30"}
                links[93]={"l":self.createLink30(w[18],w[27]), "fro":"19", "to":"28", "typ":"30"}
                links[94]={"l":self.createLink30(w[19],w[24]), "fro":"20", "to":"25", "typ":"30"}
                links[95]={"l":self.createLink30(w[19],w[25]), "fro":"20", "to":"26", "typ":"30"}
                links[96]={"l":self.createLink30(w[19],w[26]), "fro":"20", "to":"27", "typ":"30"}
                links[97]={"l":self.createLink30(w[19],w[27]), "fro":"20", "to":"28", "typ":"30"}
                
                links[98]={"l":self.createLink10(w[0],w[4]), "fro":"1", "to":"5", "typ":"10"}
                links[99]={"l":self.createLink10(w[0],w[5]), "fro":"1", "to":"6", "typ":"10"}
                links[100]={"l":self.createLink10(w[0],w[6]), "fro":"1", "to":"7", "typ":"10"}
                links[101]={"l":self.createLink10(w[0],w[7]), "fro":"1", "to":"8", "typ":"10"}
                links[102]={"l":self.createLink10(w[1],w[4]), "fro":"2", "to":"5", "typ":"10"}
                links[103]={"l":self.createLink10(w[1],w[5]), "fro":"2", "to":"6", "typ":"10"}
                links[104]={"l":self.createLink10(w[1],w[6]), "fro":"2", "to":"7", "typ":"10"}
                links[105]={"l":self.createLink10(w[1],w[7]), "fro":"2", "to":"8", "typ":"10"}
                links[106]={"l":self.createLink10(w[2],w[8]), "fro":"3", "to":"9", "typ":"10"}
                links[107]={"l":self.createLink10(w[2],w[9]), "fro":"3", "to":"10", "typ":"10"}
                links[108]={"l":self.createLink10(w[2],w[10]), "fro":"3", "to":"11", "typ":"10"}
                links[109]={"l":self.createLink10(w[2],w[11]), "fro":"3", "to":"12", "typ":"10"}
                links[110]={"l":self.createLink10(w[3],w[8]), "fro":"4", "to":"9", "typ":"10"}
                links[111]={"l":self.createLink10(w[3],w[9]), "fro":"4", "to":"10", "typ":"10"}
                links[112]={"l":self.createLink10(w[3],w[10]), "fro":"4", "to":"11", "typ":"10"}
                links[113]={"l":self.createLink10(w[3],w[11]), "fro":"4", "to":"12", "typ":"10"}
                links[114]={"l":self.createLink10(w[4],w[12]), "fro":"5", "to":"13", "typ":"10"}
                links[115]={"l":self.createLink10(w[4],w[13]), "fro":"5", "to":"14", "typ":"10"}
                links[116]={"l":self.createLink10(w[4],w[16]), "fro":"5", "to":"17", "typ":"10"}
                links[117]={"l":self.createLink10(w[4],w[17]), "fro":"5", "to":"18", "typ":"10"}
                links[118]={"l":self.createLink10(w[5],w[12]), "fro":"6", "to":"13", "typ":"10"}
                links[119]={"l":self.createLink10(w[5],w[13]), "fro":"6", "to":"14", "typ":"10"}
                links[120]={"l":self.createLink10(w[5],w[16]), "fro":"6", "to":"17", "typ":"10"}
                links[121]={"l":self.createLink10(w[5],w[17]), "fro":"6", "to":"18", "typ":"10"}
                links[122]={"l":self.createLink10(w[6],w[12]), "fro":"7", "to":"13", "typ":"10"}
                links[123]={"l":self.createLink10(w[6],w[13]), "fro":"7", "to":"14", "typ":"10"}
                links[124]={"l":self.createLink10(w[6],w[16]), "fro":"7", "to":"17", "typ":"10"}
                links[125]={"l":self.createLink10(w[6],w[17]), "fro":"7", "to":"18", "typ":"10"}
                links[126]={"l":self.createLink10(w[7],w[12]), "fro":"8", "to":"13", "typ":"10"}
                links[127]={"l":self.createLink10(w[7],w[13]), "fro":"8", "to":"14", "typ":"10"}
                links[128]={"l":self.createLink10(w[7],w[16]), "fro":"8", "to":"17", "typ":"10"}
                links[129]={"l":self.createLink10(w[7],w[17]), "fro":"8", "to":"18", "typ":"10"}
                links[130]={"l":self.createLink10(w[8],w[14]), "fro":"9", "to":"15", "typ":"10"}
                links[131]={"l":self.createLink10(w[8],w[15]), "fro":"9", "to":"16", "typ":"10"}
                links[132]={"l":self.createLink10(w[8],w[18]), "fro":"9", "to":"19", "typ":"10"}
                links[133]={"l":self.createLink10(w[8],w[19]), "fro":"9", "to":"20", "typ":"10"}
                links[134]={"l":self.createLink10(w[9],w[14]), "fro":"10", "to":"15", "typ":"10"}
                links[135]={"l":self.createLink10(w[9],w[15]), "fro":"10", "to":"16", "typ":"10"}
                links[136]={"l":self.createLink10(w[9],w[18]), "fro":"10", "to":"19", "typ":"10"}
                links[137]={"l":self.createLink10(w[9],w[19]), "fro":"10", "to":"20", "typ":"10"}
                links[138]={"l":self.createLink10(w[10],w[14]), "fro":"11", "to":"15", "typ":"10"}
                links[139]={"l":self.createLink10(w[10],w[15]), "fro":"11", "to":"16", "typ":"10"}
                links[140]={"l":self.createLink10(w[10],w[18]), "fro":"11", "to":"19", "typ":"10"}
                links[141]={"l":self.createLink10(w[10],w[19]), "fro":"11", "to":"20", "typ":"10"}
                links[142]={"l":self.createLink10(w[11],w[14]), "fro":"12", "to":"15", "typ":"10"}
                links[143]={"l":self.createLink10(w[11],w[15]), "fro":"12", "to":"16", "typ":"10"}
                links[144]={"l":self.createLink10(w[11],w[18]), "fro":"12", "to":"19", "typ":"10"}
                links[145]={"l":self.createLink10(w[11],w[19]), "fro":"12", "to":"20", "typ":"10"}
                links[146]={"l":self.createLink10(w[12],w[20]), "fro":"13", "to":"21", "typ":"10"}
                links[147]={"l":self.createLink10(w[12],w[21]), "fro":"13", "to":"22", "typ":"10"}
                links[148]={"l":self.createLink10(w[12],w[22]), "fro":"13", "to":"23", "typ":"10"}
                links[149]={"l":self.createLink10(w[12],w[23]), "fro":"13", "to":"24", "typ":"10"}
                links[150]={"l":self.createLink10(w[13],w[20]), "fro":"14", "to":"21", "typ":"10"}
                links[151]={"l":self.createLink10(w[13],w[21]), "fro":"14", "to":"22", "typ":"10"}
                links[152]={"l":self.createLink10(w[13],w[22]), "fro":"14", "to":"23", "typ":"10"}
                links[153]={"l":self.createLink10(w[13],w[23]), "fro":"14", "to":"24", "typ":"10"}
                links[154]={"l":self.createLink10(w[14],w[20]), "fro":"15", "to":"21", "typ":"10"}
                links[155]={"l":self.createLink10(w[14],w[21]), "fro":"15", "to":"22", "typ":"10"}
                links[156]={"l":self.createLink10(w[14],w[22]), "fro":"15", "to":"23", "typ":"10"}
                links[157]={"l":self.createLink10(w[14],w[23]), "fro":"15", "to":"24", "typ":"10"}
                links[158]={"l":self.createLink10(w[15],w[20]), "fro":"16", "to":"21", "typ":"10"}
                links[159]={"l":self.createLink10(w[15],w[21]), "fro":"16", "to":"22", "typ":"10"}
                links[160]={"l":self.createLink10(w[15],w[22]), "fro":"16", "to":"23", "typ":"10"}
                links[161]={"l":self.createLink10(w[15],w[23]), "fro":"16", "to":"24", "typ":"10"}
                links[162]={"l":self.createLink10(w[16],w[24]), "fro":"17", "to":"25", "typ":"10"}
                links[163]={"l":self.createLink10(w[16],w[25]), "fro":"17", "to":"26", "typ":"10"}
                links[164]={"l":self.createLink10(w[16],w[26]), "fro":"17", "to":"27", "typ":"10"}
                links[165]={"l":self.createLink10(w[16],w[27]), "fro":"17", "to":"28", "typ":"10"}
                links[166]={"l":self.createLink10(w[17],w[24]), "fro":"18", "to":"25", "typ":"10"}
                links[167]={"l":self.createLink10(w[17],w[25]), "fro":"18", "to":"26", "typ":"10"}
                links[168]={"l":self.createLink10(w[17],w[26]), "fro":"18", "to":"27", "typ":"10"}
                links[169]={"l":self.createLink10(w[17],w[27]), "fro":"18", "to":"28", "typ":"10"}
                links[170]={"l":self.createLink10(w[18],w[24]), "fro":"19", "to":"25", "typ":"10"}
                links[171]={"l":self.createLink10(w[18],w[25]), "fro":"19", "to":"26", "typ":"10"}
                links[172]={"l":self.createLink10(w[18],w[26]), "fro":"19", "to":"27", "typ":"10"}
                links[173]={"l":self.createLink10(w[18],w[27]), "fro":"19", "to":"28", "typ":"10"}
                links[174]={"l":self.createLink10(w[19],w[24]), "fro":"20", "to":"25", "typ":"10"}
                links[175]={"l":self.createLink10(w[19],w[25]), "fro":"20", "to":"26", "typ":"10"}
                links[176]={"l":self.createLink10(w[19],w[26]), "fro":"20", "to":"27", "typ":"10"}
                links[177]={"l":self.createLink10(w[19],w[27]), "fro":"20", "to":"28", "typ":"10"}
              
                for i in range(28):
                        sw.append(self.createSwitch(w[i]))
                        self.createText(w[i],self.switches[i])

                for i in range(18):
                        ho.append(self.createHost(v[i],i))
                        self.createText(v[i],self.hosts[i])
                
		self.canvas.create_line(1,640,870,640, fill="light slate gray")
                self.createSwitch([35,663])
                self.canvas.create_text(77,663,text='Enabled', fill="black")
                sleepSw = self.createSwitch([123,663])
                self.sleep_sw(sleepSw)
                self.canvas.create_text(155,663,text='Sleep', fill="dim gray")
                alrSw = self.createSwitch([190,663])
                self.alr_sw(alrSw)
                self.canvas.create_text(218,663,text='ALR', fill="dark goldenrod")
                sustSw = self.createSwitch([250,663])
                self.sust_s_sw(sustSw)
                self.canvas.create_text(298,663,text='SustNMS-S', fill="deep sky blue")
                perfSw = self.createSwitch([353,663])
                self.sust_p_sw(perfSw)
                self.canvas.create_text(403,663,text='SustNMS-P', fill="royal blue")
                sustAlrSw = self.createSwitch([453,663])
                self.sust_s_alr_sw(sustAlrSw)
                self.canvas.create_text(519,663,text='SustNMS-S+ALR', fill="lime green")
                perfAlrSw = self.createSwitch([584,663])
                self.sust_p_alr_sw(perfAlrSw)
                self.canvas.create_text(652,663,text='SustNMS-P+ALR', fill="forest green")
                sscSw = self.createSwitch([720,663])
                self.ssc_sw(sscSw)
                self.canvas.create_text(750,663,text='SC', fill="dark orange")
                sscAlrSw = self.createSwitch([787,663])
                self.ssc_alr_sw(sscAlrSw)
                self.canvas.create_text(840,663,text='SC+ALR', fill="orange red")

    	'''
    	Methods to support the creation of widgets
    	'''
        def createLinkSwH(self,sw,h):
                    l = self.canvas.create_line(sw,h, fill="brown", width=2)
                    return l
    
        def createLink30(self,sw1,sw2):
                    l = self.canvas.create_line(sw1[0],sw1[1]-5,sw2[0],sw2[1]-5, fill="gray", width=2)
                    return l
        
        def createLink10(self,sw1,sw2):
            if (sw1[0] == sw2[0]):
                l = self.canvas.create_line(sw1[0]+5,sw1[1]+5,sw2[0]+5,sw2[1]+5, fill="gray", width=2, dash=(6,3))
            else:
                l = self.canvas.create_line(sw1[0],sw1[1]+5,sw2[0],sw2[1]+5, fill="gray", width=2, dash=(6,3))
            return l
    
        def createSwitch(self,sw):
                    #sw = self.canvas.create_rectangle(sw[0]-s,sw[1]-s+3,sw[0]+s,sw[1]+s-3, fill="ivory", outline="slate gray")
                    sw = self.canvas.create_rectangle(sw[0]-s,sw[1]-s+3,sw[0]+s,sw[1]+s-3, fill="ivory", outline="slate gray")
		    return sw
    
        def createHost(self,host,numHost):
            if numHost == 1 or numHost == 5 or numHost == 9 or numHost == 13:
                ho = self.canvas.create_rectangle(host[0]-s-17,host[1]-s+3,host[0]+s+17,host[1]+s-3, fill="brown4", outline="slate gray")
            elif numHost == 2 or numHost == 6 or numHost == 10 or numHost == 14:
                ho = self.canvas.create_rectangle(host[0]-s-17,host[1]-s+3,host[0]+s+17,host[1]+s-3, fill="dark olive green", outline="slate gray")
            elif numHost == 3 or numHost == 4 or numHost == 7 or numHost == 8 or numHost == 11 or numHost == 12 or numHost == 15 or numHost == 16:
                ho = self.canvas.create_rectangle(host[0]-s-17,host[1]-s+3,host[0]+s+17,host[1]+s-3, fill="light green", outline="slate gray")               
            else:    
                ho = self.canvas.create_rectangle(host[0]-s-17,host[1]-s+3,host[0]+s+17,host[1]+s-3, fill="azure", outline="slate gray")
    		return ho
    		
    		
        def createText(self,coord,tex):
                self.canvas.create_text(coord[0],coord[1], text=tex)
    
        def change_link(self,link):
                self.canvas.itemconfig(link, fill="black")
    
        def enable_sw(self,swi):
                self.canvas.itemconfig(swi, fill="ivory", outline="slate gray")
    
        def sleep_sw(self,swi):
                self.canvas.itemconfig(swi, fill="gray", outline="black")
    
        def alr_sw(self,swi):
                self.canvas.itemconfig(swi, fill="yellow", outline="black")
    
        def sust_s_sw(self,swi):
                self.canvas.itemconfig(swi, fill="deep sky blue", outline="black")
    
        def sust_p_sw(self,swi):
                self.canvas.itemconfig(swi, fill="royal blue", outline="black")
    
        def sust_s_alr_sw(self,swi):
                self.canvas.itemconfig(swi, fill="chartreuse", outline="black")
    
        def sust_p_alr_sw(self,swi):
                self.canvas.itemconfig(swi, fill="forest green", outline="black")
    
        def ssc_sw(self,swi):
                self.canvas.itemconfig(swi, fill="dark orange", outline="black")
    
        def ssc_alr_sw(self,swi):
                self.canvas.itemconfig(swi, fill="orange red", outline="black")
   
        def use_host(self, h):
        	self.canvas.itemconfig(h,fill="wheat", outline="black")
        
        def idle_host(self,h):
        	self.canvas.itemconfig(h,fill="azure", outline="slate gray")
        
        def use_link(self,l):	
        	self.canvas.itemconfig(l,fill="red")
        
        def use_link_low_workload(self,l):
                self.canvas.itemconfig(l,fill="pink")        
        
        def idle_link(self,l):
        		self.canvas.itemconfig(l,fill="gray")	

def launch():
	return GraphicInterface()
	
