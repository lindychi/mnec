from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('order_by/category_score', views.index_order_by_category_score, name='index_order_by_category_score'),
    path('detail/<int:pk>/', views.ItemDataDetailView.as_view(), name='detail_item'),
    path('clear_soldout/', views.clear_soldout, name='clear_soldout'),
    path('load_naver_data/', views.load_naver_data, name='load_naver_data'),
    path('load_naver_data/<int:load_count>/', views.load_naver_data, name='load_naver_data_limit'),
    path('load_domeme_data/', views.load_domeme_data, name='load_domeme_data'),
    path('load_naver_price/', views.load_naver_price, name='load_naver_price'),
    path('create_item/', views.create_item, name='create_item'),
    path('refresh_item/<int:pk>/', views.refresh_item_view, name='refresh_item'),
    path('refresh_uncorrect_margin/', views.refresh_uncorrect_margin, name='refresh_uncorrect_margin'),
    path('refresh_unset_naver_sale_price/', views.refresh_unset_naver_sale_price, name='refresh_unset_naver_sale_price'),
    path('refresh_uncorrect_upper_margin/', views.refresh_uncorrect_upper_margin, name='refresh_uncorrect_upper_margin'),
    path('title_replace_view/', views.title_replace_view, name='title_replace_view'),
    path('refresh_minimum_count_list/', views.refresh_minimum_count_list, name='refresh_minimum_count_list'),
    path('delete_duplicate_item/', views.delete_duplicate_item, name='delete_duplicate_item'),
    path('refresh_oldest/', views.refresh_oldest, name='refresh_oldest'),
    path('refresh_unset_naver_edit_id/', views.refresh_unset_naver_edit_id, name='refresh_unset_naver_edit_id'),
    path('title_replace_with_search/', views.title_replace_with_search, name='title_replace_with_search'),
    path('check_tag/', views.check_tag, name='check_tag'),
    path('reset_category_score/', views.reset_category_score, name='reset_category_score'),
]
