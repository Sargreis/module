#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import HttpResponse,render,redirect
import json
from arya.service import sites

from . import models
from django.urls.resolvers import RegexURLPattern
def get_all_url(patterns,prev,is_first=False,result=[]):
    if is_first:
        result.clear()
    for item in patterns:
        v = item._regex.strip("^$")
        if isinstance(item,RegexURLPattern):
            result.append(prev+v)
        else:
            get_all_url(item.urlconf_name,prev+v)
    return result



class DepartmentConfig(sites.AryaConfig):
    list_display = ['title',]


sites.site.register(models.Department,DepartmentConfig)



class UserInfoConfig(sites.AryaConfig):
    list_display = ['name',]

    # def add_view(self, request, *args, **kwargs):
    #     return render(request,'userinfo_add.html')


''' 
    执行sites.site的register方法
    sites.site
 '''
sites.site.register(models.UserInfo,UserInfoConfig)


class CourseConfig(sites.AryaConfig):
    list_display = ['name',]


sites.site.register(models.Course,CourseConfig)


class SchoolConfig(sites.AryaConfig):

    def dabo(self, obj=None, is_header=False):
        if is_header:
            return '其他'
        return obj.title+'大波'
    list_display = ['title',dabo]
    # list_filter = [
    #     sites.FilterOption('title', True, lambda x: x.title, lambda x: x.id),
    # ]

    # def get_show_list_display(self):
    #
    #     li = []
    #     li.extend(self.list_display)
    #     return li

    def add_view(self, request, *args, **kwargs):
        """
        添加页面
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        self.request = request
        from pro_crm.urls import urlpatterns
        all_url_list = get_all_url(urlpatterns,prev='/',is_first=True)

        model_form_cls = self.get_model_form_class()
        popup_id = request.GET.get(self.popup_key)
        if request.method == 'GET':
            form = model_form_cls()
            return render(request, "permission_add_popup.html" if popup_id else "arya/add.html", {'form': form,'url_list':all_url_list})
        elif request.method == "POST":
            form = model_form_cls(data=request.POST, files=request.FILES)
            if form.is_valid():
                obj = self.save(form, True)
                if obj:
                    if popup_id:
                        context = {'pk': obj.pk, 'value': str(obj), 'popup_id': popup_id}
                        return render(request, 'arya/popup_response.html', {"popup_response_data": json.dumps(context)})
                    else:
                        return redirect(self.changelist_url_params)
            return render(request, "permission_add_popup.html" if popup_id else "arya/add.html", {'form': form,'url_list':all_url_list})


sites.site.register(models.School, SchoolConfig)