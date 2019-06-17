import requests
from django.shortcuts import render
from django.db.models import Count, Func, Subquery, IntegerField
from django.db.models.expressions import Window,RawSQL, F
from django.db.models.functions import Rank, DenseRank
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Rating, Movie, Comment
from .serializers import MovieSerializer, RatingSerializer, CommentSerializer, TopSerializer
from rest_framework.views import APIView
from.movies import pickTopComments


@api_view(['GET','POST'])
def MovieView(request):
    if request.method == 'POST':
        if not request.data['Title']:
            return Response(data={"Error": "Title not provided in POST"})
       
        title = request.data['Title']
        api_key = '9a5075c9'
        url = f'http://www.omdbapi.com/?apikey={api_key}&t={title}'
        response = requests.get(url)
       
        if response.status_code == requests.codes.ALL_OK and response.json()['Response'] == 'True':
            serialized = (MovieSerializer(data=response.json()))
            if serialized.is_valid():
                movie = Movie.objects.filter(Title = title)
                if not movie:
                    serialized.save()
            else:
                return Response(data={"Error":f"{serialized.errors}"})
            return Response(serialized.data)
        else:
            return Response(data={"Error":"Movie not found"})    

    if request.method == "GET":
        serialized = MovieSerializer(Movie.objects.all(), many=True)
        return Response(serialized.data)

@api_view(['GET','POST'])
def CommentView(request):
    if request.method == 'POST':
        if not request.data['Movie_id'] and not request.data['Comment']:
            return Response(data={'Error':'No movie_id or comment provided in POST'})

        if not Movie.objects.filter(id = request.data['Movie_id']).exists():
            return Response(data={'Error':'No movie with given id in database.'})

        serialized = CommentSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data)
        else:
            return Response(data={"Error":f"{serialized.errors}"})

    if request.method == 'GET':    
        if request.GET.get('Movie_id'): 
            comments = Comment.objects.filter(Movie_id = request.GET['Movie_id'])
        else:
            comments = Comment.objects.all()

        serialized = CommentSerializer(comments,many=True)
        return Response(serialized.data)

@api_view(['GET','POST'])
def TopView(request):
    if request.method == "GET":
        if request.GET.get('From') and request.GET.get('To'):
            From = request.GET['From']
            To = request.GET['To']

            comments = Comment.objects.raw('''SELECT com."Movie_id_id" AS id, Total_comments, dense_rank () OVER(ORDER BY Total_comments DESC) AS Place
                                            FROM movies_comment com
                                            LEFT JOIN (SELECT COUNT(mc."Movie_id_id") AS Total_comments, mc."Movie_id_id" as Movie_id
                                            		FROM "movies_comment" mc
                                                    WHERE mc."Date" BETWEEN '1555-02-02' and '3444-02-02'
                                            		GROUP BY mc."Movie_id_id"
                                            		ORDER BY mc."Movie_id_id" DESC
                                            		) subcom on  com."Movie_id_id" = subcom.Movie_id
                                            WHERE com."Date" BETWEEN '1555-02-02' and '3444-02-02'
                                            GROUP BY com."Movie_id_id", Total_comments
                                            LIMIT 4''')
            serialized = TopSerializer(comments, many=True)
            return Response(serialized.data)
        else:
            return Response(data={"Error":"No dates From and To provided in GET parameters."}, status=status.HTTP_400_BAD_REQUEST)


     


