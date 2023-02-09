from .database import get_db
from .models import Category


def create_cats():
    categories = list()
    db = get_db()

    cat1 = Category(parent="Technology", children=["Programming", "AI", "Linux"])
    cat2 = Category(
        parent="Trading", children=["Forex", "Cryptocurrency", "Wallstreet"]
    )
    cat3 = Category(
        parent="Art", children=[" Architecture", "Body Art", "Christian Art"]
    )
    cat4 = Category(parent="Sport", children=["Football", "Volleyball", "KickBoxing"])
    cat5 = Category(
        parent="Science", children=["Physics", "Biochemistry", "Bioinformatics"]
    )

    cat1.save()
    cat2.save()
    cat3.save()
    cat4.save()
    cat5.save()

    del cat1.id
    categories.append(cat1.to_mongo().to_dict())
    del cat2.id
    categories.append(cat2.to_mongo().to_dict())
    del cat3.id
    categories.append(cat3.to_mongo().to_dict())
    del cat4.id
    categories.append(cat4.to_mongo().to_dict())
    del cat5.id
    categories.append(cat5.to_mongo().to_dict())

    return categories
