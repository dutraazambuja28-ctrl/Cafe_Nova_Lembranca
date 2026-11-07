from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView
from CafeNL.models import ItemMenu, ItemPedido, Mesa, Pedido


class ItemMenuListView(ListView):
    model = ItemMenu
    template_name = "CafeNL/CafeNL_list.html"
    context_object_name = "itens_menu"
    paginate_by = 9


class ItemPedidoListView(ListView):
    model = ItemPedido
    template_name = "CafeNL/CafeNL_list.html"
    context_object_name = "itens_pedidos"
    paginate_by = 9


class MesaListView(ListView):
    model = Mesa
    template_name = "CafeNL/CafeNL_list.html"
    context_object_name = "mesas"
    paginate_by = 9


class PedidoListView(ListView):
    model = Pedido
    template_name = "CafeNL/pedidos_list.html"
    context_object_name = "pedidos"

    def get_queryset(self):
        return Pedido.objects.exclude(status="pago").order_by("mesa__numero")


class CarrinhoView(TemplateView):
    template_name = "CafeNL/carrinho.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carrinho = self.request.session.get("carrinho", {})
        itens = []
        total = 0
        for id, qtd in carrinho.items():
            produto = ItemMenu.objects.filter(pk=id).first()
            if produto:
                itens.append({"produto": produto, "quantidade": qtd, "subtotal": produto.preco * qtd})
                total = total + produto.preco * qtd
        context["itens"] = itens
        context["total"] = total
        context["mesas"] = Mesa.objects.exclude(status="reservada").order_by("numero")
        context["mesa_escolhida"] = self.request.session.get("mesa")
        return context


class AdicionarCarrinhoView(View):
    def post(self, request, pk):
        produto = get_object_or_404(ItemMenu, pk=pk)
        carrinho = request.session.get("carrinho", {})
        carrinho[str(produto.pk)] = carrinho.get(str(produto.pk), 0) + 1
        request.session["carrinho"] = carrinho
        return redirect(request.META.get("HTTP_REFERER", "/"))


class RemoverCarrinhoView(View):
    def post(self, request, pk):
        carrinho = request.session.get("carrinho", {})
        id = str(pk)
        if id in carrinho:
            carrinho[id] = carrinho[id] - 1
            if carrinho[id] == 0:
                del carrinho[id]
        request.session["carrinho"] = carrinho
        return redirect("CafeNL:carrinho")


class LimparCarrinhoView(View):
    def post(self, request):
        request.session["carrinho"] = {}
        return redirect("CafeNL:carrinho")


class FinalizarPedidoView(View):
    def post(self, request):
        carrinho = request.session.get("carrinho", {})
        if not carrinho or not request.POST.get("mesa"):
            return redirect("CafeNL:carrinho")

        mesa = get_object_or_404(Mesa, pk=request.POST.get("mesa"))
        pedido = Pedido.objects.filter(mesa=mesa).exclude(status="pago").first()
        if pedido is None:
            pedido = Pedido.objects.create(mesa=mesa)
        else:
            pedido.status = "pendente"
            pedido.save()

        for id, qtd in carrinho.items():
            produto = ItemMenu.objects.filter(pk=id).first()
            if produto:
                item = pedido.itens.filter(produto=produto).first()
                if item:
                    item.quantidade = item.quantidade + qtd
                    item.save()
                else:
                    ItemPedido.objects.create(pedido=pedido, produto=produto, quantidade=qtd)
        mesa.status = "ocupada"
        mesa.save()

        request.session["carrinho"] = {}
        request.session.pop("mesa", None)
        return redirect("CafeNL:pedidos")


class AdicionarMaisView(View):
    def post(self, request, pk):
        pedido = get_object_or_404(Pedido, pk=pk)
        request.session["mesa"] = pedido.mesa.pk
        return redirect("CafeNL:cardapio_list")


class FecharContaView(View):
    def post(self, request, pk):
        pedido = get_object_or_404(Pedido, pk=pk)
        pedido.fechar_conta()
        return redirect("CafeNL:pedidos")


class MesaCreateView(CreateView):
    model = Mesa
    fields = ["numero", "capacidade"]
    template_name = "CafeNL/mesa_form.html"
    success_url = reverse_lazy("CafeNL:carrinho")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for f in form.fields:
            form.fields[f].widget.attrs["class"] = "form-control"
        return form


class PedidoDetailView(DetailView):
    model = Pedido
    template_name = "CafeNL/pedido_detalhe.html"
