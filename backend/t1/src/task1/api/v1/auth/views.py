from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from web.models import User
from api.v1.auth.serializer import UserSerializer
import random

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    data = request.data
    print(data)
    email = data.get('email')
    
    if User.objects.filter(email=email).exists():
        response_data = {
            'status':200,
            'message':'This email is already registered'
        }
    else:
        if email:
            password=str(random.randint(000000,999999))
            user=User.objects.create_user(image=data['image'],username=data['username'],first_name=data['first_name'],last_name=data['last_name'],email=email,password=password,phone=data['phone'],gender=data['gender'],house_name=data['house_name'],street=data['street'],city=data['city'],state=data['state'],country=data['country'])
            user.save()
            if user:
                subject='Account Activation Confirmation'
                message=f"Congratulations {data['first_name']} {data['last_name']}, Welcome! Thanks for joining us – we’re here to make your shopping easy and exciting. \n Your login credentials: \nUsername:{data['username']}\nPassword:{password}"
                from_email=settings.DEFAULT_FROM_EMAIL
                receipiant_list=[data['email']]
                send_mail(subject,message,from_email,receipiant_list)
                response_data={
                    'status':200,
                    'message':'Email sent successfully'
                }
            else:
                response_data={
                    'status':201,
                    'message':'Oops! Something went wrong. Please try again.'
                }
        else:
            response_data={
                'status':201,
                'message':'Email not found'
            }
    return Response(response_data)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username=request.data.get('username')
    password=request.data.get('password')

    user=authenticate(username=username,password=password)
    if user is not None:
        token,created=Token.objects.get_or_create(user=user)
        response_data={
            'status':200,
            'message':'Success',
            'token':token.key,
            'is_admin':user.is_superuser
        }
    else:
        response_data={
            'status':201,
            'message':'Invalid Credential'
        }
        if User.objects.filter(username=username):
            user1=User.objects.get(username=username)
            if user1.check_password(password):
                response_data={
                    'status':201,
                    'message':'user is not active'
                }
    return Response(response_data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def hact_user(request,id):
    if User.objects.filter(id=id):
        user=User.objects.get(id=id)
        if user.is_active:
            message='User Inactivated'
        else:
            message='User Activated'
        user.is_active=not user.is_active
        user.save()
        response_data={
            'status':200,
            'message':message
        }
    else:
        response_data={
            'status':201,
            'message':'User not found'
        }
    return Response(response_data)

@api_view(['GET'])
def get_all_users(request):
    users = User.objects.all()  # Fetch all users
    serializer = UserSerializer(users, many=True)  # Serialize data
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def users(request):
    user = request.user
    context = {'request': request}
    serializer = UserSerializer(user, context=context)

    if serializer:
        response_data = {
            'status': 200,
            'data': serializer.data
        }
    else:
        response_data = {
            'status': 201,
            'message':'Something went wrong'
        }

    return Response(response_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userdetails(request,id):
    if User.objects.filter(id=id):
        user=User.objects.get(id=id)
        context={
            'request':request,
        }
        serializer=UserSerializer(user,context=context)
        if serializer:
            response_data={
                'status':200,
                'data':serializer.data
            }
        else:
            response_data={
                'status':201,
                'message':'Something went wrong'
            }
    else:
        response_data={
            'status':201,
            'message':f'There id no product with id {id}'
        }
    return Response(response_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_user(request):
    users=User.objects.filter(is_staff=False)
    context={
        'request':request,
    }
    serializer=UserSerializer(users,many=True,context=context)
    if serializer:
        response_data={
            'status':200,
            'data':serializer.data
        }
    else:
        response_data={
            'status':201,
            'data':'Something went wrong'
        }
    return Response(response_data)

