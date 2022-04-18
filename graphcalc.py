import directpythonplatform as dp
import utility
import numpy as np
import parser
import math
from math import sin, cos,tan
import argparse
class dppgraph:
    def __init__(self,dimensions,bounds=((-10,10), (-10,10))):
       
        # This represents our current area of focus i.e. X=-10,10 Y=-10,10
        self.bg = dp.VBuffer(dimensions) 
        self.bounds=bounds
        self.dimensions=dimensions

        self.linecolor=0xFF0000
        self.gridcolor=0x111111
        self.bgcolor=0xFFFFFF
        self.window=dp.Window(self.bg)
        self.windowopen=False
        self.cont=True

    def draw(self, graphee, bounds):
        self.bg.fill(self.bgcolor)
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
        graphed.xtble=xpts
        evaluated=np.empty(xpts.size)
        for i,eachpt in enumerate(xpts):
            x=eachpt
            evaluated[i]=eval(graphed.func)

        graphed.ytble=evaluated
        
        vlinecount=self.bounds[0][1]-self.bounds[0][0]
        pixels_per_x=self.dimensions[0]//vlinecount
        
        unitrate=1/pixels_per_x # smallest unit one pixel on the y can represent
        #to get pixel representation: divide Y-lowerbound by unitrate
        for i,each in enumerate(evaluated):
            if(i==0):continue

            calc_pixel=(each-self.bounds[1][0])//unitrate
            calc_pixel_bef=(evaluated[i-1]-self.bounds[1][0])//unitrate
            if(calc_pixel<=self.dimensions[1] and calc_pixel>0):
                if self.cont:
                    try:
                        utility.draw_line(vb, [i, self.dimensions[1]-int(round(calc_pixel)) ],[i-1, self.dimensions[1]-int(round(calc_pixel_bef))], self.linecolor)
                    except:
                        pass
                else:
                    vb.write_pixel([i,self.dimensions[1]-int(round(calc_pixel))],self.linecolor)

            
    def drawGrid(self, vb):
        x0,x1=0, self.dimensions[0]-1
        y0,y1=0,self.dimensions[1]-1
        xhalf, yhalf= x1//2, y1//2
        
        vlinecount=self.bounds[0][1]-self.bounds[0][0]
        hlinecount=self.bounds[1][1]-self.bounds[1][0]
        

        for i in range(x0,self.dimensions[0], self.dimensions[0]//vlinecount):
            utility.draw_line(vb, [i,y0],[i,y1], self.gridcolor) # Vertical
 
        for i in range(y0,self.dimensions[1], self.dimensions[1]//hlinecount):
            utility.draw_line(vb, [x0,i], [x1,i],self.gridcolor) # horizontal
        
         
        
        # y=0,x=0
        utility.draw_line(vb, [xhalf,y0],[xhalf,y1], self.gridcolor) # Vertical
        utility.draw_line(vb, [x0,yhalf], [x1,yhalf],self.gridcolor) # horizontal


class dppgraphee:
    def __init__(self, function):
        self.func = parser.expr(function).compile()
        self.xtble=None
        self.ytble=None
        pass





def main():
    parser=argparse.ArgumentParser(description='Direct Python Platform graphing utility. Graphs a given function specified from command line arguments')
    parser.add_argument('--function=', dest= 'func', metavar='func', type=str, default="x**2", help='Python parseable expression in terms of x. Supports sin, cos, and tan')
    parser.add_argument('--bounds=', dest='bounds',metavar='x0 x1 y0 y1', default="-10 10 -10 10",type=str,help='Mathematical bounds for the graph')
    parser.add_argument('--graph=', dest='go', metavar= 'graph', action='store_const', const=True, help='Graph the given function within --function')
    parser.add_argument('--dimensions=', dest='dims', metavar='l by w', type=str, default='800 800', help='Dimensions for specifiying the window in terms of pixels.')
    parser.add_argument('--darkmode=', dest='darkmode', metavar='Darkmode', action='store_const', const=True, help='In dark mode, graphed function is green, background is black, and grid is white')
    parser.add_argument('--outputtable', dest='table', action='store_const', const=True, help='Outputs a table of values in stdout: x0...x1')
    parser.add_argument('--points', dest='points', action='store_const', const=True, help='For functions with rapid changes in direction, it may help to show graph as points instead of continuous lines.')

    args=parser.parse_args()
    if(args.go):
        graph(args)



def graph(args):
    if(len(args.dims.split())>2): return
    else:
        dimensions = [int(each) for each in args.dims.split()]
    
    calc = dppgraph(dimensions)
    graphed=dppgraphee(args.func)
    calc.bounds=[int(each) for each in args.bounds.split()]
    calc.bounds= (calc.bounds[0:2], calc.bounds[2:4])

    print(calc.bounds)
    if(args.darkmode):
        calc.linecolor=0x00FF00
        calc.bgcolor=0x000000
        calc.gridcolor=0x4F4F4F
    
    if(args.points):
        calc.cont=False

    calc.draw(graphed, calc.bounds)
    while calc.window.is_open():
        if 'q' in calc.window.eventq:
            if(args.table):
                print("X        Y")
                print("----------")
                string="{x:.4f} {y:.4f}"
                for i,each in enumerate(graphed.xtble):
                    print(string.format(x=each, y=graphed.ytble[i]))
            calc.window.close()
if __name__=='__main__':
    main()