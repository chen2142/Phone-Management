from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from app01 import models
from django import forms
from django.core.validators import RegexValidator
from django.views.generic import ListView
from django.core.paginator import Paginator


# Create your views here.
def department_list(request):
    queryset = models.Department.objects.all()
    return render(request, 'department_list.html', {'queryset': queryset})


# if __name__ == '__main__':
#     print(bin(-1))
def department_add(request):
    """add department"""
    if request.method == 'GET':
        return render(request, 'department_add.html')

    # get data from POST
    title = request.POST.get('title')
    # save to database
    models.Department.objects.create(title=title)

    # redirect to department list page
    return redirect('/department/list/')


def department_delete(request):
    """delete department"""
    nid = request.GET.get('nid')
    models.Department.objects.filter(id=nid).delete()
    return redirect('/department/list/')


def department_edit(request, nid):
    """edit department"""
    if request.method == "GET":
        row_obj = models.Department.objects.filter(id=nid).first()
        return render(request, 'department_edit.html', {'row_obj': row_obj})

    # get title from user committed
    title = request.POST.get('title')
    # update data from database by id
    models.Department.objects.filter(id=nid).update(title=title)
    # redirect to department list page
    return redirect('/department/list/')


def index(request):
    return render(request, 'layout.html')


def user_list(request):
    """get user list"""
    query_set = models.UserInfo.objects.all()
    # for obj in query_set:
    #     print(obj.id, obj.name, obj.account, obj.create_time.strftime('%Y-%m-%d'), obj.gender, obj.get_gender_display())
    # obj.get_gender_display() # get the display of gender
    # obj.get_<filed name>_display() # e.g.
    # obj.depart_id # get corresponding field
    # obj.depart # get object of related table
    # obj.depart.title # get title
    return render(request, 'user_list.html', {'query_set': query_set})


def user_add(request):
    """add user in original way"""
    if request.method == 'GET':
        data = {
            'gender_choices': models.UserInfo.gender_choices,
            'department_list': models.Department.objects.all(),
        }
        return render(request, 'user_add.html', data)

    # get committed user data
    name = request.POST.get('name')
    password = request.POST.get('password')
    age = request.POST.get('age')
    account = request.POST.get('account')
    create_time = request.POST.get('create_time')
    gender = request.POST.get('gender')
    department = request.POST.get('department')

    # context = {
    #     'name': name,
    #     'password': password,
    #     'age': age,
    #     'account': account,
    #     'create_time': create_time,
    #     'gender': gender,
    #     'department': department,
    # }

    # save to database
    models.UserInfo.objects.create(name=name, password=password, age=age,
                                   account=account, create_time=create_time,
                                   gender=gender, depart_id=department)
    return redirect('/user/list/')


class UserModelForm(forms.ModelForm):
    name = forms.CharField(min_length=3, label='name')

    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'age', 'create_time', 'gender', 'depart']
        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        #     'age': forms.TextInput(attrs={'class': 'form-control'}),
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # loop to find all widgets to add style
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}


def user_model_form_add(request):
    """add user（ModelForm）"""
    if request.method == 'GET':
        form = UserModelForm()

        return render(request, 'user_model_form_add.html', {'form': form})

    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    else:
        print(form.errors)
        return render(request, 'user_model_form_add.html', {'form': form})


def user_edit(request, nid):
    """edit user"""
    if request.method == 'GET':
        # get row in database by id
        row_object = models.UserInfo.objects.filter(id=nid).first()
        form = UserModelForm(instance=row_object)

        return render(request, 'user_edit.html', {'form': form})

    row_object = models.UserInfo.objects.filter(id=nid).first()
    form = UserModelForm(data=request.POST, instance=row_object)

    if form.is_valid():
        # save all the values typed by users by default,if wanted to get the value beyond typing
        # form.instance.<filed name> = value
        form.save()
        return redirect('/user/list/')

    return render(request, 'user_edit.html', {'form': form})


def user_delete(request, nid):
    """delete user"""
    models.UserInfo.objects.filter(id=nid).delete()

    return redirect('/user/list/')


def pretty_list(request):
    """pretty number list"""
    data_dict = {}
    search_data = request.GET.get('q', '')
    if search_data:
        data_dict['mobile__contains'] = search_data

    queryset = models.PrettyNum.objects.filter(**data_dict).order_by('-level')
    return render(request, 'pretty_list.html', {'queryset': queryset, 'search_data': search_data})


class PrettyModelForm(forms.ModelForm):
    # verification method 1：regular expression
    # mobile = forms.CharField(
    #     label='phone number',
    #     validators=[RegexValidator(r'^1[3-9]\d{9}$', 'format wrong')], # validators can contain multiple rexp
    # )

    class Meta:
        model = models.PrettyNum
        # fields = ['mobile', 'price']
        fields = '__all__'
        # excludes = ['<filed name>']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}

    def clean_mobile(self):
        # verification method 2：hooks function
        # get data from users' typing
        text_mobile = self.cleaned_data['mobile']
        exsits = models.PrettyNum.objects.filter(mobile=text_mobile).exists()
        if exsits:
            # failed, the number is existing
            raise ValidationError("the number is existing")

        # successful, return the value typed
        return text_mobile


def pretty_add(request):
    """add pretty number"""
    if request.method == 'GET':
        form = PrettyModelForm()
        return render(request, 'pretty_add.html', {'form': form})

    form = PrettyModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request, 'pretty_add.html', {'form': form})


class PrettyEditModelForm(forms.ModelForm):


    class Meta:
        model = models.PrettyNum
        # fields = ['mobile', 'price']
        fields = '__all__'
        # excludes = ['<field name>']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}

    def clean_mobile(self):

        text_mobile = self.cleaned_data['mobile']

        exists = models.PrettyNum.objects.filter(mobile=text_mobile).exclude(id=self.instance.pk).exists()
        if exists:
            raise ValidationError("已存在该手机号")

        return text_mobile


def pretty_edit(request, nid):
    """edit pretty number"""
    row_object = models.PrettyNum.objects.filter(id=nid).first()

    if request.method == 'GET':
        form = PrettyEditModelForm(instance=row_object)
        return render(request, 'pretty_edit.html', {'form': form})

    form = PrettyEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')

    return render(request, 'pretty_edit.html', {'form': form})


def pretty_delete(request, nid):
    """delete pretty number"""
    models.PrettyNum.objects.filter(id=nid).delete()
    # row_object = models.PrettyNum.objects.filter(id=nid)
    # form = PrettyModelForm(instance=row_object)
    # all_object_result = models.PrettyNum.objects.filter(mobile=form.mobile).delete()
    # print(all_object_result)
    return redirect('/pretty/list/')


# class UserListView(ListView):
#     paginate_by = 2
#     model = models.UserInfo
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context

def listing(request):
    list_user = models.UserInfo.objects.all()
    paginator = Paginator(list_user, 2) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # paginator.page(page_number)
    return render(request, 'list.html', {'page_obj': page_obj})


