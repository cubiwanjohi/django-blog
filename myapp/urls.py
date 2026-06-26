from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [

    # ── Post URLs ──────────────────────────────
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/',
         views.post_detail, name='post_detail'),

    # ── Category & Tag ─────────────────────────
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('tag/<slug:slug>/',      views.tag_detail,      name='tag_detail'),

    # ── Search ─────────────────────────────────
    path('search/', views.search, name='search'),

    # ── Comments ───────────────────────────────
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/comment/',
         views.add_comment, name='add_comment'),

    # ── Auth ───────────────────────────────────
    path('register/', views.register,    name='register'),
    path('login/',    views.user_login,  name='login'),
    path('logout/',   views.user_logout, name='logout'),
    path('profile/',  views.profile,     name='profile'),
]