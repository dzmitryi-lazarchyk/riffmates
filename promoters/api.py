from ninja import Router, ModelSchema
from django.shortcuts import get_object_or_404
from .models import Promoter

class PromoterSchema(ModelSchema):
    class Meta:
        model = Promoter
        fields = [
            "id",
            "full_name",
            "date_of_birth",
            "date_of_death",
        ]

router = Router()

@router.get("/promoters/",
            response=list[PromoterSchema])
def promoters(request):
    return Promoter.objects.all()


@router.get("/promoter/{promoter_id}/",
            response=PromoterSchema)
def promoter(request, promoter_id):
    promoter = get_object_or_404(Promoter, id=promoter_id)
    return promoter
