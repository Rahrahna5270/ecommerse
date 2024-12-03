# your_app/context_processors.py
from .models import Category, Catcategory

def category_context(request):
    categories = Category.objects.all()
    catcategories = Catcategory.objects.all()
    
    return {
        'categories': categories,
        'catcategories': catcategories,
    }
