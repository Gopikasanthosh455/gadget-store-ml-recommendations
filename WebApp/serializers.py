from rest_framework import serializers

from AdminApp.models import productDB


class ProductRecommendationSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = productDB
        fields = ["id", "Product_name", "Category_name", "Description", "Price", "image_url"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if not obj.Product_image:
            return None
        if request:
            return request.build_absolute_uri(obj.Product_image.url)
        return obj.Product_image.url
