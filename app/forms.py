from django.contrib.auth import get_user_model #settings.pyのAUTH_USER_MODELに設定したモデルを呼び出す
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email',) #emailとパスワード