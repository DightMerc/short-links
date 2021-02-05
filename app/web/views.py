from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse

from core import models
from . import forms

import logging
import hashlib
from datetime import datetime

from core import utils

logger = logging.getLogger(__name__)


class BaseView(View):

    def get(self, request):

        if request.session.get('user', False):
            user_id = request.session['user']
        else:
            user_id = hashlib.md5(str(datetime.now()).encode('utf-8')).hexdigest()

            request.session['user'] = user_id

        user_instance, created = models.User.objects.get_or_create(session_id=user_id)
        user_rules = user_instance.rules.filter(active=True).order_by('-id')

        form = forms.RuleForm()

        return render(
            request,
            'web/index.html',
            {
                'form': form,
                'rules': user_rules,
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
        form = forms.RuleForm()

        return render(
            request,
            'web/index.html',
            {
                'form': form,
                'rules': user_rules,
                'hostname': request.META['HTTP_HOST'],
                'info': info,
                'info_message': info_message
            }
        )


def CreateRule(url, short_url):

    rule = models.Rule()
    rule.url = url
    rule.short_url = short_url
    rule.save()

    return rule


class RedirectView(View):

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
