from django.shortcuts import render_to_response
from django.conf import settings
from misc.lib import *

def show_template(request, template):
    temp = 'notify/%s.html' % template
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
        #'hostname': settings.SITE_ATTRIBUTES['hostname'],
        'hostname': 'http://' + request.META['HTTP_HOST'],
        'body': """<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed nisi nunc, facilisis at, iaculis posuere, porta non, tellus. Pellentesque eleifend vehicula diam. Sed vel orci. Suspendisse dapibus. Nunc blandit tortor vitae mi. Cras tristique magna vel enim. Vivamus sit amet magna ut urna fringilla iaculis. Suspendisse vulputate lorem eget mi. Aenean consequat rhoncus nunc. In hac habitasse platea dictumst. Phasellus vel ligula eget ligula ultricies tristique. Phasellus dapibus. Etiam nec massa.</p>
<br />
        Aliquam <b>rutrum</b> viverra <i>mauris</i>. Etiam <a href="http://yahoo.com">ac nisi</a>. Nulla vitae risus vel tellus accumsan sodales. Maecenas ultricies, dui quis molestie interdum, dui turpis tristique augue, eget porttitor nunc velit vitae justo. Integer neque. Nunc velit massa, pellentesque vitae, pharetra quis, posuere sit amet, tortor. Nulla mi nisi, vulputate facilisis, euismod nec, interdum sed, lacus. Sed porta dolor dignissim nibh. Donec euismod aliquam ipsum. Nulla sem libero, sagittis nec, tincidunt vel, feugiat nec, felis. Ut tellus. Integer nibh mi, rutrum a, semper a, elementum vel, orci. Nulla tortor risus, mollis non, egestas id, cursus id, elit. Sed quis metus sit amet ipsum auctor pretium. Quisque justo nisl, iaculis quis, sagittis a, rhoncus et, turpis. Vestibulum posuere, lectus et tempor auctor, erat sem cursus risus, sed porta leo ante nec urna. Integer et neque. Duis et justo at mauris lacinia malesuada.
<br />
<br />
Nam massa. Maecenas ultricies convallis metus. Vivamus mi nisl, vehicula sed, consectetur ut, malesuada sit amet, augue. Integer sollicitudin accumsan metus. Ut scelerisque urna eu justo. Vestibulum id elit ut sapien eleifend gravida. Fusce libero nisl, interdum et, fringilla sed, porttitor vitae, tortor. Aliquam fermentum, libero ornare feugiat hendrerit, orci lectus fermentum tellus, in semper massa elit id augue. Curabitur a dolor et lacus sodales aliquam. Phasellus accumsan, nulla id aliquam ornare, purus tortor mattis nibh, non facilisis tortor erat volutpat dolor. Proin dolor mauris, placerat sit amet, mattis ut, pretium at, tortor. Quisque placerat. Donec condimentum tellus sit amet nisl. Vivamus lacinia vestibulum enim. Vivamus eget arcu in felis laoreet cursus. Morbi imperdiet gravida ligula. Vivamus fringilla risus sed enim. Nam convallis mi sit amet velit.

 """,
    }
    return render_to_response(temp, context)
