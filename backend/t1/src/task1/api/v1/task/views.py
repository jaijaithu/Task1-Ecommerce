from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from web.models import User
import random
from django.db.models import Sum
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_stats(request):
    user_count = User.objects.filter(is_staff=False, is_superuser=False).count()

    # Get pending orders count
    # pending_orders = Order.objects.filter(status="Pending").count() or 0
    # shipped_orders = Order.objects.filter(status="Shipped").count() or 0
    # delivered_orders = Order.objects.filter(status="Delivered").count() or 0
    # cancelled_orders = Order.objects.filter(status="Cancelled").count() or 0
    # total_revenue = (Order.objects.filter(status='Delivered').aggregate(total=Sum('total_price'))['total'] or 0)

    
    response_data={
        'status':200,
        'count':user_count,
        # 'pending_orders':pending_orders,
        # 'shipping_orders':shipped_orders,
        # 'delivered_orders':delivered_orders,
        # 'cancelled_orders':cancelled_orders,
        # 'total_revenue':total_revenue,
        'is_admin': request.user.is_staff
    }
    return Response(response_data)

