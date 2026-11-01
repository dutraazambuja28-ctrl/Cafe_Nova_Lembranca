from django.urls import path
from CafeNL.views import CafeNLListView  # troque courses pelo nome do seu app

app_name = "CafeNL"

urlpatterns = [
    path("listar/", CafeNLListView.as_view(), name="course_list"),
]