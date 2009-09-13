from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'shoot', 'jeffgame.input.views.shoot'),
    (r'repeat', 'jeffgame.input.views.repeat'),
    (r'play', 'jeffgame.input.views.play'),
    (r'control', 'jeffgame.input.views.control'),
    (r'', 'jeffgame.input.views.index'),

)
