from django.conf.urls import url
from django.urls import path
from shortener.views import (
                                short_url_detail_view,
                                create_new_short_link,
                                create_new_link,
                                update_default_link,
                                toggle_short_link_active,
                                link_detail_view,
                                update_link,
                                remove_link,
                                get_clicks,
                                get_clicks_by_ip
                            )

app_name = 'shortener'

urlpatterns=[
    path('', create_new_short_link, name='create_new_short_link'),
    path('shorturl/<int:id>', short_url_detail_view, name="short_url_detail"),
    path('shorturl/<int:id>/new_link', create_new_link, name='create_new_link'),
    path('shorturl/<int:id>/toggle', toggle_short_link_active, name='toggle_short_link_active'),
    path('link/<int:id>/update_default', update_default_link, name='update_default_link'),
    path('link/<int:id>', link_detail_view, name='link_detail'),
    path('link/<int:id>/update_link', update_link, name='update_link'),
    path('link/<int:id>/remove_link', remove_link, name='remove_link'),
    path('click/<int:short_url_id>', get_clicks, name='get_clicks'),
    path('click/<int:short_url_id>/<ip>', get_clicks_by_ip, name='get_clicks_by_ip'),
]
