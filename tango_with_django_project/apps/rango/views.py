from datetime import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets

from apps.rango.forms import CategoryForm, PageForm
from apps.rango.models import Category, Page
from .serializers import CategorySerializer, PageSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    """
    queryset = Category.objects.all().order_by('-likes')
    serializer_class = CategorySerializer


class PageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows pages to be viewed or edited.
    """
    queryset = Page.objects.all().order_by('-views')
    serializer_class = PageSerializer


def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by number of lies in descending order
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary
    # that will be passed to the template engine.

    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {
        'categories': category_list,
        'pages': page_list,
    }

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    # Obtain our Response object early so we can add cookie information.
    response = render(request, 'rango/index.html', context_dict)

    # Return response back to the user, updating any cookies that need change.
    return response


def about(request):
    visitor_cookie_handler(request)
    context_dict = {'visits': request.session['visits']}
    return render(request, 'rango/about.html', context_dict)


def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass
    # to the template rendering engine
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an
        # exception.
        category = Category.objects.get(slug=category_name_slug)

        # Retrieve all of the associated pages.
        # Note that filter() will return a list of page objects or an empty
        # list.
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from
        # the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we did'nt find the specified category.
        # Don't do anything -
        # the template will display the "no category" message for us.
        context_dict['category'] = None
        context_dict['pages'] = None

    # Go render the response and return it to the client.
    return render(request, 'rango/category.html', context_dict)


@login_required
def add_category(request):
    form = CategoryForm()

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)
            # Now that the category is saved
            # We could give a confirmation message
            # But since the most recent category added is on the index page
            # Then we can direct the user back to the index page.
            return index(request)
        else:
            # The supplied form contained errors -
            # just print them to the terminal.
            print(form.errors)

    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                print("FORM SAVED")
                return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {'description': 'You are in the restriced page.'})


def visitor_cookie_handler(request):
    visits = int(_get_server_side_cookie(request, 'visits', '1'))

    last_visit_cookie = _get_server_side_cookie(request,
                                                'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')

    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits += 1
        # Update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = 1
        # Set the last visit cookie
        request.session['last_visit'] = last_visit_cookie

    # Update/set the visits cookie
    request.session['visits'] = visits


def _get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val
