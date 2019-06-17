from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.test import TestCase, TransactionTestCase
from .models import Movie, Comment, Rating
from .serializers import MovieSerializer, CommentSerializer, RatingSerializer, TopSerializer 
import requests

class MovieRequestsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.movie_data = {"Title":"Hulk","Year":"2003","Rated":"PG-13","Released":"20 Jun 2003","Runtime":"138 min","Genre":"Action, Sci-Fi","Director":"Ang Lee","Writer":"Stan Lee (Marvel comic book character), Jack Kirby (Marvel comic book character), James Schamus (story), John Turman (screenplay), Michael France (screenplay), James Schamus (screenplay)","Actors":"Eric Bana, Jennifer Connelly, Sam Elliott, Josh Lucas","Plot":"Bruce Banner, a genetics researcher with a tragic past, suffers an accident that causes him to transform into a raging green monster when he gets angry.","Language":"English, Spanish","Country":"USA","Awards":"3 wins & 14 nominations.","Poster":"https://m.media-amazon.com/images/M/MV5BNjcxMzZhZTEtMmEwYi00NDJmLWE5ZmUtOWJiMzRmMzEzMTY3L2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_SX300.jpg","Metascore":"54","ImdbRating":"","ImdbVotes":"","ImdbID":"","Type":"movie","DVD":"28 Oct 2003","BoxOffice":"$132,122,995","Production":"Universal Pictures","Website":"http://www.thehulk.com/"}
    
    def test_movies_get_request(self):
        movie = MovieSerializer(data=self.movie_data)
        if movie.is_valid():
            movie.save()
        response = self.client.get('/movies')
        self.assertEqual(response.status_code, requests.codes.ALL_OK)
        response_serialized = MovieSerializer(data=response.data, many=True)
        self.assertTrue(response_serialized.is_valid())
        self.assertEqual(len(response_serialized.data),1)
        self.assertEqual(response_serialized.data[0]["Title"],self.movie_data["Title"])

    def test_movies_post_request(self):
        response = self.client.post('/movies', {'Title':'Hulk'}, format='json')
        self.assertEqual(response.status_code, requests.codes.ok)
        self.assertEqual(response.data["Title"], "Hulk")

class CommentsRequestsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.movie_data = {"Title":"Hulk","Year":"2003","Rated":"PG-13","Released":"20 Jun 2003","Runtime":"138 min","Genre":"Action, Sci-Fi","Director":"Ang Lee","Writer":"Stan Lee (Marvel comic book character), Jack Kirby (Marvel comic book character), James Schamus (story), John Turman (screenplay), Michael France (screenplay), James Schamus (screenplay)","Actors":"Eric Bana, Jennifer Connelly, Sam Elliott, Josh Lucas","Plot":"Bruce Banner, a genetics researcher with a tragic past, suffers an accident that causes him to transform into a raging green monster when he gets angry.","Language":"English, Spanish","Country":"USA","Awards":"3 wins & 14 nominations.","Poster":"https://m.media-amazon.com/images/M/MV5BNjcxMzZhZTEtMmEwYi00NDJmLWE5ZmUtOWJiMzRmMzEzMTY3L2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_SX300.jpg","Metascore":"54","ImdbRating":"","ImdbVotes":"","ImdbID":"","Type":"movie","DVD":"28 Oct 2003","BoxOffice":"$132,122,995","Production":"Universal Pictures","Website":"http://www.thehulk.com/"}
        self.movie_data2 = {"Title":"Hulk2","Year":"2003","Rated":"PG-13","Released":"20 Jun 2003","Runtime":"138 min","Genre":"Action, Sci-Fi","Director":"Ang Lee","Writer":"Stan Lee (Marvel comic book character), Jack Kirby (Marvel comic book character), James Schamus (story), John Turman (screenplay), Michael France (screenplay), James Schamus (screenplay)","Actors":"Eric Bana, Jennifer Connelly, Sam Elliott, Josh Lucas","Plot":"Bruce Banner, a genetics researcher with a tragic past, suffers an accident that causes him to transform into a raging green monster when he gets angry.","Language":"English, Spanish","Country":"USA","Awards":"3 wins & 14 nominations.","Poster":"https://m.media-amazon.com/images/M/MV5BNjcxMzZhZTEtMmEwYi00NDJmLWE5ZmUtOWJiMzRmMzEzMTY3L2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_SX300.jpg","Metascore":"54","ImdbRating":"","ImdbVotes":"","ImdbID":"","Type":"movie","DVD":"28 Oct 2003","BoxOffice":"$132,122,995","Production":"Universal Pictures","Website":"http://www.thehulk.com/"}
        self.movie = MovieSerializer(data=self.movie_data)
        self.assertTrue(self.movie.is_valid())
        self.movie.save()
        self.movie2 = MovieSerializer(data=self.movie_data2)
        self.assertTrue(self.movie2.is_valid())
        self.movie2.save()

    def test_comment_post_request(self):
        count_old = Comment.objects.all().count()
        response = self.client.post('/comments', {"Movie_id":self.movie.data["id"], "Comment":"Test"},format='json')
        count_new = Comment.objects.all().count()
        self.assertEqual(count_old,count_new-1)
        self.assertEqual(Comment.objects.get(Movie_id = response.data["Movie_id"]).Comment, "Test")
        self.assertEqual(Comment.objects.get(Movie_id = response.data["Movie_id"]).Movie_id.id, self.movie.data["id"])

    def test_comment_get_with_movie_id(self):
        self.client.post('/comments', {"Movie_id":self.movie.data["id"], "Comment":"Test"},format='json')
        self.client.post('/comments', {"Movie_id":self.movie.data["id"], "Comment":"Test1"},format='json')
        self.client.post('/comments', {"Movie_id":self.movie.data["id"], "Comment":"Test2"},format='json')
        self.client.post('/comments', {"Movie_id":self.movie.data["id"], "Comment":"Test3"},format='json')
        response = self.client.get('/comments?Movie_id=' + str(self.movie.data["id"]))
        self.assertEqual(response.status_code, requests.codes.ALL_OK)
        self.assertEqual(len(response.data), 4)
        
    def test_comment_get_without_movie_id(self):
        self.client.post('/comments', {"Movie_id":self.movie.data["id"], "Comment":"Test"},format='json')
        self.client.post('/comments', {"Movie_id":self.movie.data["id"], "Comment":"Test1"},format='json')
        self.client.post('/comments', {"Movie_id":self.movie2.data["id"], "Comment":"Test2"},format='json')
        self.client.post('/comments', {"Movie_id":self.movie2.data["id"], "Comment":"Test3"},format='json')
        response = self.client.get('/comments')
        self.assertEqual(response.status_code,requests.codes.ALL_OK)
        self.assertEqual(len(response.data), Comment.objects.all().count())

class TopRequestsTestCase(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.client = APIClient()
        self.movie_data = {"Title":"Hulk","Year":"2003","Rated":"PG-13","Released":"20 Jun 2003","Runtime":"138 min","Genre":"Action, Sci-Fi","Director":"Ang Lee","Writer":"Stan Lee (Marvel comic book character), Jack Kirby (Marvel comic book character), James Schamus (story), John Turman (screenplay), Michael France (screenplay), James Schamus (screenplay)","Actors":"Eric Bana, Jennifer Connelly, Sam Elliott, Josh Lucas","Plot":"Bruce Banner, a genetics researcher with a tragic past, suffers an accident that causes him to transform into a raging green monster when he gets angry.","Language":"English, Spanish","Country":"USA","Awards":"3 wins & 14 nominations.","Poster":"https://m.media-amazon.com/images/M/MV5BNjcxMzZhZTEtMmEwYi00NDJmLWE5ZmUtOWJiMzRmMzEzMTY3L2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_SX300.jpg","Metascore":"54","ImdbRating":"","ImdbVotes":"","ImdbID":"","Type":"movie","DVD":"28 Oct 2003","BoxOffice":"$132,122,995","Production":"Universal Pictures","Website":"http://www.thehulk.com/"}
        self.movie_data2 = {"Title":"Hulk2","Year":"2003","Rated":"PG-13","Released":"20 Jun 2003","Runtime":"138 min","Genre":"Action, Sci-Fi","Director":"Ang Lee","Writer":"Stan Lee (Marvel comic book character), Jack Kirby (Marvel comic book character), James Schamus (story), John Turman (screenplay), Michael France (screenplay), James Schamus (screenplay)","Actors":"Eric Bana, Jennifer Connelly, Sam Elliott, Josh Lucas","Plot":"Bruce Banner, a genetics researcher with a tragic past, suffers an accident that causes him to transform into a raging green monster when he gets angry.","Language":"English, Spanish","Country":"USA","Awards":"3 wins & 14 nominations.","Poster":"https://m.media-amazon.com/images/M/MV5BNjcxMzZhZTEtMmEwYi00NDJmLWE5ZmUtOWJiMzRmMzEzMTY3L2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_SX300.jpg","Metascore":"54","ImdbRating":"","ImdbVotes":"","ImdbID":"","Type":"movie","DVD":"28 Oct 2003","BoxOffice":"$132,122,995","Production":"Universal Pictures","Website":"http://www.thehulk.com/"}
        self.movie_data3 = {"Title":"Hulk3","Year":"2003","Rated":"PG-13","Released":"20 Jun 2003","Runtime":"138 min","Genre":"Action, Sci-Fi","Director":"Ang Lee","Writer":"Stan Lee (Marvel comic book character), Jack Kirby (Marvel comic book character), James Schamus (story), John Turman (screenplay), Michael France (screenplay), James Schamus (screenplay)","Actors":"Eric Bana, Jennifer Connelly, Sam Elliott, Josh Lucas","Plot":"Bruce Banner, a genetics researcher with a tragic past, suffers an accident that causes him to transform into a raging green monster when he gets angry.","Language":"English, Spanish","Country":"USA","Awards":"3 wins & 14 nominations.","Poster":"https://m.media-amazon.com/images/M/MV5BNjcxMzZhZTEtMmEwYi00NDJmLWE5ZmUtOWJiMzRmMzEzMTY3L2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_SX300.jpg","Metascore":"54","ImdbRating":"","ImdbVotes":"","ImdbID":"","Type":"movie","DVD":"28 Oct 2003","BoxOffice":"$132,122,995","Production":"Universal Pictures","Website":"http://www.thehulk.com/"}
        self.movie_data4 = {"Title":"Hulk4","Year":"2003","Rated":"PG-13","Released":"20 Jun 2003","Runtime":"138 min","Genre":"Action, Sci-Fi","Director":"Ang Lee","Writer":"Stan Lee (Marvel comic book character), Jack Kirby (Marvel comic book character), James Schamus (story), John Turman (screenplay), Michael France (screenplay), James Schamus (screenplay)","Actors":"Eric Bana, Jennifer Connelly, Sam Elliott, Josh Lucas","Plot":"Bruce Banner, a genetics researcher with a tragic past, suffers an accident that causes him to transform into a raging green monster when he gets angry.","Language":"English, Spanish","Country":"USA","Awards":"3 wins & 14 nominations.","Poster":"https://m.media-amazon.com/images/M/MV5BNjcxMzZhZTEtMmEwYi00NDJmLWE5ZmUtOWJiMzRmMzEzMTY3L2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_SX300.jpg","Metascore":"54","ImdbRating":"","ImdbVotes":"","ImdbID":"","Type":"movie","DVD":"28 Oct 2003","BoxOffice":"$132,122,995","Production":"Universal Pictures","Website":"http://www.thehulk.com/"}
        self.movie_data5 = {"Title":"Hulk5","Year":"2003","Rated":"PG-13","Released":"20 Jun 2003","Runtime":"138 min","Genre":"Action, Sci-Fi","Director":"Ang Lee","Writer":"Stan Lee (Marvel comic book character), Jack Kirby (Marvel comic book character), James Schamus (story), John Turman (screenplay), Michael France (screenplay), James Schamus (screenplay)","Actors":"Eric Bana, Jennifer Connelly, Sam Elliott, Josh Lucas","Plot":"Bruce Banner, a genetics researcher with a tragic past, suffers an accident that causes him to transform into a raging green monster when he gets angry.","Language":"English, Spanish","Country":"USA","Awards":"3 wins & 14 nominations.","Poster":"https://m.media-amazon.com/images/M/MV5BNjcxMzZhZTEtMmEwYi00NDJmLWE5ZmUtOWJiMzRmMzEzMTY3L2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_SX300.jpg","Metascore":"54","ImdbRating":"","ImdbVotes":"","ImdbID":"","Type":"movie","DVD":"28 Oct 2003","BoxOffice":"$132,122,995","Production":"Universal Pictures","Website":"http://www.thehulk.com/"}
        self.movie = MovieSerializer(data=self.movie_data)
        self.assertTrue(self.movie.is_valid())
        self.movie.save()
        self.movie2 = MovieSerializer(data=self.movie_data2)
        self.assertTrue(self.movie2.is_valid())
        self.movie2.save()
        self.movie3 = MovieSerializer(data=self.movie_data3)
        self.assertTrue(self.movie3.is_valid())
        self.movie3.save()
        self.movie4 = MovieSerializer(data=self.movie_data4)
        self.assertTrue(self.movie4.is_valid())
        self.movie4.save()
        self.movie5 = MovieSerializer(data=self.movie_data5)
        self.assertTrue(self.movie5.is_valid())
        self.movie5.save()
        self.client.post('/comments', {"Movie_id":self.movie.data["id"], "Comment":"Test"},format='json')
        self.client.post('/comments', {"Movie_id":self.movie.data["id"], "Comment":"Test1"},format='json')
        self.client.post('/comments', {"Movie_id":self.movie2.data["id"], "Comment":"Test2"},format='json')
        self.client.post('/comments', {"Movie_id":self.movie2.data["id"], "Comment":"Test3"},format='json')
        self.client.post('/comments', {"Movie_id":self.movie2.data["id"], "Comment":"Test4"},format='json')
        self.client.post('/comments', {"Movie_id":self.movie2.data["id"], "Comment":"Test5"},format='json')
        self.client.post('/comments', {"Movie_id":self.movie2.data["id"], "Comment":"Test6"},format='json')
        self.client.post('/comments', {"Movie_id":self.movie2.data["id"], "Comment":"Test7"},format='json')
        self.client.post('/comments', {"Movie_id":self.movie3.data["id"], "Comment":"Test4"},format='json')
        self.client.post('/comments', {"Movie_id":self.movie4.data["id"], "Comment":"Test5"},format='json')
        self.client.post('/comments', {"Movie_id":self.movie4.data["id"], "Comment":"Test6"},format='json')
        self.client.post('/comments', {"Movie_id":self.movie4.data["id"], "Comment":"Test7"},format='json')
        self.client.post('/comments', {"Movie_id":self.movie5.data["id"], "Comment":"Test4"},format='json')
        self.client.post('/comments', {"Movie_id":self.movie5.data["id"], "Comment":"Test5"},format='json')
        self.client.post('/comments', {"Movie_id":self.movie5.data["id"], "Comment":"Test6"},format='json')
        self.client.post('/comments', {"Movie_id":self.movie5.data["id"], "Comment":"Test7"},format='json')

    def test_top_four_get(self):
        response = self.client.get('/top?From=1889-03-03&To=2222-04-04')
        self.assertEqual(response.status_code, requests.codes.ALL_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data[0]['id'], 2)
