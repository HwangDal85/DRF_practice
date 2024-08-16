from rest_framework import generics
from .models import Todo
from .serializers import TodoSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, redirect

# Create your views here.
class TodoListView(generics.ListAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

class TodoDetailView(generics.RetrieveAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    lookup_field = 'pk' # URL에서 전달된 pk(기본키)를 사용하여 특정 todo항목 조회

class TodoCreateView(generics.CreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

class TodoUpdateView(generics.UpdateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    lookup_field = 'pk'


class TodoCompleteView(APIView):
    def post(self, request, pk):
        try:
            todo = Todo.objects.get(pk=pk)
            todo.is_completed = True
            todo.save()
            serializer = TodoSerializer(todo)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Todo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class TodoDeleteView(generics.DestroyAPIView):
    queryset = Todo.objects.all()
    lookup_field = 'pk'


# 하단부터 장고뷰
def todo_list(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Todo.objects.create(title=title)
        return redirect('todo-list')

    todos = Todo.objects.all()
    return render(request, 'todo_list.html', {'todos': todos})

def todo_complete(request, pk):
    todo = Todo.objects.get(pk=pk)
    todo.is_completed = True
    todo.save()
    return redirect('todo-list')

def todo_delete(request, pk):
    todo = Todo.objects.get(pk=pk)
    todo.delete()
    return redirect('todo-list')