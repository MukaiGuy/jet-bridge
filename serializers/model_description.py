import fields
from serializers.serializer import Serializer


class ModelDescriptionFieldSerializer(Serializer):
    name = fields.CharField()
    date_type = fields.CharField()
    db_column = fields.CharField()

    class Meta:
        fields = (
            'name',
            'db_column',
            'date_type',
        )


class ModelDescriptionSerializer(Serializer):
    name = fields.CharField()
    db_table = fields.CharField()
    hidden = fields.BooleanField()
    fields = ModelDescriptionFieldSerializer(many=True)

    class Meta:
        fields = (
            'name',
            'db_table',
            'hidden',
            'fields',
        )
