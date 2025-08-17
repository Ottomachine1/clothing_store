from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# API路由
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'designers', views.DesignerViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'seasons', views.SeasonViewSet)
router.register(r'materials', views.MaterialViewSet)
router.register(r'clothes', views.ClothingViewSet)
router.register(r'history', views.ClothingHistoryViewSet)
router.register(r'permissions', views.UserPermissionViewSet)

app_name = 'clothes'

urlpatterns = [
    # 传统Django视图
    path('', views.clothing_list, name='clothing_list'),
    path('clothing/<int:pk>/', views.clothing_detail, name='clothing_detail'),
    path('designers/', views.designer_list, name='designer_list'),
    path('designer/<int:pk>/', views.designer_detail, name='designer_detail'),
    
    # API路由
    path('api/', include(router.urls)),
]
