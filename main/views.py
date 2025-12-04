from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from main.models import Customer, Order, Product

products = [
    {
        "id": 1,
        "title": "Визитки",
        "description": "Цветные и чёрно-белые визитки на плотной мелованной бумаге различной плотности. Возможна печать односторонних и двусторонних вариантов, с матовой или глянцевой ламинацией. Отлично подходят для деловых встреч и презентаций.",
        "price": 1500,
        "in_stock": True,
        "quantity": 150,
        "image_url": "/static/images/business-cards.jpg",
        "images": [
            {"image": "/static/images/cards1.jpg", "alt": "Визитки образец 1"},
            {"image": "/static/images/cards2.jpg", "alt": "Визитки образец 2"},
            {"image": "/static/images/cards3.jpg", "alt": "Визитки образец 3"}
        ],
        "reviews": [
            {
                "author": "Александр Иванов",
                "rating": 5,
                "text": "Отличное качество печати, визитки вышли яркими и чёткими. Быстрая доставка.",
                "created_at": "2024-01-15"
            },
            {
                "author": "Мария Петрова",
                "rating": 3,
                "text": "Хорошие визитки, но хотелось бы больше вариантов бумаги. В целом довольна.",
                "created_at": "2024-01-10"
            }
        ],
        "slug": "vizitki",
        "category": {"name": "Полиграфия", "slug": "polygraphy"}
    },
    {
        "id": 2,
        "title": "Буклеты",
        "description": "Рекламные буклеты формата от A6 до A4, с одно- или двухфальцевыми сгибами. Яркая полноцветная печать на плотной бумаге или дизайнерском картоне. Идеальны для продвижения услуг, мероприятий или товарных линеек.",
        "price": 4500,
        "in_stock": True,
        "quantity": 75,
        "image_url": "/static/images/booklets.jpg",
        "images": [
            {"image": "/static/images/booklet1.jpg", "alt": "Буклет А4"},
            {"image": "/static/images/booklet2.jpg", "alt": "Буклет А5"},
            {"image": "/static/images/booklet3.jpg", "alt": "Буклет с фальцем"}
        ],
        "reviews": [
            {
                "author": "ООО 'Технопром'",
                "rating": 5,
                "text": "Сделали рекламные буклеты для выставки. Отличная цветопередача, качественная бумага.",
                "created_at": "2024-01-20"
            }
        ],
        "slug": "buklety",
        "category": {"name": "Полиграфия", "slug": "polygraphy"}
    },
    {
        "id": 3,
        "title": "Календари",
        "description": "Настенные, настольные и карманные календари с индивидуальным дизайном. Возможна печать на плотной бумаге с выбором вариантов переплёта и отделки: пружина, скрепка, ламинация. Отличный сувенир и практичный подарок для клиентов и партнёров.",
        "price": 3200,
        "in_stock": False,
        "quantity": 0,
        "image_url": "/static/images/calendars.jpg",
        "images": [
            {"image": "/static/images/calendar1.jpg", "alt": "Настенный календарь"},
            {"image": "/static/images/calendar2.jpg", "alt": "Настольный календарь"},
            {"image": "/static/images/calendar3.jpg", "alt": "Карманный календарь"}
        ],
        "reviews": [],
        "slug": "kalendari",
        "category": {"name": "Сувенирная продукция", "slug": "souvenirs"}
    },
    {
        "id": 4,
        "title": "Брошюры",
        "description": "Многостраничные брошюры с различными видами переплёта: скрепка, термоклей, пружина. Печать на офсетной или мелованной бумаге. Отлично подходят для каталогов, инструкций, презентационных материалов.",
        "price": 7500,
        "in_stock": True,
        "quantity": 30,
        "image_url": "/static/images/brochures.jpg",
        "images": [
            {"image": "/static/images/brochure1.jpg", "alt": "Брошюра на скрепке"},
            {"image": "/static/images/brochure2.jpg", "alt": "Брошюра на пружине"}
        ],
        "reviews": [
            {
                "author": "Университет",
                "rating": 5,
                "text": "Заказывали методические материалы для студентов. Отличное качество печати, чёткие тексты и изображения.",
                "created_at": "2024-01-18"
            },
            {
                "author": "Ирина Смирнова",
                "rating": 4,
                "text": "Хорошие брошюры, но сроки изготовления можно было бы сократить.",
                "created_at": "2024-01-12"
            },
            {
                "author": "Дмитрий Козлов",
                "rating": 5,
                "text": "Лучшее качество в городе! Брошюры выглядят дорого и презентабельно.",
                "created_at": "2024-01-05"
            }
        ],
        "slug": "broshury",
        "category": {"name": "Полиграфия", "slug": "polygraphy"}
    }
]


class ReviewObj:
    def __init__(self, rev_data):
        self.author = rev_data["author"]
        self.rating = rev_data["rating"]
        self.text = rev_data["text"]
        self.created_at = rev_data["created_at"]

    # Создаем объект images
class ImageObj:
    def __init__(self, img_data):
        self.image = type('obj', (object,), {'url': img_data["image"]})()
        self.alt_text = img_data["alt"]


def index_page(request):
    return render(request, 'index.html')

def about_page(request):
    return render(request, 'about.html')

def catalog_page(request):
    return render(request, "catalog.html", {"products": products})

def cabinet_page(request):
    return render(request, "cabinet.html")


def product_page(request, product_id):
    product_data = next((p.copy() for p in products if p["id"] == product_id), None)

    if not product_data:
        return render(request, "404.html", status=404)

    product_data["image"] = type('obj', (object,), {'url': product_data["image_url"]})()

    product_data["images"] = type('obj', (object,), {
        'all': [ImageObj(img) for img in product_data["images"]]
    })()

    product_data["reviews"] = type('obj', (object,), {
        'all': [ReviewObj(rev) for rev in product_data["reviews"]],
        'count': len(product_data["reviews"])
    })()

    product_data["category"] = type('obj', (object,), {
        'name': product_data["category"]["name"],
        'slug': product_data["category"]["slug"]
    })()

    return render(request, "product.html", {"product": product_data})