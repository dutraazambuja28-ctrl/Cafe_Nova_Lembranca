from django.db import models
from django.db import models
from decimal import Decimal

class ItemMenu(models.Model):
    class Categoria(models.TextChoices):
        BEBIDA = "bebida", "Bebida"
        SALGADO = "salgado", "Salgado"
        SOBREMESA = "sobremesa", "Sobremesa"

    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    categoria = models.CharField(max_length=20, choices=Categoria.choices)

    def __str__(self):
        return f"{self.nome} (R$ {self.preco:.2f})"

class Mesa(models.Model):
    # class Status(models.TextChoices):
    #     LIVRE = "livre", "Livre"
    #     OCUPADA = "ocupada", "Ocupada"
    #     RESERVADA = "reservada", "Reservada"
    #  CASO NECESSARIO ATIVO O CODIGO ACIMA 
    numero = models.PositiveIntegerField(unique=True)
    capacidade = models.PositiveIntegerField()
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"Mesa {self.numero}"


class Pedido(models.Model):
    class Status(models.TextChoices):
        PENDENTE = "pendente", "Pendente"
        PREPARANDO = "preparando", "Preparando"
        ENTREGUE = "entregue", "Entregue"
        PAGO = "pago", "Pago"

    mesa = models.ForeignKey(Mesa, on_delete=models.PROTECT, related_name="pedidos")
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDENTE)
    horario_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.mesa}"

    @property
    def total(self): #Calculando o total da conta da mesa
        return sum(item.subtotal for item in self.itens.all())

    def fechar_conta(self, taxa_servico_percentual=Decimal("10")):
        subtotal = self.total
        taxa = subtotal * (taxa_servico_percentual / 100)
        self.status = self.Status.PAGO
        self.save()
        self.mesa.status = Mesa.Status.LIVRE
        self.mesa.save()
        return {"subtotal": subtotal, "taxa_servico": taxa, "total_geral": subtotal + taxa}


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey(ItemMenu, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.produto.preco * self.quantidade
