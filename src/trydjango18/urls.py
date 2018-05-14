from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import TemplateView
from blog.views import home, formset_view
from dashboard.views import (AboutView,
                                MyView,
                                BookDetailView,
                                BookListView,
                                BookCreateView,
                                BookUpdateView,
                                BookDeleteView)

urlpatterns = [
    # Examples:
    url(r'^$', 'newsletter.views.home', name='home'),
    url(r'^contact/$', 'newsletter.views.contact', name='contact'),
    #url(r'^about/$', 'trydjango18.views.about', name='about'),
    #url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^blog/$', home, name='home_test'),
    url(r'^blog/formset$', formset_view, name='formset_view'),
    url(r'^book/new/$', BookCreateView.as_view(), name='book_create'),
    url(r'^book/(?P<slug>[-\w]+)/delete/$', BookDeleteView.as_view(), name='book_delete'),
    url(r'^book/(?P<slug>[-\w]+)/update/$', BookUpdateView.as_view(), name='book_update'),
    url(r'^book/(?P<slug>[-\w]+)$', BookDetailView.as_view(), name='book_detail'),
    url(r'^book/$', BookListView.as_view(), name='book_list'),
    url(r'^about/$', AboutView.as_view(), name='about'),
    url(r'^someview/$', MyView.as_view(), name='myview'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
