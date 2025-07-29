import tkinter as tk
from tkinter import colorchooser, simpledialog, filedialog, messagebox

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python 画板 (256×256)")
        
        # 设置默认值
        self.pen_color = "black"
        self.pen_size = 1
        self.eraser_on = False
        self.prev_point = None
        self.drawn_points = []
        self.save_interval = 2
        self.coord_label = None  # 用于显示坐标的标签
        
        # 创建画布 (256×256)
        self.canvas = tk.Canvas(root, bg="white", width=256, height=256)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # 创建坐标显示标签
        self.coord_display = tk.Label(root, text="坐标: (0, 0)", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.coord_display.pack(fill=tk.X)
        
        # 创建工具栏框架
        self.toolbar = tk.Frame(root)
        self.toolbar.pack(fill=tk.X)
        
        # 添加工具按钮
        
        self.interval_btn = tk.Button(self.toolbar, text="设置保存间隔", command=self.set_save_interval)
        self.interval_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.clear_btn = tk.Button(self.toolbar, text="清空画布", command=self.clear_canvas)
        self.clear_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.save_btn = tk.Button(self.toolbar, text="保存坐标", command=self.save_coordinates)
        self.save_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # 绑定鼠标事件
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.reset_prev_point)
        self.canvas.bind("<Motion>", self.show_coordinates)  # 鼠标移动时显示坐标
    
    def show_coordinates(self, event):
        """实时显示鼠标坐标"""
        x, y = event.x, event.y
        # 确保坐标在画布范围内
        x = max(0, min(x, 255))
        y = max(0, min(y, 255))
        self.coord_display.config(text=f"坐标: ({x}, {y})")


    
    def set_save_interval(self):
        interval = simpledialog.askinteger("保存间隔", "每隔多少个点保存一个(1-100):", 
                                         parent=self.root, minvalue=1, maxvalue=100)
        if interval:
            self.save_interval = interval
            messagebox.showinfo("设置成功", f"已设置为每 {self.save_interval} 个点保存一个")
    
    
    def clear_canvas(self):
        self.canvas.delete("all")
        self.drawn_points = []
    
    def draw(self, event):
        current_point = (event.x, event.y)
        self.drawn_points.append(current_point)
        
        if self.prev_point:
            x1, y1 = self.prev_point
            x2, y2 = current_point
            self.canvas.create_line(x1, y1, x2, y2, 
                                   width=self.pen_size, 
                                   fill=self.pen_color,
                                   capstyle=tk.ROUND, 
                                   smooth=tk.TRUE)
        self.prev_point = current_point
    
    def reset_prev_point(self, event):
        self.prev_point = None
    
    def save_coordinates(self):
        if not self.drawn_points:
            messagebox.showwarning("警告", "没有可保存的坐标点！")
            return
        
        sampled_points = self.drawn_points[::self.save_interval]
        x_coords = [str(point[0]) for point in sampled_points]
        y_coords = [str(point[1]) for point in sampled_points]
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")],
            title="保存坐标点"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(f"Canvas Size: 256×256\n")
                    f.write(f"Save Interval: 每 {self.save_interval} 个点保存一个\n")
                    f.write(f"Original Points: {len(self.drawn_points)}\n")
                    f.write(f"Saved Points: {len(sampled_points)}\n\n")
                    
                    f.write("x_coords = [\n")
                    f.write(",".join(x_coords) + "\n")
                    f.write("]\n\n")
                    
                    f.write("y_coords = [\n")
                    f.write( ",".join(y_coords) + "\n")
                    f.write("]\n")
                
                messagebox.showinfo("成功", f"坐标点已保存到:\n{file_path}\n"
                                  f"原始点数: {len(self.drawn_points)}\n"
                                  f"保存点数: {len(sampled_points)}")
            except Exception as e:
                messagebox.showerror("错误", f"保存文件时出错:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()