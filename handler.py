import re
import json
import PyPDF2
import requests
from ai import get_gpt_3_5_result
from search import get_product_url


def extract_text_from_pdf(pdf_file_path):
    pdf_text = {}

    # Open the PDF file in read-binary mode
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Loop through each page and extract text
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            ##################
            ##################
            if page_num == 80:
                break
            ##################
            ##################
            pdf_text[page_num] = page_text

    return pdf_text


def parse_page_text(s: str) -> str:
    s = s.strip()
    s = re.sub("\t", " ", s)
    return s


def parse_pdf(file_path) -> list[list[str]]:
    pages = extract_text_from_pdf(file_path)
    for page in pages:
        pages[page] = parse_page_text(pages[page])
    return list(pages.values())

def scan_page(page: str) -> list[str]:
    PROMPT = f"""\
Given the following page:
```````````````````
{page}
```````````````````

You task is to identify products. If there is a product on the page, and the following conditions are true for the product:  
1) The author reccomends the product.
2) The product is something that the user can buy online, such as an item from a shopping website or a subscription to a service provider.

then create a list for the product containing A) the name of the product and B) the chunk of text containing the product
and add the product's list to a list of lists.

Respond with a list of lists containing the products on the page, if any. You response will be loaded using Python's json.loads() function.
"""
    
    resp = get_gpt_3_5_result(PROMPT)

    resp = resp.strip()


    lst = []
    try:
        lst = json.loads(resp)
        print("Successfully loaded json from AI response")
    except:
        print("Could not load json from AI response")

    return lst

def ___get_product_url(product: str) -> str:
    # depreciated for consistency in development. Use search.get_product_url instead
    URL = "http://bilan604.pythonanywhere.com"
    pars = {
        "id": "",
        "operation": "get_product_url",
        "request_data": json.dumps({
            "product_description": product[0]
        })

    }
    try:
        resp = requests.post(f"{URL}/api/", params=pars)
        respObj = json.loads(resp.text)
        product_url = respObj["message"]
        return product_url
    except Exception as e:
        print("Error occured getting product url:", str(e))        
        return ""

def add_product_url(product: list[list[str]]) -> str:
    url = get_product_url(product[0])
    product.append(url)
    return product

def add_product_urls(products: list[list[str]]) -> list[list[str]]:
    new = []
    for i, product in enumerate(products):
        url = get_product_url(product[0])
        if not url:
            continue
        products[i].append(url)
        new.append(products[i])
    
    return new

def filter_add_source(page_num, products):
    new = []
    for pr in products:
        if len(pr) != 2:
            continue
        pr[0] = pr[0].strip()
        pr[1] = pr[1].strip()
        if not pr[0] or not pr[1]:
            continue

        pr[1] = f"(p.{int(page_num)}) " + pr[1]
        new.append(pr)
    return new

def extract_products(file_path):
    pages = parse_pdf(file_path)
    ##################
    ##################
    pages = pages[60:80]
    ##################
    ##################
    products = []
    for i, page in enumerate(pages):
        page_number = i + 1
        print(f"Parsing products for page: {page_number} / {len(pages)}")
        page_products = scan_page(page)

        page_products = filter_add_source(page_number, page_products)
        products += page_products

    print("Getting urls for products")
    products = add_product_urls(products)

    vis = set({})
    uq_products = []
    for product in products:
        if product[0] not in vis:
            vis.add(product[0])
            uq_products.append(product)
    return uq_products


def save_products(file_name: str, products: list[list[str]]):
    name, extension = file_name.split(".")
    file_path = f'products/{name}.txt'
    with open(file_path, "w+") as f:
        for product in products:
            obj = {
                "product_name": product[0],
                "product_snippet": product[1],
                "product_url": product[2]
            }
            f.write(json.dumps(obj) + "\n")

def load_products(file_name):
    name, extension = file_name.split(".")
    objs = []
    with open(f"products/{name}.txt", "r") as f:
        for line in f.readlines():
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            objs.append(obj)
    return objs
