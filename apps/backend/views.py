from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from apps.core.models import SaasInstance
from apps.core.models import SaasCustomer
from apps.core.models import SaasPlan
from apps.backend.forms import PlanForm
from django.db.models import Q
from django.db import connection
from collections import namedtuple


@login_required
@staff_member_required
def customers(request):
    with connection.cursor() as cursor:

        sql = """SELECT email_address, first_name, last_name, saas_instance.identifier as instance_identifier
            FROM saas_customer, saas_instance, saas_contract
            WHERE saas_contract.customer_id = saas_customer.id
            AND saas_contract.instance_id = saas_instance.id"""

        cursor.execute(sql)
        result = cursor.fetchall()

        customers = []
        for row in result:
            # create an associative array
            a = dict(zip([c[0] for c in cursor.description], row))
            # create an object
            o = namedtuple("customer", a.keys())(*a.values())
            # add the object to resulting array
            customers.append(o)

    return render(request,"customers.html",
            {'customers':customers})

@login_required
@staff_member_required
def instances(request):
    unused_instances = SaasInstance.objects.filter(Q(status='free') | Q(status='in_preparation'))

    return render(request,"instances.html",
            {'unused_instances':unused_instances })


@login_required
@staff_member_required
def plans(request):
    plans = SaasPlan.objects.all()

    return render(request,"plans.html",
            { 'plans':plans })

@login_required
@staff_member_required
def addplan(request):


    if request.method == "POST":
        # request.POST is immutable, so make a copy
        values = request.POST.copy()
        values['owner'] = request.user.id
        form = PlanForm(values)
        if form.is_valid():
            try:
                form.save()
                return redirect('/')
            except:
                pass
    else:
        form = PlanForm()
    return render(request,'addplan.html',{'form':form})

@login_required
@staff_member_required
def editplan(request, id):
    plan = SaasPlan.objects.get(id=id)
    form = PlanForm(request.POST or None, instance = plan)
    return render(request,'editplan.html', {'plan':plan, 'form': form})

@login_required
@staff_member_required
def updateplan(request, id):
    plan = SaasPlan.objects.get(id=id)
    # request.POST is immutable, so make a copy
    values = request.POST.copy()
    form = PlanForm(values, instance = plan)
    if form.is_valid():
        form.save()
        return redirect("/")
    return render(request, 'editplan.html', {'plan': plan, 'form': form})

@login_required
@staff_member_required
def deleteplan(request, id):
    plan = SaasPlan.objects.get(id=id)
    plan.delete()
    return redirect("/")

def products(request):
    products = SaasProduct.objects.all()

    return render(request,"products.html",
            { 'products':products })

@login_required
@staff_member_required
def addproduct(request):


    if request.method == "POST":
        # request.POST is immutable, so make a copy
        values = request.POST.copy()
        values['owner'] = request.user.id
        form = ProductForm(values)
        if form.is_valid():
            try:
                form.save()
                return redirect('/')
            except:
                pass
    else:
        form = ProductForm()
    return render(request,'addproduct.html',{'form':form})

@login_required
@staff_member_required
def editproduct(request, id):
    product = SaasProduct.objects.get(id=id)
    form = ProductForm(request.POST or None, instance = Product)
    return render(request,'editproduct.html', {'product':Product, 'form': form})

@login_required
@staff_member_required
def updateproduct(request, id):
    product = SaasProduct.objects.get(id=id)
    # request.POST is immutable, so make a copy
    values = request.POST.copy()
    form = ProductForm(values, instance = product)
    if form.is_valid():
        form.save()
        return redirect("/")
    return render(request, 'editproduct.html', {'product': product, 'form': form})

@login_required
@staff_member_required
def deleteproduct(request, id):
    product = SaasProduct.objects.get(id=id)
    product.delete()
    return redirect("/")
