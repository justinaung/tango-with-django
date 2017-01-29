from django.conf.urls import url, include
from rest_framework import routers
from apps.rango import views

router = routers.DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'pages', views.PageViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.show_category, name='show_category'),
]
