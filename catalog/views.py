from django.shortcuts import render, get_object_or_404
from catalog.models import Category, Product, ProductReview

from django.core import urlresolvers
from stats import stats
from cart import cart
from catalog.forms import ProductAddToCartForm, ProductReviewForm
from django.http import HttpResponseRedirect
from skart.settings import PRODUCTS_PER_ROW
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import HttpResponse
import json


def index(request, template_name='catalog/index.html'):
    search_recs = stats.recommended_from_search(request)
    featured = Product.featured.all()[0:PRODUCTS_PER_ROW]
    recently_viewed = stats.get_recently_viewed(request)
    view_recs = stats.recommended_from_views(request)
    page_title = 'Online Grocery Shopping - Buy Fruits, Vegetables, Groceries and More | Speedkart'
    return render(request, template_name, locals())


def show_category(request, category_slug, template_name='catalog/category.html'):
    c = get_object_or_404(Category, slug=category_slug)
    products = c.product_set.all()
    page_title = c.name
    meta_keywords = c.meta_keywords
    meta_description = c.meta_description
    return render(request, template_name, locals())


# product view with POST vs GET detection
def show_product(request, product_slug, template_name='catalog/product.html'):
    p = get_object_or_404(Product, slug=product_slug)
    categories = p.categories.filter(is_active=True)
    page_title = p.name
    meta_keywords = p.meta_keywords
    meta_description = p.meta_description
    # need to evaluate the HTTP method
    if request.method == 'POST':
        # add to cart...create the bound form
        postdata = request.POST.copy()
        form = ProductAddToCartForm(request, postdata)
        # check if posted data is valid
        if form.is_valid():
            # add to cart and redirect to cart page
            cart.add_to_cart(request)
            # if test cookie worked, get rid of it
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            url = urlresolvers.reverse('show_cart')
            return HttpResponseRedirect(url)
    else:
        # it's a GET, create the unbound form. Note request as a kwarg
        form = ProductAddToCartForm(request=request, label_suffix=':')
    # assign the hidden input the product slug
    form.fields['product_slug'].widget.attrs['value'] = product_slug
    # set the test cookie on our first GET request
    request.session.set_test_cookie()
    stats.log_product_view(request, p)
    product_reviews = ProductReview.approved.filter(product=p).order_by('-date')
    review_form = ProductReviewForm()
    return render(request, template_name, locals())


@login_required
def add_review(request):
    form = ProductReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        slug = request.POST.get('slug')
        product = Product.active.get(slug=slug)
        review.user = request.user
        review.product = product
        review.save()

        template = "catalog/product_review.html"
        html = render_to_string(template, {'review': review})
        response = {'success': 'True', 'html': html}
    else:
        html = form.errors.as_ul()
        response = {'success': 'False', 'html': html}
    return HttpResponse(json.dumps(response), content_type='application/json')
