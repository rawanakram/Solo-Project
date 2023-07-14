from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contractor, Material
import bcrypt

# Create your views here.
def index(request):
    context = {
        'all_contractors': Contractor.objects.all(),
    }
    return render(request, 'index.html',context)



def filter_contractors(request):
    spcialized_in = request.POST.get('specialized_in', False)
    if spcialized_in == 'All':
        myselection = Contractor.objects.all()
    else:
        myselection = Contractor.objects.filter(spcialized_in =spcialized_in)
    context = {
        'all_contractors': Contractor.objects.all(),
        'myselection':myselection,
    }
    print(request.POST['specialized_in'])
            
    return render(request, 'index.html', context)


def register(request):
    errors = Contractor.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/loginreg')

    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        spcialized_in = request.POST['spcialized_in']
        phone_num = request.POST['phone_num']
        phone = phone_num.replace('-','')
        contractor = Contractor.objects.create(first_name=first_name,last_name=last_name,
                                            email= email, password= pw_hash,
                                            spcialized_in=spcialized_in, phone_num=int(phone))
                                            
        request.session['contractor_name'] = f'{first_name}{last_name}'
        request.session['contractor_id']= contractor.id  
        return redirect('/contractors')


def login(request):
    errors2 = Contractor.objects.login_validator(request.POST)

    print(errors2)
    if len(errors2) > 0:
        for key, value in errors2.items():
            messages.error(request, value)
        return redirect('/loginreg')

    else:
        contractor = Contractor.objects.filter(email=request.POST['email2'])
        if contractor:
            logged_contractor = contractor[0]
            if bcrypt.checkpw(request.POST['inputPassword2'].encode(), logged_contractor.password.encode()):
                request.session['contractor_name'] = logged_contractor.first_name + logged_contractor.last_name
                request.session['contractor_id'] = logged_contractor.id   
            print(request.session['contractor_id'])
        return redirect('/contractors')


def contractors(request):
    context = {
        'all_contractors': Contractor.objects.all(),
        'contractor_name': request.session['contractor_name'],
    }
    return render(request, 'contractors.html', context)


def filter(request):
    spcialized_in = request.POST.get('specialized_in', False)
    if spcialized_in == 'All':
        myselection = Contractor.objects.all()
    else:
        myselection = Contractor.objects.filter(spcialized_in =spcialized_in)
    context = {
        'all_contractors': Contractor.objects.all(),
        'contractor_name': request.session['contractor_name'],
        'myselection':myselection,
    }
    print(request.POST['specialized_in'])
            
    return render(request, 'contractors.html', context)


def loginreg(request):
    return render(request, 'loginreg.html')


def contractordetails(request, contractor_id):
    context={
        'contractor': Contractor.objects.get(id = contractor_id),
        'all_materials': Material.objects.all(),
        'materials': Material.objects.filter(added_by = Contractor.objects.get(id = contractor_id)),
        
    }
    return render(request, 'contractordetails.html', context)   


# ******update the information of the contractor******
def update_info(request, contractor_id):
    errors = Contractor.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/contractordetails/{contractor_id}')

    else:
        contractor_to_update = Contractor.objects.get(id= contractor_id)
        contractor_to_update.first_name = request.POST['first_name']
        contractor_to_update.last_name = request.POST['last_name']
        contractor_to_update.email = request.POST['email']
        contractor_to_update.spcialized_in = request.POST['spcialized_in']
        phone_num = request.POST['phone_num']
        phone = phone_num.replace('-','')
        contractor_to_update.phone = request.POST['phone_num']
        contractor_to_update.save()
        return redirect(f'/contractordetails/{contractor_id}')


def edit(request, material_id):
    contractor_id = request.session['contractor_id']
    context={
        'contractor': Contractor.objects.get(id= contractor_id),
        'material': Material.objects.get(id = material_id),
    }
    return render(request, 'update.html', context)  


def add(request):
    contractor_id = request.session['contractor_id']
    context={
        'contractor': Contractor.objects.get(id= contractor_id),
    }
    return render(request, 'add.html', context)  

def addmaterial(request):
    contractor_id = request.session['contractor_id']
    contractor_create = Contractor.objects.get(id= request.session['contractor_id'])
    print(request.session['contractor_id'])
    new_material = Material.objects.create(
        name = request.POST['name'],
        description = request.POST['description'],
        specifications = request.POST['specifications'],
        added_by = contractor_create
    )
    request.session['material_id'] = new_material.id
    return redirect(f'contractordetails/{contractor_id}')


def materialdetails(request, material_id, contractor_id):  
    context={
        'contractor': Contractor.objects.get(id= contractor_id),
        'material': Material.objects.get(id = material_id),
        'all_materials': Material.objects.all(),
    }
    return render(request, 'materialdetails.html', context)


#******update the material details******
def update_material(request, material_id):
    contractor_id = request.session['contractor_id']
    material_to_update = Material.objects.get(id = material_id)
    material_to_update.name = request.POST['name']
    material_to_update.description = request.POST['description']
    material_to_update.specifications = request.POST['specifications']
    material_to_update.save()
    return redirect(f'/materialdetails/{material_id}/{contractor_id}')


def delete(request, material_id):
    contractor_id = request.session['contractor_id']
    material_to_delete = Material.objects.get(id = material_id)
    material_to_delete.delete()
    return redirect(f'/contractordetails/{contractor_id}')


def logout(request):
    request.session.flush()
    return redirect('/')