from django.urls import path,include
from rest_framework.routers import DefaultRouter
from olcha import views, customobtainview
app_name = 'olcha'

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='categories')
router.register(r'subcategory', views.SubCategoryViewSet, basename='subcategory')
router.register(r'products', views.ProductViewSet, basename='products')
router.register(r'comments', views.CommentViewSet, basename='comments')
router.register(r'order', views.OrderViewSet, basename='order')
router.register(r'orderitem', views.OrderItemsViewSet, basename='order_item')

urlpatterns = [
    path('', include(router.urls)),

# ----------------------------------------------- Product --------------------------------------------------------
    path('products-detail/<int:pk>/', views.ProductDetailViewSet.as_view(), name='product'),


# ----------------------------------------------- Categories --------------------------------------------------------
    path('categories/<int:category_id>/subcategories/', views.SubCategoryViewSet.as_view({'get': 'list'}), name='subcategory-list'),
    path('categories/<int:category_id>/subcategories/<int:subcategory_id>/product/', views.ProductViewSet.as_view({'get': 'list'}), name='product-list'),


# ----------------------------------------------- Order --------------------------------------------------------
    path('order-detail/<int:pk>/', views.OrderDetailViewSet.as_view(), name='order-detail'),
    path('order-item-detail/<int:pk>/', views.OrderItemDetailViewSet.as_view(), name='order-detail'),


# ----------------------------------------------- AUTHENTICATION --------------------------------------------------------
    path('register-token/', views.RegisterView.as_view(), name='register'),
    path('Login-tokens/',views.LoginView.as_view(), name='login'),
    path('login-token/', customobtainview.CustomAuthToken.as_view(), name='login'),
    path('logout-token/', views.Logout.as_view(), name='logout'),
]