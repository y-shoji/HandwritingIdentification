import tkinter
import tkinter.ttk

class Application(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('tkinter canvas trial')
        self.pack()
        self.create_widgets()
        self.x =[]
        self.y = []
    def create_widgets(self):
        # canvas消去
        self.clear_button = tkinter.Button(self, text='canvas削除',width=15)
        self.clear_button.grid(row=0, column=1)
        self.clear_button.bind("<Button-1>", self.clear_canvas)
        # 保存処理
        self.save_button = tkinter.Button(self, text='canvas保存',width=15)
        self.save_button.grid(row=1, column=1)
        self.save_button.bind("<Button-1>", self.save_canvas)
        # 描画処理
        self.test_canvas = tkinter.Canvas(self, bg='ghostwhite', width=300, height=300, highlightthickness=0)
        self.test_canvas.grid(row=0, column=0, rowspan=7)
        self.test_canvas.bind('<ButtonPress-1>', self.start_pickup)
        self.test_canvas.bind('<B1-Motion>', self.pickup_position)
        self.test_canvas.bind('<ButtonRelease-1>', self.stop_pickup)

    def clear_canvas(self,event):
        self.test_canvas.delete('draw')
        # f.seek(0)
        # f.truncate()
        self.x =[]
        self.y = []

    def save_canvas(self,event):
        with open('test.txt','a') as f:
            for x,y in zip(self.x,self.y):
                if x == '' or y == '':
                    f.write('{},{}\n'.format(-1,-1))
                    break
                f.write('{},{}\n'.format(x,y))
        self.clear_canvas(event)
        self.x = []
        self.y = []


    def start_pickup(self, event):
        self.sx = event.x
        self.sy = event.y

    def pickup_position(self, event):
        # f.write('{},{}\n'.format(str(event.x),str(event.y)))
        self.x.append(int(event.x))
        self.y.append(int(event.y))
        self.test_canvas.create_line(self.sx, self.sy, event.x, event.y, width=5, tag='draw')
        self.sx = event.x
        self.sy = event.y

    def stop_pickup(self, event):
        self.x.append('')
        self.y.append('')
        
        # f.write('\n')

# f = open('test.txt','a')
root = tkinter.Tk()
app = Application(master=root)
app.mainloop()
# f.close()