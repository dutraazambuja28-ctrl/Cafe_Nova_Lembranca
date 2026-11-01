from django.contrib import admin
from CafeNL.models import ItemMenu, Mesa, Pedido, ItemPedido

class ItemMenuAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "phone")
    search_fields = ("first_name", "last_name", "email")
 
 
class MesaAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
 
 
class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1
    autocomplete_fields = ("product",)
    readonly_fields = ("unit_price", "subtotal_display")
    fields = ("product", "quantity", "unit_price", "subtotal_display")
 
    @admin.display(description="Subtotal (R$)")
    def subtotal_display(self, obj):
        if obj.pk is None:
            return "-"
        return f"{obj.subtotal:.2f}"
 
 
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer",
        "status",
        "payment_method",
        "total_display",
        "created_at",
    )
    list_editable = ("status",)
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
 
    def get_queryset(self, request):
        # Busca os itens de todos os pedidos de uma vez, para o total
        return super().get_queryset(request).prefetch_related("itens")
 
    @admin.display(description="Total (R$)")
    def total_display(self, obj):
        if obj.pk is None:
            return "-"
        return f"{obj.total:.2f}"
 
    @admin.action(description="Marcar como Em preparo")
    def marcar_em_preparo(self, request, queryset):
        queryset.update(status="A")
 
    @admin.action(description="Marcar como Pronto para retirada")
    def marcar_pronto(self, request, queryset):
        queryset.update(status="R")
 
    @admin.action(description="Marcar como Entregue")
    def marcar_entregue(self, request, queryset):
        queryset.update(status="E")
 
 
admin.site.register(ItemMenu, ItemMenuAdmin)
admin.site.register(Mesa, MesaAdmin)
admin.site.register(Pedido, PedidoAdmin)
 