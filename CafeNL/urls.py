from django.urls import path
from CafeNL.views import ItemMenuListView

app_name = "CafeNL"

urlpatterns = [
    path("listar/", ItemMenuListView.as_view(), name="cardapio_list"),
]