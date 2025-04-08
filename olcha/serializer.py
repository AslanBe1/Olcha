from rest_framework import serializers
from olcha.models import Product, Category, SubCategory, Attribute, AttributeValue, ProductAttribute, Image, Comment, \
    Order, OrderItem


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'slug', 'subcategories']

    def get_subcategories(self, instance):
        return instance.sub_categories.count()

class SubCategorySerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'image', 'slug', 'category_id']


class ProductSerializer(serializers.ModelSerializer):
    sub_category_id = serializers.PrimaryKeyRelatedField(
        queryset=SubCategory.objects.all(), source='sub_category', write_only=True
    )

    class Meta:
        model = Product
        fields = ['id','name', 'price', 'quantity', 'discount', 'description', 'rating', 'slug', 'sub_category_id']


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ['name']


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = ['value']


class ProductAtrributeSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer()
    attribute_value = AttributeValueSerializer()

    class Meta:
        model = ProductAttribute
        fields = ['attribute', 'attribute_value']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image']

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['username', 'comment', 'rating', 'created_at']

    def get_username(self, obj):
        return obj.user.username


class ProductDetailSerializer(serializers.ModelSerializer):
    product_attribute = ProductAtrributeSerializer(many=True, read_only=True)
    image = ImageSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'quantity', 'discount', 'description', 'rating', 'slug', 'image', 'comments', 'product_attribute']



class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'quantity', 'price']



class OrderSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'username', 'total_price', 'address', 'is_paid', 'status', 'items', 'created_at']

    def get_username(self, obj):
        return obj.user.username


class OrderItemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'