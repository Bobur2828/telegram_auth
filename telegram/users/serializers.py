from rest_framework import serializers
from .models import User,UZB,KOR,KAZ,AME,RUS
from .utils import check_country

class SignUpSerializer(serializers.ModelSerializer):
    auth_country=serializers.CharField(required=False,read_only=True)
    auth_status=serializers.CharField(required=False,read_only=True)

    def __init__(self,*args, **kwargs):
        
        super(SignUpSerializer,self).__init__(*args, **kwargs)
        self.fields['phone_number']=serializers.CharField(required=False)

    class Meta:
        model = User
        fields=('auth_country','auth_status')

    def validate(self,data):
        user_input=data.get('phone_number')
        print(user_input)
        country=check_country(user_input)
        data={
            'auth_country':country,
            'phone_number':user_input,
        }
        return data
            