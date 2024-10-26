import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageOps, ImageTk

class FotoCarnetApp:
    def __init__(self, root):
        # Configuración de la ventana
        self.root = root
        self.root.title("Generador de Fotos Carnet")
        self.root.geometry("400x600")  # Aumentar altura para más espacio
        self.root.configure(bg='lightblue')  # Cambiar color de fondo

        # Crear un menú
        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)

        # Añadir un menú "Ayuda"
        ayuda_menu = tk.Menu(self.menu_bar, tearoff=0)
        ayuda_menu.add_command(label="Instrucciones", command=self.mostrar_instrucciones)
        self.menu_bar.add_cascade(label="Ayuda", menu=ayuda_menu)

        # Añadir un menú "Contacto"
        contacto_menu = tk.Menu(self.menu_bar, tearoff=0)
        contacto_menu.add_command(label="Enviar Email", command=self.mostrar_contacto)
        self.menu_bar.add_cascade(label="Contacto", menu=contacto_menu)

        # Variables de configuración de la imagen
        self.dpi = 300
        self.lado_cm = 4
        self.lado_px = int(self.dpi * self.lado_cm / 2.54)  # Convertir a píxeles
        self.borde = 2
        self.listones = []  # Almacena los listones de fotos

        # Etiqueta de instrucciones
        self.instrucciones_label = tk.Label(root, text="Cargue hasta 7 imágenes para generar fotos carnet.", wraplength=300, bg='lightblue')
        self.instrucciones_label.pack(pady=10)

        # Etiqueta informativa sobre el estado del proceso
        self.estado_label = tk.Label(root, text="", bg='lightblue')
        self.estado_label.pack(pady=5)

        # Botón para cargar la imagen
        self.boton_cargar = ttk.Button(root, text="Cargar Imágenes", command=self.cargar_imagenes)
        self.boton_cargar.pack(pady=10)

        # Botón para cerrar la aplicación
        self.boton_cerrar = ttk.Button(root, text="Cerrar", command=root.quit)
        self.boton_cerrar.pack(pady=5)

        # Label para mostrar el resultado
        self.etiqueta_imagen = tk.Label(root)
        self.etiqueta_imagen.pack(pady=10)

        # Mensaje de resultado
        self.resultado_label = tk.Label(root, text="", bg='lightblue')
        self.resultado_label.pack()

        # Etiqueta "by Mrk" al final
        self.credito_label = tk.Label(root, text="by Mrk", bg='lightblue', font=("Arial", 10))
        self.credito_label.pack(side=tk.BOTTOM, pady=10)

    def mostrar_instrucciones(self):
        instrucciones = (
            "Instrucciones:\n\n"
            "1. Haga clic en 'Cargar Imágenes' para seleccionar hasta 5 fotos.\n"
            "2. Las fotos deben ser en formato JPG, JPEG, PNG o BMP.\n"
            "3. Las fotos se ajustarán a un tamaño de 4x4 cm con un borde blanco.\n"
            "4. La hoja resultante se guardará como PNG y PDF.\n"
            "5. Haga clic en 'Cerrar' para salir."
        )
        messagebox.showinfo("Instrucciones", instrucciones)

    def mostrar_contacto(self):
        contacto_info = "Para consultas, envíame un correo a:\n\nmglibertini@gmail.com"
        messagebox.showinfo("Contacto", contacto_info)

    def cargar_imagenes(self):
        # Abrir cuadro de diálogo para seleccionar múltiples imágenes
        rutas_imagenes = filedialog.askopenfilenames(
            filetypes=[("Archivos de imagen", "*.jpg *.jpeg *.png *.bmp")]
        )
        
        if not rutas_imagenes:
            return
        
        if len(rutas_imagenes) > 7:
            messagebox.showwarning("Advertencia", "Por favor, seleccione hasta 7 imágenes.")
            return
        
        # Crear una lista de imágenes cargadas y actualizar el estado
        self.estado_label.config(text="Cargando imágenes...")
        
        try:
            self.fotos_originales = [Image.open(ruta) for ruta in rutas_imagenes]
        
            if any(foto.size[0] < (self.lado_px - (self.borde * 2)) for foto in self.fotos_originales):
                messagebox.showwarning("Advertencia", "Una o más imágenes son demasiado pequeñas.")
                return
            
            self.generar_hoja()
        
            # Actualizar el estado al finalizar el proceso
            self.estado_label.config(text="Proceso completado.")
        
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al cargar las imágenes: {e}")
            self.estado_label.config(text="Error al cargar imágenes.")

    def generar_hoja(self):
        # Crear listones con las imágenes cargadas
        for foto_original in self.fotos_originales:
            lado_sin_borde = self.lado_px - (self.borde * 2)  # Ajustar tamaño sin borde
            foto_cuadrada = ImageOps.fit(foto_original, (lado_sin_borde, lado_sin_borde), Image.LANCZOS)
            foto_con_borde = ImageOps.expand(foto_cuadrada, border=self.borde, fill="white")

            liston_ancho = self.lado_px * 5 + self.borde * 10
            liston_alto = self.lado_px + 2 * self.borde  
            liston = Image.new("RGB", (liston_ancho, liston_alto), "white")
            
            for i in range(5):
                liston.paste(foto_con_borde, (i * (self.lado_px + self.borde * 2), 0))
            self.listones.append(liston)

            a4_ancho = int(21 * self.dpi / 2.54)
            a4_alto = int(29.7 * self.dpi / 2.54)
            
        # Actualizar el estado antes de crear la hoja A4
        self.estado_label.config(text="Generando hoja A4...")
        
        hoja_a4 = Image.new("RGB", (a4_ancho, a4_alto), "white")
            
        offset_x = (a4_ancho - liston_ancho) // 2  

        y_offset = 100  
        
        for liston in self.listones:
            if y_offset + liston.size[1] > a4_alto:
                break  
            hoja_a4.paste(liston, (offset_x, y_offset))
            y_offset += liston.size[1] + 10  

        hoja_a4.save("fotos_carnet_a4.png")
        hoja_a4.save("fotos_carnet_a4.pdf", "PDF", resolution=self.dpi)

        imagen_miniatura = hoja_a4.resize((int(a4_ancho / 12), int(a4_alto / 12)))  # Hacer la miniatura más pequeña
        
        imagen_tk = ImageTk.PhotoImage(imagen_miniatura)
        
        self.etiqueta_imagen.config(image=imagen_tk)
        self.etiqueta_imagen.image = imagen_tk
        
        # Mensaje sobre el guardado exitoso
        self.resultado_label.config(text="Imagen guardada como fotos_carnet_a4.png y fotos_carnet_a4.pdf")

# Crear y ejecutar la ventana principal de Tkinter
root = tk.Tk()
app = FotoCarnetApp(root)
root.mainloop()
