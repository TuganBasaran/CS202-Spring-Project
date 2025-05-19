# CS202 Restoran Yönetim Sistemi

## İçindekiler

- [Giriş](#giriş)
- [Proje Genel Bakış](#proje-genel-bakış)
- [Teknoloji Yığını](#teknoloji-yığını)
- [Proje Yapısı](#proje-yapısı)
- [Veritabanı Tasarımı](#veritabanı-tasarımı)
- [Backend: Entity Sınıfları](#backend-entity-sınıfları)
- [Backend: Service Sınıfları](#backend-service-sınıfları)
- [Frontend: HTML Şablonları](#frontend-html-şablonları)
- [Projeyi Çalıştırma](#projeyi-çalıştırma)
- [Müşteri Tarafını Nasıl Geliştirirsiniz (Adım Adım)](#müşteri-tarafını-nasıl-geliştirirsiniz-adım-adım)
- [Örnek Müşteri Özellikleri](#örnek-müşteri-özellikleri)
- [Yeni Başlayanlar İçin İpuçları](#yeni-başlayanlar-için-ipuçları)

---

## Giriş

Bu proje, restoran yöneticileri ve müşteriler için tam kapsamlı bir restoran yönetim ve yemek sipariş sistemidir. Yönetici tarafı tamamen uygulanmıştır; bu rehber, kod tabanını anlamanızı ve Python ile Flask'a yeni olsanız bile müşteri tarafını nasıl geliştireceğinizi öğretir.

---

## Proje Genel Bakış

- **Yöneticiler:**
  - Restoran, menü ve indirim ekleyip yönetebilir
  - Siparişleri görebilir ve işleyebilir
  - Analitikleri görebilir (satışlar, en iyi müşteriler vb.)
- **Müşteriler** (uygulanacak):
  - Restoranları ve menüleri inceleyebilir
  - Sipariş verebilir ve sipariş geçmişini görebilir
  - Restoranları puanlayabilir

---

## Teknoloji Yığını

- **Backend:** Python 3, Flask
- **Frontend:** HTML, CSS, Jinja2 (Flask'ın şablon motoru)
- **Veritabanı:** MySQL

---

## Proje Yapısı

```
CS202-Spring-Project/
├── app.py                  # Ana Flask uygulaması (routelar, başlatma)
├── Connector.py            # Veritabanı bağlantı yardımcı sınıfı
├── Entity/                 # Veri modeli sınıfları (Python)
│   ├── Address.py
│   ├── Cart.py
│   ├── Discount.py
│   ├── Keyword.py
│   ├── Menu_Item.py
│   ├── Rating.py
│   ├── Restaurant.py
│   └── User/
│       ├── Customer.py
│       ├── Restaurant_Manager.py
│       └── User.py
├── Service/                # İş mantığı sınıfları
│   ├── Customer_Service.py
│   └── Manager_Service.py
├── templates/              # HTML şablonları (Jinja2)
│   ├── index.html
│   └── manager/
│       ├── add_discount.html
│       ├── add_menu_item.html
│       ├── discounts.html
│       ├── manager_dashboard.html
│       ├── menu_stats.html
│       ├── orders.html
│       ├── restaurant_keywords.html
│       └── restaurant_page.html
├── Database/DDL.sql        # Veritabanı şeması
├── Database/DML.sql        # Örnek veri
└── requirements.txt        # Python bağımlılıkları
```

---

## Veritabanı Tasarımı

- **User**: Tüm kullanıcılar (yöneticiler ve müşteriler)
- **Restaurant_Manager**: Yöneticiler (User'dan türetilir)
- **Customer**: Müşteriler (User'dan türetilir)
- **Restaurant**: Restoran bilgisi
- **Menu_Item**: Her restoranın menü öğeleri
- **Cart**: Siparişler (her müşteri için bir sipariş)
- **Contains**: Her sepetin içindeki ürünler
- **Discount**: İndirim kampanyaları
- **Has_Discount**: Hangi menüde hangi indirim var
- **Rating**: Müşteri geri bildirimi
- **Keyword**: Restoran etiketleri
- **Restaurant_Keyword**: Hangi restoran hangi etikete sahip
- **Address**: Adres bilgisi

---

## Backend: Entity Sınıfları

Bunlar, veritabanı tablolarını temsil eden Python sınıflarıdır. `Entity/` klasöründe bulunurlar.

### Örnek: `Menu_Item.py`

```python
class Menu_Item():
    def __init__(self, id, name, image, description, price, restaurant_id):
        self.id = id
        self.name = name
        self.image = image
        self.description = description
        self.price = price
        self.restaurant_id = restaurant_id
        self.has_discount = False
        self.discount_rate = 0
        self.original_price = price
```

- **İpucu:** Tüm entity sınıfları, veriler için basit konteynerlerdir. Müşteri tarafı için ihtiyaç duyarsanız daha fazla özellik ekleyebilirsiniz.

### Örnek: `Cart.py`

```python
class Cart:
    def __init__(self, id, customer_id, restaurant_id, status, order_time):
        self.id = id
        self.customer_id = customer_id
        self.restaurant_id = restaurant_id
        self.status = status
        self.order_time = order_time
        self.customer_name = None
        self.items = None
        self.total_price = None
```

---

## Backend: Service Sınıfları

Service sınıfları, iş mantığını içerir. İşlem yapmak için entity sınıflarını ve veritabanı bağlantısını kullanırlar.

### Örnek: `Manager_Service.py`

- Tüm yönetici işlemlerini (menü öğesi ekleme, siparişleri işleme, analitikler vb.) yönetir.
- Örnek metot:

```python
def get_restaurant_menu_items_with_discounts(self, restaurant_id):
    # İlgili indirim bilgileriyle birlikte bir restoran için menü öğelerinin listesini döndürür
```

### Örnek: `Customer_Service.py` (uygulamanız için)

- Tüm müşteri işlemlerini (göz atma, sipariş verme, puanlama vb.) yönetir.
- **İpucu:** Tüm veri nesneleri için entity sınıflarını kullanın.
- Örnek metot:

```python
def get_all_restaurants(self):
    # Restaurant nesnelerinin bir listesini döndürür
```

---

## Frontend: HTML Şablonları

Şablonlar `templates/` klasöründedir. Python'dan veri eklemek için Jinja2 sözdizimini (küçük parantezler) kullanırlar.

### Örnek: `manager/restaurant_page.html`

```html
<ul>
  {% for menu in menu_item_list %}
  <li>
    <img src="{{ menu.image }}" alt="{{ menu.name }}" />
    <strong>{{ menu.name }}</strong>
    {% if menu.has_discount %}
    <span style="text-decoration: line-through; color: #999"
      >{{ menu.original_price }} TL</span
    >
    <span style="color: #e74c3c; font-weight: bold">{{ menu.price }} TL</span>
    {% else %}
    <span>{{ menu.price }} TL</span>
    {% endif %}
    <br />
    {{ menu.description }}
  </li>
  {% endfor %}
</ul>
```

- **İpucu:** Bu şablonları müşteri tarafı için kopyalayıp uyarlayabilirsiniz.

---

## Projeyi Çalıştırma

1. **Python 3'ü yükleyin** (henüz yüklemediyseniz)
2. **MySQL'i yükleyin** ve veritabanını `Database/DDL.sql` ile oluşturun ve `Database/DML.sql` ile doldurun
3. **Bağımlılıkları yükleyin:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Uygulamayı başlatın:**
   ```sh
   python app.py
   ```
5. **Tarayıcınızı açın:** [http://localhost:5000](http://localhost:5000) adresine gidin

---

## Müşteri Tarafını Nasıl Geliştirirsiniz (Adım Adım)

### 1. Entity Sınıflarını Anlayın

- İhtiyacınız olan tüm veriler (restoranlar, menü öğeleri, sepetler vb.), `Entity/` içinde Python sınıfları olarak temsil edilmektedir.
- Örnek: Bir restoranın menüsünü göstermek için `Menu_Item` sınıfını kullanın.

### 2. Bir Müşteri Servis Sınıfı Oluşturun

- `Service/Customer_Service.py` içinde bir `Customer_Service` sınıfı oluşturun.
- Veritabanı bağlantısını kullanarak veri alın ve entity nesneleri olarak döndürün.
- Örnek metotlar:
  - `get_all_restaurants()` → `Restaurant` nesnelerinin listesini döndürür
  - `get_restaurant_menu(restaurant_id)` → `Menu_Item` nesnelerinin listesini döndürür
  - `add_to_cart(cart_id, menu_item_id, quantity)` → sepete ürün ekler
  - `submit_order(cart_id)` → siparişi tamamlar

### 3. `app.py` Dosyasına Müşteri Routelarını Ekleyin

- Müşteri sayfaları için Flask routelarını ekleyin:
  - `/customer/restaurants` → tüm restoranları göster
  - `/customer/restaurant/<id>` → menüyü göster ve sipariş vermeye izin ver
  - `/customer/cart` → sepeti göster ve güncelle
  - `/customer/orders` → sipariş geçmişini göster
  - `/customer/add_rating/<restaurant_id>/<cart_id>` → bir restoranı puanla

### 4. Müşteri HTML Şablonlarını Oluşturun

- Yönetici şablonlarını kopyalayın ve müşteri tarafı için uyarlayın.
- Örnek: `templates/customer/restaurants.html`, `templates/customer/cart.html`, vb.
- Verileri döngüyle gösterip tarayıcıda görüntülemek için Jinja2 kullanın.

### 5. Servisinizde Entity Sınıflarını Kullanın

- Veritabanından veri alırken her zaman entity nesneleri oluşturun ve döndürün (örneğin, `Restaurant`, `Menu_Item`, `Cart`).
- Bir dizi öğe depolamanız gerekiyorsa (örneğin, bir sepet için), Python'un `set` türünü kullanabilirsiniz.

### 6. Özelliklerinizi Test Edin

- Eklediğiniz tüm müşteri özelliklerini test etmek için tarayıcıyı kullanın.
- Gerekirse Flask routelarınızdaki hata ayıklama bilgilerini yazdırın.

---

## Örnek Müşteri Özellikleri

- **Restoranları Göz At:** Tüm restoranları mutfak, şehir gibi filtrelerle listele
- **Menüyü Görüntüle:** Menü öğelerini, fiyatları ve indirimleri göster
- **Sepete Ekle:** Menü öğelerini bir sepete (sipariş) ekle
- **Ödeme:** Sepeti bir sipariş olarak gönder
- **Sipariş Geçmişi:** Tüm önceki siparişleri göster
- **Restoranı Puanla:** Bir sipariş sonrası, müşterinin restoranı puanlamasına ve yorum yapmasına izin ver

---

## Yeni Başlayanlar İçin İpuçları

- **Entity sınıfları** sadece verileri tutmak için Python sınıflarıdır. İhtiyacınız varsa daha fazla özellik ekleyebilirsiniz.
- **Service sınıfları** işi yapar: veritabanıyla konuşurlar ve entity nesnelerini döndürürler.
- **HTML şablonları** verileri Python'dan göstermek için süslü parantezler (`{{ }}`) kullanır.
- **Takıldığınızda:**
  - Python kodunuzda hata ayıklama bilgilerini yazdırın
  - Flask ve Jinja2 belgelerine bakın
  - Çalışan örnekler için yönetici tarafına bakın

---

## Adım Adım: Bir Service Methodu, Route ve Template Nasıl Çalışır?

Bu bölümde, bir örnek üzerinden **Manager_Service** içindeki bir methodun nasıl çalıştığını, bu methodun `app.py`'da nasıl kullanıldığını ve HTML template'te nasıl gösterildiğini adım adım açıklayacağız. Aynı mantıkla customer tarafını da kolayca geliştirebilirsiniz.

### 1. Entity Katmanı (Model)

Örneğin bir menü öğesi (Menu_Item) için:

```python
# Entity/Menu_Item.py
default
class Menu_Item():
    def __init__(self, id, name, image, description, price, restaurant_id):
        self.id = id
        self.name = name
        self.image = image
        self.description = description
        self.price = price
        self.restaurant_id = restaurant_id
        self.has_discount = False
        self.discount_rate = 0
        self.original_price = price
```

- **Amaç:** Veritabanındaki Menu_Item tablosunun Python karşılığıdır. Tüm menü öğesi verileri bu class ile tutulur.

### 2. Service Katmanı (İş Mantığı)

Örneğin, bir restoranın menü öğelerini ve indirimlerini getiren method:

```python
# Service/Manager_Service.py
def get_restaurant_menu_items_with_discounts(self, restaurant_id):
    """Get all menu items for a restaurant with discount information if available"""
    query = """
    SELECT
        M.id, M.name, M.image, M.description, M.price, M.restaurant_id,
        D.id, D.discount_rate, D.start_date, D.end_date
    FROM
        Menu_Item M
    LEFT JOIN
        Has_Discount HD ON M.id = HD.menu_item_id
    LEFT JOIN
        Discount D ON HD.discount_id = D.id
            AND CURDATE() BETWEEN D.start_date AND D.end_date
    WHERE
        M.restaurant_id = {}
    """.format(restaurant_id)

    result = self.connection.execute_query(query)
    menu_items = []
    if result and len(result) > 0:
        for row in result:
            menu_item = Menu_Item(row[0], row[1], row[2], row[3], row[4], row[5])
            if row[6] is not None:
                menu_item.has_discount = True
                menu_item.discount_rate = row[7]
                menu_item.original_price = menu_item.price
                menu_item.price = round(menu_item.price * (1 - row[7]/100), 2)
            menu_items.append(menu_item)
    return menu_items
```

- **Amaç:**
  - SQL ile veritabanından menü öğelerini ve varsa indirim bilgilerini çeker.
  - Her satır için bir `Menu_Item` nesnesi oluşturur.
  - İndirim varsa, ilgili alanları doldurur.
  - Sonuç olarak bir `Menu_Item` listesi döner.

### 3. Route (app.py)

Bu methodu bir web sayfasında göstermek için bir Flask route'u tanımlanır:

```python
# app.py
@app.route('/restaurant/<int:restaurant_id>')
def restaurant_page(restaurant_id):
    if manager_service.manager is None:
        return render_template("index.html", error="Manager not set!")
    result = manager_service.get_a_restaurant(restaurant_id)
    if result != -1 and result is not None:
        restaurant = result[0] if isinstance(result, list) and len(result) > 0 else result
        menu_items = manager_service.get_restaurant_menu_items_with_discounts(restaurant_id)
        return render_template('manager/restaurant_page.html',
                              restaurant=restaurant,
                              menu_item_list=menu_items)
    else:
        return "Restoran bulunamadı", 404
```

- **Amaç:**
  - URL'den restaurant_id alır.
  - Service katmanından menü ve restoran bilgilerini çeker.
  - Sonucu HTML template'e yollar.

### 4. Template (HTML)

Son olarak, bu veriler HTML'de gösterilir:

```html
<!-- templates/manager/restaurant_page.html -->
<ul>
  {% for menu in menu_item_list %}
  <li>
    <img src="{{ menu.image }}" alt="{{ menu.name }}" />
    <strong>{{ menu.name }}</strong>
    {% if menu.has_discount %}
    <span style="text-decoration: line-through; color: #999"
      >{{ menu.original_price }} TL</span
    >
    <span style="color: #e74c3c; font-weight: bold">{{ menu.price }} TL</span>
    {% else %}
    <span>{{ menu.price }} TL</span>
    {% endif %}
    <br />
    {{ menu.description }}
  </li>
  {% endfor %}
</ul>
```

- **Amaç:**
  - Python'dan gelen menü listesini döngüyle ekrana basar.
  - Eğer indirim varsa hem orijinal hem indirimli fiyatı gösterir.

---

## Step-by-Step Example: From Database to Webpage (Entity → Service → Route → Template)

This section provides a **detailed, beginner-friendly walkthrough** of how data flows from the database to the web page in this project. We use the example of listing menu items (with discounts) for a restaurant on the manager side. The same logic applies to the customer side!

### 1. Database Connection: The `Connector` Class

All database operations go through the `Connector` class (`Connector.py`). This class:

- Connects to the MySQL database.
- Runs SQL queries.
- Returns results to the Service classes.

**Example:**

```python
# Connector.py
class Connector():
    def execute_query(self, query):
        self.cursor.execute(query)
        if query.strip().lower().startswith("select"):
            return self.cursor.fetchall()
        else:
            self.connection.commit()
        return None
```

- **Usage:** The Service class creates a `Connector` object and uses it to fetch data.

### 2. Data Model: The `Entity` Classes

Entity classes (in the `Entity/` folder) represent tables in the database. For example, `Menu_Item` holds all the data for a menu item.

**Example:**

```python
# Entity/Menu_Item.py
class Menu_Item():
    def __init__(self, id, name, image, description, price, restaurant_id):
        self.id = id
        self.name = name
        self.image = image
        self.description = description
        self.price = price
        self.restaurant_id = restaurant_id
        self.has_discount = False
        self.discount_rate = 0
        self.original_price = price
```

- **Tip:** Always use Entity classes to pass data between Service, Route, and Template.

### 3. Business Logic: The Service Method

Service classes (like `Manager_Service.py`) contain methods that:

- Use the `Connector` to run SQL queries.
- Create Entity objects from the results.
- Return lists of Entity objects.

**Example:**

```python
# Service/Manager_Service.py
def get_restaurant_menu_items_with_discounts(self, restaurant_id):
    query = """
    SELECT
        M.id, M.name, M.image, M.description, M.price, M.restaurant_id,
        D.id, D.discount_rate, D.start_date, D.end_date
    FROM
        Menu_Item M
    LEFT JOIN
        Has_Discount HD ON M.id = HD.menu_item_id
    LEFT JOIN
        Discount D ON HD.discount_id = D.id
            AND CURDATE() BETWEEN D.start_date AND D.end_date
    WHERE
        M.restaurant_id = {}
    """.format(restaurant_id)
    result = self.connection.execute_query(query)
    menu_items = []
    for row in result:
        menu_item = Menu_Item(row[0], row[1], row[2], row[3], row[4], row[5])
        if row[6] is not None:
            menu_item.has_discount = True
            menu_item.discount_rate = row[7]
            menu_item.original_price = menu_item.price
            menu_item.price = round(menu_item.price * (1 - row[7]/100), 2)
        menu_items.append(menu_item)
    return menu_items
```

- **Key Points:**
  - The method uses the `Connector` to get data from the database.
  - It creates a `Menu_Item` object for each row.
  - If there is a discount, it updates the object.
  - Returns a list of `Menu_Item` objects.

### 4. Flask Route: Connecting Service to Web

The Flask route (in `app.py`) calls the Service method and passes the data to the template.

**Example:**

```python
# app.py
@app.route('/restaurant/<int:restaurant_id>')
def restaurant_page(restaurant_id):
    if manager_service.manager is None:
        return render_template("index.html", error="Manager not set!")
    restaurant = manager_service.get_a_restaurant(restaurant_id)
    menu_items = manager_service.get_restaurant_menu_items_with_discounts(restaurant_id)
    return render_template('manager/restaurant_page.html',
                          restaurant=restaurant,
                          menu_item_list=menu_items)
```

- **Key Points:**
  - The route gets the `restaurant_id` from the URL.
  - Calls the Service method to get menu items (as Entity objects).
  - Passes the list to the template as `menu_item_list`.

### 5. HTML Template: Displaying Data

The template (in `templates/manager/restaurant_page.html`) uses Jinja2 to loop over the data and display it.

**Example:**

```html
<ul>
  {% for menu in menu_item_list %}
  <li>
    <img src="{{ menu.image }}" alt="{{ menu.name }}" />
    <strong>{{ menu.name }}</strong>
    {% if menu.has_discount %}
    <span style="text-decoration: line-through; color: #999"
      >{{ menu.original_price }} TL</span
    >
    <span style="color: #e74c3c; font-weight: bold">{{ menu.price }} TL</span>
    {% else %}
    <span>{{ menu.price }} TL</span>
    {% endif %}
    <br />
    {{ menu.description }}
  </li>
  {% endfor %}
</ul>
```

- **Key Points:**
  - Loops over `menu_item_list` (a list of `Menu_Item` objects).
  - Shows the name, image, price, and discount info.

---

### Summary Table: How Everything Connects

| Layer     | File/Folder                            | Example Symbol/Class                     | Role/Responsibility                    |
| --------- | -------------------------------------- | ---------------------------------------- | -------------------------------------- |
| Database  | MySQL                                  | Menu_Item table                          | Stores the data                        |
| Connector | Connector.py                           | Connector                                | Runs SQL, returns results              |
| Entity    | Entity/Menu_Item.py                    | Menu_Item                                | Holds data as Python objects           |
| Service   | Service/Manager_Service.py             | get_restaurant_menu_items_with_discounts | Fetches data, returns Entity objects   |
| Route     | app.py                                 | restaurant_page                          | Calls Service, passes data to template |
| Template  | templates/manager/restaurant_page.html | menu_item_list                           | Displays data using Jinja2             |

---

### How to Apply This to the Customer Side

- Create similar Service methods in `Customer_Service.py` (use Entity classes!).
- Add routes in `app.py` for customer pages.
- Pass Entity objects to your templates.
- Use Jinja2 to display the data.

**If you follow this pattern, you can build any feature!**

---

## Notlar ve İpuçları (Türkçe)

- Service methodları her zaman Entity döndürmeli, böylece template ve diğer methodlarda kolayca kullanılabilir.
- Connector class'ı ile SQL sorgularını çalıştır, sonucu Entity'ye aktar.
- Route'ta Service methodunu çağır, sonucu template'e gönder.
- Template'te Jinja2 ile veriyi döngüyle göster.
- Manager tarafındaki örnekleri inceleyerek customer tarafını kolayca yazabilirsin.
