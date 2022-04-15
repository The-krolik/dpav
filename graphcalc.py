import directpythonplatform as dp
import utility

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

    # THis will 
    def draw(self):
        self.bg.fill(0xFFFFFF)
        self.bg=self.drawGrid(self.bg)
        self.window.open()
        pass

    def drawGrid(self, vb):
        x0,x1=0, self.dimensions[0]-1
        y0,y1=0,self.dimensions[1]-1
        xhalf, yhalf= x1//2, y1//2
        
        vlinecount=self.bounds[0][1]-self.bounds[0][0]
        hlinecount=self.bounds[1][1]-self.bounds[1][0]
        print(vlinecount, hlinecount)
        for i in range(x0,self.dimensions[0], vlinecount):
            utility.draw_line(vb, [i,y0],[i,y1], 0x000000) # Vertical
 
        for i in range(x0,self.dimensions[1], hlinecount):
            utility.draw_line(vb, [x0,i], [x1,i],0x000000) # horizontal
  

        # y=0,x=0
        print(x0,x1)
        utility.draw_line(vb, [xhalf,y0],[xhalf,y1], 0x000000) # Vertical
        utility.draw_line(vb, [x0,yhalf], [x1,yhalf],0x000000) # horizontal

class dppgraphee:
    def __init__(self, function, interval):
        pass





def main():
    dimensions = (600, 600)
    calc = dppgraph(dimensions)
    calc.draw()
    while calc.window.isOpen:

        pass

if __name__ == "__main__":
    main()
