from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
# Create your views here.


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return JsonResponse({"message": "User activated"}, status=200)
    else:
        return JsonResponse({"message": "Activation link is not valid"},
                            status=400)


def activationEmail(request, user, to_email):
    mail_subject = "Activate your account."
    message = (
        f'Hi {user.username},\n\n'
        f'Please click on the link below to activate your account.\n\n'
        f'http://{get_current_site(request).domain}/user/activate/'
        f'{urlsafe_base64_encode(force_bytes(user.pk))}/'
        f'{account_activation_token.make_token(user)}'
    )

    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()


class RegisterUser(CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """Some doc here!"""
        obj = serializer.save()
        activationEmail(self.request, obj, obj.email)


class UpdateUser(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
