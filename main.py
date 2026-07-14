from pathlib import Path
import sqlite3
from datetime import datetime
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

KV = r"""
<NavButton@Button>:
    size_hint_y: None
    height: '48dp'
    background_normal: ''
    background_color: (0.04,0.22,0.40,1)
    color: (1,1,1,1)

<Panel@BoxLayout>:
    orientation: 'vertical'
    padding: '10dp'
    spacing: '8dp'
    canvas.before:
        Color:
            rgba: (1,1,1,1)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [8]

RootShell:
    orientation: 'vertical'
    canvas.before:
        Color:
            rgba: (0.92,0.95,0.98,1)
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        size_hint_y: None
        height: '70dp'
        padding: '10dp'
        canvas.before:
            Color:
                rgba: (0.02,0.17,0.32,1)
            Rectangle:
                pos: self.pos
                size: self.size
        Label:
            text: 'NTH POS'
            color: (1,0.79,0.27,1)
            bold: True
            font_size: '24sp'
        Label:
            text: app.clock_text
            color: (1,1,1,1)
    BoxLayout:
        size_hint_y: None
        height: '52dp'
        NavButton:
            text: 'Dashboard'
            on_release: manager.current='dashboard'
        NavButton:
            text: 'Billing'
            on_release: manager.current='billing'
        NavButton:
            text: 'Stock'
            on_release: manager.current='products'
        NavButton:
            text: 'Customers'
            on_release: manager.current='customers'
        NavButton:
            text: 'Reports'
            on_release: manager.current='reports'
    ScreenManager:
        id: manager
        DashboardScreen:
            name: 'dashboard'
        BillingScreen:
            name: 'billing'
        ProductsScreen:
            name: 'products'
        CustomersScreen:
            name: 'customers'
        ReportsScreen:
            name: 'reports'

<DashboardScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: '10dp'
        spacing: '10dp'
        Label:
            text: 'DASHBOARD'
            size_hint_y: None
            height: '40dp'
            color: (0.03,0.27,0.52,1)
            bold: True
            font_size: '18sp'
        GridLayout:
            cols: 2
            spacing: '10dp'
            Panel:
                Label:
                    text: "Today's Sales
₹ " + root.today_sales
                    color: (0.05,0.45,0.20,1)
                    bold: True
                    font_size: '22sp'
            Panel:
                Label:
                    text: 'Bills
' + root.bill_count
                    color: (0.05,0.32,0.64,1)
                    bold: True
                    font_size: '22sp'
            Panel:
                Label:
                    text: 'Products
' + root.product_count
                    color: (0.42,0.23,0.68,1)
                    bold: True
                    font_size: '22sp'
            Panel:
                Label:
                    text: 'Low Stock
' + root.low_stock
                    color: (0.84,0.18,0.20,1)
                    bold: True
                    font_size: '22sp'

<BillingScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: '8dp'
        spacing: '8dp'
        TextInput:
            id: scan
            hint_text: 'Scan barcode or search product'
            multiline: False
            size_hint_y: None
            height: '48dp'
            on_text_validate: root.search(self.text)
        BoxLayout:
            spacing: '8dp'
            Panel:
                Label:
                    text: 'PRODUCTS'
                    size_hint_y: None
                    height: '36dp'
                    color: (0.03,0.27,0.52,1)
                    bold: True
                ScrollView:
                    GridLayout:
                        id: product_list
                        cols: 1
                        spacing: '4dp'
                        size_hint_y: None
                        height: self.minimum_height
            Panel:
                Label:
                    text: 'CURRENT CART'
                    size_hint_y: None
                    height: '36dp'
                    color: (0.03,0.27,0.52,1)
                    bold: True
                ScrollView:
                    GridLayout:
                        id: cart_list
                        cols: 1
                        spacing: '4dp'
                        size_hint_y: None
                        height: self.minimum_height
                Label:
                    text: 'Grand Total: ₹ ' + root.grand_total
                    size_hint_y: None
                    height: '44dp'
                    color: (0.05,0.45,0.20,1)
                    bold: True
                    font_size: '19sp'
                Button:
                    text: 'PAY NOW'
                    size_hint_y: None
                    height: '50dp'
                    background_normal: ''
                    background_color: (0.10,0.63,0.28,1)
                    on_release: root.complete_sale()

<ProductsScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: '10dp'
        spacing: '8dp'
        TextInput:
            id: code
            hint_text: 'Product code / barcode'
            multiline: False
        TextInput:
            id: name
            hint_text: 'Product name'
            multiline: False
        TextInput:
            id: price
            hint_text: 'Sale price'
            input_filter: 'float'
            multiline: False
        TextInput:
            id: stock
            hint_text: 'Opening stock'
            input_filter: 'float'
            multiline: False
        Button:
            text: 'SAVE PRODUCT'
            size_hint_y: None
            height: '48dp'
            on_release: root.save_product(code.text,name.text,price.text,stock.text)
        ScrollView:
            GridLayout:
                id: products
                cols: 1
                spacing: '4dp'
                size_hint_y: None
                height: self.minimum_height

<CustomersScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: '10dp'
        spacing: '8dp'
        TextInput:
            id: cname
            hint_text: 'Customer name'
            multiline: False
        TextInput:
            id: mobile
            hint_text: 'Mobile number'
            multiline: False
        Button:
            text: 'SAVE CUSTOMER'
            size_hint_y: None
            height: '48dp'
            on_release: root.save_customer(cname.text,mobile.text)
        ScrollView:
            GridLayout:
                id: customers
                cols: 1
                spacing: '4dp'
                size_hint_y: None
                height: self.minimum_height

<ReportsScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: '10dp'
        spacing: '8dp'
        Button:
            text: 'REFRESH SALES REPORT'
            size_hint_y: None
            height: '48dp'
            on_release: root.refresh()
        ScrollView:
            GridLayout:
                id: sales
                cols: 1
                spacing: '4dp'
                size_hint_y: None
                height: self.minimum_height
"""

class DB:
    def __init__(self,path):
        self.path=path
        with self.conn() as c:
            c.executescript("""
            CREATE TABLE IF NOT EXISTS products(id INTEGER PRIMARY KEY,code TEXT UNIQUE,name TEXT,price REAL,stock REAL);
            CREATE TABLE IF NOT EXISTS customers(id INTEGER PRIMARY KEY,name TEXT,mobile TEXT);
            CREATE TABLE IF NOT EXISTS sales(id INTEGER PRIMARY KEY,invoice TEXT,date TEXT,total REAL);
            CREATE TABLE IF NOT EXISTS sale_items(id INTEGER PRIMARY KEY,sale_id INTEGER,product_id INTEGER,qty REAL,rate REAL,total REAL);
            """)
    def conn(self):
        c=sqlite3.connect(self.path); c.row_factory=sqlite3.Row; return c

class RootShell(BoxLayout): pass

class DashboardScreen(Screen):
    today_sales=StringProperty('0.00'); bill_count=StringProperty('0'); product_count=StringProperty('0'); low_stock=StringProperty('0')
    def on_pre_enter(self):
        db=App.get_running_app().db
        with db.conn() as c:
            r=c.execute("SELECT COALESCE(SUM(total),0) t,COUNT(*) n FROM sales WHERE substr(date,1,10)=?",(datetime.now().strftime('%Y-%m-%d'),)).fetchone()
            self.today_sales=f"{r['t']:.2f}"; self.bill_count=str(r['n'])
            self.product_count=str(c.execute('SELECT COUNT(*) FROM products').fetchone()[0])
            self.low_stock=str(c.execute('SELECT COUNT(*) FROM products WHERE stock<=5').fetchone()[0])

class BillingScreen(Screen):
    grand_total=StringProperty('0.00')
    def __init__(self,**kw): super().__init__(**kw); self.cart=[]
    def on_pre_enter(self): self.load_products(); self.render_cart()
    def load_products(self,q=''):
        from kivy.uix.button import Button
        box=self.ids.product_list; box.clear_widgets(); db=App.get_running_app().db
        with db.conn() as c: rows=c.execute('SELECT * FROM products WHERE code LIKE ? OR name LIKE ? ORDER BY name',(f'%{q}%',f'%{q}%')).fetchall()
        for r in rows:
            b=Button(text=f"{r['code']} | {r['name']} | ₹{r['price']:.2f} | Stock {r['stock']:g}",size_hint_y=None,height=48)
            b.bind(on_release=lambda _,x=dict(r): self.add(x)); box.add_widget(b)
    def search(self,t):
        db=App.get_running_app().db
        with db.conn() as c: r=c.execute('SELECT * FROM products WHERE upper(code)=upper(?)',(t.strip(),)).fetchone()
        if r: self.add(dict(r)); self.ids.scan.text=''
        else: self.load_products(t.strip())
    def add(self,p):
        if p['stock']<=0:return
        for i in self.cart:
            if i['id']==p['id']: i['qty']+=1; self.render_cart(); return
        p['qty']=1; self.cart.append(p); self.render_cart()
    def render_cart(self):
        from kivy.uix.button import Button
        box=self.ids.cart_list; box.clear_widgets(); total=0
        for n,i in enumerate(self.cart):
            x=i['qty']*i['price']; total+=x
            b=Button(text=f"{i['name']} × {i['qty']} = ₹{x:.2f}",size_hint_y=None,height=48)
            b.bind(on_release=lambda _,k=n:self.remove(k)); box.add_widget(b)
        self.grand_total=f'{total:.2f}'
    def remove(self,n): self.cart.pop(n); self.render_cart()
    def complete_sale(self):
        if not self.cart:return
        db=App.get_running_app().db; invoice=datetime.now().strftime('INV-%Y%m%d-%H%M%S'); total=sum(i['qty']*i['price'] for i in self.cart)
        with db.conn() as c:
            sid=c.execute('INSERT INTO sales(invoice,date,total) VALUES(?,?,?)',(invoice,datetime.now().isoformat(),total)).lastrowid
            for i in self.cart:
                c.execute('INSERT INTO sale_items(sale_id,product_id,qty,rate,total) VALUES(?,?,?,?,?)',(sid,i['id'],i['qty'],i['price'],i['qty']*i['price']))
                c.execute('UPDATE products SET stock=stock-? WHERE id=?',(i['qty'],i['id']))
        self.cart=[]; self.render_cart(); self.load_products()

class ProductsScreen(Screen):
    def on_pre_enter(self): self.refresh()
    def save_product(self,code,name,price,stock):
        if not code.strip() or not name.strip(): return
        with App.get_running_app().db.conn() as c: c.execute('INSERT OR REPLACE INTO products(code,name,price,stock) VALUES(?,?,?,?)',(code.strip(),name.strip(),float(price or 0),float(stock or 0)))
        self.refresh()
    def refresh(self):
        from kivy.uix.label import Label
        b=self.ids.products; b.clear_widgets()
        with App.get_running_app().db.conn() as c: rows=c.execute('SELECT * FROM products ORDER BY name').fetchall()
        for r in rows:b.add_widget(Label(text=f"{r['code']} | {r['name']} | ₹{r['price']:.2f} | Stock {r['stock']:g}",size_hint_y=None,height=44,color=(.08,.14,.24,1)))

class CustomersScreen(Screen):
    def on_pre_enter(self): self.refresh()
    def save_customer(self,name,mobile):
        if name.strip():
            with App.get_running_app().db.conn() as c:c.execute('INSERT INTO customers(name,mobile) VALUES(?,?)',(name.strip(),mobile.strip()))
            self.refresh()
    def refresh(self):
        from kivy.uix.label import Label
        b=self.ids.customers; b.clear_widgets()
        with App.get_running_app().db.conn() as c: rows=c.execute('SELECT * FROM customers ORDER BY id DESC').fetchall()
        for r in rows:b.add_widget(Label(text=f"{r['name']} {r['mobile'] or ''}",size_hint_y=None,height=44,color=(.08,.14,.24,1)))

class ReportsScreen(Screen):
    def on_pre_enter(self): self.refresh()
    def refresh(self):
        from kivy.uix.label import Label
        b=self.ids.sales; b.clear_widgets()
        with App.get_running_app().db.conn() as c: rows=c.execute('SELECT * FROM sales ORDER BY id DESC').fetchall()
        for r in rows:b.add_widget(Label(text=f"{r['invoice']} | {r['date']} | ₹{r['total']:.2f}",size_hint_y=None,height=44,color=(.08,.14,.24,1)))

class NTHPOSApp(App):
    clock_text=StringProperty('')
    def build(self):
        self.db=DB(Path(self.user_data_dir)/'nth_pos.db'); Builder.load_string(KV)
        from kivy.clock import Clock; Clock.schedule_interval(self.tick,1); self.tick(); return RootShell()
    def tick(self,*_):self.clock_text=datetime.now().strftime('%d %b %Y\n%I:%M:%S %p')

if __name__=='__main__':NTHPOSApp().run()
