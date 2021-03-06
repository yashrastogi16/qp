from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('qpscsmas.views',
    # Examples:
    # url(r'^$', 'qpmms.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', 'login'),
    url(r'^logout/', 'logout'),
    url(r'^$', 'login'),
    url(r'^index/','index'),
    url(r'^dashboard','dashboard'),
    url(r'^registeremployee','registeremployee'),
    url(r'^viewemployee','viewemployee'),
    url(r'^registercompanies','registercompanies'),
    url(r'^viewcompanies','viewcompanies'),
    url(r'^registerdevices','registerdevices'),
    url(r'^viewdevices','viewdevices'),
    url(r'^mealreports','mealreports'),
    url(r'^mtconfigure','mtconfigure'),
    url(r'^priceconfigure','priceconfigure'),
    url(r'^detailedmealsreport','detailedmealsreport'),
    url(r'^areports','areports'),
    url(r'^dareports','dareports'),
    url(r'^export_to_excel','export_to_excel'),

)
# if settings.DEBUG:
#     urlpatterns += [
#         url(r'^media/(?P<path>.*)$', serve, {
#             'document_root': settings.MEDIA_ROOT,
#         }),
#    ]
handler404 = 'views.custom_404'