import tkinter as tk
from tkinter import colorchooser, filedialog
from PIL import Image, ImageDraw

# Set up the main application window
root = tk.Tk()
root.title("Drawing Application")
root.geometry("900x700")

# Global variables
draw_color = "black"
brush_size = 5
current_tool = "pen"
undo_stack = []  # For Undo/Redo feature
canvas_width, canvas_height = 800, 600

# Canvas and image setup
canvas = tk.Canvas(root, bg="white", width=canvas_width, height=canvas_height)
canvas.pack()

# Create an image to draw on for saving
image = Image.new("RGB", (canvas_width, canvas_height), "white")
draw = ImageDraw.Draw(image)

# Functions
def change_color():
    global draw_color
    color = colorchooser.askcolor()[1]
    if color:
        draw_color = color

def change_brush_size(size):
    global brush_size
    brush_size = int(size)

def set_tool(tool):
    global current_tool
    current_tool = tool

def save():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_path:
        image.save(file_path)

def undo():
    if undo_stack:
        canvas.delete("all")
        undo_stack.pop()
        if undo_stack:
            canvas_image = undo_stack[-1]
            canvas.create_image(0, 0, image=canvas_image, anchor="nw")

# Draw and Erase on the canvas
def paint(event):
    x1, y1 = (event.x - brush_size), (event.y - brush_size)
    x2, y2 = (event.x + brush_size), (event.y + brush_size)
    
    if current_tool == "pen":
        canvas.create_oval(x1, y1, x2, y2, fill=draw_color, outline=draw_color)
        draw.ellipse([x1, y1, x2, y2], fill=draw_color)
    elif current_tool == "eraser":
        canvas.create_oval(x1, y1, x2, y2, fill="white", outline="white")
        draw.ellipse([x1, y1, x2, y2], fill="white")
    
    # Save canvas state for undo
    canvas_image = canvas.postscript(colormode="color")
    undo_stack.append(canvas_image)

# Shape tools
def draw_rectangle():
    set_tool("rectangle")

def draw_circle():
    set_tool("circle")

def draw_line():
    set_tool("line")

def on_click(event):
    global start_x, start_y
    start_x, start_y = event.x, event.y

def on_release(event):
    global current_tool
    end_x, end_y = event.x, event.y
    
    if current_tool == "rectangle":
        canvas.create_rectangle(start_x, start_y, end_x, end_y, outline=draw_color, width=brush_size)
        draw.rectangle([start_x, start_y, end_x, end_y], outline=draw_color, width=brush_size)
    elif current_tool == "circle":
        canvas.create_oval(start_x, start_y, end_x, end_y, outline=draw_color, width=brush_size)
        draw.ellipse([start_x, start_y, end_x, end_y], outline=draw_color, width=brush_size)
    elif current_tool == "line":
        canvas.create_line(start_x, start_y, end_x, end_y, fill=draw_color, width=brush_size)
        draw.line([start_x, start_y, end_x, end_y], fill=draw_color, width=brush_size)

# Bind paint function to the canvas
canvas.bind("<B1-Motion>", paint)
canvas.bind("<Button-1>", on_click)
canvas.bind("<ButtonRelease-1>", on_release)

# Toolbar for tools and color picker
toolbar = tk.Frame(root)
toolbar.pack()

# Buttons for tools
color_btn = tk.Button(toolbar, text="Pick Color", command=change_color)
color_btn.grid(row=0, column=0, padx=5, pady=5)

pen_btn = tk.Button(toolbar, text="Pen", command=lambda: set_tool("pen"))
pen_btn.grid(row=0, column=1, padx=5, pady=5)

eraser_btn = tk.Button(toolbar, text="Eraser", command=lambda: set_tool("eraser"))
eraser_btn.grid(row=0, column=2, padx=5, pady=5)

rectangle_btn = tk.Button(toolbar, text="Rectangle", command=draw_rectangle)
rectangle_btn.grid(row=0, column=3, padx=5, pady=5)

circle_btn = tk.Button(toolbar, text="Circle", command=draw_circle)
circle_btn.grid(row=0, column=4, padx=5, pady=5)

line_btn = tk.Button(toolbar, text="Line", command=draw_line)
line_btn.grid(row=0, column=5, padx=5, pady=5)

save_btn = tk.Button(toolbar, text="Save", command=save)
save_btn.grid(row=0, column=6, padx=5, pady=5)

undo_btn = tk.Button(toolbar, text="Undo", command=undo)
undo_btn.grid(row=0, column=7, padx=5, pady=5)

# Brush size slider
brush_slider = tk.Scale(toolbar, from_=1, to=20, orient=tk.HORIZONTAL, command=change_brush_size, label="Brush Size")
brush_slider.set(brush_size)
brush_slider.grid(row=0, column=8, padx=5, pady=5)

# Run the application
root.mainloop()
