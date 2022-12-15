from rest_framework import serializers


class ServicesSerializer(serializers.Serializer):
    date = serializers.DateField()
    saloon = serializers.IntegerField(required=False)
    master = serializers.IntegerField(required=False)
    service = serializers.IntegerField(required=False)

    class Meta:
        fields = ['date', 'saloon', 'master', 'service']
