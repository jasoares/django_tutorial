""" Polls Views """
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.views import generic
from django.utils import timezone
from polls.models import Choice, Poll

class IndexView(generic.ListView):
    """ Generic view for the polls list/index """
    # Used to override the default template path(polls/poll_list.html)
    # template_name = 'polls/index.html'
    # Used to override the default context variable(poll_list)
    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        """ Return the last five published polls. """
        return Poll.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    """ Generic view for the details of a single poll """
    model = Poll
    # Used to override the default template path(polls/poll_detail.html)
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any polls that aren't published yet.
        """
        return Poll.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    """ Generic view fot the results details of a single poll """
    model = Poll
    # Used to override the default template path(polls/poll_detail.html)
    template_name = 'polls/results.html'

def simple_index(request):
    """ Polls list """
    latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
    context = {'latest_poll_list': latest_poll_list}
    return render(request, 'polls/index.html', context)

def old_index(request):
    """ Verbose polls list view """
    latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = RequestContext(request, {
        'latest_poll_list': latest_poll_list,
    })
    return HttpResponse(template.render(context))

def simple_detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/detail.html', {'poll': poll})

def old_detail(request, poll_id):
    """ Poll detail view """
    try:
        poll = Poll.objects.get(pk=poll_id)
    except Poll.DoesNotExist:
        raise Http404
    return render(request, 'polls/detail.html', {'poll': poll})

def simple_results(request, poll_id):
    """ Poll results stub view """
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/results.html', {'poll': poll})

def vote(request, poll_id):
    """ Poll vote stub view """
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
