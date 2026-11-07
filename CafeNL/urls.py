from django.urls import path
from CafeNL.views import ItemMenuListView, CarrinhoView, AdicionarCarrinhoView, RemoverCarrinhoView, LimparCarrinhoView, FinalizarPedidoView, PedidoDetailView, MesaCreateView, PedidoListView, AdicionarMaisView, FecharContaView

app_name = "CafeNL"

urlpatterns = [
    path('', ItemMenuListView.as_view(), name="cardapio_list"),
    path('listar/', ItemMenuListView.as_view(), name="cardapio_listar"),
    path('carrinho/', CarrinhoView.as_view(), name="carrinho"),
    path('carrinho/adicionar/<int:pk>/', AdicionarCarrinhoView.as_view(), name="carrinho_adicionar"),
    path('carrinho/remover/<int:pk>/', RemoverCarrinhoView.as_view(), name="carrinho_remover"),
    path('carrinho/limpar/', LimparCarrinhoView.as_view(), name="carrinho_limpar"),
    path('carrinho/finalizar/', FinalizarPedidoView.as_view(), name="carrinho_finalizar"),
    path('pedidos/', PedidoListView.as_view(), name="pedidos"),
    path('pedido/<int:pk>/', PedidoDetailView.as_view(), name="pedido_detalhe"),
    path('pedido/<int:pk>/adicionar/', AdicionarMaisView.as_view(), name="pedido_adicionar"),
    path('pedido/<int:pk>/fechar/', FecharContaView.as_view(), name="pedido_fechar"),
    path('mesa/nova/', MesaCreateView.as_view(), name="mesa_criar"),
]
