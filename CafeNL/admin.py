from django.contrib import admin
from CafeNL.models import ItemMenu, Mesa, Pedido, ItemPedido
 
 
class ItemMenuAdmin(admin.ModelAdmin):
    list_display = ("nome", "categoria", "preco")
    list_filter = ("categoria",)
    list_editable = ("preco",)
    # Necessário para o autocomplete_fields do ItemPedidoInline funcionar
    search_fields = ("nome",)
 
 
class MesaAdmin(admin.ModelAdmin):
    list_display = ("numero", "capacidade", "status")
    list_filter = ("status",)
    list_editable = ("status",)
    ordering = ("numero",)
 
 
class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1
    autocomplete_fields = ("produto",)
    readonly_fields = ("subtotal_display",)
    fields = ("produto", "quantidade", "subtotal_display")
 
    @admin.display(description="Subtotal (R$)")
    def subtotal_display(self, obj):
        if obj.pk is None:
            return "-"
        return f"{obj.subtotal:.2f}"
 
 
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "mesa", "status", "total_display", "horario_criacao")
    list_editable = ("status",)
<<<<<<< HEAD
    list_filter = ("status", "payment_method", "created_at")
    list_select_related = ("customer",)
    search_fields = (
        "customer__first_name",
        "customer__last_name",
        "customer__email",
    )
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "total_display")
    inlines = [ItemPedidoInline]
    actions = ["marcar_em_preparo", "marcar_pronto", "marcar_entregue"]
=======
    list_filter = ("status", "mesa", "horario_criacao")
    list_select_related = ("mesa",)
    search_fields = ("=mesa__numero",)
    date_hierarchy = "horario_criacao"
    readonly_fields = ("horario_criacao", "total_display")
    inlines = [ItemPedidoInline]
    actions = ["marcar_preparando", "marcar_entregue", "marcar_pago"]
>>>>>>> bb908710579d3d5301bfe974536300e2f2259257
 
    def get_queryset(self, request):
        # Busca itens e produtos de todos os pedidos de uma vez,
        # para o total não gerar várias consultas por linha da listagem.
        return super().get_queryset(request).prefetch_related("itens__produto")
 
    @admin.display(description="Total (R$)")
    def total_display(self, obj):
        if obj.pk is None:
            return "-"
        return f"{obj.total:.2f}"
 
    @admin.action(description="Marcar como Preparando")
    def marcar_preparando(self, request, queryset):
        queryset.update(status=Pedido.Status.PREPARANDO)
 
    @admin.action(description="Marcar como Entregue")
    def marcar_entregue(self, request, queryset):
        queryset.update(status=Pedido.Status.ENTREGUE)
 
    @admin.action(description="Marcar como Pago")
    def marcar_pago(self, request, queryset):
        queryset.update(status=Pedido.Status.PAGO)
 
 
admin.site.register(ItemMenu, ItemMenuAdmin)
admin.site.register(Mesa, MesaAdmin)
<<<<<<< HEAD
admin.site.register(Pedido, PedidoAdmin)
 
=======
admin.site.register(Pedido, PedidoAdmin)
>>>>>>> bb908710579d3d5301bfe974536300e2f2259257
