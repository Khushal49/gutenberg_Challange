from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.query_params.get('title', None)
        if title:
            queryset = queryset.filter(title__icontains=title)

        author = self.request.query_params.get('author', None)
        if author:
            queryset = queryset.filter(author__icontains=author)

        topic = self.request.query_params.get('topic', None)
        if topic:
            queryset = queryset.filter(subjects__icontains=topic) | queryset.filter(bookshelves__icontains=topic)

        page = self.request.query_params.get('page', 1)
        page_size = self.request.query_params.get('page_size', 20)
        paginator = self.paginate_queryset(queryset)
        if paginator is not None:
            return paginator.page(page_size)
        
        return queryset
