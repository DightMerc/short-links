from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse

from django.core.paginator import Paginator

from core import models
from core import utils
from . import forms

import logging
import hashlib
from datetime import datetime


logger = logging.getLogger(__name__)


class BaseView(View):

    """
    Main Page View

    Allows two methods: get, post.
    - get method:
        renders index.html with rules of current session based user and new rule form.
        If user does not exist creates new session based user with MD5 hashed time of now
        as user unique id.

        ?page= int param is using for pagination.
        If page param > current user rules page count returns the last page.
    - post method:
        get data from page and creates new rule object
    """

    def get(self, request):

        if request.session.get('user', False):
            user_id = request.session['user']
        else:
            user_id = hashlib.md5(str(datetime.now()).encode('utf-8')).hexdigest()

            request.session['user'] = user_id

        user_instance, created = models.User.objects.get_or_create(session_id=user_id)
        user_rules = user_instance.rules.filter(active=True).order_by('-id')

        paginator = Paginator(user_rules, 5)
        page = int(request.GET.get('page')) if request.GET.get('page') else 1
        user_rules = paginator.page(page if page <= paginator.num_pages else paginator.num_pages)

        form = forms.RuleForm()

        return render(
            request,
            'web/index.html',
            {
                'form': form,
                'page': user_rules,
                'hostname': request.META['HTTP_HOST']

            }
        )

    def post(self, request):

        if request.session.get('user', False):
            user_id = request.session['user']
        else:
            user_id = hashlib.md5(str(datetime.now()).encode('utf-8')).hexdigest()

            request.session['user'] = user_id

        user_instance, created = models.User.objects.get_or_create(session_id=user_id)

        form = forms.RuleForm(request.POST)

        if form.is_valid():
            info = False
            if form.cleaned_data['short_url'] == '':
                if form.cleaned_data['url'][:4] != 'http':
                    info = True
                    info_message = 'Ссылка должна сожержать http:// или https://'
                else:
                    generated = hashlib.md5(str(datetime.now()).encode('utf-8')).hexdigest()
                    user_instance.rules.add(CreateRule(form.cleaned_data['url'], generated))

                    info = True
                    info_message = 'Ссылка успешно создана'
            else:
                if not models.Rule.objects.filter(short_url=form.cleaned_data['short_url'], active=True).exists():
                    if form.cleaned_data['url'][:4] != 'http':
                        info = True
                        info_message = 'Ссылка должна сожержать http:// или https://'
                    else:

                        user_instance.rules.add(CreateRule(form.cleaned_data['url'], form.cleaned_data['short_url']))

                        info = True
                        info_message = 'Ссылка успешно создана'
                else:
                    info = True
                    info_message = f'Ссылка с таким сокращением ({form.cleaned_data["short_url"]}) уже существует. Измените сокращение'

        user_rules = user_instance.rules.filter(active=True).order_by('-id')

        paginator = Paginator(user_rules, 5)
        page = int(request.GET.get('page')) if request.GET.get('page') else 1
        user_rules = paginator.page(page if page <= paginator.num_pages else paginator.num_pages)

        form = forms.RuleForm()

        return render(
            request,
            'web/index.html',
            {
                'form': form,
                'page': user_rules,
                'hostname': request.META['HTTP_HOST'],
                'info': info,
                'info_message': info_message
            }
        )


def CreateRule(url, short_url):

    """
    Main Create Rule method.
    short_url - new rule str short_url
    """

    rule = models.Rule()
    rule.url = url
    rule.short_url = short_url
    rule.save()

    return rule


class RedirectView(View):

    """
    Redirect View

    Allows get method:
        Redirects to cureent Rule url.
        Cache is used for redis based caching.
        If Rule not found renders 404.html 
    """

    def get(self, request, short_url):

        cache = utils.RedisCache()

        url = cache.get(short_url)
        if url != '':

            return HttpResponseRedirect(url)
        else:
            if models.Rule.objects.filter(short_url=short_url, active=True).exists():
                rule = models.Rule.objects.get(short_url=short_url)

                cache.set(short_url, rule.url)

                return HttpResponseRedirect(rule.url)
            else:
                return render(
                    request,
                    'web/404.html'
                )
