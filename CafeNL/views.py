from django.views.generic import ListView
from CafeNL.models import ItemMenu, ItemPedido, Mesa, Pedido


class ItemMenuListView(ListView):
    model = ItemMenu
    template_name = "CafeNL/CafeNL_list.html"
    context_object_name = "itens_menu"
    paginate_by = 10


class ItemPedidoListView(ListView):
    model = ItemPedido
    template_name = "CafeNL/CafeNL_list.html"
    context_object_name = "itens_pedidos"
    paginate_by = 10


class MesaListView(ListView):
    model = Mesa
    template_name = "CafeNL/CafeNL_list.html"
    context_object_name = "mesas"
    paginate_by = 10


class PedidoListView(ListView):
    model = Pedido
    template_name = "CafeNL/pedidos_list.html"
    context_object_name = "pedidos"
    paginate_by = 10