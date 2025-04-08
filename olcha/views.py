from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from jazzmin.templatetags.jazzmin import User
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from olcha.models import Category, SubCategory, Product, Comment, Order, OrderItem
from olcha.permissions import CrudPermission
from olcha.serializer import CategorySerializer, SubCategorySerializer, ProductSerializer, ProductDetailSerializer, \
    CommentSerializer, OrderSerializer, OrderItemSerializer, OrderItemDetailSerializer
from rest_framework.filters import SearchFilter, OrderingFilter

# Create your views here.

# --------------------------------------------- Categories -------------------------------------------------------
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (CrudPermission,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name', 'id')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @method_decorator(cache_page(60))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoryViewSet, self).dispatch(request, *args, **kwargs)


class SubCategoryViewSet(ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    # permission_classes = (CrudPermission,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name', 'id')

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        if category_id:
            return SubCategory.objects.filter(category_id=category_id)
        return SubCategory.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @method_decorator(cache_page(60))
    def dispatch(self, request, *args, **kwargs):
        return super(SubCategoryViewSet, self).dispatch(request, *args, **kwargs)


# --------------------------------------------- Products -------------------------------------------------------

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (CrudPermission,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name', 'rating', 'price','id')

    def get_queryset(self):
        queryset = Product.objects.all().select_related('sub_category').prefetch_related('sub_category')
        category_id = self.kwargs.get('category_id')
        subcategory_id = self.kwargs.get('subcategory_id')

        if category_id:
            queryset = queryset.filter(sub_category__category__id=category_id)

        if subcategory_id:
            queryset = queryset.filter(sub_category__id=subcategory_id)

        return queryset

    @method_decorator(cache_page(60))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductViewSet, self).dispatch(request, *args, **kwargs)


class ProductDetailViewSet(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = (AllowAny,)


# --------------------------------------------- Comments -------------------------------------------------------

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('user__username','rating','id')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @method_decorator(cache_page(60))
    def dispatch(self, request, *args, **kwargs):
        return super(CommentViewSet, self).dispatch(request, *args, **kwargs)


# ----------------------------------------------- Order ---------------------------------------------------------

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('user__username','is_paid','id')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @method_decorator(cache_page(60))
    def dispatch(self, request, *args, **kwargs):
        return super(OrderViewSet, self).dispatch(request, *args, **kwargs)


class OrderItemsViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [AllowAny]
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('user__username','is_paid','id')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @method_decorator(cache_page(60))
    def dispatch(self, request, *args, **kwargs):
        return super(OrderItemsViewSet, self).dispatch(request, *args, **kwargs)


class OrderDetailViewSet(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]


class OrderItemDetailViewSet(RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemDetailSerializer
    permission_classes = [AllowAny]

# --------------------------------------------- AUTHENTICATION -------------------------------------------------------

class RegisterView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'Login successful',
            }, status=status.HTTP_200_OK)
        else:
            raise AuthenticationFailed('Invalid username or password')


class Logout(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)

    def post(self, request):
        request.user.auth_token.delete()
        return Response({
            'message': 'Successfully logged out.',
        })


# ------------------------------------------------ FINAL ---------------------------------------------------------