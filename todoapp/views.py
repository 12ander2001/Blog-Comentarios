from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import todo
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import TodoForm
from .models import todo
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError


@login_required 
def home(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                new_todo = form.save(commit=False)
                new_todo.user = request.user
                new_todo.save()
                messages.success(request, '')
                return redirect('home-page')
            except IntegrityError:
                messages.error(request, 'Ya existe una tarea con ese nombre.')
    else:
        form = TodoForm()

    all_todos = todo.objects.filter(user=request.user)
    context = {
        'form': form,
        'todos': all_todos
    }
    return render(request, 'todoapp/todo.html', context)



def register(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if len(password) < 3:
            messages.error(request, 'la contraseña debe tener mas de 3 caracteres')
            return redirect('register')

        get_all_users_by_username = User.objects.filter(username=username)
        if get_all_users_by_username:
            messages.error(request, 'El usuario ya existe')
            return redirect('register')

        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()

        messages.success(request, 'Usuario creado con éxito, inicie sesión ahora')
        return redirect('login')
    return render(request, 'todoapp/register.html', {})

def LogoutView(request):
    logout(request)
    return redirect('login')

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')

        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
            login(request, validate_user)
            return redirect('home-page')
        else:
            messages.error(request, 'Ese usuario no existe')
            return redirect('login')


    return render(request, 'todoapp/login.html', {})

@login_required
def DeleteTask(request, name):
    get_todo = todo.objects.get(user=request.user, todo_name=name)
    get_todo.delete()
    return redirect('home-page')

@login_required
def Update(request, name):
    get_todo = todo.objects.get(user=request.user, todo_name=name)
    get_todo.status = True
    get_todo.save()
    return redirect('home-page')

def list_tasks(request):
    tasks = todo.objects.all()
    return render(request, "list_tasks.html", {"tasks": tasks})


from django.core.mail import send_mail
from django.conf import settings
from .models import todo
from django.shortcuts import render, redirect
from .forms import EmailForm

def send_todo_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            comment = form.cleaned_data.get("comment") 
            selected_todo_ids = request.POST.getlist('todo_ids')
            selected_todos = []
            for todo_id in selected_todo_ids:
                todo_name = request.POST.get(f'todo_name_{todo_id}')
                description = request.POST.get(f'description_{todo_id}')
                status = request.POST.get(f'status_{todo_id}')
                selected_todos.append({
                    'id': todo_id,
                    'todo_name': todo_name,
                    'description': description,
                    'status': status,
                })
            
            print("IDs seleccionados:", selected_todo_ids)
            print("Tareas seleccionadas:", selected_todos)
            
            email_content = "Elementos enviados:\n"
            for todo_item in selected_todos:
                email_content += f"Título: {todo_item['todo_name']}, Descripción: {todo_item['description']}, Estado: {'Completado' if todo_item['status'] == 'True' else 'En progreso'}\n"
            email_content += f"\nComentario:\n{comment}"
            
            # Enviar el correo electrónico
            send_mail(
                'Elementos seleccionados',
                email_content,
                settings.EMAIL_HOST_USER,
                [email], 
                fail_silently=False,
            )
            
            return redirect('send-email')
        
    else:
        form = EmailForm()
    todos = todo.objects.filter(user=request.user)
    return render(request, 'email_form.html', {'form': form, 'todos': todos})




