from django.contrib import messages
from django.db.models import Q
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse
from django.views.generic.detail import DetailView
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone

from .forms import VariationInventoryFormSet
from .mixins import StaffRequiredMixin, LoginRequiredMixin
from .models import Product, Variation, Category

class CategoryListView(ListView):
    model = Category
    queryset = Category.objects.all()
    template_name = "products/product_list.html"

class CategoryDetailView(DetailView):
    model = Category
    template_name = "products/category_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
        obj = self.get_object()
        print "obj"
        print obj
        print obj.title
        product_set = obj.product_set.all()
        print "product_set"
        print product_set
        default_products = obj.default_category.all()
        print "default products ++++"
        print default_products
        products = ( product_set | default_products )
        context["products"] = products
        return context

class  VariationListView(StaffRequiredMixin, ListView):
    model = Variation
    queryset = Variation.objects.all()
    template_name = "products/variation_list.html"

    def get_context_data(self, *args, **kwargs):
        print "kwargs!!!!!!!!!!!!!!!11111111"
        print self.kwargs
        print "context!!!!!!!!!!!!!!!!!!!!11"
        context = super(VariationListView, self).get_context_data(*args, **kwargs)
        context["formset"] = VariationInventoryFormSet(queryset=self.get_queryset())
        return context

    def get_queryset(self, *args, **kwargs):
        print "get_queryset!!!!!!!!!!!!!!11"
        print "kwargs!!!!!!!!!!!!!!!2222222"
        print self.kwargs
        product_pk = self.kwargs.get("pk") #is a way to get value of key
        if product_pk:
            product = get_object_or_404(Product, pk=product_pk)
            # queryset = qs.filter(product=product)
            queryset = Variation.objects.filter(product=product)
        return queryset
        # if product_pk

    def post(self, request, *args, **kwargs):
        print "post"
        formset = VariationInventoryFormSet(request.POST, request.FILES)
        # print request.POST
        if formset.is_valid():
            formset.save(commit=False)
            for form in formset:
                new_item = form.save(commit=False)
                print new_item
                if new_item.title:
                    product_pk = self.kwargs.get("pk")
                    product = get_object_or_404(Product, pk=product_pk)
                    new_item.product = product
                    new_item.save()
                # form.save()
            messages.success(request, "Your inventory and pricing has been updated.")
            return redirect("products")
        raise Http404



class ProductListView(ListView):
    model = Product
    queryset = Product.objects.filter(active=True)
    # query = request.GET.get("q",)
    # if query:
    #     queryset = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    #     try:
    #         queryset = Product.objects.filter(Q(price=query))
    #     except:
    #         pass


    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(ProductListView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q",)
        if query:
            qs = self.model.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
            try:
                qs2 = self.model.objects.filter(
                    Q(price=query)
                )
                qs = (qs | qs2).distinct()
            except:
                pass
        return qs

    # def post(self, request, *args, **kwargs):
    #     formset = VariationInventoryFormSet(request.POST, request.FILES)
    #     print request.POST
    #     if formset.is_Valid():
    #         formset.save(commit=False)
    #         for form in formset:
    #             form.save()
    #     raise Http404

import random


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    #template_name = "<appname>/<modelname>_detail.html"
    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        instance = self.get_object()
        # order_by(-reverse)
        context["related"] = sorted(Product.objects.get_related(instance)[:6], key= lambda x: random.random())
        return context

# def product_detail_view_func(request, id):
#     product_instance = get_object_or_404(Product, id=id)
#     # product_instance = Product.objects.get(id=id)
#     try:
#         product_instance = get_object_or_404(Product, id=id)
#     except Product.DoesNotExist:
#         raise Http404
#     except:
#         raise Http404
#
#     template = "products/product_detail.html"
#     context = {
#         "object": product_instance,
#     }
#
#     return render(request, template, context)
