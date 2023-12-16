from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'home.html'  # あなたのテンプレートの適切なパスに変更してください
