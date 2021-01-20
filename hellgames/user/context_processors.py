
# Context processor to remove login/register buttons from base_layout if user is already logged in.
def if_user(request):
    if request.user.is_authenticated:
        return {'displayloginreg':False, 'currentuser':request.user.username}
    elif request.user.is_authenticated == False:
        return {'displayloginreg':True}