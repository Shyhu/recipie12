from django.shortcuts import render
from recipie.models import Recipe,Review
from recipie.serializers import RecipeSerializer,ReviewSerializer
from rest_framework import mixins,generics,viewsets
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from rest_framework.response import Response
from django.db.models import Q
from recipie.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

class Recipedetail(viewsets.ModelViewSet):
    queryset=Recipe.objects.all()
    serializer_class = RecipeSerializer

class Allrecipe(APIView):
    def get(self,request):
        query=self.request.query_params.get('filter')
        if(query):
            recipe=Recipe.objects.filter(Q(cuisine_icontains = query) | Q(ingredientsicontains =query) | Q(meal_type_icontains =query))
            serializer=RecipeSerializer(recipe,many=True)
            return Response(serializer.data)


# class AllRecipe(APIView):
#     def get_object(self, pk):
#         try:
#             return Recipe.objects.get(pk=pk)
#         except Recipe.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk):
#         recipe = self.get_object(pk)
#         filtered_recipes = Recipe.objects.filter(cuisine=recipe.cuisine, meal_type=recipe.meal_type, ingredients=recipe.ingredients)
#         serializer = RecipeSerializer(filtered_recipes, many=True)
#         return Response(serializer.data)

class CreateUser(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# class Reviewdetail(viewsets.ModelViewSet):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

class Reviewlist(APIView):
    def get(self,request):
        r = Review.objects.all()
        s=ReviewSerializer(r,many=True)
        return Response(s.data)
    def post(self,request):
        s=ReviewSerializer(data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class Reviewdetail(APIView):
    def get_object(self,request,pk):
        try:
            return Review.objects.get(pk=pk)
        except:
            raise Http404
    def get(self,request,pk):
        r=self.get_object(request,pk)
        s = ReviewSerializer(r)
        return Response(s.data)

    def put(self,request,pk):
        r=self.get_object(request,pk)
        s=ReviewSerializer(r,data=request.data)  #converts json data send from client to django object data
        if(s.is_valid()):
            s.save()  #save record into database table
            return Response(s.data,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_404_NOT_FOUND)
    def delete(self,request,pk):
        r=self.get_object(request,pk)
        r.delete()  #deletes from table
        return Response(status=status.HTTP_204_NO_CONTENT)


class search(APIView):
    def get(self,request):
        query=self.request.query_params.get('search')
        if(query):
            recipe=Recipe.objects.filter(Q(name__icontains=query) | Q(desc__icontains=query))
            p=RecipeSerializer(recipe,many=True)
            return Response(p.data)



class userlogout(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self,request):
        self.request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
