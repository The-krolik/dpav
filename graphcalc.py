import directpythonplatform as dp
import utility
import numpy as np
import parser
import math
from math import sin, cos,tan
class dppgraph:
    def __init__(self,dimensions,bounds=((-10,10), (-10,10))):
       
        # This represents our current area of focus i.e. X=-10,10 Y=-10,10
        self.bg = dp.VBuffer(dimensions) 
        self.bounds=bounds
        self.dimensions=dimensions

        self.linecolor=None
        self.gridcolor=None
        self.bgcolor=None
        self.window=dp.Window(self.bg)
        self.windowopen=False

    def draw(self, graphee, bounds):
        self.bg.fill(0xFFFFFF)
        self.drawGrid(self.bg)
        self.drawFunc(self.bg , graphee)
        if(self.windowopen):
            self.window.write_to_screen()
        else:
            self.window.open()
            self.windowopen=True
        pass
    
    def drawFunc(self, vb, graphed):
        xpts=np.linspace(self.bounds[0][0], self.bounds[0][1], self.dimensions[1])
        evaluated=np.empty(xpts.size)

        for i,eachpt in enumerate(xpts):
            x=eachpt
            evaluated[i]=eval(graphed.func)

        vlinecount=self.bounds[0][1]-self.bounds[0][0]
        pixels_per_x=self.dimensions[0]//vlinecount
        
        unitrate=1/pixels_per_x # smallest unit one pixel on the y can represent
        #to get pixel representation: divide Y-lowerbound by unitrate
        for i,each in enumerate(evaluated):
            calc_pixel=(each-self.bounds[1][0])//unitrate
            if(calc_pixel<=self.dimensions[1]):
                vb.write_pixel([i,self.dimensions[1]-int(round(calc_pixel))], 0xFF0000) 

            
    def drawGrid(self, vb):
        x0,x1=0, self.dimensions[0]-1
        y0,y1=0,self.dimensions[1]-1
        xhalf, yhalf= x1//2, y1//2
        
        vlinecount=self.bounds[0][1]-self.bounds[0][0]
        hlinecount=self.bounds[1][1]-self.bounds[1][0]
        

        for i in range(x0,self.dimensions[0], self.dimensions[0]//vlinecount):
            utility.draw_line(vb, [i,y0],[i,y1], 0x000000) # Vertical
 
        for i in range(y0,self.dimensions[1], self.dimensions[1]//hlinecount):
            utility.draw_line(vb, [x0,i], [x1,i],0x000000) # horizontal
        
         
        
        # y=0,x=0
        utility.draw_line(vb, [xhalf,y0],[xhalf,y1], 0x000000) # Vertical
        utility.draw_line(vb, [x0,yhalf], [x1,yhalf],0x000000) # horizontal

class dppgraphmenu:
    def __init__(self, dppgraph):
        print("Welcome to the Direct Python Platform Graphing Calculator")
        print("Use these options to navigate: (q) to quit, (f) to enter a function, (o) for color options")

    def print_menu(self):
        print("Welcome to the Direct Python Platform Graphing Calculator")
        print("Use these options to navigate: (q) to quit, (f) to enter a function, (o) for color options")

    def change_color(self,dppgraph):
        pass

class dppgraphee:
    def __init__(self, function):
        self.func = parser.expr(function).compile()
        print(function)
        pass





def main():
    dimensions = (600, 600)
    calc = dppgraph(dimensions)
    graphed=dppgraphee("x**2 -1")

    menu=dppgraphmenu(calc)
    calc.draw(graphed, calc.bounds)
    while calc.window.isOpen:

        pass

if __name__ == "__main__":
    main()
