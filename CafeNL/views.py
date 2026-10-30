from django.views.generic import ListView
from CafeNL.models import  ItemMenu, ItemPedido, Mesa, Pedido


class CafeNListView(ListView):
    model = ItemMenu
    template_name = "CafeNL/CafeNL_list.html"
    context_object_name = "CafeNL"
    paginate_by = 10


class CafeNListView(ListView):
    model = ItemPedido
    template_name = "CafeNL/CafeNL_list.html"
    context_object_name = "CafeNL"
    paginate_by = 10


class CafeNListView(ListView):
    model = Mesa
    template_name = "CafeNL/CafeNL_list.html"
    context_object_name = "CafeNL"
    paginate_by = 10


class CafeNLListView(ListView):
    model = Pedido
    template_name = "CafeNL/CafeNL_list.html"
    context_object_name = "CafeNL"
    paginate_by = 10