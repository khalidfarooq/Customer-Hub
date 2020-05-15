from django.shortcuts import render ,redirect
from django.forms import inlineformset_factory
from django.http import HttpResponse
# Create your views here.
from .models import *
from .forms import OrderForm

def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    totalorders = orders.count()
    pending = orders.filter(status = 'Pending').count()
    delivered = orders.filter(status = 'Delivered').count()

    context = {'orders':orders ,'customers':customers,
               'totalorders':totalorders, 'pending':pending,
               'delivered':delivered}
    return render(request,'accounts/dashboard.html',context)

def customer(request,pk):
    customer = Customer.objects.get(id = pk)
    orders = customer.order_set.all() #order_set is to query the data of child model
    orders_count = orders.count()
    context = {'customer':customer,'orders':orders,'orders_count':orders_count}

    return render(request,'accounts/customer.html',context)

def products(request):
    products = Product.objects.all()
    return render(request,'accounts/products.html',{'products':products})

def createOrder(request,pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10 )
    #customer ->parentTemp #Order->ChildTemp
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	#form = OrderForm(initial={'customer':customer})
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		#form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'form':formset}
	return render(request, 'accounts/order_form.html', context)

def updateOrder(request,pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={'form':form}
    return render(request,'accounts/order_form.html',context)

def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item':order}
    return render(request,'accounts/delete.html',context)
