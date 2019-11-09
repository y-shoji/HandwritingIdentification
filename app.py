import tkinter
import tkinter.ttk
import torch
import numpy as np
import torch.utils.data as data

from utils.predict import ImageTransform, Model, Plt_to_Pil
from utils.char_trans import Fourier, char_trans


class Application(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('tkinter canvas trial')
        self.pack()
        self.create_widgets()
        self.x, self.y = [], []
        self.net = Model('./weights_fine_tuning.pth')
        self.F_char = char_trans()
        self.transform = ImageTransform(resize=150,
            mean=(0.485, 0.456, 0.406),std=(0.229, 0.224, 0.225))
        self.labels = {0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',
                       6:'G',7:'H',8:'I',9:'J',10:'k'}

    def create_widgets(self):
        # canvas消去
        self.clear_button = tkinter.Button(self, text='canvas削除',width=15)
        self.clear_button.grid(row=0, column=1)
        self.clear_button.bind("<Button-1>", self.clear_canvas)
        # 保存処理
        self.save_button = tkinter.Button(self, text='canvas保存',width=15)
        self.save_button.grid(row=1, column=1)
        self.save_button.bind("<Button-1>", self.save_canvas)
        # 推論処理
        self.predict_button = tkinter.Button(self, text='canvas推論',width=15)
        self.predict_button.grid(row=2, column=1)
        self.predict_button.bind("<Button-1>", self.predict_canvas)

        self.predict_txt = tkinter.StringVar()
        self.predict_label = tkinter.ttk.Label(self, textvariable=self.predict_txt)
        self.predict_label.grid(row=3, column=1)

        # 終了処理
        self.close_button = tkinter.Button(self, text='終了',width=15)
        self.close_button.grid(row=5, column=1)
        self.close_button.bind("<Button-1>", self.close_window)

        # 描画処理
        self.test_canvas = tkinter.Canvas(self, bg='ghostwhite', width=300, height=300, highlightthickness=0)
        self.test_canvas.grid(row=0, column=0, rowspan=7)
        self.test_canvas.bind('<ButtonPress-1>', self.start_pickup)
        self.test_canvas.bind('<B1-Motion>', self.pickup_position)
        self.test_canvas.bind('<ButtonRelease-1>', self.stop_pickup)

    def clear_canvas(self,event):
        self.test_canvas.delete('draw')
        self.x =[]
        self.y = []

    def save_canvas(self,event):
        with open('test.txt','a') as f:
            for x,y in zip(self.x,self.y):
                if x == '' or y == '':
                    f.write('{},{}\n'.format(-1,-1))
                    break
                f.write('{},{}\n'.format(x,y))

    def predict_canvas(self,event):
        i,j = self.F_char.write_fourier_dot(X=self.x,Y=self.y)
        img = Plt_to_Pil(i,j)
        img_transformed = self.transform(img)
        valloader  = data.DataLoader([img_transformed,0])
        Input, _ = valloader
        with torch.no_grad():
            Output = self.net.call(Input)

        np_Output = Output.cpu().numpy()
        self.predict_txt.set(self.labels[np.argmax(np_Output)])


    def start_pickup(self, event):
        self.sx = event.x  
        self.sy = event.y

    def pickup_position(self, event):
        self.x.append(int(event.x))
        self.y.append(int(event.y))
        self.test_canvas.create_line(self.sx, self.sy, event.x, event.y, width=5, tag='draw')
        self.sx = event.x
        self.sy = event.y

    def stop_pickup(self, event):
        self.x.append('')
        self.y.append('')
    

    def close_window(self,event):
        self.master.quit()

root = tkinter.Tk()
app = Application(master=root)
app.mainloop()