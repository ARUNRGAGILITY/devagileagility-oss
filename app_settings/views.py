from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import *
from .forms import *
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from mptt.exceptions import InvalidMove
from copy import copy
from copy import deepcopy
from mptt.exceptions import InvalidMove
from mptt.utils import tree_item_iterator
from mptt.templatetags.mptt_tags import cache_tree_children
def list_todolist(request):
    return HttpResponse('Todo List List')

@login_required(login_url='login')
def toplevel_home(request):
    newtodolist = NewLevels.objects.filter(active=True, author=request.user, parent=None).order_by('position')
    newtodolist_count = newtodolist.count()
    form = NewLevelsForm(request.user)
    if request.method == 'POST':
        form = NewLevelsForm(request.user, request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            todo_count = newtodolist.count()
            return redirect('toplevel_home')
        else:
            print(f"form is invalid {form}")
    context = {'toplevel': newtodolist,'form':form, 'toplevel_count': newtodolist_count}
    return render(request, 'app_settings/list_toplevel.html', context)


@login_required(login_url='login')
def levels_edit(request, pk):
    newtodolist_form = NewLevelsForm(request.user)
    newtodolist_item = None
    parent_item = None
    try:
        newtodolist_item = NewLevels.objects.get(id=pk)
        parent_item = newtodolist_item.parent
        newtodolist_form = NewLevelsForm(request.user, instance=newtodolist_item)
    except:
        print(f"EDIT TODOLIST TOPIC>>> TOPIC {pk}  not found.")
        messages.error(request, f"Edit: TOPIC {pk}  not found.")
    if request.method == 'POST':
        form = NewLevelsForm(request.user, request.POST or None, instance=newtodolist_item)
        if form.is_valid():
            form.save()
            if parent_item != None:
                if newtodolist_item.parent != None:
                    url = reverse('list_newlevels', args=[newtodolist_item.parent.id])
                    return redirect(url)
            else:
                return redirect('toplevel_home')
                
            return redirect('toplevel_home')

    context = {'form': newtodolist_form}
    return render(request, 'app_settings/edit_newtodolist.html', context)

def recurse_delete_items(object_tree, request):
    for eobject in object_tree:
        print(f"====> eobject {eobject}")
        NewLevels.objects.filter(id=eobject.id).update(active=False, author=request.user)
        if eobject.get_descendant_count() != 0:
            print(f"===> has children")
            recurse_delete_items(eobject,request)
        else:
            print(f"===> no children")

@login_required(login_url='login')
def newtodolist_delete(request, pk):
    newtodolist_form = NewLevelsForm(request.user)
    newtodolist_item = None
    parent_item = None
    newtodolist_item = NewLevels.objects.get(id=pk)
    parent_item = newtodolist_item.parent
    if request.method == 'POST':
        NewLevels.objects.filter(id=pk).update(active=False,  author=request.user)
        NewLevels.objects.filter(id=pk).get_descendants().update(active=False,  author=request.user)
        print(f"====> PARENTITEM ===> {parent_item}")
        if parent_item == None:
            return redirect('todolist_home')
        else:
            url = reverse('list_newtodolistitems', args=[newtodolist_item.parent.id])
            return redirect(url)
    context = {'form': newtodolist_form, 'newtodolist_item': newtodolist_item}
    return render(request, 'app_settings/delete_newtodolist.html', context)

@login_required(login_url='login')
def newtodolist_sorted(request):
    if request.method == 'POST':
        ajax_data = request.POST['sorted_list_data']
        new_data = ajax_data.replace("[",'')
        new_data = new_data.replace("]",'')
        sorted_list = new_data.split(",")
        seq = 1
        for item in sorted_list:
            str = item.replace('"','')
            position = str.split('_')
            NewLevels.objects.filter(pk=position[0]).update(position=seq)
            seq = seq + 1
        return render(request, 'app_settings/list_newtodolist.html', {'ajax_data': ajax_data})

@login_required(login_url='login')
def newtodolist_update(request):
    if request.method == 'POST':
        print("AJAX CHECKBOX METHOD TEST")
        ajax_data = request.POST['checkbox_data']
        checkbox_details = ajax_data.split('_')
        checkbox_id = checkbox_details[0]
        checkbox_position = checkbox_details[1]
        checkbox_status = checkbox_details[2]
        db_status = False
        todolist_item = None
        if checkbox_status == 'done':
            db_status = True
        try:
            NewLevels.objects.filter(pk=checkbox_id).update(done=db_status, author=request.user, completed_at=timezone.now())
            todolist_item = NewLevels.objects.get(pk=checkbox_id)
        except:
            print(f"EDIT TODOLIST ITEM>>> todolist {checkbox_id} item not found.")
        print(f"CHECKBOX DETAILS GOT: ID>>>{checkbox_id} POS>>>{checkbox_position} STATUS>>>{checkbox_status}")
        print(f"{todolist_item.updated_at}>>>>> UPDATED TIME")
        response_data = {}
        response_data['result'] = None
        if todolist_item.completed_at:
          if todolist_item.completed_at:
            readmainobject = NewLevels.objects.get(pk=checkbox_id)
            duration = readmainobject.completed_at - readmainobject.created_at
            readmainobject.duration_in_hours = duration.total_seconds() / 3600.0
            response_data['result'] = str(readmainobject.completed_at)
            response_data['duration_in_hours'] = str(round(readmainobject.duration_in_hours,2))
            readmainobject.save()
        return JsonResponse(response_data)

# next from 2nd level onwards of the django mptt model (topic/items)
@login_required(login_url='login')
def list_newtodolistitems(request, pk):
    parent = None
    imm_parent = None
    get_last_item = None
    parent = get_object_or_404(NewLevels, pk=pk)

    children = parent.get_children()
    ancestors = None
    # iterate through children and get their parents
    if children:
        print(f" CHILDREN PRESENT {children}")
    else:
        ancestors = parent.get_ancestors()
    for child in children:
        ancestors = child.get_ancestors()
        if ancestors:
            parent = ancestors[0]
            imm_parent = ancestors.reverse()[0]
        else:
            print(f"{child} has no parent")
    newtodolistitems = NewLevels.objects.filter(parent_id=pk, active=True).order_by('position')
    newtodolistitems_count = newtodolistitems.count()
    if newtodolistitems_count == 0:
        get_last_item = NewLevels.objects.get(id=pk)
    new_todo_list = NewLevelsForm(request.user)
    if request.method == 'POST':
        new_todo_list = NewLevelsForm(request.user, request.POST)
        if new_todo_list.is_valid():
            parent = new_todo_list.cleaned_data['parent']
            new_todo_list = new_todo_list.save(commit=False)
            new_todo_list.parent = parent
            new_todo_list.author = request.user
            new_todo_list.description = ""
            new_todo_list.save()
    newtodolistitems_count = newtodolistitems.count()
    context = {'get_last_item': get_last_item, 'ancestors': ancestors, 'parent': parent,
    'todolist_parent_id': pk, 'newtodolist': newtodolistitems,
    'form': new_todo_list, 'newtodolistitems_count': newtodolistitems_count}
    return render(request, 'app_settings/list_newtodolistitems.html', context)

@login_required(login_url='login')
def display_todolist_as_table(request):
    my_objects = NewLevels.objects.filter(active=True).order_by('position')
    cache_tree_children(my_objects)
    return render(request, 'app_settings/display_todolist_as_table.html', {'my_objects': my_objects, 'user': request.user})

@login_required(login_url='login')
def display_todolist_as_table_id(request, pk):
    my_objects = NewLevels.objects.filter(id=pk, active=True).order_by('position')
    print(f"====> {my_objects} {pk} == ===>>>>>> list_id table")
    cache_tree_children(my_objects)
    return render(request, 'app_settings/display_todolist_as_table_id.html', {'my_objects': my_objects, 'user': request.user})

@login_required(login_url='login')
def display_tree(request):
    my_objects = NewLevels.objects.filter(active=True)
    cache_tree_children(my_objects)
    return render(request, 'app_settings/display_tree.html', {'my_objects': my_objects, 'user': request.user})

@login_required(login_url='login')
def display_newtodolistitems(request):
    main_model = NewLevels()
    #newtodolist = main_model.objects.all()
    newtodolist = NewLevels.objects.filter(active=True, author=request.user).order_by('position')
    cache_tree_children(newtodolist)
    newtodolist_count = newtodolist.count()
    print(newtodolist)
    form = NewLevelsForm()
    if request.method == 'POST':
        form = NewLevelsForm(request.POST)
        if form.is_valid():
           form.instance.author = request.user
           form.save()
           todo_count = newtodolist.count()
    context = {'newtodolist': newtodolist, 'tags': newtodolist,'form':form, 'newtodolist_count': newtodolist_count}
    return render(request, 'app_settings/display_newtodolistitems.html', context)

@login_required(login_url='login')
def clone_newtodolistitems(request, pk):
    node = NewLevels.objects.get(id=pk)
    clone_node = NewLevels.objects.create(title=node.title, parent=node.parent)
    print(f"CLONE node: {clone_node}")
    url = reverse('list_newtodolistitems', args=[node.parent.id])
    return redirect(url)

@login_required(login_url='login')
def deepclone_newtodolistitems(request, pk):
    node = NewLevels.objects.get(id=pk)
    descendants = node.get_descendants(include_self=True)
    clone_node = NewLevels.objects.create(title=node.title + " (cloned) ", parent=node.parent)
    print(f">>> STEP1: node {node.id} {node} is cloned as {clone_node.id} {clone_node.id}")

    map_nodes = {}
    for descendant in node.get_descendants().filter(active=True):
        step2_flag = True
        print(f">>> STEP2: Map nodes {descendant.parent.id}|{descendant.id}")
        if descendant.parent.id in map_nodes:
            map_nodes[descendant.parent.id].update({descendant.id: descendant.title})
        else:
            map_nodes[descendant.parent.id] = {descendant.id: descendant.title}

    backup_nodes = map_nodes
    print(f">>> STEP3: Cloned Node takes place {map_nodes} and backup nodes {backup_nodes}")
    map_nodes[clone_node.id] = map_nodes[node.id]
    del map_nodes[node.id]
    print(f">>> STEP4: Move to cloned node {map_nodes}")
    if clone_node.id in map_nodes:
        for k,v in map_nodes[clone_node.id].items():
            ic = NewLevels.objects.create(title=v, parent_id=clone_node.id)
            # recurse from here
            # recurse_clone_from_map(k, ic.id, map_nodes)
            recurse_clone_from_map(k, ic, map_nodes, NewLevels, request)
            print(f"IMMEDIATE CLONE {node.id}, {node}: {ic.parent.id}, {ic.parent}, {ic.id}")
        del map_nodes[clone_node.id]
    print(f"CLONE_NODE {clone_node.id} from NODE {node.id}")
    print(f"MAP NODES after cloning: {map_nodes}")

    url = reverse('list_newtodolistitems', args=[node.parent.id])
    return redirect(url)

def recurse_clone_from_map(k, ic, map_nodes, mainobject, request):
    if k in map_nodes:
        print(f" RECURSE ******* {k}")
        for k1,v1 in map_nodes[k].items():
            iic = mainobject.objects.create(title=v1, parent_id=ic.id, author=request.user)
            if k1 in map_nodes:
                print(f" ******* {k1}")
                recurse_clone_from_map(k1, iic, map_nodes, mainobject, request)
    return map

