from Tkinter import * 
from ttk import Frame, Button, Style
from collections import defaultdict

links = [] #the ids for the links in canvas
sw = []
ho = []
flows = []
paintlink = defaultdict(lambda:defaultdict(lambda:None))

'''
Main GUI. We do not detach (yet) it from the controller code. We are working on the use of sockets to send/receive all infos from controller.
'''
class GraphicInterface(Frame):
        
        global s, v, w, links, sw, ho
        #coordinates of the hosts
        #v=[[623,38], [643,83], [133,493], [283,493], [38,133], [38,283], [653,413], [638,463]]
        #coordinates of the switches
        #w=[[458,53], [583,153], [583,223], [708,258], [583,293], [708,328], [583,363], [453,398], [333,313], [208,363], [303,403], [208,443], [113,403], [373,188], [83,208], [208,173], [708,188]]
        #size of circle and rectangle
	#383,73
	v=[[383,73], [483,73], [133,493], [283,493], [198,110], [136,150], [633,393], [533,393], [136,200], [198,240]]
        #coordinates of the switches
	#433,123
        w=[[413,113], [583,123], [583,188], [708,238], [583,273], [708,308], [583,343], [473,343], [373,343], [208,363], [303,403], [208,443], [113,403], [433,188], [198,188], [293,188], [708,158]]	
        s = 30
        s/=2
	#
        c1=0
        s1=0
	#
	time=None
	#
	flag=True #to control the painting of functionalities
	#
        def __init__(self, master=None):

                # create main frame
                master = Tk()
                Frame.__init__(self, master)
                self.master.title("Topology")
                self.master.style = Style()

                # configure the geometry
                self.grid(padx = 10, pady = 10)
		
                # call the funtions
               	self.createWidgets()			
		self.paint_topo()
		
	def paint_topo(self):
		global paintlink
		for src,dict in paintlink.iteritems():
			for dst, workload in dict.iteritems():					
				for pos, l in enumerate(links):
					if workload < 1:	
						if src == int(l["fro"][1:]) and dst == int(l["to"][1:]):							
							self.idle_link(l["l"])
					if workload >=1 and workload <= 10.0:
						if src == int(l["fro"][1:]) and dst == int(l["to"][1:]) and str(l["typ"]) == "ss10":
							self.use_link(l["l"])
					else:
						if src == int(l["fro"][1:]) and dst == int(l["to"][1:]) and str(l["typ"]) == "ss30":
							self.use_link(l["l"])
		self.after(500,self.paint_topo)

	'''
	All the widgets on GUI
	'''
        def createWidgets(self):

                #self.hosts = ["Source 1","Source 2","Sink 3","Sink 4","Source 5","Source 6","Sink 7","Sink 8"]
		self.hosts = ["Source 1","Source 2","Sink 3","Sink 4","Source 5","Source 6","Sink 7","Sink 8", "Source 9", "Source 10"]
                self.switches = ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11", "s12", "s13", "s14", "s15", "s16", "s17"]
		self.canvas = Canvas(self,width=870, height=580)
                self.canvas.grid(row=0, column=0, padx = 10)
                self.canvas.create_rectangle(1, 1, 870, 560, fill="white")
                self.canvas.create_rectangle(730,20,840,90, outline="light slate gray")
                self.canvas.create_line(750,35,760,35, fill="gray")
                self.canvas.create_text(810,35, text="30Mbps", fill="navy")
                self.canvas.create_line(750,55,760,55, fill="gray", dash=(6,3))
                self.canvas.create_text(810,55, text="10Mbps", fill="navy")
                self.canvas.create_line(750,75,760,75, fill="brown")
                self.canvas.create_text(810,75, text="X Mbps", fill="navy")
		self.canvas.create_rectangle(20,15, 80, 45, fill="white") 
		self.time = self.canvas.create_text(50, 30, text="hh:mm", fill="black", tag="time")
		

                for i in range(52):
                        links.append({})

                links[0]={"l":self.createLinkSwH(w[0],v[0]), "fro":"s1", "to":"h1", "typ":"sh"}
                links[1]={"l":self.createLinkSwH(w[0],v[1]), "fro":"s1", "to":"h2", "typ":"sh"}
                links[2]={"l":self.createLinkSwH(w[11],v[2]), "fro":"s12", "to":"h3", "typ":"sh"}
                links[3]={"l":self.createLinkSwH(w[11],v[3]), "fro":"s12", "to":"h4", "typ":"sh"}
                links[4]={"l":self.createLinkSwH(w[14],v[4]), "fro":"s15", "to":"h5", "typ":"sh"}
                links[5]={"l":self.createLinkSwH(w[14],v[5]), "fro":"s15", "to":"h6", "typ":"sh"}
		links[50]={"l":self.createLinkSwH(w[14],v[8]), "fro":"s15", "to":"h9", "typ":"sh"}
		links[51]={"l":self.createLinkSwH(w[14],v[9]), "fro":"s15", "to":"h10", "typ":"sh"}		
                links[6]={"l":self.createLinkSwH(w[6],v[6]), "fro":"s7", "to":"h7", "typ":"sh"}
                links[7]={"l":self.createLinkSwH(w[6],v[7]), "fro":"s7", "to":"h8", "typ":"sh"}

                links[8]={"l":self.createLink30(w[0],w[1]), "fro":"s1", "to":"s2", "typ":"ss30"}
                links[9]={"l":self.createLink10(w[0],w[1]), "fro":"s1", "to":"s2", "typ":"ss10"}
                links[10]={"l":self.createLink30(w[0],w[13]), "fro":"s1", "to":"s14", "typ":"ss30"}
                links[11]={"l":self.createLink10(w[0],w[13]), "fro":"s1", "to":"s14", "typ":"ss10"}
                links[12]={"l":self.createLink30(w[0],w[15]), "fro":"s1", "to":"s16", "typ":"ss30"}
                links[13]={"l":self.createLink10(w[0],w[15]), "fro":"s1", "to":"s16", "typ":"ss10"}
                links[14]={"l":self.createLink30(w[1],w[16]), "fro":"s2", "to":"s17", "typ":"ss30"}
                links[15]={"l":self.createLink10(w[1],w[16]), "fro":"s2", "to":"s17", "typ":"ss10"}
                links[16]={"l":self.createLink30(w[16],w[2]), "fro":"s17", "to":"s3", "typ":"ss30"}
                links[17]={"l":self.createLink10(w[16],w[2]), "fro":"s17", "to":"s3", "typ":"ss10"}
                links[18]={"l":self.createLink30(w[2],w[3]), "fro":"s3", "to":"s4", "typ":"ss30"}
                links[19]={"l":self.createLink10(w[2],w[3]), "fro":"s3", "to":"s4", "typ":"ss10"}
                links[20]={"l":self.createLink30(w[3],w[4]), "fro":"s4", "to":"s5", "typ":"ss30"}
                links[21]={"l":self.createLink10(w[3],w[4]), "fro":"s4", "to":"s5", "typ":"ss10"}
                links[22]={"l":self.createLink30(w[4],w[5]), "fro":"s5", "to":"s6", "typ":"ss30"}
                links[23]={"l":self.createLink10(w[4],w[5]), "fro":"s5", "to":"s6", "typ":"ss10"}
                links[24]={"l":self.createLink30(w[5],w[6]), "fro":"s6", "to":"s7", "typ":"ss30"}
                links[25]={"l":self.createLink10(w[5],w[6]), "fro":"s6", "to":"s7", "typ":"ss10"}
                links[26]={"l":self.createLink30(w[6],w[13]), "fro":"s7", "to":"s14", "typ":"ss30"}
                links[27]={"l":self.createLink10(w[6],w[13]), "fro":"s7", "to":"s14", "typ":"ss10"}
                links[28]={"l":self.createLink30(w[6],w[7]), "fro":"s7", "to":"s8", "typ":"ss30"}
                links[29]={"l":self.createLink10(w[6],w[7]), "fro":"s7", "to":"s8", "typ":"ss10"}
                links[30]={"l":self.createLink30(w[7],w[8]), "fro":"s8", "to":"s9", "typ":"ss30"}
                links[31]={"l":self.createLink10(w[7],w[8]), "fro":"s8", "to":"s9", "typ":"ss10"}
                links[32]={"l":self.createLink30(w[8],w[9]), "fro":"s9", "to":"s10", "typ":"ss30"}
                links[33]={"l":self.createLink10(w[8],w[9]), "fro":"s9", "to":"s10", "typ":"ss10"}
                links[34]={"l":self.createLink30(w[8],w[15]), "fro":"s9", "to":"s16", "typ":"ss30"}
                links[35]={"l":self.createLink10(w[8],w[15]), "fro":"s9", "to":"s16", "typ":"ss10"}
                links[36]={"l":self.createLink30(w[9],w[10]), "fro":"s10", "to":"s11", "typ":"ss30"}
                links[37]={"l":self.createLink10(w[9],w[10]), "fro":"s10", "to":"s11", "typ":"ss10"}
                links[38]={"l":self.createLink30(w[9],w[12]), "fro":"s10", "to":"s13", "typ":"ss30"}
                links[39]={"l":self.createLink10(w[9],w[12]), "fro":"s10", "to":"s13", "typ":"ss10"}
                links[40]={"l":self.createLink30(w[9],w[13]), "fro":"s10", "to":"s14", "typ":"ss30"}
                links[41]={"l":self.createLink10(w[9],w[13]), "fro":"s10", "to":"s14", "typ":"ss10"}
                links[42]={"l":self.createLink30(w[10],w[11]), "fro":"s11", "to":"s12", "typ":"ss30"}
                links[43]={"l":self.createLink10(w[10],w[11]), "fro":"s11", "to":"s12", "typ":"ss10"}
                links[44]={"l":self.createLink30(w[11],w[12]), "fro":"s12", "to":"s13", "typ":"ss30"}
                links[45]={"l":self.createLink10(w[11],w[12]), "fro":"s12", "to":"s13", "typ":"ss10"}
                links[46]={"l":self.createLink30(w[13],w[15]), "fro":"s14", "to":"s16", "typ":"ss30"}
                links[47]={"l":self.createLink10(w[13],w[15]), "fro":"s14", "to":"s16", "typ":"ss10"}
                links[48]={"l":self.createLink30(w[14],w[15]), "fro":"s15", "to":"s16", "typ":"ss30"}
                links[49]={"l":self.createLink10(w[14],w[15]), "fro":"s15", "to":"s16", "typ":"ss10"}
		
                for i in range(17):
                        sw.append(self.createSwitch(w[i]))
                        self.createText(w[i],self.switches[i])

                for i in range(10):
                        ho.append(self.createHost(v[i],i))
                        self.createText(v[i],self.hosts[i])
                
		self.canvas.create_line(1,520,870,520, fill="light slate gray")
                self.createSwitch([35,543])
                self.canvas.create_text(77,543,text='Enabled', fill="black")
                sleepSw = self.createSwitch([123,543])
                self.sleep_sw(sleepSw)
                self.canvas.create_text(155,543,text='Sleep', fill="dim gray")
                alrSw = self.createSwitch([190,543])
                self.alr_sw(alrSw)
                self.canvas.create_text(218,543,text='ALR', fill="dark goldenrod")
                sustSw = self.createSwitch([250,543])
                self.sust_s_sw(sustSw)
                self.canvas.create_text(298,543,text='SustNMS-S', fill="deep sky blue")
                perfSw = self.createSwitch([353,543])
                self.sust_p_sw(perfSw)
                self.canvas.create_text(403,543,text='SustNMS-P', fill="royal blue")
                sustAlrSw = self.createSwitch([453,543])
                self.sust_s_alr_sw(sustAlrSw)
                self.canvas.create_text(519,543,text='SustNMS-S+ALR', fill="lime green")
                perfAlrSw = self.createSwitch([584,543])
                self.sust_p_alr_sw(perfAlrSw)
                self.canvas.create_text(652,543,text='SustNMS-P+ALR', fill="forest green")
                sscSw = self.createSwitch([720,543])
                self.ssc_sw(sscSw)
                self.canvas.create_text(750,543,text='SC', fill="dark orange")
                sscAlrSw = self.createSwitch([787,543])
                self.ssc_alr_sw(sscAlrSw)
                self.canvas.create_text(840,543,text='SC+ALR', fill="orange red")
				
	'''
	Methods to support the creation of widgets
	'''
        def createLinkSwH(self,sw,h):
                l = self.canvas.create_line(sw,h, fill="brown", width=2)
                return l

        def createLink30(self,sw1,sw2):
                l = self.canvas.create_line(sw1[0],sw1[1]-3,sw2[0],sw2[1]-3, fill="gray", width=2)
                return l

        def createLink10(self,sw1,sw2):
                l = self.canvas.create_line(sw1[0],sw1[1]+3,sw2[0],sw2[1]+3, fill="gray", width=2, dash=(6,3))
                return l

        def createSwitch(self,sw):
                sw = self.canvas.create_rectangle(sw[0]-s,sw[1]-s+3,sw[0]+s,sw[1]+s-3, fill="ivory", outline="slate gray")
                return sw

        def createHost(self,host,numHost): 
		if numHost == 0 or numHost == 1 or numHost == 4 or numHost == 5 or numHost == 8 or numHost == 9: 
			ho = self.canvas.create_rectangle(host[0]-s-15,host[1]-s+4,host[0]+s+16,host[1]+s-3, fill="azure", outline="slate gray")
		else:	
			ho = self.canvas.create_rectangle(host[0]-s-5,host[1]-s+3,host[0]+s+5,host[1]+s-3, fill="azure", outline="slate gray")
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
	def idle_link(self,l):
		self.canvas.itemconfig(l,fill="gray")	

class Flow(object):
	src_host = ''
	dst_host = ''
	path = []
	workload = 0


def launch():
	return GraphicInterface()
