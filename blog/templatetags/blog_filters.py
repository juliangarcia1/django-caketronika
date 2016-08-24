from  django import template
from django.db.models import Q
from django.utils.safestring import mark_safe

register = template.Library()

from blog.models import Category, SubCategory, Post


@register.filter( needs_autoscape=True)
def just_text_safe(bod):
    """
    Takes out img, code tags and content from body, just for description
    :param body:
    :return: body without images and code sections
    """
    from BeautifulSoup import BeautifulSoup
    soup = BeautifulSoup(bod)
    for tag in ['img','code']:
        for match in soup.findAll('code'):
            match.replaceWith('')
    return mark_safe(soup.text)



@register.filter
def dict_by_key(dict, key):
    try:
        return dict[key]
    except:
        return ''


@register.filter
def try_img_key(dict, key):
    try:
        dict[key]
        return True
    except:
        return False


@register.filter
def get_categories(model_name, limit=None):
    # if model_name == "categories":
    categories = Category.objects.all()[:limit]
    return categories


@register.filter
def get_subcategories(category_pk, limit=None):
    if category_pk =='':
        subcategories = SubCategory.objects.all()[:limit]
    else:
        subcategories = SubCategory.objects.filter(category_id=category_pk)[:limit]

    return subcategories

@register.filter
def get_posts_by_subcategory(category_pk, subcategory_pk):
    posts = Post.objects.filter(Q(category_id=category_pk) &
                                Q(subcategory_id = subcategory_pk)
                               )

