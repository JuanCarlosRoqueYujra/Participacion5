from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Conexión a la base de datos y creación de tabla
def init_db():
    conn = sqlite3.connect('almacen.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS producto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Ruta para listar productos
@app.route('/')
def index():
    conn = sqlite3.connect('almacen.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM producto")
    productos = cursor.fetchall()
    conn.close()
    return render_template('index.html', productos=productos)

# Ruta para crear un producto
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        cantidad = request.form['cantidad']
        precio = request.form['precio']
        
        conn = sqlite3.connect('almacen.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO producto (descripcion, cantidad, precio) VALUES (?, ?, ?)",
                       (descripcion, cantidad, precio))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('create.html')

# Ruta para actualizar un producto
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    conn = sqlite3.connect('almacen.db')
    cursor = conn.cursor()
    
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        cantidad = request.form['cantidad']
        precio = request.form['precio']
        
        cursor.execute("UPDATE producto SET descripcion = ?, cantidad = ?, precio = ? WHERE id = ?",
                       (descripcion, cantidad, precio, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM producto WHERE id = ?", (id,))
    producto = cursor.fetchone()
    conn.close()
    return render_template('update.html', producto=producto)

# Ruta para eliminar un producto
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('almacen.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM producto WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
