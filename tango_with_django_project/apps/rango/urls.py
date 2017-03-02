from django.conf.urls import url, include
from rest_framework import routers
from apps.rango import views

router = routers.DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'pages', views.PageViewSet)

app_name = 'rango'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),

    url(r'^add_category/$', views.add_category, name='add_category'),

    url(r'^api/', include(router.urls)),

    url(
        r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$',
        views.add_page,
        name='add_page'
    ),

    url(
        r'^category/(?P<category_name_slug>[\w\-]+)/$',
        views.show_category,
        name='show_category'
    ),

    url(r'^restricted/$', views.restricted, name='restricted'),

    url(r'^search/$', views.search, name='search'),
]
