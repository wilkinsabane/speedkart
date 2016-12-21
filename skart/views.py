from django.shortcuts import render


def file_not_found_404(request, template_name='404.html'):
    page_title = 'Page Not Found'
    return render(request, template_name, locals())


def server_error_500(request, template_name='500.html'):
    page_title = 'Server Error - 500'
    return render(request, template_name, locals())