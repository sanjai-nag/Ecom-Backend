from urllib import response
from requests import request
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import views,viewsets,generics,mixins
from .models import *
from django.http import HttpResponse
from .serializers import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.mail import send_mail
import math, random
from rest_framework.response import Response
from rest_framework.decorators import api_view
# from django.conf import settings 
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from main import settings
# Create your views here.
# * Twilio Imports
# from twilio.rest import Client
# import subprocess
# import snscrape.modules.twitter as sntwitter
import itertools
import instaloader

class mike(APIView):
    def post(self, request):
        keyword = "@Ruutu1331"
        tweets = sntwitter.TwitterSearchScraper('from:'+keyword).get_items()
        
        # Get the latest tweet and extract its like count
        latest_tweet = next(itertools.islice(tweets, 1))
        like_count = latest_tweet.likeCount
        http_response = f"<div style='display:flex; justify-content:center; align-items:center; height:100vh;'>Number of views: {like_count}</div>"
        # return Response({'like_count':like_count})
        return HttpResponse(http_response)


class ProductView(generics.GenericAPIView,mixins.ListModelMixin,mixins.RetrieveModelMixin):
    queryset = Product.objects.all().order_by("-id")
    serializer_class=ProductSerializers
    lookup_field = "id"

    def get(self,request,id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

class Cos_ProductView(generics.GenericAPIView,mixins.ListModelMixin,mixins.RetrieveModelMixin):
    queryset = Cos_Product.objects.all().order_by("-id")
    serializer_class=Cos_ProductSerializers
    lookup_field = "id"

    def get(self,request,id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

class filterr(views.APIView):
    def post(self, request):
        
        san=request.data
        print(san)
        kan=request.data["pro_name"]
        print(kan)
        serializer = SearchSerializer(data=san)
        if serializer.is_valid():
            serializer.save()  # Save the serializer data to the model
            # products = Product.objects.get(title='Glanza')
            # c=0
            obj=Filterpro.objects.all()
            obj.delete()
            products=Product.objects.get(title=kan)
            print(products.title,products.selling_price,products.selling_price1,products.selling_price2)
            Filterpro.objects.create(protitle=products.title,prodate=products.date,proselling_price=products.selling_price,procategory=products.category,proselling_price1=products.selling_price1,proselling_price2=products.selling_price2,prodescription=products.description,proimage=products.image,proimage1=products.image1,proimage2=products.image2,proimage3=products.image3,proimage4=products.image4)
            # for i in products:
                # print(i)
            
                # if(i='Glanza'):
                # Filterpro.objects.create(title=i,selling_price=i.selling_price)
                    # c=c+1
            # print(c)
            # print(products.selling_price)
            # c=0
            # print(products.selling_price)
            # for i in products:
                # print(i)

                # print(san)
            # Filterpro.objects.create(title='San')
                    # print(i.title,i.selling_price,i.description)
                # if i==san:
            # print(new)
                # newobj=Filterpro.objects.create(title=Product.title)
                # c=c+1
            # print(c)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

class SearchView(APIView):
    def get(self, request):
        search_query = request.query_params.get('query', '')
        filtered_books = Product.objects.filter(title__icontains=search_query)
        serializer = ProductSerializer(filtered_books, many=True)
        return Response(serializer.data)

class ProfileView(views.APIView):
    authentication_classes=[TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    def get(self,request):
        try:
            query = Profile.objects.get(prouser=request.user)
            serializer = ProfileSerializers(query)
            response_message = {"error":False,"data":serializer.data}
        except:
            response_message = {"error":True,"message":"Somthing is Wrong"}
        return Response(response_message)
  



class MyCart(viewsets.ViewSet):
    authentication_classes=[TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    
    def list(self,request):
        query = Cart.objects.filter(customer=request.user.profile)
        serializers = CartSerializer(query,many=True)
        all_data=[]
        for cart in serializers.data:
            cart_product = CartProduct.objects.filter(cart=cart["id"])
            cart_product_serializer = CartProductSerializer(cart_product,many=True)
            cart["cartproduct"] = cart_product_serializer.data
            all_data.append(cart)
        return Response(all_data)



class OrderViewset(viewsets.ViewSet):
    authentication_classes=[TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def list(self,request):
        query = Order.objects.filter(cart__customer = request.user.profile)
        serializers = OrderSerializer(query,many=True)
        all_data = []
        for order in serializers.data:
            cartproduct = CartProduct.objects.filter(cart_id=order['cart']['id'])
            cartproduct_serializer = CartProductSerializer(cartproduct,many=True)
            order['cartproduct'] = cartproduct_serializer.data
            all_data.append(order)
        return Response(all_data)
    def retrieve(self,request,pk=None):
        try:
            queryset = Order.objects.get(id=pk)
            serializers = OrderSerializer(queryset)
            data = serializers.data
            all_date=[]
            cartproduct = CartProduct.objects.filter(cart_id=data['cart']['id'])
            cartproduct_serializer = CartProductSerializer(cartproduct,many=True)
            data['cartproduct'] = cartproduct_serializer.data
            all_date.append(data)
            response_message = {"error":False,"data":all_date}
        except:
            response_message = {"error":True,"data":"No data Found for This id"}

        return Response(response_message)

    def destroy(self,request,pk=None):
        try:
            order_obj=Order.objects.get(id=pk)
            cart_obj = Cart.objects.get(id=order_obj.cart.id)

            print("in")
            order_obj.isdeleted=True
            order_obj.reason=request.data["reason"]
            print("in1")
            order_obj.save()
            cart_obj.save()
            print("in")
            send_mail('order canceled :( Your order placed is -Ecars ur order is cancelled, card id'+str(pk)+' for more info visit Ecars.',
            settings.EMAIL_HOST_USER,
            settings.EMAIL_RECEIVING_USER1,
            [email],
            fail_silently=False
            )
            responsemessage = {"erroe":False,"message":"Order delated","order id":pk}
        except:
            responsemessage = {"erroe":True,"message":"Order Not Found"}
        return Response(responsemessage)

    def create(self,request):
        cart_id = request.data["cartId"]
        cart_obj = Cart.objects.get(id=cart_id)
        total=request.data["total"]
        address = request.data["address"]
        mobile = request.data["mobile"]
        email = request.data["email"]
        mode = request.data["mode"]
        cart_obj.complit=True
        recipient_list=email
        # title = request.data["title"]
        # data=Product.objects.get(title=title)
        # data.sold=0
        # data.save()
        cart_obj.save()

        created_order = Order.objects.create(
            cart=cart_obj,
            address=address,
            mobile=mobile,
            email=email,
            total=total,
            mode=mode,
            discount=3,
            # title=title
            # order_status="Order Received"
        )
        
        send_mail('order placed :) Your order placed is -Ecars ur order is placed order id'+str(created_order.id)+'. Payment mode: '+str(mode)+' for more info visit Ecars.',
        settings.EMAIL_HOST_USER,
        settings.EMAIL_RECEIVING_USER1,
        [email],
        fail_silently=False
        )

        # sanjainagaraaja@gmail.com
        # if Order.objects.create(): 
            # send_mail('OTP request for resetting wwadsdsad password ecars',[email],fail_silently=False)
        return Response({"message":"order created","cart id":cart_id,"order id":created_order.id})

class CatagoryViewset(viewsets.ViewSet):
    def list(self,request):
        query = Category.objects.all()
        serializer = CatagorySerializer(query,many=True)
        # all_data = []
        # for cata in serializer.data:
        #     catagory_product = Product.objects.filter(category_id=cata['id'])
        #     catagory_product_serilazer = ProductSerializers(catagory_product,many=True)
        #     cata['category_product'] = catagory_product_serilazer.data
        #     all_data.append(cata)
        # return Response(all_data)
        return Response(serializer.data)

    def retrieve(self,request,pk=None):
        query = Category.objects.get(id=pk)
        serializer = CatagorySerializer(query)
        data_data = serializer.data
        all_data = []
        catagory_product = Product.objects.filter(category_id=data_data['id'])
        catagory_product_serilazer = ProductSerializers(catagory_product,many=True)
        data_data['category_product'] = catagory_product_serilazer.data
        all_data.append(data_data)
        return Response(all_data)

class RegisterView(views.APIView):
    def post(self,request):
        serializers =UserSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            print(serializer)
            # user = request.user
            # data = request.data       
            # user_obj = User.objects.get(username=user)
            # user_obj.first_name = data["first_name"]
            # print(user_obj.first_name)
            # user_obj.last_name = data["last_name"]
            # user_obj.save()
            return Response({"error":False,"message":f"user is created for '{serializers.data['username']}' ","data":serializers.data})
        return Response({"error":True,"message":"A user with that username already exists! Try Another Username"})

class AddtoCartView(views.APIView):
    permission_classes=[IsAuthenticated, ]
    authentication_classes=[TokenAuthentication, ]
    
    def post(self,request):
        product_id = request.data['id']
        product_obj = Product.objects.get(id=product_id)
        # print(product_obj,"product_obj")        
        cart_cart = Cart.objects.filter(customer=request.user.profile).filter(complit=False).first()
        cart_product_obj = CartProduct.objects.filter(product__id=product_id).first()
        
        try:
            if cart_cart:
                # print(cart_cart)
                # print("OLD CART")
                this_product_in_cart = cart_cart.cartproduct_set.filter(product=product_obj)
                if this_product_in_cart.exists():
                    # print("OLD CART PRODUCT--OLD CART")
                    cartprod_uct = CartProduct.objects.filter(product=product_obj).filter(cart__complit=False).first()
                    cartprod_uct.quantity +=1
                    cartprod_uct.subtotal +=product_obj.selling_price
                    cartprod_uct.save()
                    cart_cart.total +=product_obj.selling_price
                    cart_cart.save()
                else:
                    # print("NEW CART PRODUCT CREATED--OLD CART")
                    cart_product_new=CartProduct.objects.create(
                        cart = cart_cart,
                        price  =product_obj.selling_price,
                        quantity = 1,
                        subtotal = product_obj.selling_price
                    )
                    cart_product_new.product.add(product_obj)
                    cart_cart.total +=product_obj.selling_price
                    cart_cart.save()
            else:
                # print(cart_cart)
                # print("NEW CART CREATED")
                Cart.objects.create(customer=request.user.profile,total=0,complit=False)
                new_cart = Cart.objects.filter(customer=request.user.profile).filter(complit=False).first()
                cart_product_new=CartProduct.objects.create(
                        cart = new_cart,
                        price  =product_obj.selling_price,
                        quantity = 1,
                        subtotal = product_obj.selling_price
                    )
                cart_product_new.product.add(product_obj)
                # print("NEW CART PRODUCT CREATED")    
                new_cart.total +=product_obj.selling_price
                new_cart.save()

            response_mesage = {'error':False,'message':"Product add to card successfully","productid":product_id}
        
        except:
            response_mesage = {'error':True,'message':"Product Not add!Somthing is Wromg"}

        return Response(response_mesage)


class UpdateCartProduct(views.APIView):
    permission_classes=[IsAuthenticated, ]
    authentication_classes=[TokenAuthentication, ]
    def post(self,request):
        cp_obj = CartProduct.objects.get(id=request.data["id"])
        cart_obj = cp_obj.cart

        cp_obj.quantity +=1
        cp_obj.subtotal += cp_obj.price
        cp_obj.save()

        cart_obj.total += cp_obj.price
        cart_obj.save()
        return Response({"message":"CartProduct Add Update","product":request.data['id']})

class EditCartProduct(views.APIView):
    permission_classes=[IsAuthenticated, ]
    authentication_classes=[TokenAuthentication, ]
    def post(self,request):
        cp_obj = CartProduct.objects.get(id=request.data["id"])
        cart_obj = cp_obj.cart

        cp_obj.quantity -=1
        cp_obj.subtotal -= cp_obj.price
        cp_obj.save()

        cart_obj.total -= cp_obj.price
        cart_obj.save()
        if(cp_obj.quantity==0):
            cp_obj.delete()   
        return Response({"message":"CartProduct Add Update","product":request.data['id']})



class Delatecartproduct(views.APIView):
    permission_classes=[IsAuthenticated, ]
    authentication_classes=[TokenAuthentication, ]
    def post(self,request):
        cp_obj = CartProduct.objects.get(id=request.data['id'])
        cp_obj.delete()        
        return Response({"message":"CartProduct Delated","product":request.data['id']})

class Delatefullcart(views.APIView):
    permission_classes=[IsAuthenticated, ]
    authentication_classes=[TokenAuthentication, ]
    def post(self,request):
        try:
            card_obj = Cart.objects.get(id=request.data['id'])
            card_obj.delete()
            responsemessage = {"message":"Cart Delated"}
        except:
            responsemessage = {"message":"Somthing wright"}
        return Response(responsemessage)

class Updateuser(views.APIView):
    permission_classes=[IsAuthenticated, ]
    authentication_classes=[TokenAuthentication, ]
    def post(self,request):
        try:
            user = request.user
            data = request.data       
            user_obj = User.objects.get(username=user)
            user_obj.first_name = data["first_name"]
            user_obj.last_name = data["last_name"]
            # user_obj.email = data["email"]
            user_obj.save()
            response_data = {"error":False,"message":"User Data is Updated"}
        except:
            response_data = {"error":True,"message":"User Data is not Update Try agane !"}
        return Response(response_data)


class Upprofile(views.APIView):
    permission_classes=[IsAuthenticated, ]
    authentication_classes=[TokenAuthentication, ]
    def post(self,request):
        try:
            user = request.user
            query = Profile.objects.get(prouser=user)
            data = request.data
            query.address=data["address"]
            query.mobile=data["mobile"]
            # query.amount=data["amount"]
            # query.counts=data["counts"]
            query.save()
            return_res={"message":"data is Updated"}
        except:
            return_res={"message":"Somthing is Wrong Try Agane !"}
        return Response(return_res)

class Urofile(views.APIView):
    permission_classes=[IsAuthenticated, ]
    authentication_classes=[TokenAuthentication, ]
    def post(self,request):
        try:
            user = request.user
            query = Profile.objects.get(prouser=user)
            data = request.data
            query.dis=data["dis"]
            query.save()
            return_res={"message":"data is Updated"}
        except:
            return_res={"message":"Somthing is Wrong Try Agane !"}
        return Response(return_res)

class Uprofile(views.APIView):
    mission_classes=[IsAuthenticated, ]
    authentication_classes=[TokenAuthentication, ]
    def post(self,request):
        try:
            user = request.user
            query = Profile.objects.get(prouser=user)
            data = request.data
            query.reward=data["reward"]
            query.bill=data["bill"]
            query.save()
            return_res={"message":"data is Updated"}
        except:
            return_res={"message":"Somthing is Wrong Try Agane !"}
        return Response(return_res)

class tprofile(views.APIView):
    permission_classes=[IsAuthenticated, ]
    authentication_classes=[TokenAuthentication, ]
    def post(self,request):
        try:
            p=Profile.objects.all()
            max_value = Profile.objects.aggregate(max_value=models.Max('ru'))['max_value']
            print(max_value)
            # for i in p:
            #     print(i.ru)
            user = request.user
            query = Profile.objects.get(prouser=user)
            data = request.data
            query.tname=data["tname"]
            # keyword = data["tname"]
            # tweets = sntwitter.TwitterSearchScraper('from:'+keyword).get_items()
            # latest_tweet = next(itertools.islice(tweets, 1))
            # like_count = latest_tweet.likeCount
            # query.like=like_count
            query.save()
            return_res={"message":"data is Updated"}
        except:
            return_res={"message":"Somthing is Wrong Try Agane !"}
        return Response(return_res)

class InstagramPostView(views.APIView):
    permission_classes=[IsAuthenticated, ]
    authentication_classes=[TokenAuthentication, ]
    def post(self, request):
        # Initialize Instaloader and login if required
 
        user = request.user
        query = Profile.objects.get(prouser=user)
        data=request.data
        keyword = data["tname"]
        
        # keyword=query.tname
        # Load profile and get the latest post
        L = instaloader.Instaloader()

        profile = instaloader.Profile.from_username(L.context, keyword)
        post = None
        for p in profile.get_posts():
            post = p
            break


        # Get the like count of the post
        like_count = post.likes
    
        # Save the like count to a model
        InstagramPost.objects.create(like_count=like_count,tname=keyword)

        return Response({'message': 'Like count saved successfully!'})


class likecountprofile(views.APIView):
    permission_classes=[IsAuthenticated, ]
    authentication_classes=[TokenAuthentication, ]
    def post(self,request):
        try:
            user = request.user
            query = Profile.objects.get(prouser=user)
            data = request.data
            keyword = data["tname"]
            # tweets = sntwitter.TwitterSearchScraper('from:'+keyword).get_items()
            # latest_tweet = next(itertools.islice(tweets, 1))
            # like_count = latest_tweet.likeCount
            L = instaloader.Instaloader()

            profile = instaloader.Profile.from_username(L.context, keyword)
            post = None
            for p in profile.get_posts():
                post = p
                break
            if post.is_video:
                view_count = post.video_view_count
            else:
                view_count = None
            num_comments = post.comments

        #     igtv_post = profile.get_igtv_videos().next()
        #     view_count = igtv_post.video_view_count
        # # Get the like count of the post
        #     query.views=view_count
            # mentioning_posts = post.get_mentioned_by()

# Count the number of posts
            # num_mentions = sum(1 for i in mentioning_posts)

            like_count = post.likes
            query.followers=profile.followers
            query.like=like_count
            query.views=view_count
            # query.comments=num_comments
            # query.repost=num_mentions
            query.ru=query.like*0.01
            # for post in profile.get_posts():
            #     repost_count = post.get_sidecar_children_profiles().count()
            # query.repost=repost_count
            query.save()
            return_res={"message":"data is Updated"}
        except:
            return_res={"message":"Somthing is Wrong Try Agane !"}
        return Response(return_res)


class Updateprofile(views.APIView):
    permission_classes=[IsAuthenticated, ]
    authentication_classes=[TokenAuthentication, ]
    def post(self,request):
        try:
            user = request.user
            print(user)
            query = Profile.objects.get(prouser=user)
            data = request.data
            serializers = ProfileSerializers(query,data=data,context={"request":request})
            serializers.is_valid(raise_exception=True)
            serializers.save()
            return_res={"message":"Profile is Updated"}
        except:
            return_res={"message":"Somthing is Wrong Try Agane !"}
        return Response(return_res)


# def instaget(tname):

# @api_view(['GET', 'POST'])
# def likecheck(request):
#         user = request.user
#         query = Profile.objects.get(prouser=user)        
#         data=request.data
        

def generateOTP(email) :
    digits = "0123456789"
    OTP = ""
    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

@api_view(['GET', 'POST'])
def send_otp(request):
    email = request.data['email']
    if User.objects.filter(email=email).exists():  
        print(email)
        generatedOTP = generateOTP(email)
    else:
        return Response({"OTPSent": False})

    # print(generatedOTP)
    if generatedOTP:
        if OTPVerifiaction.objects.filter(email=email).exists():
            data = OTPVerifiaction.objects.get(email=email)
            data.otp= generatedOTP
            data.save()
            o=generatedOTP
            htmlgen = '<p>Your OTP is <strong>'+o+'</strong>.</p>'
            send_mail('OTP request for resetting password',o,'ecars',[email],fail_silently=False,html_message=htmlgen)
            return Response({"OTPSent": True})
                  
        else:

            data = OTPVerifiaction(email=email, otp=generatedOTP)
            data.save()
            print(generatedOTP)
            o=generatedOTP
            htmlgen = '<p>Your OTP is <strong>'+o+'</strong>.</p>'
            send_mail('OTP request for resetting password',o,'ecars',[email],fail_silently=False,html_message=htmlgen)
            return Response({"OTPSent": True})
    else:
        print("false")
        return Response({"OTPSent": False})

#         @api_view(['GET', 'POST'])
# def send_otp(request):
#     email = request.data['email']
#     print(email)
#     generatedOTP = generateOTP(email)
#     print(generatedOTP)
#     if generatedOTP:
#         if OTPVerifiaction.objects.filter(email=email).exists():
#             data = OTPVerifiaction.objects.get(email=email)
#             data.otp= generatedOTP
#             data.save()
#             o=generatedOTP
#             htmlgen = '<p>Your OTP is <strong>'+o+'</strong></p>'
#             send_mail('OTP request',o,'<gmail id>',[email],fail_silently=False,html_message=htmlgen)
#             return Response({"OTPSent": True})
                  
#         else:

#             data = OTPVerifiaction(email=email, otp=generatedOTP)
#             data.save()
#             print(generatedOTP)
#             o=generatedOTP
#             htmlgen = '<p>Your OTP is <strong>'+o+'</strong></p>'
#             send_mail('OTP request',o,'<gmail id>',[email],fail_silently=False,html_message=htmlgen)
#             return Response({"OTPSent": True})
#     else:
#         print("false")
#         return Response({"OTPSent": False})
    # if request.method=='POST':
    #     email=request.POST.get('email')
    #     print(email)
    #     o=generateOTP()
    #     print(o)
    #     htmlgen = '<p>Your OTP is <strong>'+o+'</strong></p>'
    #     send_mail('OTP request',o,'<gmail id>',[email],fail_silently=False,html_message=htmlgen)
    # return HttpResponse(o)
@api_view(['PUT'])
def checkOTP(request):
    email = request.data['email']
    otp = request.data['otp']
    generatedOTP = OTPVerifiaction.objects.filter(
        email=email).values_list('otp')
    print(generatedOTP)
    print(email)
    print(otp)
    if generatedOTP[0][0] == otp:
        data = OTPVerifiaction.objects.get(email=email)
        data.is_verfied = True
        data.save()
        return Response({"status": True})

    else:
        return Response({"status": False})
    

@api_view(['GET', 'POST'])
def registerr(request):
        firstname=request.data['firstname']
        lastname=request.data['lastname']
        username=request.data['username']
        email=request.data['email']
        password=request.data['password']
        confirm_password=request.data['confirm_password']
        print(firstname)
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                return Response({"email": False})
            else:
                if User.objects.filter(email=email).exists():
                   return Response({"email": False})
                else:
                    user = User.objects.create_user(first_name=firstname, last_name=lastname,username=username, email=email, password=password)
                    user.save()
                    pro=Profile.objects.create(prouser=user)
                    pro.save()
                    print("user saved")
                    return  Response({"log": True})
                    
        else:
            return Response({"password": False})

@api_view(['GET', 'POST'])
def reset(request):
        email=request.data['email']
        password=request.data['password']
        data = User.objects.get(email=email)
        data.set_password(password)
        data.save()
        print(password)
        print(data.username)
        print(data.password)
        
        return Response({"password": True})
   
@api_view(['GET', 'POST'])
def contact(request):
    usname=request.data['usname']
    email = request.data['email']
    phone_number=request.data['phone_number']
    message=request.data['message']
    send_mail(str(usname)+'has filled contact us form. contact no'+str(phone_number),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER,[email])
    # send_mail(str(usname)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER,[email], fail_silently = False)    
    return Response({"log": True})

class PostView(APIView):    
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        posts_serializer = PostSerializer(data=request.data)
        if posts_serializer.is_valid():
            posts_serializer.save()
            name=request.data['name']
            email=request.data['email']
            message=request.data['phone_number']
            send_mail('Request for selling car from Mr '+str(name),str(name)+' has requested to sell his car. Please click the below link to get information http://127.0.0.1:8000/admin/shop/post/. contact using :'+str(email)+' Phone number: '+str(message),settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return Response(posts_serializer.data, {"log":True})
        else:
            print('error', posts_serializer.errors)
            return Response(posts_serializer.data, {"log":False})

class CallView(APIView):    
    def get(self, request, *args, **kwargs):
        calls = Call.objects.all()
        serializer = CallSerializer(calls, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        calls_serializer = CallSerializer(data=request.data)
        if calls_serializer.is_valid():
            calls_serializer.save()
            name=request.data['name']
            message=request.data['phone_number']
            send_mail('Request for speaking to agent from Mr '+str(name),str(name)+' has requested to speak to agent. Please click the below link to get information http://127.0.0.1:8000/admin/shop/call/. Phone number: '+str(message),settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return Response(calls_serializer.data, {"log":True})
        else:
            print('error', calls_serializer.errors)
            return Response(calls_serializer.data, {"log":False})


class ReviewViewset(viewsets.ViewSet):
    # authentication_classes=[TokenAuthentication, ]
    # permission_classes = [IsAuthenticated, ]

    def list(self,request):
        reviewlist=[]
        reviewlist=review.objects.all()
        serializer = ReviewSerializer(reviewlist, many=True)
        # print("hi")
        # print(serializer.data)
        return Response(serializer.data)
        
    def create(self,request):
        productname=request.data['productname']
        customername=request.data['customername']
        comments=request.data['comments']
        customerrating=request.data['rating']
        review.objects.create(productname=productname,customername=customername,comments=comments,customerrating=customerrating)
        reviewcount=review.objects.filter(productname=productname)
        productdetails=Product.objects.get(title=productname)
        productdetails.allrating=productdetails.allrating+int(customerrating)
        productdetails.rating=productdetails.allrating/len(reviewcount)
        productdetails.save()
        print(productdetails.rating)
        print(len(reviewcount))
        return Response("True")

    def destroy(self,request):
        productname=request.data['productname']
        customername=request.data['customername']
        comments=request.data['comments']
        customerrating=request.data['rating']
        obj=review.objects.filter(productname=productname,customername=customername,comments=comments,customerrating=customerrating)
        obj.delete()
        return Response("True")