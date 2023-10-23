import json
from validate import is_valid_user
from validate import encrypt
from validate import decrypt
from handler import extract_products
from handler import save_products
from handler import load_products
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

URL = "http://127.0.0.1:5000"


@app.route('/files/<username>/<filename>')
def view_uploaded_file(username, filename):
    # Here, you can serve the uploaded file or perform any other actions you want
    # For example, you can return a download link or display the content of the file.

    print(f"loading product with filename: {filename}")
    products = load_products(filename)

    def make_table(products):
        columns = list(products[0].keys())
        rows = [list(product.values()) for product in products]
        table_rows = [columns] + rows
        for i in range(len(table_rows)):
            for j in range(len(table_rows[0])):
                if i != 0 and j == 2:
                    table_rows[i][j] = f"<td><a href='{table_rows[i][j]}'>link</a><td>"
                else:
                    table_rows[i][j] = f"<td>{table_rows[i][j]}<td>"
        table_rows = "\n".join(["<tr>"+"\n".join(row)+"</tr>" for row in table_rows])
        table = f"""<table>{table_rows}</table>"""
        return table
    
    return f"""
<!doctype html>
<head>
    <link href="{ url_for('static', filename='main.css') }" rel="stylesheet"  />
</head>
<body>
<div id="tableContainer">
    {make_table(products)}
<div>
</body>
"""


@app.route("/upload", methods=("GET", "POST"))
def index():
    username = request.form["username"]
    password = request.form["password"]
    if is_valid_user(username, password) == False:
        return render_template('index.html', success_message="could not validate login credentials")

    uploaded_file = request.files['file']
    if not uploaded_file:
        return render_template('index.html', success_message="no file uploaded")
    
    file_path = 'files/' + uploaded_file.filename
    
    uploaded_file.save(file_path)
    print(f"PDF saved to {file_path}")

    page_start = request.form["from_page"]
    page_stop = request.form["to_page"]
    if not page_start:
        page_start = 0
    else:
        page_start = int(page_start)

    if not page_stop:
        page_stop = 99999
    else:
        page_stop = int(page_stop)

    products = extract_products(file_path, page_start, page_stop)

    print("Saving products locally")
    save_products(uploaded_file.filename, products)
    
    enc_username = encrypt(username)
    return redirect(url_for('view_uploaded_file', filename=uploaded_file.filename, username=enc_username))


    """
    return f'''
    <!doctype html>
    <title>Products Parsing</title>
    <h1>Parsing Products From Uploaded File</h1>
    <p>The products for {uploaded_file.filename} will be ready at:</p>\n
    <a src="{URL}/files/{uploaded_file.filename}">
    '''
    """
    


@app.route('/')
def home():
    return render_template('index.html', success_message="")

