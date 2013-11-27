from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout

from myapp.models import DbxUser

from dropbox.client import DropboxClient, DropboxOAuth2Flow

def index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('myapp:login'))
    else:
        # get the user from db
        dbx_user = DbxUser.objects.get(user=request.user)
        dbx_client = DropboxClient(dbx_user.dbx_access_token)

        # get the user dropbox account info
        account_info = dbx_client.account_info()
        context = {
            'dbx_user' : dbx_user,
            'dbx_account_info' : account_info,
        }
        return render(request, 'myapp/index.html', context)

def dropbox_auth_finish(request):
    try:
        access_token, user_id, url_state = get_auth_flow(request).finish(request.GET)
        dbx_user = DbxUser(dbx_user_id=user_id, dbx_access_token=access_token)
        dbx_user.save()
        request.session['dbx_user_id'] = user_id
        return HttpResponseRedirect(reverse('myapp:signup'))
    except DropboxOAuth2Flow.BadRequestException, e:
        return HttpResponseBadRequest()
    except DropboxOAuth2Flow.BadStateException, e:
        return HttpResponseBadRequest()
    except DropboxOAuth2Flow.CsrfException, e:
        return HttpResponseForbidden()
    except DropboxOAuth2Flow.NotApprovedException, e:
        return render(request, 'myapp/login.html', {'error': 'Why not aprrove?'})
    except DropboxOAuth2Flow.ProviderException, e:
        print e
        return HttpResponseForbidden()

def signup(request):
    if request.method == 'GET':
        return render(request, 'myapp/signup.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if request.session['dbx_user_id'] is not None:
            dbx_user = DbxUser.objects.get(
                dbx_user_id=request.session['dbx_user_id'])
            dbx_user.user.username = username
            dbx_user.user.set_password(password)
            dbx_user.user.save()
            auth_user = authenticate(username=username, password=password)
            return _login(request, auth_user)
        else:
            return HttpResponseForbidden() 
    else:
        return HttpResponseBadRequest()


def dropbox_auth_start(request):
    return HttpResponseRedirect(get_auth_flow(request).start())

def dropbox_unlink(request):
    pass

def do_login(request):
    if request.method == 'GET':
        return render(request, 'myapp/login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        return _login(request, user)
    else:
        return HttpResponseBadRequest()

def do_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('myapp:login'))

def _login(request, authenticate_user):
    if authenticate_user is not None:
        if authenticate_user.is_active:
            login(request, authenticate_user)
            return HttpResponseRedirect(reverse('myapp:index'))
        else:
            # Return a 'disabled account' error message
            return render(request, 'myapp/login.html', {'error': 'disabled account'})
    else:
        # Return an 'invalid login' error message.
        return render(request, 'myapp/login.html', {'error': 'unxpected exception'})

def get_auth_flow(request):
    redirect_uri = request.build_absolute_uri(reverse('myapp:dropbox_auth_finish'));
    _keys = settings.DROPBOX_SETTINGS
    return DropboxOAuth2Flow(_keys['APP_KEY'], _keys['APP_SECRET'], redirect_uri,
                                       request.session, 'dropbox-auth-csrf-token')
