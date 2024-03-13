from rest_framework import serializers
from .models import User,UZB,KOR,KAZ,AME,RUS
from .utils import check_country,send_sms
from rest_framework.validators import ValidationError
class SignUpSerializer(serializers.ModelSerializer):
    auth_country=serializers.CharField(required=False,read_only=True)
    auth_status=serializers.CharField(required=False,read_only=True)

    def __init__(self,*args, **kwargs):
        
        super(SignUpSerializer,self).__init__(*args, **kwargs)
        self.fields['phone_number']=serializers.CharField(required=False)

    class Meta:
        model = User
        fields=('auth_country','auth_status')
    def validate_phone_number(self,phone_number):
        user=User.objects.filter(phone_number=phone_number)
        if user.exists():
            data={
                "status": "False",
                "message": "Foydalanuvchi allaqachon mavjud"
            } 
            raise ValidationError(data)
        else:
            return phone_number
    def validate(self,data):
        user_input=data.get('phone_number')
        print(user_input)
        country=check_country(user_input)
        data={
            'auth_country':country,
            'phone_number':user_input,
        }
        return data
            
    def create(self,validated_data):
        user = super(SignUpSerializer,self).create(validated_data)
        auth_country=validated_data.get('auth_country')
        if auth_country==UZB:
            code=user.create_confirmation_code(UZB)
            send_sms(code)
       
        else:
            data={
                'status':False,
                'message':"Kod yuborishda hatolik mavjud"

            }
            raise ValidationError(data)
        return user
    
    def to_representation(self, instance):
        data=super(SignUpSerializer,self).to_representation(instance)
        data['access']=instance.token()['access']
        data['refresh']=instance.token()['refresh']

        return data